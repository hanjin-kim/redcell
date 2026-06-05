"""Scenario seed extraction and path-history helpers.

Extracted from ``nplayer_simulator.py`` (Phase 2e refactor step 2). These
three utilities are pure state bookkeeping — no LLM orchestration, no engine
math — so they read more clearly in isolation than when inlined next to the
300-line turn orchestration code.
"""

from __future__ import annotations

import logging

from .sim_utils import _safe_parse_json

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Seed extraction
# ---------------------------------------------------------------------------

def _extract_initial_state(scenario: dict) -> tuple[dict, dict, dict, dict, list, float]:
    """Extract companies, shares, cash, power, and rest_of_market residual from scenario sides.

    The wargaming invariant (Phase 2d) is ``sum(tracked) + rest_of_market == 1.0``
    at all times. Here we compute the seed residual as ``1 - sum(tracked)`` so
    scenarios with partial coverage (e.g. 2-player duopoly covering 70% of the
    real market) surface the remaining 30% as an explicit untracked pool
    instead of silently normalizing the duopoly to 100%.

    Returns (companies, shares, cash, power, sides_data, rest_share).
    Raises ValueError if tracked sum exceeds 1.0 (seed data is inconsistent).
    """
    sides_data = scenario.get("sides", [])
    companies = {s["id"]: s.get("company", {}).get("name", s["id"]) for s in sides_data}
    shares: dict = {}
    cash: dict = {}
    power: dict = {}
    for s in sides_data:
        sid = s["id"]
        bu = s["business_units"][0]
        shares[sid] = bu.get("market_share", 0.25)
        cash[sid] = bu.get("cash_reserves", 0.5)
        power[sid] = bu.get("competitive_power", 50)
    tracked_sum = sum(shares.values())
    if tracked_sum > 1.0 + 1e-6:
        raise ValueError(
            f"Scenario seed invalid: tracked market_share sum = {tracked_sum:.3f} > 1.0. "
            "Check scenario.sides[*].business_units[0].market_share."
        )
    rest_share = max(0.0, 1.0 - tracked_sum)
    return companies, shares, cash, power, sides_data, rest_share


# ---------------------------------------------------------------------------
# Path history — for C-suite reasoning about prior turns
# ---------------------------------------------------------------------------

def _collect_path_history(node, our_side: str, companies: dict) -> list[dict]:
    """Collect turn history from root to this node.

    Returns list of dicts:
      [{turn, actions, actions_detail, shares, prev_shares, share_deltas, summary}]

    share_deltas is what the C-suite needs to reason "did my last move
    actually move the needle, and which competitor action ate it?" — the
    Impact Factor engine already computed this at simulation time, so we
    just surface it here instead of letting the LLM re-derive it from
    absolute-share snapshots.

    Walks parent chain from node to root, then reverses.
    """
    # First collect the chain in forward order so we can compute deltas
    # between consecutive turns without a second pass.
    chain: list = []
    current = node
    while current and current.turn > 0:
        chain.append(current)
        current = current.parent
    chain.reverse()

    # Starting shares come from the root (turn 0) if available.
    if chain and chain[0].parent is not None:
        prev_shares = dict(chain[0].parent.shares)
    else:
        prev_shares = {}

    history: list[dict] = []
    for n in chain:
        deltas = {}
        for sid, now in n.shares.items():
            before = prev_shares.get(sid, now)
            deltas[sid] = float(now) - float(before)
        history.append({
            "turn": n.turn,
            "actions": dict(n.actions),
            "actions_detail": dict(getattr(n, "actions_detail", {}) or {}),
            "shares": dict(n.shares),
            "prev_shares": dict(prev_shares),
            "share_deltas": deltas,
            "summary": n.market_eval or "",
        })
        prev_shares = dict(n.shares)
    return history


def _compact_history(llm, history: list[dict], our_side: str, companies: dict) -> str:
    """Compress multi-turn history into a single summary string (~100 tokens).

    Format surfaces action_type + intensity + per-player share delta so the
    next-turn C-suite can reason about "did my last move actually land, and
    which competitor action ate it?". Absolute-share is kept as a trailing
    anchor but deltas are the primary signal.

    Called once per deliberation to keep prompt size constant regardless of depth.
    """
    if not history:
        return ""

    def _player_label(sid: str) -> str:
        name = companies.get(sid, sid)
        return "우리" if sid == our_side else name

    def _pct(v: float) -> str:
        return f"{v:+.1%}"

    def _fmt_turn(h):
        detail = h.get("actions_detail") or {}
        deltas = h.get("share_deltas") or {}
        raw_actions = h.get("actions") or {}
        parts: list[str] = []
        # Our side first, then everyone else in the order they appear.
        order = [our_side] + [sid for sid in raw_actions if sid != our_side]
        for sid in order:
            if sid not in raw_actions:
                continue
            label = _player_label(sid)
            d = detail.get(sid) or {}
            atype = d.get("action_type") or ""
            intensity = d.get("intensity")
            delta = deltas.get(sid, 0.0)
            if atype and intensity is not None:
                parts.append(
                    f"{label}: {atype}(강도={float(intensity):.1f}) → {_pct(delta)}"
                )
            else:
                # Fallback when Impact Factor detail is absent (legacy runs)
                text = raw_actions.get(sid, "?")
                parts.append(f"{label}: {text} → {_pct(delta)}")
        our_share = h["shares"].get(our_side, 0)
        return (
            f"Turn {h['turn']}: "
            + " / ".join(parts)
            + f"  (우리 누적 점유율 {our_share:.1%})"
        )

    if len(history) <= 2:
        # Short history — raw format, no LLM needed
        return "\n".join(_fmt_turn(h) for h in history)

    # Depth 3+: LLM compact (English prompt for token efficiency)
    raw_lines = [_fmt_turn(h) for h in history]

    prompt = f"""Summarize this strategy simulation history in 2-3 sentences.
Focus on: what strategy was pursued, how competitors responded, how market share evolved.

{chr(10).join(raw_lines)}

Summary:"""

    try:
        response = llm.complete(system=prompt, user="Summarize.", temperature=0.2, max_tokens=500)
        return response.strip()
    except Exception as e:
        logger.warning("History compact failed: %s", e)
        return "\n".join(raw_lines[-2:])


# ---------------------------------------------------------------------------
# Non-actor list — per-scenario denylist for downstream actor substitution
# ---------------------------------------------------------------------------

def _generate_non_actor_list(llm, scenario: dict, companies: dict) -> list[str]:
    """Extract every named non-player entity from the scenario context.

    Phase 2f addition. Hard-coded brand denylists (Microsoft / Azure / etc.)
    only covered AI scenarios; HBM, automotive, telecom, defense scenarios
    each have their own partner / supplier / regulator / standard names that
    the LLM tends to substitute as actors. Generating the denylist from
    the scenario context per simulation makes the guard work for any industry.

    Returns the canonical names of partners, suppliers, products, regulators,
    standards, geographic markets, etc. that LITERALLY appear in scenario
    text but are NOT players. Downstream prompts (turn, action grouping,
    pattern insight, analysis) get this list and are forbidden from naming
    any of these entities as the SUBJECT of an action.

    Empty list on LLM failure — guards still operate via player-name match
    only, just without the broader entity coverage.
    """
    if not llm:
        return []

    sides = scenario.get("sides", []) or []
    industry = scenario.get("industry", "unknown")
    player_names = list(companies.values())

    structural_lines: list[str] = []
    for sd in sides:
        name = sd.get("company", {}).get("name", sd.get("id", "?"))
        for adv in sd.get("structural_advantages", []) or []:
            structural_lines.append(f"  {name} (+): {adv}")
        for dis in sd.get("structural_disadvantages", []) or []:
            structural_lines.append(f"  {name} (-): {dis}")
    additional = scenario.get("_additional_context", "") or ""
    trigger = scenario.get("trigger_event", "") or ""

    system = f"""You are extracting NAMED non-player entities from a scenario context.

Industry: {industry}
Players (the ONLY valid actors in the simulation): {", ".join(player_names)}

Scenario context — structural advantages, disadvantages, trigger, recent context:
{chr(10).join(structural_lines)}

Trigger event:
{trigger}

Additional context:
{additional[:2000]}

TASK
List every named entity in the context above that is NOT a player. Categories:
- Cloud / chip / infrastructure providers (e.g. AWS, Microsoft Azure, NVIDIA, TSMC)
- Product / model names (e.g. ChatGPT, GPT-5, Claude, B100, HBM3E)
- Regulators / regulatory frameworks / standards bodies (e.g. EU AI Act, FDA, JEDEC, NIST)
- Geographic markets where the regulation/event is anchored (e.g. EU, China, US)
- Side competitors mentioned but not in the player list (e.g. Mistral, Llama, CXMT)
- Specific events or tightenings (e.g. CHIPS Act, Q4 2025 export controls)

Use thinking mode to enumerate carefully. False negatives (missed entities)
will let the downstream actor-substitution bug recur (e.g. "Microsoft가 X
했다" attributed to OpenAI's partner instead of OpenAI itself).

Hard rules:
- Output entities that LITERALLY appear in the context above. Do NOT invent.
- Use canonical form as it appears (Microsoft, not MS; Azure, not azure;
  EU AI Act, not "EU's AI Act").
- Players themselves MUST NOT appear in the list.
- Output JSON only.
"""

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "non_actors",
            "schema": {
                "type": "object",
                "properties": {
                    "non_actors": {
                        "type": "array",
                        "items": {"type": "string", "maxLength": 80},
                        "minItems": 0,
                        "maxItems": 60,
                    },
                },
                "required": ["non_actors"],
                "additionalProperties": False,
            },
        },
    }

    try:
        # Thinking mode + generous max_tokens (8000): SGLang Qwen3 dumps
        # reasoning into reasoning_content first, then writes the JSON answer.
        # 1500 tokens was too tight — entire budget went to reasoning, content
        # came back empty. 8000 leaves ~5-6k for thinking + 2k headroom for
        # the JSON answer (which is small, <500 tokens).
        response = llm.complete(
            system=system,
            user="Output the non_actors JSON.",
            temperature=0.2,
            max_tokens=8000,
            response_format=schema,
            enable_thinking=False,
        )
        data = _safe_parse_json(response)
        if data and "non_actors" in data:
            entities = []
            seen = set()
            player_lower = {p.lower() for p in player_names}
            for e in data["non_actors"]:
                ent = str(e).strip()
                if not ent or ent.lower() in player_lower:
                    continue
                low = ent.lower()
                if low in seen:
                    continue
                seen.add(low)
                entities.append(ent)
            logger.info("Non-actor list generated: %d entities", len(entities))
            return entities
    except Exception as e:
        logger.warning("Non-actor list generation failed: %s", e)
    return []
