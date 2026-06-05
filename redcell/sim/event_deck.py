"""Event deck: White Cell / Control Team exogenous injection system.

Generates and manages mid-game events that inject environmental uncertainty
into the Markov game simulation, analogous to the Control Team in MBB/RAND wargames.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class EventDeckState:
    """Mutable state tracking event draws across a single game run."""

    deck: list[dict]
    rng: random.Random
    fired: dict[str, int] = field(default_factory=dict)
    history: list[tuple[int, list[dict]]] = field(default_factory=list)

    def fork(self) -> "EventDeckState":
        """Independent copy — used to branch the event tree.

        The deck is immutable and shared; the rng state, fired counts, and
        history are copied so the two branches diverge cleanly.
        """
        clone_rng = random.Random()
        clone_rng.setstate(self.rng.getstate())
        return EventDeckState(
            deck=self.deck,
            rng=clone_rng,
            fired=dict(self.fired),
            history=list(self.history),
        )


def create_event_deck_state(deck: list[dict], seed: int) -> EventDeckState:
    return EventDeckState(deck=deck, rng=random.Random(seed))


def _draw_events(
    state: EventDeckState,
    turn: int,
    max_per_turn: int = 2,
    exclude_ids: set[str] | None = None,
) -> list[dict]:
    """Draw events for this turn from the deck.

    Each eligible event is drawn independently (Bernoulli) with its probability.
    Respects max_occurrences, eligible_turns, and mutex_group constraints.
    Returns at most max_per_turn events.

    ``exclude_ids`` withholds specific events from the stochastic draw — used
    by the event-branch tree so a turn's pivotal event is resolved by the
    branch fork, not by the random draw.
    """
    candidates = []
    excluded = exclude_ids or set()

    for event in state.deck:
        eid = event["id"]
        if eid in excluded:
            continue

        eligible = event.get("eligible_turns")
        if eligible and turn not in eligible:
            continue

        max_occ = event.get("max_occurrences", 1)
        if state.fired.get(eid, 0) >= max_occ:
            continue

        prob = event.get("probability", 0.1)
        if state.rng.random() < prob:
            candidates.append(event)

    # Enforce mutex_group: keep first drawn per group
    seen_groups: set[str] = set()
    filtered = []
    for evt in candidates:
        group = evt.get("mutex_group")
        if group:
            if group in seen_groups:
                continue
            seen_groups.add(group)
        filtered.append(evt)

    # Cap at max_per_turn
    drawn = filtered[:max_per_turn]

    # Update state
    for evt in drawn:
        eid = evt["id"]
        state.fired[eid] = state.fired.get(eid, 0) + 1
    if drawn:
        state.history.append((turn, drawn))

    return drawn


def _build_event_effects(
    drawn_events: list[dict],
    players: list[str],
    max_cash_delta: float = 0.10,
) -> dict:
    """Convert drawn events into effects dict.

    Returns {side_id: {"cash_delta": float}}.
    cash_delta is clamped to [-max_cash_delta, +max_cash_delta] per side
    as a safety net against uncalibrated LLM-generated values.
    """
    effects: dict[str, dict[str, float]] = {
        sid: {"cash_delta": 0.0} for sid in players
    }

    for event in drawn_events:
        eff = event.get("effects", {})
        mode = eff.get("mode", "uniform")

        if mode == "uniform":
            c_delta = float(eff.get("uniform_cash_delta", 0))
            for sid in players:
                effects[sid]["cash_delta"] += c_delta
        else:
            side_effects = eff.get("side_effects", {})
            for sid, deltas in side_effects.items():
                if sid in effects:
                    effects[sid]["cash_delta"] += float(deltas.get("cash_delta", 0))

    for sid in players:
        effects[sid]["cash_delta"] = max(-max_cash_delta, min(max_cash_delta, effects[sid]["cash_delta"]))

    return effects


def _event_deck_to_prompt(events: list[dict]) -> str:
    """Format drawn events as prompt context for agent deliberation."""
    if not events:
        return ""

    lines = ["[이번 턴 외부 이벤트 — 시장 뉴스]"]
    for evt in events:
        label = evt.get("label_ko") or evt.get("name", "Unknown")
        desc = evt.get("description", "")
        cat = evt.get("category", "")
        lines.append(f"• [{cat}] {label}: {desc}")
    lines.append("")
    return "\n".join(lines)
