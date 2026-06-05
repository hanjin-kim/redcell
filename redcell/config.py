"""Configuration — LLM settings + run config schema.

LLM settings are read from environment variables; a ``.env`` file in the
current working directory (or any parent directory) is loaded automatically
on first ``load_llm_settings()`` call.

Recognized env vars (any one provider's set works):
  - ``OPENAI_API_KEY`` (+ optional ``SF_QWEN_MODEL`` to override default ``gpt-4o``)
  - ``SF_QWEN_API_KEY`` / ``SF_QWEN_MODEL`` / ``SF_QWEN_BASE_URL`` (Qwen via
    DashScope, sglang local, or any OpenAI-compatible endpoint)
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


def _walk_up_for_env(start: Path | None = None, max_levels: int = 5) -> Path | None:
    """Walk up from ``start`` (default CWD) looking for a ``.env`` file."""
    cur = (start or Path.cwd()).resolve()
    for _ in range(max_levels):
        candidate = cur / ".env"
        if candidate.is_file():
            return candidate
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


_env_loaded = False


def _load_env_once() -> None:
    """Load ``.env`` (if any) into ``os.environ``. Idempotent."""
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True
    path = _walk_up_for_env()
    if path is None:
        return
    # Minimal .env parser — avoid python-dotenv hard dep. Format:
    #   KEY=value
    #   KEY="quoted value"
    # Lines starting with # are comments; blank lines skipped.
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        # Don't overwrite existing env vars (real env wins).
        os.environ.setdefault(key, val)


class LLMSettings(BaseModel):
    api_key: str = ""
    model: str = "qwen-plus"
    base_url: str = ""


class RunConfig(BaseModel):
    """A single redcell run — everything needed to generate scenarios."""

    industry: str
    our_company: str
    competitors: list[str]
    strategy: str
    worried_risk: str
    n_scenarios: int = 5
    max_turns: int = 5
    # Path to the underlying scenario YAML (sides, rulebook hints, etc.)
    scenario_path: str

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RunConfig":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls(**data)


def load_llm_settings() -> LLMSettings:
    """Load LLM settings from env vars (and any ``.env`` walked up from CWD).

    Resolution order for each field:
      1. ``SF_QWEN_*`` env var (preferred — explicit redcell convention)
      2. ``OPENAI_API_KEY`` fallback for api_key only
      3. Built-in default (``qwen-plus`` model, no base_url → OpenAI direct)
    """
    _load_env_once()
    api_key = (
        os.environ.get("SF_QWEN_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )
    model = os.environ.get("SF_QWEN_MODEL") or os.environ.get("OPENAI_MODEL") or "qwen-plus"
    base_url = os.environ.get("SF_QWEN_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or ""
    return LLMSettings(api_key=api_key, model=model, base_url=base_url)
