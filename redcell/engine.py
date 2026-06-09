"""Engine adapter — thin wrapper over the vendored simulation engine.

redcell runs a *linear* multi-turn simulation: each turn, all players'
C-suite teams deliberate, an adjudication panel awards positions, and cash
is booked. No branching, no matched counterfactual (branch_budget=0).

The simulation modules (deliberation panel, adjudicator, event deck,
rulebook generator) live in ``redcell.sim`` — vendored from the original
strategyforge implementation. redcell has zero runtime dependency on
strategyforge as of v0.2.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import LLMSettings
from .llm import LLMAdapter
from .sim import run_event_tree_simulation


def make_llm(settings: LLMSettings) -> Any:
    """Construct the redcell-native LLM adapter. Provider auto-detected
    from ``settings.base_url`` and ``settings.model`` — see ``redcell.llm``
    for the supported providers (sglang, DashScope, OpenAI, OpenAI-compat)."""
    return LLMAdapter(
        model=settings.model,
        api_key=settings.api_key,
        base_url=settings.base_url,
    )


def run_linear_scenario(
    *,
    scenario: dict,
    strategy: str,
    environment: str = "",
    llm: Any,
    our_side: str = "side_a",
    max_turns: int = 5,
    cache_dir: str | Path = ".redcell_cache",
    callback=None,
) -> list[dict]:
    """Run ONE linear simulation (no branching) and return our side's
    per-turn trace.

    The ``environment`` text is the initial exogenous condition (a risk /
    market state / competitor stance the strategy is executed under). It
    is injected into the scenario as ``trigger_event`` so the engine's
    competitor-strategy generator and bucket builder pick it up — making
    competitors react to it, not just our side.

    Returns a list of turn dicts:
      {turn, position, momentum, cash, our_action, audit_action_type,
       audit_intensity, events, narrative, cash_attribution}
    """
    # Shallow-copy scenario so we don't mutate the caller's dict, and
    # inject the environment text as the engine's ``trigger_event`` hook
    # (used by simulation_setup._generate_competitor_strategies and the
    # bucket/momentum generator).
    scenario_with_env = dict(scenario)
    if environment:
        scenario_with_env["trigger_event"] = environment

    result = run_event_tree_simulation(
        scenario=scenario_with_env,
        strategy=strategy,
        our_side=our_side,
        llm=llm,
        max_turns=max_turns,
        our_branch_factor=1,
        n_runs=1,
        branch_budget=0,  # LINEAR — no tree, no counterfactual
        callback=callback,
        cache_dir=Path(cache_dir),
        regenerate=False,
    )
    leaves = result.leaves
    if not leaves:
        return []
    return _linearize(leaves[0], our_side)


def _linearize(leaf, our_side: str) -> list[dict]:
    """Turn each TreeNode along the leaf path into a structured dict that
    exposes every side's data — so the renderer can show competitor
    reactions, not just our trajectory."""
    nodes = leaf.path_from_root()
    out = []
    for n in nodes:
        if n.turn < 1:
            continue
        # Build per-side detail
        sides_data: dict[str, dict] = {}
        for sid, pos in (n.positions or {}).items():
            det = (n.actions_detail or {}).get(sid, {}) or {}
            sides_data[sid] = {
                "position": pos.get("position", "?"),
                "momentum": pos.get("momentum", ""),
                "rationale": pos.get("rationale", "")[:400],
                "cash": (n.cash or {}).get(sid, 0.0),
                "action_text": (n.actions or {}).get(sid, "")[:200],
                "action_type": det.get("action_type", ""),
                "action_intensity": det.get("intensity", 0.5),
                "cash_attribution":
                    dict((n.cash_attribution or {}).get(sid) or {}),
                "is_us": sid == our_side,
            }
        out.append({
            "turn": n.turn,
            "events": [e.get("label_ko", e.get("name", "?"))
                       for e in (n.events or [])],
            "narrative": (n.adjudication or {}).get("turn_narrative", "")[:600],
            "interaction": (n.adjudication or {}).get("interaction_analysis", "")[:400],
            "sides": sides_data,
        })
    return out
