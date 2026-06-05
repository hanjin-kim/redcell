"""Lightweight adapter: N-player dict state → GameStateProtocol.

Allows DeliberationV2 to consume N-player simulator's plain-dict state
(shares, cash, power, companies) without coupling to CompetitiveState.

Also provides deliberate_for_nplayer() bridge function that runs 3-phase
deliberation and converts results to N-player's (action_str, delib_dict) format.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .deliberation_v2 import DeliberationV2

logger = logging.getLogger(__name__)


@dataclass
class AdaptedBusinessUnit:
    """Minimal entity satisfying what deliberation accesses on entities."""

    id: str
    side: str
    name: str
    status: str = "ACTIVE"
    segment_key: str = ""
    market_share: float = 0.0
    cash_reserves: float = 0.5
    competitive_power: float = 50.0
    brand_loyalty: float = 50.0
    r_and_d: float = 0.5
    position: str = ""
    momentum: str = ""


class SimulationStateAdapter:
    """Wraps N-player dict state into GameStateProtocol interface."""

    def __init__(
        self,
        *,
        turn: int,
        shares: dict[str, float],
        cash: dict[str, float],
        power: dict[str, float],
        companies: dict[str, str],
        industry: str = "unknown",
        positions: dict[str, dict] | None = None,
    ) -> None:
        self.turn = turn
        self._sides = list(companies.keys())
        self._units: dict[str, AdaptedBusinessUnit] = {}

        for sid, company_name in companies.items():
            unit_id = f"bu_{sid}"
            pos_data = (positions or {}).get(sid, {})
            self._units[unit_id] = AdaptedBusinessUnit(
                id=unit_id,
                side=sid,
                name=company_name,
                segment_key=f"{industry}:main",
                market_share=shares.get(sid, 0.25),
                cash_reserves=cash.get(sid, 0.5),
                competitive_power=power.get(sid, 50.0),
                brand_loyalty=50.0,
                r_and_d=0.5,
                position=pos_data.get("position", ""),
                momentum=pos_data.get("momentum", ""),
            )

    def get_entity(self, entity_id: str):
        return self._units.get(entity_id)

    def get_entities_by_side(self, side: str) -> list:
        return [u for u in self._units.values() if u.side == side]

    def get_all_sides(self) -> list[str]:
        return list(self._sides)

    def advance_turn(self) -> None:
        self.turn += 1

    def to_snapshot(self) -> dict:
        return {
            "turn": self.turn,
            "units": {uid: {"side": u.side, "name": u.name, "market_share": u.market_share}
                      for uid, u in self._units.items()},
            "sides": self._sides,
        }


# ---------------------------------------------------------------------------
# Bridge: DeliberationV2 → N-player (action_str, delib_dict) format
# ---------------------------------------------------------------------------

def deliberate_for_nplayer(
    deliberator: DeliberationV2,
    side: str,
    turn: int,
    shares: dict[str, float],
    cash: dict[str, float],
    power: dict[str, float],
    companies: dict[str, str],
    industry: str,
    n_options: int = 1,
    strategic_buckets: list[dict] | None = None,
    common_core: str = "",
) -> list[tuple[str, dict]]:
    """Run 3-phase C-suite deliberation per strategic bucket.

    When strategic_buckets are provided (from _generate_strategic_buckets),
    each bucket gets its own deliberation with a distinct theory of winning.
    This produces genuinely different options, not intensity variants.

    When no buckets are provided (n_options=1 or fallback), runs single
    deliberation with the original strategic direction.

    Returns list of (action_str, deliberation_dict) tuples.
    """
    adapter = SimulationStateAdapter(
        turn=turn,
        shares=shares,
        cash=cash,
        power=power,
        companies=companies,
        industry=industry,
    )

    orig_dir = deliberator._strategic_direction.get(side, "")
    options: list[tuple[str, dict]] = []

    # Build bucket list: use provided buckets, or single default
    if strategic_buckets and n_options > 1:
        buckets = strategic_buckets[:n_options]
    else:
        buckets = [{"name": "default", "direction": "", "theory_of_winning": ""}]

    for bucket in buckets:
        try:
            # Inject bucket direction (replaces old lens approach)
            if bucket.get("direction"):
                core_note = f"\n[기본값 (이미 결정됨)]: {common_core}" if common_core else ""
                deliberator._strategic_direction[side] = (
                    f"{orig_dir}\n"
                    f"[전략 버킷: {bucket['name']}] {bucket['direction']}\n"
                    f"[Theory of winning] {bucket.get('theory_of_winning', '')}\n"
                    f"위 버킷의 방향에서 구체적 실행을 토론하세요. 다른 방향은 고려하지 마세요."
                    f"{core_note}"
                )
            else:
                deliberator._strategic_direction[side] = orig_dir

            actions, phases = deliberator.deliberate_side(side, adapter)

            if not actions:
                continue

            action_str = "; ".join(
                a.strategy_description or a.action_type for a in actions
            )

            delib = _build_delib_dict(actions, phases)
            # Tag with bucket name for reporting
            delib["_bucket"] = bucket.get("name", "")
            options.append((action_str, delib))

        except Exception as e:
            logger.warning("Deliberation failed for %s bucket '%s': %s",
                          side, bucket.get("name", "?"), e)

    # Restore original direction
    deliberator._strategic_direction[side] = orig_dir
    return options


def _build_delib_dict(actions: list, phases: dict) -> dict:
    """Convert StrategicAction + phases into N-player deliberation dict.

    Produces both:
    - Structured phase data (phase1/phase2/phase3) for v2 reporting
    - Legacy flat keys (ceo/cfo/.../decision) for tree_report.py compat
    """
    phase1 = phases.get("phase1", {})
    phase2 = phases.get("phase2", {})
    position_changes = phases.get("position_changes", [])

    def _role_summary(role: str) -> str:
        """제안 → 최종 포지션 한 줄 요약."""
        proposal = phase1.get(role, {})
        final = phase2.get(role, proposal)
        prop_acts = "+".join(a.get("action", "?") for a in proposal.get("actions", []))
        final_acts = "+".join(a.get("action", "?") for a in final.get("actions", []))
        reason = final.get("changed_because") or proposal.get("reason", "")
        if prop_acts != final_acts and reason:
            return f"{prop_acts} → {final_acts}: {reason}"
        elif reason:
            return f"{final_acts}: {reason}"
        return final_acts

    # Decision & reasoning from Phase 3
    decision_parts = []
    for a in actions:
        desc = a.strategy_description or a.action_type
        intensity = f"({a.intensity:.0%})" if hasattr(a, "intensity") else ""
        decision_parts.append(f"{desc}{intensity}")
    decision = "; ".join(decision_parts)

    reasoning_parts = [a.reasoning for a in actions if a.reasoning and not a.reasoning.startswith("[fallback]")]
    reasoning = " | ".join(reasoning_parts) if reasoning_parts else decision

    # Primary (action_type, intensity) for direct Impact Factor feed. V2 already
    # classified and scored each action during deliberation; downstream market-
    # scenario generation should not re-derive these from the text blob. Expose
    # the dominant (first) action plus the full list for multi-action futures.
    actions_payload = []
    for a in actions:
        a_type = getattr(a, "action_type", "")
        if hasattr(a_type, "value"):
            a_type = a_type.value
        actions_payload.append({
            "action_type": str(a_type or ""),
            "intensity": float(getattr(a, "intensity", 0.5) or 0.5),
            "text": getattr(a, "strategy_description", "") or str(a_type or ""),
        })
    primary = actions_payload[0] if actions_payload else {"action_type": "", "intensity": 0.5, "text": ""}

    return {
        # Structured phases for v2 reporting
        "phase1": phase1,
        "phase2": phase2,
        "phase3": phases.get("phase3", {}),
        "devils_advocate": phases.get("devils_advocate", ""),
        "majority_action": phases.get("majority_action", ""),
        "position_changes": position_changes,
        # Impact Factor engine input (pre-classified by V2, no re-derivation needed)
        "action_type": primary["action_type"],
        "intensity": primary["intensity"],
        "actions_payload": actions_payload,
        # Legacy flat keys for tree_report.py compat
        "ceo": _role_summary("CEO"),
        "cfo": _role_summary("CFO"),
        "cto": _role_summary("CTO"),
        "cmo": _role_summary("CMO"),
        "coo": _role_summary("COO"),
        "decision": decision,
        "reasoning": reasoning,
    }
