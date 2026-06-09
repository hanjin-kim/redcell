"""Provider-portable LLM adapter for redcell.

Auto-detects provider from base_url and isolates provider quirks behind a
strategy class. Adding a new provider = subclass `Provider`.

Today's known providers and quirks (verified empirically 2026-05-27 / 28):
  - sglang local Qwen: guided_json strict (token-level), enable_thinking via
    chat_template_kwargs, qwen sampling defaults (top_k=20, presence=1.5)
  - DashScope qwen: enable_thinking via extra_body; strict json_schema is
    *advisory only* (relies on prompt-explicit field listing); empty-content
    edge case observed once but not reproducible
  - OpenAI proper: real json_schema strict, no enable_thinking kwarg
    (use o1/o3 model names for reasoning), standard chat.completions
  - Unknown OpenAI-compatible: conservative passthrough (no Qwen extras)

The caller (engine) does NOT need to know the provider — it just calls
``llm.complete(system, user, enable_thinking=..., response_format=..., ...)``
and the provider class translates appropriately.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# JSON parsing (vendored from strategyforge.llm.utils — kept here so the
# adapter is fully self-contained)
# ----------------------------------------------------------------------

def parse_llm_json(response: str) -> dict | None:
    """Extract JSON object from LLM response text.

    Handles: markdown fences, surrounding prose, nested braces, and
    common malformations (trailing commas, missing braces) via the
    optional ``json_repair`` dependency.
    """
    text = (response or "").strip()
    if "```" in text:
        lines = [ln for ln in text.split("\n") if not ln.strip().startswith("```")]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
    if start >= 0:
        try:
            import json_repair
            repaired = json_repair.repair_json(text[start:], return_objects=True)
            if isinstance(repaired, dict):
                return repaired
        except Exception:
            pass
    logger.debug("JSON parse failed: %s", text[:300])
    return None


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------

class EmptyContentError(RuntimeError):
    """Provider returned empty content. Caller decides whether to retry
    or surface to user — we fail-fast rather than silently defaulting."""


# ----------------------------------------------------------------------
# Provider strategies — one per backend, encoding its quirks
# ----------------------------------------------------------------------

class Provider:
    """Strategy interface. Subclass to add a backend."""

    name: str = "base"

    def prepare(
        self, *, model: str, system: str, user: str,
        temperature: float, max_tokens: int,
        enable_thinking: bool | None,
        presence_penalty: float | None,
        response_format: dict | None,
        **caller_extras: Any,
    ) -> dict:
        """Translate uniform call params into the API request dict for
        this provider. Default = vanilla OpenAI-compatible (no extras)."""
        req: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if presence_penalty is not None:
            req["presence_penalty"] = presence_penalty
        if response_format is not None:
            req["response_format"] = response_format
        return req

    def extract(self, response) -> tuple[str, str, str | None]:
        """Return ``(content, reasoning_content, finish_reason)``."""
        msg = response.choices[0].message
        content = msg.content or ""
        reasoning = getattr(msg, "reasoning_content", None) or ""
        finish = response.choices[0].finish_reason
        return content, reasoning, finish


class SglangProvider(Provider):
    """Local sglang serving Qwen — full guided_json + enable_thinking +
    Qwen sampling defaults. Recommended for development."""

    name = "sglang"

    def prepare(self, *, model, system, user, temperature, max_tokens,
                enable_thinking, presence_penalty, response_format, **caller_extras):
        req: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        extra_body: dict = {}

        is_qwen = "qwen" in (model or "").lower()

        # Default thinking OFF for Qwen if caller didn't specify. Qwen3's
        # own default is ON — that burns reasoning budget on every call and
        # frequently produces empty content (observed: synthesis call with
        # max_tokens=32768 → reasoning=124k chars, content=0). Callers who
        # want thinking must say so explicitly (enable_thinking=True).
        ethink = enable_thinking
        if is_qwen and ethink is None:
            ethink = False

        # Qwen-via-sglang sampling defaults (per official Qwen3 README).
        if is_qwen:
            extra_body.setdefault("top_k", 20)
            extra_body.setdefault("min_p", 0.0)
            extra_body.setdefault("repetition_penalty", 1.0)
            if ethink:
                # Thinking ON: official temperature=0.7-1.0, top_p=0.95
                req["temperature"] = max(temperature, 1.0)
                req.setdefault("top_p", 0.95)
            else:
                req.setdefault("top_p", 0.8)
            # presence_penalty=1.5 default for Qwen — but if caller passes 0.0
            # (e.g., for structured JSON to avoid early-stop), respect it.
            if presence_penalty is not None:
                req["presence_penalty"] = presence_penalty
            else:
                req["presence_penalty"] = 1.5

        if ethink is not None:
            extra_body.setdefault("chat_template_kwargs", {})
            extra_body["chat_template_kwargs"]["enable_thinking"] = bool(ethink)

        if response_format is not None:
            # sglang's guided_json honors both top-level and extra_body —
            # pass both for maximum compatibility across sglang versions.
            req["response_format"] = response_format
            extra_body["response_format"] = response_format

        if extra_body:
            req["extra_body"] = extra_body
        return req


class DashscopeProvider(Provider):
    """DashScope (Alibaba) — Qwen via cloud OpenAI-compatible endpoint.

    Differences from sglang:
    - enable_thinking still goes via extra_body.chat_template_kwargs (same)
    - strict json_schema is *advisory only* — model usually follows it when
      the prompt explicitly lists required fields, but the API does not
      enforce at token level. Caller's prompts must be self-sufficient.
    - empty-content edge case observed in early testing; not reproducible
      today but caller should be ready for EmptyContentError.
    """

    name = "dashscope"

    def prepare(self, *, model, system, user, temperature, max_tokens,
                enable_thinking, presence_penalty, response_format, **caller_extras):
        req: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        # Same as sglang: default thinking OFF for Qwen if caller silent.
        # Qwen3's own default is ON; that's a recipe for reasoning runaway
        # on heavy structured-output calls.
        ethink = enable_thinking
        if "qwen" in (model or "").lower() and ethink is None:
            ethink = False
        extra_body: dict = {}
        if ethink is not None:
            extra_body["chat_template_kwargs"] = {"enable_thinking": bool(ethink)}
        if presence_penalty is not None:
            req["presence_penalty"] = presence_penalty
        if response_format is not None:
            req["response_format"] = response_format
        if extra_body:
            req["extra_body"] = extra_body
        return req


class OpenAIProvider(Provider):
    """OpenAI direct (api.openai.com) — real strict json_schema.

    Quirks:
    - No ``enable_thinking`` kwarg. Reasoning is enabled via model name
      (e.g. gpt-5, o1, o3). enable_thinking is dropped silently.
    - Newer reasoning models use ``max_completion_tokens`` instead of
      ``max_tokens``; we map automatically based on model name.
    """

    name = "openai"

    _REASONING_MODELS = ("o1", "o3", "gpt-5")

    def prepare(self, *, model, system, user, temperature, max_tokens,
                enable_thinking, presence_penalty, response_format, **caller_extras):
        req: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
        }
        # Reasoning models use max_completion_tokens instead.
        is_reasoning = any(model.lower().startswith(p) for p in self._REASONING_MODELS)
        if is_reasoning:
            req["max_completion_tokens"] = max_tokens
        else:
            req["max_tokens"] = max_tokens
        if presence_penalty is not None and not is_reasoning:
            # Reasoning models reject sampling params; only set on chat models.
            req["presence_penalty"] = presence_penalty
        if response_format is not None:
            req["response_format"] = response_format
        if enable_thinking is not None and not is_reasoning:
            logger.debug(
                "OpenAIProvider: ignoring enable_thinking=%s (non-reasoning model "
                "%s — enable reasoning by using o1/o3/gpt-5 model names)",
                enable_thinking, model,
            )
        return req


class OpenAICompatibleProvider(Provider):
    """Unknown OpenAI-compatible endpoint — conservative defaults.

    No provider-specific extras. Standard OpenAI chat.completions only.
    Use this for custom inference servers (TGI, vLLM-direct, LM Studio,
    Together, Groq, etc.) where we don't know the quirks.
    """

    name = "openai_compatible"
    # Inherits default Provider.prepare (vanilla OpenAI). enable_thinking
    # is silently dropped — server probably doesn't know that kwarg.


# ----------------------------------------------------------------------
# Auto-detection
# ----------------------------------------------------------------------

def detect_provider(base_url: str | None, model: str) -> Provider:
    """Auto-detect provider from (base_url, model). Falls back to
    ``OpenAICompatibleProvider`` (conservative) for unknown endpoints."""
    url = (base_url or "").lower()
    mdl = (model or "").lower()

    # No base_url → OpenAI default
    if not url or "openai.com" in url:
        return OpenAIProvider()
    # DashScope (Alibaba)
    if "dashscope" in url or "aliyuncs.com" in url:
        return DashscopeProvider()
    # Local / private network + Qwen model name → assume sglang
    is_local = any(host in url for host in (
        "localhost", "127.0.0.1", "0.0.0.0",
        "10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
        "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
    ))
    if is_local and "qwen" in mdl:
        return SglangProvider()
    # Unknown OpenAI-compatible endpoint → conservative
    return OpenAICompatibleProvider()


# ----------------------------------------------------------------------
# Adapter
# ----------------------------------------------------------------------

class LLMAdapter:
    """Provider-portable LLM call adapter.

    Construct once with ``model``, ``api_key``, ``base_url``; call
    ``complete(system, user, ...)`` with the same kwargs the engine uses.
    Provider quirks are handled internally.
    """

    def __init__(
        self, *,
        model: str,
        api_key: str,
        base_url: str | None = None,
        provider: Provider | None = None,
        timeout: float = 600.0,
    ):
        self._model = model
        self._client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
        self.provider = provider or detect_provider(base_url, model)
        # Telemetry
        self.total_calls = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        logger.info(
            "redcell LLM: provider=%s, model=%s, base_url=%s",
            self.provider.name, self._model, base_url or "(default openai)",
        )

    # --- properties expected by the simulation engine ---

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def cost_tier(self) -> str:
        return "standard"

    def is_available(self) -> bool:
        return True

    # --- main call ---

    def complete(
        self, system: str, user: str, *,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        enable_thinking: bool | None = None,
        presence_penalty: float | None = None,
        response_format: dict | None = None,
        _retry_no_thinking: bool = True,
        **caller_extras: Any,
    ) -> str:
        """Issue one chat completion. Returns ``content`` only.

        Raises ``EmptyContentError`` if the provider returns no content
        (rather than silently returning empty string and letting the
        caller hit a downstream KeyError on missing JSON).

        If ``enable_thinking=True`` and the call returns empty content due
        to reasoning runaway (finish=length + content=""), retries ONCE
        with thinking=False. Without this, Qwen models occasionally burn
        the entire token budget on reasoning and emit nothing, breaking
        the trial. The retry trades thinking depth for a structured
        answer; set ``_retry_no_thinking=False`` to disable.
        """
        req = self.provider.prepare(
            model=self._model,
            system=system, user=user,
            temperature=temperature, max_tokens=max_tokens,
            enable_thinking=enable_thinking,
            presence_penalty=presence_penalty,
            response_format=response_format,
            **caller_extras,
        )
        response = self._client.chat.completions.create(**req)
        content, reasoning, finish = self.provider.extract(response)

        if response.usage:
            self.total_prompt_tokens += response.usage.prompt_tokens
            self.total_completion_tokens += response.usage.completion_tokens
            self.total_calls += 1

        # Reasoning-runaway recovery: thinking ON + empty content + abnormal
        # finish (length truncation OR DashScope's None) → retry once without
        # thinking. The model exhausted its budget on reasoning OR dropped
        # the answer into the reasoning channel; either way, a no-thinking
        # retry gives us a structured answer.
        # NB: DashScope's thinking+structured failures surface as finish=None,
        # not finish=length (verified 2026-06-09 smoke). Our condition must
        # accept both.
        if (finish in ("length", None) and not content and enable_thinking
                and _retry_no_thinking):
            logger.warning(
                "Reasoning runaway (finish=%s, max_tokens=%d, reasoning=%dc, "
                "content=0c) — retrying with thinking=False",
                finish, max_tokens, len(reasoning),
            )
            return self.complete(
                system, user,
                temperature=temperature, max_tokens=max_tokens,
                enable_thinking=False,
                presence_penalty=presence_penalty,
                response_format=response_format,
                _retry_no_thinking=False,  # prevent infinite loop
                **caller_extras,
            )

        if finish == "length":
            # Truncation is expected when callers size max_tokens too small
            # (especially with thinking models burning reasoning budget).
            # Callers handle empty/short content downstream; warn and return.
            logger.warning(
                "Output truncated (finish=length): provider=%s, model=%s, "
                "max_tokens=%d, content_chars=%d, reasoning_chars=%d",
                self.provider.name, self._model, max_tokens,
                len(content), len(reasoning),
            )
            return content  # may be "" — caller handles

        if not content:
            # finish != "length" but content empty → provider weirdness
            # (e.g., DashScope thinking-mode dropping content into reasoning).
            # Fail-fast — this is unexpected and silently defaulting risks
            # corrupting downstream sims.
            raise EmptyContentError(
                f"LLM returned empty content. provider={self.provider.name}, "
                f"model={self._model}, finish={finish}, "
                f"reasoning_len={len(reasoning)}, thinking={enable_thinking}, "
                f"has_schema={response_format is not None}. "
                "If you see this repeatedly on DashScope with thinking+schema, "
                "try a different provider or retry (DashScope thinking+structured "
                "output has been observed to fail intermittently)."
            )
        return content
