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
from .render import render_brief, render_trace
from .scrub import scrub_cjk_leakage


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

    log(f"[redcell] running {config.max_turns}-turn simulation"
        f"{f' (n_runs={config.n_runs})' if config.n_runs > 1 else ''}...")
    if config.n_runs > 1:
        log("  ⚠ n_runs > 1: the engine will run M trials but the current "
            "renderer only emits the first trajectory. Multi-trace render "
            "is TODO (see RunConfig.n_runs docstring).")
    t0 = time.time()
    trace = run_linear_scenario(
        scenario=scenario,
        strategy=strategy_with_env,
        environment=config.environment,
        llm=llm,
        our_side="side_a",
        max_turns=config.max_turns,
        n_runs=config.n_runs,
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
    """Run the simulation and emit two files side-by-side:

      - ``{output}``                — headline brief (compact)
      - ``{output_stem}_trace.md``  — full per-turn deliberation dump

    The brief links into the trace via ``#turn-N`` anchors so a reader can
    drill into any turn's C-suite reasoning without bloating the
    top-level brief.
    """
    data = run(config, cache_dir=cache_dir, log=log)

    out_path = Path(output)
    # Companion trace sits next to the brief with a `_trace` suffix.
    trace_path = out_path.with_name(f"{out_path.stem}_trace{out_path.suffix}")
    trace_link = trace_path.name  # relative path for the markdown link

    # CJK-leak scrub: a fresh LLM client (cheap — just an OpenAI SDK
    # instance) for the final pass that rewrites any Chinese/Japanese
    # token leakage Qwen tends to emit in Korean output. See
    # ``redcell/scrub.py`` for the detector + rewrite logic. Paragraphs
    # without leakage skip the LLM entirely so cost stays minimal.
    scrub_llm = make_llm(load_llm_settings())

    brief = render_brief(data, trace_link=trace_link)
    brief = scrub_cjk_leakage(brief, scrub_llm, log=log)
    out_path.write_text(brief, encoding="utf-8")
    log(f"[redcell] brief → {out_path} ({len(brief)} chars)")

    trace = render_trace(data)
    trace = scrub_cjk_leakage(trace, scrub_llm, log=log)
    trace_path.write_text(trace, encoding="utf-8")
    log(f"[redcell] trace → {trace_path} ({len(trace)} chars)")

    return brief
