"""Engine adapter — the single extraction boundary to strategyforge.

redcell needs a *linear* multi-turn simulation: each turn, all players'
C-suite teams deliberate, an adjudication panel awards positions, and cash
is booked. No branching, no matched counterfactual (branch_budget=0).

During the 0.1 bootstrap this delegates to strategyforge's
run_event_tree_simulation. To vendor the engine into redcell (cutting the
strategyforge dependency), only this file needs to change — replace the
import + call with a self-contained linear runner over the copied
deliberation / adjudicator / event-deck modules.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from strategyforge.simulation.event_tree import run_event_tree_simulation

from .config import LLMSettings
from .llm import LLMAdapter


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
    llm: Any,
    our_side: str = "side_a",
    max_turns: int = 5,
    cache_dir: str | Path = ".redcell_cache",
    callback=None,
) -> list[dict]:
    """Run ONE linear scenario (no branching) and return a per-turn trace
    for ``our_side``.

    Returns a list of turn dicts:
      {turn, position, momentum, cash, our_action, audit_action_type,
       audit_intensity, events, narrative, cash_attribution}
    """
    result = run_event_tree_simulation(
        scenario=scenario,
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


def _linearize(leaf, side: str) -> list[dict]:
    nodes = leaf.path_from_root()
    out = []
    for n in nodes:
        if n.turn < 1:
            continue
        det = (n.actions_detail or {}).get(side, {}) or {}
        out.append({
            "turn": n.turn,
            "position": (n.positions or {}).get(side, {}).get("position", "?"),
            "momentum": (n.positions or {}).get(side, {}).get("momentum", ""),
            "cash": (n.cash or {}).get(side, 0.0),
            "our_action": (n.actions or {}).get(side, "")[:200],
            "audit_action_type": det.get("action_type", ""),
            "audit_intensity": det.get("intensity", 0.5),
            "events": [e.get("label_ko", e.get("name", "?"))
                       for e in (n.events or [])],
            "narrative": (n.adjudication or {}).get("turn_narrative", "")[:600],
            "cash_attribution":
                dict(n.cash_attribution) if n.cash_attribution else {},
        })
    return out
