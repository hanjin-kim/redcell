"""Industry competition rulebook generation and formatting."""

from __future__ import annotations

import logging

from .sim_utils import _safe_parse_json

logger = logging.getLogger(__name__)


def _get_rules_for_side(rulebook: dict, side_id: str = "") -> list[dict]:
    """Return rules available to a specific side.

    Backward-compatible: rules without ``available_to`` are treated as shared.
    """
    rules = (rulebook or {}).get("rules", []) or []
    if not side_id:
        return rules
    return [
        r for r in rules
        if not r.get("available_to")
        or "all" in r.get("available_to", [])
        or side_id in r.get("available_to", [])
    ]


def _generate_rulebook(llm, scenario: dict, our_side: str) -> dict:
    """Generate industry-specific competition rulebook via LLM.

    The rulebook defines expected effect ranges for common strategic actions,
    providing calibration anchors for the simulation. This makes delta values
    traceable to explicit assumptions rather than opaque LLM outputs.

    If scenario contains _interview.rulebook_hints, those user-provided
    parameters are injected as anchors to guide LLM generation.
    """
    sides = scenario.get("sides", [])
    companies = {s["id"]: s.get("company", {}).get("name", s["id"]) for s in sides}
    industry = scenario.get("industry", "unknown")
    player_list = ", ".join(companies.values())
    side_ids = [s["id"] for s in sides]
    side_id_list = ", ".join(side_ids)
    side_id_example = side_ids[0] if side_ids else "player_a"

    structural_lines = []
    for sd in sides:
        name = sd.get("company", {}).get("name", sd["id"])
        for adv in sd.get("structural_advantages", []):
            structural_lines.append(f"  {name} (+): {adv}")
        for dis in sd.get("structural_disadvantages", []):
            structural_lines.append(f"  {name} (-): {dis}")
    structural = "\n".join(structural_lines)

    # Inject user-provided hints from interview if present
    hints_block = ""
    interview = scenario.get("_interview", {})
    hints = interview.get("rulebook_hints", {})
    if hints:
        hint_lines = ["USER-PROVIDED MARKET DYNAMICS (use these as anchors):"]
        if hints.get("price_war_share_swing"):
            hint_lines.append(f"  - Price war share swing: {hints['price_war_share_swing']}")
        if hints.get("innovation_cycle_months"):
            hint_lines.append(f"  - Innovation cycle: {hints['innovation_cycle_months']} months")
        if hints.get("regulation_impact"):
            hint_lines.append(f"  - Regulation impact: {hints['regulation_impact']}")
        if hints.get("switching_cost"):
            hint_lines.append(f"  - Switching cost: {hints['switching_cost']}")
        if hints.get("winner_take_all"):
            hint_lines.append(f"  - Winner-take-all tendency: {hints['winner_take_all']}")
        if hints.get("key_dynamics"):
            for d in hints["key_dynamics"]:
                hint_lines.append(f"  - Key dynamic: {d}")
        hint_lines.append("Honor these user inputs when generating delta ranges.")
        hints_block = "\n".join(hint_lines) + "\n\n"

    prompt = f"""You are an industry analyst creating a COMPETITION RULEBOOK for the {industry} market.

Players: {player_list}

Structural context:
{structural}

{hints_block}Generate a rulebook that defines expected share/cash delta ranges for strategic actions in THIS specific industry.
These ranges will constrain a competitive simulation to produce realistic outcomes.

For each rule, specify (all numeric ranges as [low, high] in percentage-point units unless noted):
- action_type: the type of strategic action in English (2-4 words, Title Case, must be UNIQUE across rules). This is the MATCH KEY for the engine — keep it English and stable.
- label_ko: 같은 action_type의 한국어 라벨 (3-8자, 동사+목적어 형태). 보고서 표/차트에 표시됨. 예: "가격 인하", "안전성 인증", "플랫폼 통합"
- description: Korean one-sentence description shown in the rulebook table and Decision Lever panel. 한국어 한 문장으로 작성.
- share_delta_range: [min, max] competitive impact for the ACTOR in percentage-point units. min CAN BE NEGATIVE for high-risk actions where failure erodes position. Competitors are affected proportionally through market normalization — you do NOT need to specify competitor losses separately.
  CRITICAL — asymmetric risk/reward profiles:
  - Safe/operational actions (cost optimization, incremental improvement): [2, 5] — low risk, low reward.
  - Moderate actions (partnerships, marketing push): [3, 8] — standard range.
  - Bold/transformative actions (major R&D bet, market pivot, aggressive acquisition): [-5, 20] — high risk, high reward. These can BACKFIRE (negative min) if execution fails or market rejects.
  - Defensive/hedge actions (diversification, compliance): [1, 4] — small but reliable.
  Each player's action set MUST include at least one bold high-risk action and one safe action. If all actions have similar [2, 8] ranges, the simulation cannot distinguish strategies — this defeats the purpose of the wargame.
- cash_cost_range: [min, max] cash reserve fraction consumed (e.g. [-0.05, -0.02] means 2-5% of cash). Always negative or zero. Bold actions should cost significantly more ([-0.12, -0.06]). Safe actions are cheap ([-0.02, -0.01]).
- delay_turns: how many turns before effect is felt (0 = immediate).
  IMPORTANT: Most competitive actions produce IMMEDIATE market impact (delay=0).
  In a real wargame, facilitators design the rulebook so that every turn produces
  observable share movement — otherwise early turns are dead and the simulation
  is uninformative. Reserve delay≥1 ONLY for genuinely long-lead investments
  (e.g. new fab construction, multi-year R&D). Pricing, partnerships, marketing,
  talent moves, and operational improvements are ALL delay=0.
  Target: at least 70% of rules should be delay=0.
- available_to: list of player IDs who can use this action, or ["all"] if any player can use it.

Player IDs: {side_id_list}

Generate rules in TWO categories:
1. SHARED (available_to: ["all"]): 3-5 generic strategic actions any player can take (pricing, R&D, marketing, talent, regulation).
2. PLAYER-SPECIFIC (available_to: ["{side_id_example}"]): For each player, first identify 3 DISTINCT strategic directions based on their structural advantages (e.g. "ecosystem lock-in", "cost leadership", "customer diversification"). Then for EACH direction, define 2 concrete tactical action_types. This ensures 6 unique tactics per player covering different strategic dimensions — not generic moves relabeled.

Total: 20-25 rules. Each player should end up with 9-11 available actions (shared + their unique ones).
Tune all ranges to {industry}'s real-world dynamics — slow, regulated industries should have tighter share ranges; fast, disruption-heavy industries should have wider ones.
The SPREAD between the safest and boldest action must be at least 15pp (e.g. safe=[1,3] vs bold=[-5,20]). If all actions cluster around [2,8], the simulation will show no strategic differentiation and is USELESS as a wargame tool.

Also specify ONE industry-wide constant:
- revenue_coefficient: fraction of cash reserve that each 100%p of market share generates per turn (typical range 0.02–0.15).
  Software/SaaS/ad-platforms with high margin → higher (0.08-0.15).
  Hardware/manufacturing/capex-heavy → lower (0.02-0.06).
  Commodity/low-margin → low (0.02-0.04).

Respond with ONLY JSON:
{{
  "industry": "{industry}",
  "revenue_coefficient": 0.08,
  "rules": [
    {{
      "action_type": "Price Cut",
      "label_ko": "가격 인하",
      "description": "공격적 가격 인하로 가격 민감 시장을 확보",
      "share_delta_range": [2, 5],
      "cash_cost_range": [-0.06, -0.02],
      "delay_turns": 0,
      "available_to": ["all"]
    }},
    {{
      "action_type": "Breakthrough R&D Bet",
      "label_ko": "차세대 기술 도박",
      "description": "차세대 기술에 대규모 베팅 — 성공 시 시장 재편, 실패 시 자원 낭비",
      "share_delta_range": [-5, 20],
      "cash_cost_range": [-0.12, -0.06],
      "delay_turns": 1,
      "available_to": ["{side_id_example}"]
    }}
  ],
  "market_characteristics": {{
    "switching_cost": "low/medium/high",
    "winner_take_all_tendency": "low/medium/high",
    "regulation_impact": "low/medium/high",
    "innovation_cycle": "fast/medium/slow"
  }}
}}"""

    response = llm.complete(
        system=prompt,
        user="Generate the rulebook.",
        temperature=0.3,
        max_tokens=4000,
    )
    data = _safe_parse_json(response)
    if not data or "rules" not in data:
        raise RuntimeError(
            f"Rulebook generation failed for industry={industry!r}: "
            f"LLM returned no parseable 'rules' field. "
            f"Either fix the LLM connection, or supply `rulebook:` at the "
            f"top level of scenario.yaml to skip generation."
        )
    logger.info("Rulebook generated: %d rules for %s", len(data["rules"]), industry)
    return data


def _rulebook_to_prompt(rulebook: dict) -> str:
    """Convert rulebook to a prompt instruction string for LLM calls."""
    if not rulebook or not rulebook.get("rules"):
        return ""

    lines = ["COMPETITION RULEBOOK — industry-specific effect ranges per action type:"]
    for rule in rulebook["rules"]:
        lo, hi = rule.get("share_delta_range", [1, 5])
        cash_lo, cash_hi = rule.get("cash_cost_range", [-0.05, -0.02])
        avail = rule.get("available_to", ["all"])
        avail_tag = "" if "all" in avail else f" [{', '.join(avail)} only]"
        lines.append(
            f"  - {rule['action_type']}{avail_tag}: impact {lo:+g}~{hi:+g}, "
            f"cash {cash_lo:+.2f}~{cash_hi:+.2f}, "
            f"delay={rule.get('delay_turns', 0)}t"
        )

    chars = rulebook.get("market_characteristics", {})
    if chars:
        lines.append(f"  Market: switching_cost={chars.get('switching_cost', 'medium')}, "
                     f"winner_take_all={chars.get('winner_take_all_tendency', 'medium')}, "
                     f"regulation={chars.get('regulation_impact', 'medium')}")

    lines.append("These ranges are the industry's calibration. Pick (action_type, intensity) "
                 "so the resulting engine-computed delta falls inside these ranges.")
    return "\n".join(lines)


def _generate_event_deck(llm, scenario: dict, rulebook: dict) -> list[dict]:
    """Generate industry-calibrated event deck (White Cell injects) via LLM.

    The event deck provides exogenous shocks injected between turns,
    replacing the archetype system with a more methodologically sound
    Control Team mechanism (per MBB/RAND wargaming practice).
    """
    sides = scenario.get("sides", [])
    companies = {s["id"]: s.get("company", {}).get("name", s["id"]) for s in sides}
    industry = scenario.get("industry", "unknown")
    side_ids = list(companies.keys())
    player_list = ", ".join(f"{sid}={companies[sid]}" for sid in side_ids)

    # Calibration reference from rulebook
    rules = rulebook.get("rules", [])
    cash_ranges = [r["cash_cost_range"] for r in rules if r.get("cash_cost_range")]
    if not cash_ranges:
        raise ValueError(
            "Rulebook has no cash_cost_range — cannot calibrate event deck. "
            "Fix rulebook generation or provide cash_cost_range in rules."
        )
    cash_lo = sum(abs(r[0]) for r in cash_ranges) / len(cash_ranges)
    cash_hi = sum(abs(r[1]) for r in cash_ranges) / len(cash_ranges)
    chars = rulebook.get("market_characteristics", {})

    structural_lines = []
    for sd in sides:
        name = sd.get("company", {}).get("name", sd["id"])
        for adv in sd.get("structural_advantages", []):
            structural_lines.append(f"  {name} ({sd['id']}) (+): {adv}")
        for dis in sd.get("structural_disadvantages", []):
            structural_lines.append(f"  {name} ({sd['id']}) (-): {dis}")
    structural = "\n".join(structural_lines)

    time_horizon = scenario.get("time_horizon", 8)

    prompt = f"""You are a White Cell / Control Team for a {industry} wargame.

Players: {player_list}

Structural context:
{structural}

Market characteristics: {chars}

Time horizon: {time_horizon} turns

Generate an EVENT DECK: 12-18 exogenous market events that a Control Team would
inject between turns to test player adaptability. These are NOT player actions —
they are external shocks, shifts, and news items that change the competitive landscape.

Categories (generate 2-3 events per category):
1. regulatory: new laws, policy changes, compliance requirements
2. demand_shock: customer behavior shifts, end-market growth/decline
3. supply_shock: capacity constraints, input scarcity, logistics disruption
4. technology: next-gen breakthrough, standard change, architecture shift
5. geopolitical: trade tensions, sanctions, regional conflicts
6. black_swan: unexpected crises, IP disputes, leadership scandals

CRITICAL — cash_delta scale:
- cash is a [0, 1] normalized resource index (0=depleted, 1=full, start≈0.5)
- Typical player action costs: {cash_hi:.2f} to {cash_lo:.2f} per turn
- Event cash_delta MUST be within ±{cash_lo:.2f} (same order as action costs)
- NEVER exceed ±0.10 — even a catastrophic black swan is at most ±0.08
- Most events should be ±0.01 to ±0.05

Other rules:
- per-side effects should reflect structural advantages/disadvantages
  (e.g. a player with China exposure is more hurt by export controls)
- probability: 0.08-0.25 per turn (most events are unlikely any given turn)
- Contradictory events share a mutex_group (e.g. "demand_up" and "demand_down")
- eligible_turns: early events [2,3,4], mid-game [3,4,5,6], late [5..{time_horizon}], or broad [2..{time_horizon}]
  (turn 1 is excluded — players need one clean turn to establish baseline)

Player IDs for side_effects: {', '.join(side_ids)}
Effect schema — pick ONE shape per event, matching "mode" EXACTLY:
- mode="uniform": every player gets the SAME delta. Provide a single scalar
  field "uniform_cash_delta" (a number). Do NOT include "side_effects".
- mode="per_side": players get asymmetric deltas reflecting structural
  exposure. Provide "side_effects" with a per-player {{"cash_delta": <num>}}.
  Do NOT include "uniform_cash_delta".

Respond with ONLY JSON:
{{
  "event_deck": [
    {{
      "id": "evt_01",
      "name": "Export Control Tightening",
      "label_ko": "수출규제 강화",
      "description": "미국 정부가 AI 반도체 수출통제를 추가 강화하여 중국향 매출 감소",
      "category": "geopolitical",
      "effects": {{
        "mode": "per_side",
        "side_effects": {{
          "{side_ids[0]}": {{"cash_delta": -0.03}},
          "{side_ids[1] if len(side_ids) > 1 else side_ids[0]}": {{"cash_delta": -0.05}}
        }}
      }},
      "probability": 0.15,
      "eligible_turns": [2, 3, 4, 5],
      "max_occurrences": 1,
      "mutex_group": "trade_policy"
    }},
    {{
      "id": "evt_02",
      "name": "Industry-Wide Demand Surge",
      "label_ko": "산업 전반 수요 급증",
      "description": "AI 인프라 투자 확대로 산업 전체 수요가 동반 상승",
      "category": "market",
      "effects": {{
        "mode": "uniform",
        "uniform_cash_delta": 0.03
      }},
      "probability": 0.12,
      "eligible_turns": [3, 4, 5],
      "max_occurrences": 1,
      "mutex_group": "demand_cycle"
    }}
  ]
}}"""

    response = llm.complete(
        system=prompt,
        user="Generate the event deck.",
        temperature=0.4,
        max_tokens=4000,
    )
    data = _safe_parse_json(response)
    if not data or "event_deck" not in data:
        raise RuntimeError(
            f"Event deck generation failed for industry={industry!r}: "
            f"LLM returned no parseable 'event_deck' field. "
            f"Either fix the LLM connection, or supply `event_deck:` at the "
            f"top level of scenario.yaml to skip generation."
        )
    deck = data["event_deck"]
    logger.info("Event deck generated: %d events for %s", len(deck), industry)
    return deck
