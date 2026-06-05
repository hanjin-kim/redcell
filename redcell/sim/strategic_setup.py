"""Strategic-setup helpers: no-regret moves, distinct buckets, initial deliberation.

Extracted from ``nplayer_simulator.py`` (Phase 2e refactor step 6). These
three LLM calls run once per simulation before the tree/bookend/archetype
paths start, and answer three framing questions:

- ``_extract_common_core`` — what moves should be baseline ("table stakes")
  rather than strategic choices? Keeps the bucket LLM from treating them
  as differentiating options.
- ``_generate_strategic_buckets`` — what genuinely different theories of
  winning exist for this industry, given the user's strategic intent?
  Used to seed distinct tree branches instead of intensity variants of
  the same idea.
- ``_generate_initial_deliberation`` — C-suite one-liner per role for the
  Turn 0 framing shown at the top of each path in the report. Also used
  as a fallback when the in-turn options generator fails.
"""

from __future__ import annotations

import logging

from .sim_utils import _safe_parse_json, _build_player_states_text

logger = logging.getLogger(__name__)


def _extract_common_core(llm, strategy: str, our_side: str, companies: dict,
                         shares: dict, industry: str) -> str:
    """Identify no-regret moves that should be baseline, not options.

    Returns a short description of common core actions.
    """
    our_company = companies[our_side]
    player_states = _build_player_states_text(shares, {}, {}, companies)

    prompt = f"""You are a strategy consultant. Given this competitive situation:

Industry: {industry}
Our company: {our_company} (share: {shares.get(our_side, 0):.1%})
Strategic direction: "{strategy}"

Players:
{player_states}

Identify 1-3 NO-REGRET MOVES — actions that make sense regardless of which strategy we pursue.
These are table stakes, not strategic choices. Examples: maintaining key partnerships, basic compliance, talent retention.

Respond in 2-3 bullet points, English, under 80 words total.
Do NOT include strategic bets or bold moves."""

    try:
        response = llm.complete(system=prompt, user="Identify no-regret moves.",
                                temperature=0.2, max_tokens=800)
        return response.strip()
    except Exception as e:
        logger.warning("Common core extraction failed: %s", e)
        return ""


def _generate_strategic_buckets(llm, strategy: str, our_side: str, companies: dict,
                                shares: dict, industry: str, common_core: str,
                                n_buckets: int = 3,
                                last_actions: dict | None = None) -> list[dict]:
    """Generate distinct strategic buckets with different theories of winning.

    Each bucket defines: direction, theory of winning, key trade-off.
    Returns list of dicts: [{name, direction, theory_of_winning}]
    """
    our_company = companies[our_side]
    player_states = _build_player_states_text(shares, {}, {}, companies)

    comp_actions_block = ""
    if last_actions:
        comp_lines = [f"  {companies.get(sid, sid)}: {act}"
                      for sid, act in last_actions.items() if sid != our_side and act]
        if comp_lines:
            comp_actions_block = f"\nCompetitors' latest actions (react to these, not just our intent):\n" + "\n".join(comp_lines) + "\n"

    prompt = f"""You are a strategy consultant designing a war game for {our_company} in the {industry} market.

Strategic intent: "{strategy}"
Current position: share {shares.get(our_side, 0):.1%}

Players:
{player_states}
{comp_actions_block}
Already decided (common core — NOT part of options):
{common_core or "(none identified)"}

Generate {n_buckets} GENUINELY DIFFERENT strategic options.
Each must have a different THEORY OF WINNING — not the same strategy at different intensity.
Options must RESPOND to competitor actions above, not just restate the strategic intent.

Test: if two options produce the same 18-month roadmap, they are NOT different.

Good examples of distinct buckets:
- "Scale platform leader" (win via ecosystem)
- "Vertical specialist" (win via depth in 2-3 industries)
- "Standards setter" (win via shaping regulation)
- "Fast follower with optionality" (win via flexibility)
- "Capability fortress" (win via one unmatched capability)

Respond with ONLY JSON:
{{"buckets": [
  {{"name": "short English label", "direction": "Korean 30자 이내, 구체적 전략 방향", "theory_of_winning": "English, how we win"}}
]}}"""

    try:
        response = llm.complete(system=prompt, user=f"Generate {n_buckets} distinct strategic buckets.",
                                temperature=0.6, max_tokens=2000)
        data = _safe_parse_json(response)
        if data and "buckets" in data:
            return data["buckets"][:n_buckets]
    except Exception as e:
        logger.warning("Strategic bucket generation failed: %s", e)

    # Fallback: generic buckets
    return [
        {"name": "Scale", "direction": strategy, "theory_of_winning": "win via scale and distribution"},
        {"name": "Focus", "direction": f"{strategy} — 핵심 2-3개 산업에 집중", "theory_of_winning": "win via depth in key verticals"},
        {"name": "Shape", "direction": f"산업 표준을 주도하여 경쟁 우위 확보", "theory_of_winning": "win via setting the rules"},
    ][:n_buckets]


def _generate_competitor_strategies(
    llm, our_side: str, companies: dict, shares: dict, industry: str,
    sides_data: list[dict], trigger_event: str = "",
) -> dict[str, str]:
    """Generate a strategic direction for each competitor based on their persona and position.

    Returns {side_id: strategy_text} for all non-player sides.
    """
    our_company = companies[our_side]
    player_states = _build_player_states_text(shares, {}, {}, companies)

    competitor_blocks = []
    for sd in sides_data:
        sid = sd["id"]
        if sid == our_side:
            continue
        cmds = sd.get("commanders", [])
        cmd = cmds[0] if cmds else {}
        strengths = sd.get("strengths", [])
        weaknesses = sd.get("weaknesses", [])
        competitor_blocks.append(
            f"- {companies[sid]} ({sid}): share={shares.get(sid, 0):.1%}\n"
            f"  CEO: {cmd.get('name', 'Unknown')} — {cmd.get('management_style', 'N/A')}\n"
            f"  Tendency: {cmd.get('strategic_tendency', 'N/A')}\n"
            f"  Strengths: {', '.join(strengths[:3]) if strengths else 'N/A'}\n"
            f"  Weaknesses: {', '.join(weaknesses[:3]) if weaknesses else 'N/A'}"
        )

    trigger_block = f"\nTrigger event: {trigger_event}" if trigger_event else ""

    prompt = f"""You are a competitive intelligence analyst preparing briefing books for a strategy war game.

Industry: {industry}
Players:
{player_states}
{trigger_block}

Competitor profiles:
{chr(10).join(competitor_blocks)}

For EACH competitor, generate a 1-2 sentence strategic direction that:
1. Reflects their CEO's management style and strategic tendency
2. Responds to their current market position (share, strengths, weaknesses)
3. Is specific enough to guide 3-turn tactical decisions (not generic platitudes)
4. Reads like a briefing book entry: "Pursue X by leveraging Y to counter Z"

Write in Korean. Each strategy must be genuinely different — reflecting that company's unique position.

Respond with ONLY JSON:
{{{", ".join(f'"{sid}": "전략 방향 1-2문장"' for sd in sides_data if (sid := sd["id"]) != our_side)}}}"""

    try:
        response = llm.complete(
            system=prompt, user="Generate competitor strategic directions.",
            temperature=0.4, max_tokens=2000,
        )
        data = _safe_parse_json(response)
        if data and isinstance(data, dict):
            return {k: v for k, v in data.items() if k != our_side and isinstance(v, str)}
    except Exception as e:
        logger.warning("Competitor strategy generation failed: %s", e)

    # Fallback: use management_style from persona
    fallback: dict[str, str] = {}
    for sd in sides_data:
        sid = sd["id"]
        if sid == our_side:
            continue
        cmds = sd.get("commanders", [])
        cmd = cmds[0] if cmds else {}
        fallback[sid] = cmd.get("management_style", "") or cmd.get("strategic_tendency", "")
    return fallback


def _generate_initial_deliberation(
    llm, strategy, our_side, companies, shares, cash, power, industry,
) -> dict:
    """Generate C-suite deliberation for the initial strategy (Turn 1)."""
    our_company = companies[our_side]
    player_states = _build_player_states_text(shares, cash, power, companies)

    prompt = f"""You are the C-suite of {our_company} in the {industry} market.
STRATEGIC DIRECTION: "{strategy}"

CURRENT STATE:
{player_states}

Each C-suite member assesses this strategy in ONE sentence.
Keep each response under 40 words. Write all text in Korean. Follow JSON structure strictly.

Respond with ONLY JSON (no markdown fences):
{{"ceo": "한줄 평가", "cfo": "한줄 평가", "cto": "한줄 평가", "cmo": "한줄 평가", "coo": "한줄 평가", "decision": "{strategy[:50]}", "reasoning": "종합 평가"}}"""

    try:
        response = llm.complete(system=prompt, user="Assess.", temperature=0.3, max_tokens=2500)
        data = _safe_parse_json(response)
        if data:
            return data
    except Exception as e:
        logger.warning("Initial deliberation failed: %s", e)
    return {}
