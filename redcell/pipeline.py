"""Pipeline orchestrator — adversary → simulate → analyze → render.

Ties the four stages into one call so the CLI (and tests) can run a full
redcell job from a RunConfig.
"""
from __future__ import annotations

import time
from pathlib import Path

import yaml

from .adversary import generate_adversary_moves
from .analysis import analyze_scenario
from .config import RunConfig, load_llm_settings
from .engine import make_llm, run_linear_scenario
from .render import render_brief


def _augmented_strategy(base: str, move: dict) -> str:
    return (
        f"{base}\n\n"
        f"[Red Team scenario context — adversary stress to anticipate]\n"
        f"  Axis: {move['axis']}\n"
        f"  Primary stressor: {move['primary_stressor']}\n"
        f"  Secondary conditions: {move['secondary_conditions']}\n"
        f"  Expected failure mode (hypothesis): {move['expected_failure_mode']}\n"
        f"위 시나리오 압박이 *진행 중*이라는 가정 하에 전략을 펼쳐 deliberate 하라."
    )


def run(config: RunConfig, *, cache_dir: str = ".redcell_cache",
        log=print) -> dict:
    """Execute a full redcell job. Returns the analyzed run dict
    (renderable via render_brief)."""
    llm = make_llm(load_llm_settings())
    scenario = yaml.safe_load(
        Path(config.scenario_path).read_text(encoding="utf-8")
    )

    log(f"[redcell] generating {config.n_scenarios} adversary moves...")
    moves = generate_adversary_moves(
        llm,
        industry=config.industry,
        our_company=config.our_company,
        competitor_list=config.competitors,
        strategy=config.strategy,
        worried_risk=config.worried_risk,
        n_scenarios=config.n_scenarios,
    )
    for i, m in enumerate(moves, 1):
        log(f"  [{i}] ({m['axis']}) {m['label_ko']}")

    scenarios_out = []
    for idx, move in enumerate(moves):
        log(f"[redcell] scenario {idx+1}/{len(moves)}: {move['label_ko']}")
        t0 = time.time()
        trace = run_linear_scenario(
            scenario=scenario,
            strategy=_augmented_strategy(config.strategy, move),
            llm=llm,
            our_side="side_a",
            max_turns=config.max_turns,
            cache_dir=cache_dir,
        )
        log(f"    sim done in {time.time() - t0:.1f}s ({len(trace)} turns)")
        s = {"scenario_idx": idx, "move": move, "trace": trace}
        log(f"    analyzing...")
        s["analysis"] = analyze_scenario(llm, scenario=s)
        scenarios_out.append(s)

    return {
        "user_worried_risk": config.worried_risk,
        "user_strategy": config.strategy,
        "industry": config.industry,
        "scenarios": scenarios_out,
    }


def run_and_render(config: RunConfig, *, output: str,
                   cache_dir: str = ".redcell_cache", log=print) -> str:
    data = run(config, cache_dir=cache_dir, log=log)
    brief = render_brief(data)
    Path(output).write_text(brief, encoding="utf-8")
    log(f"[redcell] brief → {output} ({len(brief)} chars)")
    return brief
