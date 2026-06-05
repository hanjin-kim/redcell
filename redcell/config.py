"""Configuration — LLM settings + run config schema.

LLM settings reuse the SF_QWEN_* env vars during bootstrap (shared with
the parent strategyforge install). A run config is a single YAML file that
combines scenario context + strategy + worry + scenario count.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class LLMSettings(BaseModel):
    api_key: str = Field(default_factory=lambda: os.environ.get("SF_QWEN_API_KEY", ""))
    model: str = Field(default_factory=lambda: os.environ.get("SF_QWEN_MODEL", "qwen-plus"))
    base_url: str = Field(
        default_factory=lambda: os.environ.get(
            "SF_QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
    )


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
    """Load LLM settings. During bootstrap, delegate to strategyforge's
    settings (which loads the shared .env via pydantic-settings) so the
    SF_QWEN_* credentials resolve. Falls back to raw env vars if
    strategyforge is unavailable (post-vendoring)."""
    try:
        from strategyforge.config import get_settings
        sf = get_settings()
        return LLMSettings(
            api_key=sf.qwen_api_key,
            model=sf.qwen_model,
            base_url=sf.qwen_base_url,
        )
    except Exception:
        return LLMSettings()
