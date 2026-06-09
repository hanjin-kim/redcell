"""Pipeline orchestrator — single run per (strategy, environment).

v0.3: drops the LLM-driven adversary-scenario generation stage. The
environment is a user input, not something the tool invents. A single
simulation runs with that environment injected into BOTH our strategy
context AND every competitor's strategy context — so competitors react
to the environment, not just our team.
"""
from __future__ import annotations

import time
from pathlib import Path

import yaml

from .config import RunConfig, load_llm_settings
from .engine import make_llm, run_linear_scenario
from .render import render_brief


def _extract_cast(scenario: dict) -> tuple[str, str, list[str]]:
    """Read industry + our_company + competitors from the scenario YAML.

    Our side is ``side_a`` by convention; everyone else is a competitor.
    Falls back to the side ID if a side has no ``company.name``.
    """
    industry = scenario.get("industry", "")
    sides = scenario.get("sides", []) or []
    our_company = ""
    competitors: list[str] = []
    for s in sides:
        sid = s.get("id", "")
        name = (s.get("company") or {}).get("name") or sid
        if sid == "side_a":
            our_company = name
        else:
            competitors.append(name)
    return industry, our_company, competitors


def _augmented_strategy(strategy: str, environment: str) -> str:
    """Append the environment block to a strategy text so the side reading
    it deliberates with the environment in context."""
    return (
        f"{strategy}\n\n"
        f"[배경 환경 — 이 시뮬레이션 시작 시점의 시장/위협 조건]\n"
        f"{environment}\n"
        f"위 환경을 *주어진 외부 조건*으로 받아들이고, 자기 입장에서 합리적으로 반응하라."
    )


def run(config: RunConfig, *, cache_dir: str = ".redcell_cache",
        log=print) -> dict:
    """Execute a redcell job. Returns the renderable run dict."""
    llm = make_llm(load_llm_settings())
    scenario = yaml.safe_load(
        Path(config.scenario_path).read_text(encoding="utf-8")
    )
    industry, our_company, competitors = _extract_cast(scenario)
    log(f"[redcell] cast: {our_company} vs {', '.join(competitors)} "
        f"({industry})")
    log(f"[redcell] environment: {config.environment[:80]}"
        f"{'...' if len(config.environment) > 80 else ''}")

    strategy_with_env = _augmented_strategy(config.strategy, config.environment)

    log(f"[redcell] running {config.max_turns}-turn simulation...")
    t0 = time.time()
    trace = run_linear_scenario(
        scenario=scenario,
        strategy=strategy_with_env,
        environment=config.environment,
        llm=llm,
        our_side="side_a",
        max_turns=config.max_turns,
        cache_dir=cache_dir,
        callback=lambda msg, pct=0.0: log(
            f"  [{pct:5.1%}] {msg[:80]}"
        ),
    )
    log(f"[redcell] sim done in {time.time() - t0:.1f}s ({len(trace)} turns)")

    return {
        "user_strategy": config.strategy,
        "environment": config.environment,
        "industry": industry,
        "our_company": our_company,
        "competitors": competitors,
        "trace": trace,
    }


def run_and_render(config: RunConfig, *, output: str,
                   cache_dir: str = ".redcell_cache", log=print) -> str:
    data = run(config, cache_dir=cache_dir, log=log)
    brief = render_brief(data)
    Path(output).write_text(brief, encoding="utf-8")
    log(f"[redcell] brief → {output} ({len(brief)} chars)")
    return brief
