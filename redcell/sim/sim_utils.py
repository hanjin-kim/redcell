"""Shared utility functions for tree simulation."""

from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


def _safe_parse_json(response: str) -> dict | None:
    """Parse JSON from LLM response, stripping markdown fences.

    Falls back to ``json_repair`` for common LLM JSON malformations
    (trailing commas, missing closing braces). Always applies a
    *misnesting-recovery* pass: synthesis outputs sometimes embed
    ``interaction_analysis`` and ``turn_narrative`` inside ``positions``
    (the LLM closes ``positions`` too late or never), producing JSON that
    parses cleanly but loses the top-level fields downstream code reads.
    """
    text = response.strip()
    if "```" in text:
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    start = text.find("{")
    if start < 0:
        return None

    parsed: dict | None = None
    # First try strict balanced-brace extraction.
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    parsed = json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    pass
                break

    if parsed is None:
        # Repair fallback for syntax-level errors (trailing commas, missing
        # braces) — common with LLM-generated structured output.
        try:
            import json_repair
            repaired = json_repair.repair_json(text[start:], return_objects=True)
            if isinstance(repaired, dict):
                parsed = repaired
        except Exception:
            pass

    if not isinstance(parsed, dict):
        return None

    # Misnesting recovery — runs on BOTH valid and repaired paths because
    # the most common synthesis failure is *syntactically valid* JSON with
    # top-level keys swallowed into ``positions``. Observed pattern:
    #   {"positions": {"side_a": {...}, "side_b": {...}, "side_c": {...},
    #                  "interaction_analysis": "...", "turn_narrative": "..."}}
    # Downstream reads ``data["turn_narrative"]`` and sees nothing.
    positions = parsed.get("positions")
    if isinstance(positions, dict):
        for promoted_key in ("interaction_analysis", "turn_narrative"):
            if promoted_key in positions and promoted_key not in parsed:
                parsed[promoted_key] = positions.pop(promoted_key)
    return parsed


def _clamp_delta(val: float, lo: float = -0.25, hi: float = 0.25) -> float:
    return max(lo, min(hi, float(val)))


def _apply_share_changes(
    shares: dict,
    cash: dict,
    gains: dict[str, float],
    losses: dict[str, float],
    cash_deltas: dict[str, float],
    revenue_coefficient: float = 0.08,
    rest_share: float = 0.0,
) -> tuple[dict, dict, float]:
    """Apply pre-computed gains and losses to shares. Pure deterministic.

    Returns (new_shares, new_cash, new_rest_share).
    """
    new_shares = {}
    new_cash = dict(cash)

    for sid in shares:
        raw = shares[sid] + gains.get(sid, 0.0) - losses.get(sid, 0.0)
        new_shares[sid] = max(0.01, min(0.99, raw))

    raw_player_total = sum(new_shares.values())
    if rest_share > 0:
        new_rest = max(0.0, 1.0 - raw_player_total)
    else:
        new_rest = 0.0

    total = raw_player_total + new_rest
    if total > 0 and abs(total - 1.0) > 1e-9:
        factor = 1.0 / total
        new_shares = {sid: s * factor for sid, s in new_shares.items()}
        new_rest *= factor

    for sid in new_shares:
        cd = cash_deltas.get(sid, 0.0)
        revenue = new_shares[sid] * revenue_coefficient
        new_cash[sid] = max(0.0, min(1.0, new_cash.get(sid, 0.0) + cd + revenue))

    return new_shares, new_cash, new_rest


def _resolve_cash_costs(
    actions: dict,
    rulebook: dict,
    players: list | None = None,
) -> dict[str, float]:
    """Extract cash costs from rulebook for each player's actions.

    Cash costs have empirical basis (industry benchmarks for R&D spend,
    marketing budgets, etc.) — this is deterministic bookkeeping, not
    competitive adjudication.
    """
    if players is None:
        players = list(actions.keys())
    cash_deltas: dict[str, float] = {sid: 0.0 for sid in players}

    for actor_sid, act_or_list in (actions or {}).items():
        if actor_sid not in cash_deltas:
            continue
        act_list = act_or_list if isinstance(act_or_list, list) else [act_or_list]
        for act in act_list:
            action_type = str(act.get("action_type", "") or "")
            try:
                intensity = float(act.get("intensity", 0.5))
            except (TypeError, ValueError):
                intensity = 0.5
            intensity = max(0.0, min(1.0, intensity))

            rule = _match_action_type(action_type, rulebook)
            if rule is None:
                continue

            cash_delta = _lerp_range(
                rule.get("cash_cost_range", [0, 0]), intensity, (0, 0),
            )
            cash_deltas[actor_sid] += cash_delta

    for sid in cash_deltas:
        cash_deltas[sid] = _clamp_delta(cash_deltas[sid], -0.12, 0.05)

    return cash_deltas


def _apply_cash_bookkeeping(
    cash: dict[str, float],
    cash_deltas: dict[str, float],
    positions: dict[str, dict],
    position_revenue: dict[str, float] | None = None,
) -> dict[str, float]:
    """Apply cash costs and position-based revenue. Pure deterministic.

    Revenue is tied to competitive position via ordinal mapping,
    not share percentage.
    """
    from .adjudicator import POSITION_REVENUE

    rev_map = position_revenue or POSITION_REVENUE
    new_cash: dict[str, float] = {}
    for sid in cash:
        cd = cash_deltas.get(sid, 0.0)
        pos = positions.get(sid, {}).get("position", "contested")
        revenue = rev_map.get(pos, 0.05)
        new_cash[sid] = max(0.0, min(1.0, cash.get(sid, 0.5) + cd + revenue))
    return new_cash


def _proportional_loss_distribution(
    gains: dict[str, float],
    shares: dict[str, float],
    rest_share: float = 0.0,
) -> dict[str, float]:
    """Distribute total gains as losses proportional to current share.

    Pure Python fallback for code paths without LLM access.
    Zero-sum invariant: sum(losses) == sum(gains) in closed market.
    """
    total_gain = sum(max(0.0, g) for g in gains.values())
    if total_gain <= 0:
        return {sid: 0.0 for sid in gains}

    rest_absorption = total_gain * rest_share if rest_share > 0 else 0.0
    player_loss_pool = total_gain - rest_absorption

    if player_loss_pool <= 0:
        return {sid: 0.0 for sid in gains}

    total_share = sum(shares.get(sid, 0.0) for sid in gains)
    if total_share <= 0:
        n = len(gains)
        return {sid: player_loss_pool / n for sid in gains}

    losses = {}
    for sid in gains:
        share_weight = shares.get(sid, 0.0) / total_share
        losses[sid] = player_loss_pool * share_weight

    return losses


def _mature_pending_effects(
    parent_pending: list,
    current_effects: dict,
) -> list:
    """Decrement turns_remaining on deferred effects; merge matured ones into current_effects.

    Each entry in parent_pending: {"turns_remaining": int, "deltas": {sid: float}, "label": str}.
    When turns_remaining reaches 0, the share deltas are added to the corresponding
    player's share_delta in current_effects. Cash was already applied on the originating turn.

    Returns the still-pending entries (turns_remaining > 0 after decrement).
    """
    still_pending = []
    for entry in parent_pending:
        remaining = entry.get("turns_remaining", 0) - 1
        if remaining <= 0:
            for sid, delta in entry.get("deltas", {}).items():
                if sid not in current_effects or not isinstance(current_effects[sid], dict):
                    current_effects[sid] = {"share_gain_pp": 0.0, "cash_delta": 0.0, "resolved": []}
                current_effects[sid]["share_gain_pp"] = _clamp_delta(
                    current_effects[sid].get("share_gain_pp", 0.0) + delta
                )
                if "resolved" in current_effects[sid]:
                    current_effects[sid]["resolved"].append({
                        "action_type": f"[matured] {entry.get('label', '')}",
                        "intensity": 0,
                        "actor_pp": round(delta * 100, 2),
                        "cash_delta": 0,
                        "delay_turns": 0,
                    })
        else:
            still_pending.append({
                "turns_remaining": remaining,
                "deltas": entry.get("deltas", {}),
                "label": entry.get("label", ""),
            })
    return still_pending


def _build_player_states_text(
    shares: dict,
    cash: dict,
    power: dict,
    companies: dict,
    rest_share: float | None = None,
) -> str:
    """Render per-player state block for LLM prompts.

    Appends a "Rest of market" line whenever tracked shares don't fully cover
    the market (invariant ``tracked + rest = 1.0``). The LLM must see this
    residual so it doesn't treat the duopoly as the whole market — otherwise
    the deliberation layer overclaims share moves.

    ``rest_share`` is preferred when the caller has the engine's authoritative
    value; otherwise we derive it from ``1 - sum(shares)``. Explicit 0 hides
    the line for closed-market scenarios (sum already 1.0).
    """
    if rest_share is None:
        tracked_sum = sum(shares.values())
        rest_share = max(0.0, 1.0 - tracked_sum)
    lines = []
    for sid, name in companies.items():
        s = shares.get(sid, 0.0)
        c = cash.get(sid, 0.5)
        p = power.get(sid, 50)
        lines.append(f"  {name}: share={s:.1%}, cash={c:.1%}, power={p:.0f}")
    if rest_share > 0.001:
        lines.append(
            f"  Rest of market: share={rest_share:.1%} "
            f"(passive — open-source / regional / untracked minors, no C-suite, no direct action)"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Impact Factor — engine-side resolution of (action_type, intensity) → effects
#
# All coefficient ranges come from the rulebook. This module only performs
# lookup + linear interpolation; it does not embed any industry-specific
# numbers or keyword mappings.
# ---------------------------------------------------------------------------


def _build_competitor_personas_block(
    side_personas: dict, companies: dict, our_side: str,
) -> str:
    """Build a prompt block describing each competitor's behavioral persona."""
    if not side_personas:
        return ""
    lines = ["COMPETITOR PERSONAS (each player's behavior MUST reflect their persona):"]
    for sid, name in companies.items():
        if sid == our_side:
            continue
        persona = side_personas.get(sid, {})
        if not persona:
            continue
        parts = []
        style = persona.get("management_style", "")
        if style:
            parts.append(f"경영 스타일={style}")
        tendency = persona.get("strategic_tendency", "")
        if tendency:
            parts.append(f"전략 성향={tendency}")
        aggression = persona.get("aggression")
        if aggression is not None:
            parts.append(f"공격성={aggression}")
        if parts:
            lines.append(f"  {name}: {', '.join(parts)}")
    if len(lines) <= 1:
        return ""
    lines.extend([
        "",
        "APPLICATION: conservative/low-aggression players favor defensive/incremental "
        "action_types at moderate intensity. disruptive/high-aggression players favor "
        "aggressive/innovative action_types at higher intensity. Use the aggression "
        "value as an intensity anchor (±0.15 based on scenario pressure).",
    ])
    return "\n".join(lines)


def _list_action_types(rulebook: dict, side_id: str = "") -> str:
    """Format rulebook action_types as a ' | '-separated enum for prompt injection."""
    from .rulebook import _get_rules_for_side
    rules = _get_rules_for_side(rulebook, side_id)
    names = [r.get("action_type", "") for r in rules if r.get("action_type")]
    return " | ".join(names)


def _match_action_type(name: str, rulebook: dict) -> dict | None:
    """Find a rulebook rule matching `name` via exact → substring match.

    Returns None when the rulebook is empty, the name is blank, or no rule
    matches even loosely. A None return is a SIGNAL: the caller (and the
    report) should treat the invoking actor as non-contributing and log it
    as an LLM compliance failure. We deliberately do NOT fall back to any
    rule — silent fallbacks hide rulebook-enum violations and were shown to
    mask "state-frozen" bugs during depth-3/4 testing. Enforcement must
    come from upstream (JSON-schema enum constraints in the LLM prompt),
    not from quiet engine-side papering over.
    """
    rules = (rulebook or {}).get("rules", []) or []
    if not rules:
        return None
    nm = (name or "").strip().lower()
    if not nm:
        return None

    for r in rules:
        if r.get("action_type", "").lower() == nm:
            return r
    for r in rules:
        rt = r.get("action_type", "").lower()
        if rt and (rt in nm or nm in rt):
            return r

    logger.error(
        "No rulebook match for action_type %r (this is an LLM compliance "
        "failure — schema enum should have prevented it)", name
    )
    return None


def _lerp_range(pair, intensity: float, default=(0.0, 0.0)) -> float:
    """Linearly interpolate between pair=[lo, hi] by intensity ∈ [0, 1].

    When the range is entirely negative (e.g. [-5, -2] or [-0.06, -0.02]),
    intensity=1.0 is mapped to the more-extreme magnitude boundary rather
    than the numerically-larger value. This preserves the intuitive semantic
    that 'higher intensity → stronger impact' regardless of sign convention.
    """
    try:
        a, b = float(pair[0]), float(pair[1])
    except (TypeError, ValueError, IndexError):
        a, b = float(default[0]), float(default[1])
    if abs(a) > abs(b):
        weak, strong = b, a
    else:
        weak, strong = a, b
    return weak + intensity * (strong - weak)


def _resolve_impact_factor(
    actions: dict,
    rulebook: dict,
    players: list | None = None,
) -> dict:
    """Convert per-player (action_type, intensity) into share gain pp using rulebook.

    Direct pp delta model: each action produces a position-independent
    share gain. Loss distribution is handled separately by the facilitator.

    Returns ``{sid: {'share_gain_pp': float, 'cash_delta': float, 'resolved': [...]}}``.
    """
    if players is None:
        players = list(actions.keys())
    effects: dict = {
        sid: {"share_gain_pp": 0.0, "cash_delta": 0.0, "resolved": []}
        for sid in players
    }
    pending: list = []

    jitter = float((rulebook or {}).get("intensity_jitter", 0))
    _jitter_rng = None
    if jitter > 0:
        import hashlib, random as _rnd
        def _seed_val(a):
            if isinstance(a, list):
                return [(x.get("action_type", ""), x.get("intensity", 0)) for x in a]
            return (a.get("action_type", ""), a.get("intensity", 0))
        seed_str = json.dumps(
            {s: _seed_val(a) for s, a in sorted((actions or {}).items())},
            sort_keys=True,
        )
        _jitter_rng = _rnd.Random(hashlib.md5(seed_str.encode()).hexdigest())

    for actor_sid, act_or_list in (actions or {}).items():
        if actor_sid not in effects:
            continue
        act_list = act_or_list if isinstance(act_or_list, list) else [act_or_list]
        for act in act_list:
            try:
                intensity = float(act.get("intensity", 0.5))
            except (TypeError, ValueError):
                intensity = 0.5
            if _jitter_rng is not None:
                intensity += _jitter_rng.uniform(-jitter, jitter)
            intensity = max(0.0, min(1.0, intensity))

            action_type = str(act.get("action_type", "") or "")
            rule = _match_action_type(action_type, rulebook)
            if rule is None:
                logger.warning(
                    "action_type '%s' (actor=%s) did not match any rulebook rule — skipped",
                    action_type, actor_sid,
                )
                continue

            actor_pp = _lerp_range(rule.get("share_delta_range", [0, 0]), intensity, (0, 0))
            cash_delta = _lerp_range(rule.get("cash_cost_range", [0, 0]), intensity, (0, 0))

            logger.debug(
                "RESOLVE %s: type='%s' i=%.2f actor_pp=%+.2f",
                actor_sid, action_type, intensity, actor_pp,
            )

            delay = int(rule.get("delay_turns", 0))
            if delay > 0:
                pending.append({
                    "turns_remaining": delay,
                    "deltas": {actor_sid: actor_pp / 100.0},
                    "label": f"{rule.get('action_type', action_type)} by {actor_sid}",
                })
            else:
                effects[actor_sid]["share_gain_pp"] += actor_pp / 100.0

            effects[actor_sid]["cash_delta"] += cash_delta

            effects[actor_sid]["resolved"].append({
                "action_type": rule.get("action_type", action_type),
                "intensity": round(intensity, 3),
                "actor_pp": round(actor_pp, 2),
                "cash_delta": round(cash_delta, 4),
                "delay_turns": delay,
            })

    # Clamp to engine safety bounds.
    for sid in effects:
        effects[sid]["share_gain_pp"] = _clamp_delta(effects[sid]["share_gain_pp"])
        effects[sid]["cash_delta"] = _clamp_delta(effects[sid]["cash_delta"], -0.12, 0.05)

    effects["_pending"] = pending
    return effects
