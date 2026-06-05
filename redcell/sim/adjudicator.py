"""LLM adjudication: multi-call panel architecture per MBB wargame methodology.

Three independent expert calls (parallelized) + one synthesis call.
Each expert sees all players' simultaneous actions and assesses positions
from their domain expertise. The synthesis call reconciles into consensus.

This architecture scales to N players without token overflow — each expert
call has focused thinking, and the synthesis call receives structured input.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from .sim_utils import _safe_parse_json

logger = logging.getLogger(__name__)

POSITION_TIERS = ["dominant", "strong", "contested", "weak", "marginal"]
MOMENTUM_SYMBOLS = ["↑", "↗", "→", "↘", "↓"]

POSITION_REVENUE: dict[str, float] = {
    "dominant": 0.12,
    "strong": 0.08,
    "contested": 0.05,
    "weak": 0.03,
    "marginal": 0.01,
}


def _build_expert_schema(side_ids: list[str]) -> dict:
    """Strict schema for expert assessment output.

    DashScope's `strict: true` is partially enforced — required string/enum
    fields are honored when the schema is paired with an explicit prompt
    listing (which EXPERT_PROMPT already has). Boolean fields are NOT
    enforced; this schema uses string enums only.
    """
    assessment_props = {
        sid: {
            "type": "object",
            "properties": {
                "position": {"type": "string", "enum": POSITION_TIERS},
                "momentum": {"type": "string", "enum": MOMENTUM_SYMBOLS},
                "rationale": {"type": "string", "maxLength": 400},
            },
            "required": ["position", "momentum", "rationale"],
            "additionalProperties": False,
        }
        for sid in side_ids
    }
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "expert_assessment",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "assessments": {
                        "type": "object",
                        "properties": assessment_props,
                        "required": list(side_ids),
                        "additionalProperties": False,
                    },
                    "key_observation": {"type": "string", "maxLength": 400},
                },
                "required": ["assessments", "key_observation"],
                "additionalProperties": False,
            },
        },
    }


def _build_synthesis_schema(side_ids: list[str]) -> dict:
    """Strict schema for chief-adjudicator synthesis output.

    Same shape as expert but with longer narrative fields. The position
    field uses POSITION_TIERS enum so the model cannot invent tiers
    (e.g. "stable", "emerging") that would crash downstream consumers.
    """
    position_props = {
        sid: {
            "type": "object",
            "properties": {
                "position": {"type": "string", "enum": POSITION_TIERS},
                "momentum": {"type": "string", "enum": MOMENTUM_SYMBOLS},
                "rationale": {"type": "string", "maxLength": 500},
            },
            "required": ["position", "momentum", "rationale"],
            "additionalProperties": False,
        }
        for sid in side_ids
    }
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "synthesis_decision",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "positions": {
                        "type": "object",
                        "properties": position_props,
                        "required": list(side_ids),
                        "additionalProperties": False,
                    },
                    "interaction_analysis": {"type": "string", "maxLength": 600},
                    "turn_narrative": {"type": "string", "maxLength": 1500},
                },
                "required": ["positions", "interaction_analysis", "turn_narrative"],
                "additionalProperties": False,
            },
        },
    }

EXPERT_ROLES = [
    {
        "id": "industry_veteran",
        "name": "Industry Veteran",
        "desc": "20년차 반도체 산업 애널리스트",
        "expertise": "supply chain dynamics, technology cycles, customer switching behavior, ecosystem lock-in effects",
        "focus": "기술 사이클과 공급망 역학 관점에서 각 플레이어의 경쟁 포지션을 평가하라. 고객 전환 비용, 생태계 효과, 기술 성숙도를 중점적으로 고려하라.",
    },
    {
        "id": "strategy_consultant",
        "name": "Strategy Consultant",
        "desc": "MBB 시니어 파트너",
        "expertise": "competitive interaction effects, game-theoretic reasoning, market structure shifts, resource allocation efficiency",
        "focus": "경쟁 상호작용과 게임이론적 관점에서 평가하라. 동시 행동 간 상쇄/증폭 효과, 자원 배분 효율성, 시장 구조 변화를 중점적으로 분석하라.",
    },
    {
        "id": "regulatory_expert",
        "name": "Regulatory/Policy Expert",
        "desc": "반독점/규제 전문가",
        "expertise": "antitrust implications, compliance costs, government intervention dynamics, open-standard mandates",
        "focus": "규제 환경과 정책 변화 관점에서 평가하라. 반독점 리스크, 규제 비용, 정부 개입 가능성, 오픈 표준 움직임이 각 플레이어에게 미치는 영향을 분석하라.",
    },
]

EXPERT_PROMPT = """You are the {role_name} ({role_desc}) on an adjudication panel for a {industry} competitive wargame.

YOUR EXPERTISE: {expertise}

{previous_positions_block}

{cumulative_arc_block}

CASH STATE:
{cash_block}

THIS TURN'S ACTIONS (all submitted simultaneously):
{actions_block}

{events_block}

{structural_context}

ASSESSMENT INSTRUCTIONS:
{focus}

PRINCIPLES:
1. Assess each action IN CONTEXT of all other players' simultaneous moves
2. Cash-constrained players executing expensive strategies: declining momentum
3. Position changes are INCREMENTAL — max 1 tier per turn, but USE the full range when warranted
4. Market inertia: maintaining position requires effort; passivity means DECLINE
5. External events that structurally favor one side MUST be reflected
6. CUMULATIVE ARC matters: multi-turn capex / R&D / brand-building investments
   are now maturing. A player that invested in stores/clinical/manufacturing
   N turns ago should be earning revenue/capability/credibility from those
   stocks today — even if THIS turn's headline action is small. Conversely,
   serial cash drains without compounding benefit are a structural problem.
   Use the cumulative arc above to weigh accumulated stocks, not just the
   single current move.
7. FACT DISCIPLINE — do NOT invent events. Only the events explicitly listed
   in EXOGENOUS EVENTS THIS TURN (above) or in the cumulative arc's event
   field are real. Do NOT introduce regulatory shifts, supply shocks,
   competitor announcements, or macro changes in your rationale unless they
   are in those lists. Industry background (from structural_context) may
   describe long-running tensions, but treating a background tension as a
   *fired event* without it being in the event list is hallucination.

POSITION TIERS: dominant | strong | contested | weak | marginal
MOMENTUM: ↑ (가속 상승) | ↗ (상승) | → (유지) | ↘ (하락) | ↓ (가속 하락)

{tier_constraint_block}

LANGUAGE: 모든 서술형 텍스트(rationale, key_observation)는 한국어(한글)로만
작성하십시오. 한자(漢字)·중국어·일본어 문자를 절대 사용하지 마십시오.
회사명·기술 약어 등 고유명사는 원문 표기를 그대로 둡니다.

Respond with ONLY JSON:
{{
  "assessments": {{
    {assessment_keys_template}
  }},
  "key_observation": "<한국어 1-2문장: 당신의 전문 영역에서 가장 중요한 관찰>"
}}"""

SYNTHESIS_PROMPT = """You are the CHIEF ADJUDICATOR for a {industry} competitive wargame.
Three expert panelists have independently assessed this turn. Synthesize their opinions into a consensus.

{cumulative_arc_block}

EXPERT ASSESSMENTS:
{expert_assessments_block}

{tier_constraint_block}

SYNTHESIS RULES:
1. Where experts AGREE: adopt the consensus position confidently
2. Where experts DISAGREE: lean toward the BOLDER position change, not conservative compromise
3. The rationale must integrate insights from all experts, not just repeat one
4. interaction_analysis: explain how simultaneous actions interacted (한국어 2-3문장)
5. turn_narrative: describe this turn's market dynamics (한국어 3-5문장).
   IMPORTANT — the narrative must TRACE the cumulative arc, not just restate
   this turn. Example:
     bad: "Shiseido 자본력 압도, AURIE 추락" (반복적, propagation 없음)
     good: "AURIE가 T1-T3 동안 일본 직영 capex를 집중하면서 cash burn이
     누적됐고, T4부터 그 매장 매출이 일부 회수되기 시작했으나 Shiseido의
     T2-T4 가격 공세가 그 마진 회복분을 초과 흡수, T5에 AURIE 일본 매출
     기여가 cash burn을 따라잡지 못해 marginal로 진입"
   즉 *어느 턴의 어떤 투자/행동이* *지금* 결과로 이어졌는지 *연결*하는
   서사를 쓰십시오.
6. FACT DISCIPLINE — narrative MUST NOT invent events. Only events listed
   in the expert assessments or the cumulative arc are real. Do NOT
   reference "regulation", "supply shock", "policy change", "macro shift"
   in the narrative unless they actually appeared as fired events in this
   turn or prior turns. Industry tensions described in scenario background
   are NOT fired events — treating them as such is hallucination.
7. turn_narrative MUST be non-empty. Always produce a 3-5 sentence Korean
   narrative even if signals are mixed.

LANGUAGE: 모든 서술형 텍스트(rationale, interaction_analysis, turn_narrative)는
한국어(한글)로만 작성하십시오. 한자(漢字)·중국어·일본어 문자를 절대 사용하지
마십시오. 회사명·기술 약어 등 고유명사는 원문 표기를 그대로 둡니다.

Respond with ONLY JSON:
{{
  "positions": {{
    {position_keys_template}
  }},
  "interaction_analysis": "<한국어 2-3문장>",
  "turn_narrative": "<한국어 3-5문장>"
}}"""


def _initial_positions(
    shares: dict[str, float],
    companies: dict[str, str],
) -> dict[str, dict]:
    """Bootstrap ordinal positions from initial share percentages."""
    positions = {}
    for sid in companies:
        s = shares.get(sid, 0.25)
        if s >= 0.50:
            pos = "dominant"
        elif s >= 0.35:
            pos = "strong"
        elif s >= 0.20:
            pos = "contested"
        elif s >= 0.10:
            pos = "weak"
        else:
            pos = "marginal"
        positions[sid] = {"position": pos, "momentum": "→", "rationale": "초기 상태"}
    return positions


def _positions_to_text(
    positions: dict[str, dict],
    companies: dict[str, str],
) -> str:
    """Render positions as human-readable text for prompts."""
    lines = []
    for sid, name in companies.items():
        p = positions.get(sid, {})
        pos = p.get("position", "contested")
        mom = p.get("momentum", "→")
        lines.append(f"  {name}: {pos} {mom}")
    return "\n".join(lines)


def _build_context_blocks(
    companies: dict[str, str],
    actions_detail: dict[str, dict],
    previous_positions: dict[str, dict],
    cash: dict[str, float],
    structural_context: str,
    turn_events: list[dict] | None,
    action_history: list[dict] | None = None,
) -> dict[str, str]:
    """Build shared context blocks used by both expert and synthesis prompts.

    ``action_history`` is a list of prior-turn snapshots, oldest first:
        [{"turn": 1, "actions_detail": {sid: {...}}, "positions": {sid: {...}},
          "cash": {sid: float}, "events": [{"label_ko": ...}]}, ...]
    Used to render a multi-turn arc so the adjudicator can reason about
    accumulated capex / R&D / brand-building, not just this turn's snapshot.
    """

    def _sid_label(sid: str) -> str:
        return f"{companies[sid]} ({sid})"

    if previous_positions:
        prev_lines = ["PREVIOUS POSITIONS:"]
        for sid in companies:
            p = previous_positions.get(sid, {})
            pos = p.get("position", "contested")
            mom = p.get("momentum", "→")
            prev_lines.append(f"  {_sid_label(sid)}: {pos} {mom}")
        previous_positions_block = "\n".join(prev_lines)
    else:
        previous_positions_block = "FIRST TURN — no prior position data."

    # Cumulative arc — multi-turn action + position trajectory per side.
    # Lets the panel weigh accumulated stocks (mature capex, R&D pipeline,
    # brand equity) instead of judging on the current turn alone.
    #
    # Sliding window: keep the most recent ARC_DETAIL_WINDOW turns in full
    # detail, summarize older turns as a single line per side. Without this
    # cap, the prompt grows linearly with the run length and the synthesis
    # call truncates its JSON response by ~T5 (observed in probe v4).
    ARC_DETAIL_WINDOW = 3
    if action_history:
        recent = action_history[-ARC_DETAIL_WINDOW:]
        older = action_history[:-ARC_DETAIL_WINDOW]
        arc_lines = [
            "CUMULATIVE ARC (prior turns — read for accumulated stocks like",
            "  matured capex, R&D pipeline, brand-building, or compounding burn):",
        ]
        for sid in companies:
            arc_lines.append(f"\n  {_sid_label(sid)}:")
            if older:
                # Compact summary of older turns: just start/end position + cash.
                first = older[0]
                last = older[-1]
                f_pos = (first.get("positions") or {}).get(sid, {})
                l_pos = (last.get("positions") or {}).get(sid, {})
                f_cash = (first.get("cash") or {}).get(sid, 0.0)
                l_cash = (last.get("cash") or {}).get(sid, 0.0)
                t_lo = first.get("turn", "?")
                t_hi = last.get("turn", "?")
                arc_lines.append(
                    f"    T{t_lo}-T{t_hi} (요약): "
                    f"position {f_pos.get('position', '?')}→{l_pos.get('position', '?')}, "
                    f"cash {f_cash:.0%}→{l_cash:.0%}"
                )
            for snap in recent:
                t = snap.get("turn", "?")
                det = (snap.get("actions_detail") or {}).get(sid, {})
                pos = (snap.get("positions") or {}).get(sid, {})
                c = (snap.get("cash") or {}).get(sid, 0.0)
                action_summary = (
                    det.get("action_type", "")
                    or (det.get("text", "")[:50] if det.get("text") else "(no action)")
                )
                pos_str = (
                    f"{pos.get('position', '?')} {pos.get('momentum', '')}"
                    if pos else "?"
                )
                arc_lines.append(
                    f"    T{t}: action={action_summary} "
                    f"| position={pos_str} | cash={c:.0%}"
                )
                evs = snap.get("events") or []
                if evs:
                    ev_labels = ", ".join(
                        e.get("label_ko", e.get("name", "?")) for e in evs[:3]
                    )
                    arc_lines.append(f"          events: {ev_labels}")
        cumulative_arc_block = "\n".join(arc_lines)
    else:
        cumulative_arc_block = ""

    cash_lines = []
    for sid in companies:
        c = cash.get(sid, 0.5)
        cash_lines.append(f"  {_sid_label(sid)}: cash={c:.0%}")
    cash_block = "\n".join(cash_lines)

    action_lines = []
    for sid in companies:
        detail = actions_detail.get(sid, {})
        text = detail.get("text", "")
        actions_list = detail.get("actions", [])
        if actions_list:
            acts_str = "; ".join(
                f"{a.get('action_type', '?')}(intensity={a.get('intensity', 0.5):.1f}): "
                f"{a.get('text', '')}"
                for a in actions_list
            )
            action_lines.append(f"  {_sid_label(sid)}: {acts_str}")
        elif text:
            at = detail.get("action_type", "")
            intensity = detail.get("intensity", 0.5)
            action_lines.append(f"  {_sid_label(sid)}: {at}(intensity={intensity:.1f}): {text}")
        else:
            action_lines.append(f"  {_sid_label(sid)}: (no action)")
    actions_block = "\n".join(action_lines)

    events_block = ""
    if turn_events:
        ev_lines = ["EXOGENOUS EVENTS THIS TURN:"]
        for ev in turn_events:
            ev_lines.append(
                f"  - {ev.get('label_ko', ev.get('name', '?'))}: "
                f"{ev.get('description', '')}"
            )
        events_block = "\n".join(ev_lines)

    tier_constraint_block = ""
    if previous_positions:
        lines = [
            "TIER JUMP CONSTRAINT "
            "(previous → current, max 1 tier change per turn):"
        ]
        for sid in companies:
            prev_pos = previous_positions.get(sid, {}).get("position", "contested")
            idx = (
                POSITION_TIERS.index(prev_pos)
                if prev_pos in POSITION_TIERS
                else 2
            )
            lo = max(0, idx - 1)
            hi = min(len(POSITION_TIERS) - 1, idx + 1)
            allowed = [POSITION_TIERS[i] for i in range(lo, hi + 1)]
            lines.append(f"  {_sid_label(sid)}: {prev_pos} → allowed: {', '.join(allowed)}")
        tier_constraint_block = "\n".join(lines)

    return {
        "previous_positions_block": previous_positions_block,
        "cumulative_arc_block": cumulative_arc_block,
        "cash_block": cash_block,
        "actions_block": actions_block,
        "events_block": events_block,
        "structural_context": structural_context,
        "tier_constraint_block": tier_constraint_block,
    }


def _run_expert(
    llm: Any,
    role: dict,
    turn: int,
    companies: dict[str, str],
    industry: str,
    ctx: dict[str, str],
) -> dict:
    """Run one expert panelist assessment. Returns parsed assessment dict."""
    assessment_parts = []
    for sid, name in companies.items():
        assessment_parts.append(
            f'    "{sid}": {{"position": "dominant|strong|contested|weak|marginal", '
            f'"momentum": "↑|↗|→|↘|↓", '
            f'"rationale": "{name}에 대한 한국어 1문장 근거"}}'
        )
    assessment_keys_template = ",\n".join(assessment_parts)

    prompt = EXPERT_PROMPT.format(
        role_name=role["name"],
        role_desc=role["desc"],
        expertise=role["expertise"],
        focus=role["focus"],
        industry=industry,
        assessment_keys_template=assessment_keys_template,
        **ctx,
    )

    response = llm.complete(
        system=prompt,
        user=f"Turn {turn}: assess positions from your expertise.",
        temperature=1.0,
        max_tokens=32768,
        enable_thinking=True,
        response_format=_build_expert_schema(list(companies.keys())),
    )

    data = _safe_parse_json(response)
    if not data or "assessments" not in data:
        logger.warning(
            "Expert %s returned unparseable response (turn %d): %s",
            role["id"], turn, (response or "")[:200],
        )
        return {}

    return {
        "role": role["name"],
        "role_id": role["id"],
        "assessments": data["assessments"],
        "key_observation": data.get("key_observation", ""),
    }


def _synthesize_panel(
    llm: Any,
    turn: int,
    companies: dict[str, str],
    industry: str,
    expert_results: list[dict],
    tier_constraint_block: str,
    cumulative_arc_block: str = "",
) -> dict:
    """Synthesize expert assessments into consensus positions."""
    expert_lines = []
    for er in expert_results:
        expert_lines.append(f"[{er['role']}]")
        expert_lines.append(f"  Key observation: {er.get('key_observation', '')}")
        for sid, name in companies.items():
            a = er.get("assessments", {}).get(sid, {})
            expert_lines.append(
                f"  {name} ({sid}): {a.get('position', '?')} {a.get('momentum', '?')} "
                f"— {a.get('rationale', '')}"
            )
        expert_lines.append("")
    expert_assessments_block = "\n".join(expert_lines)

    pos_parts = []
    for sid, name in companies.items():
        pos_parts.append(
            f'    "{sid}": {{"position": "dominant|strong|contested|weak|marginal", '
            f'"momentum": "↑|↗|→|↘|↓", '
            f'"rationale": "{name}에 대한 한국어 1-2문장 근거"}}'
        )
    position_keys_template = ",\n".join(pos_parts)

    prompt = SYNTHESIS_PROMPT.format(
        industry=industry,
        cumulative_arc_block=cumulative_arc_block,
        expert_assessments_block=expert_assessments_block,
        tier_constraint_block=tier_constraint_block,
        position_keys_template=position_keys_template,
    )

    response = llm.complete(
        system=prompt,
        user=f"Turn {turn}: synthesize expert opinions into consensus positions.",
        # Synthesis emits structured JSON with repeated keys (side_a/b/c)
        # and frequent braces/quotes. Qwen's default presence_penalty=1.5
        # penalizes repeated tokens, causing the model to emit an early
        # stop token mid-JSON in probe v3-v6 (finish_reason=stop with
        # incomplete output). Override to presence_penalty=0.0 so the
        # structure can repeat freely. Low temperature also helps.
        temperature=0.3,
        max_tokens=32768,
        presence_penalty=0.0,
        response_format=_build_synthesis_schema(list(companies.keys())),
    )

    data = _safe_parse_json(response)
    if not data or "positions" not in data:
        # Dump full prompt + raw response for offline analysis of the
        # truncation pattern (root cause investigation).
        _dump_synthesis_failure(turn, "unparseable", prompt, response or "")
        raise ValueError(
            f"Synthesis returned unparseable response (turn {turn}): "
            f"{(response or '')[:300]}"
        )
    # Detect empty narrative as a soft failure (not raised — caller has a
    # fallback). Dump so we can diagnose why the model dropped the field.
    if not (data.get("turn_narrative") or "").strip():
        _dump_synthesis_failure(turn, "empty_narrative", prompt, response or "")
    return data


def _dump_synthesis_failure(
    turn: int, kind: str, prompt: str, response: str,
) -> None:
    """Write a full prompt + raw response dump for offline truncation analysis.

    Triggered on synthesis parse failure (kind="unparseable") or empty
    narrative (kind="empty_narrative"). Files go into tmp_review/ which is
    not committed but is the standard probe inspection lane.
    """
    import time
    from pathlib import Path
    try:
        out_dir = Path("tmp_review")
        out_dir.mkdir(exist_ok=True)
        ts = time.strftime("%H%M%S")
        fp = out_dir / f"synthesis_fail_t{turn}_{kind}_{ts}.txt"
        body = (
            f"=== TURN {turn} synthesis failure ({kind}) ===\n"
            f"=== PROMPT (chars={len(prompt)}) ===\n"
            f"{prompt}\n\n"
            f"=== RAW RESPONSE (chars={len(response)}) ===\n"
            f"{response}\n"
        )
        fp.write_text(body, encoding="utf-8")
        logger.warning("Synthesis %s dump → %s", kind, fp)
    except Exception as e:
        logger.warning("Failed to write synthesis dump: %s", e)


def _adjudicate_turn(
    llm: Any,
    turn: int,
    companies: dict[str, str],
    actions_detail: dict[str, dict],
    previous_positions: dict[str, dict],
    cash: dict[str, float],
    industry: str,
    structural_context: str = "",
    turn_events: list[dict] | None = None,
    action_history: list[dict] | None = None,
) -> dict:
    """Multi-call panel adjudication: 3 expert calls (parallel) + 1 synthesis.

    ``action_history`` is the optional multi-turn arc (oldest first) used so
    the panel can reason about accumulated capex/R&D/brand stocks instead of
    only the current turn's headline action. See _build_context_blocks for
    the expected schema.

    Returns:
        {
            "positions": {sid: {"position": str, "momentum": str, "rationale": str}},
            "interaction_analysis": str,
            "turn_narrative": str,
        }
    """
    ctx = _build_context_blocks(
        companies, actions_detail, previous_positions,
        cash, structural_context, turn_events,
        action_history=action_history,
    )

    # Phase 1: parallel expert assessments
    expert_results: list[dict] = []
    with ThreadPoolExecutor(max_workers=len(EXPERT_ROLES)) as executor:
        futures = {
            executor.submit(
                _run_expert, llm, role, turn, companies, industry, ctx,
            ): role
            for role in EXPERT_ROLES
        }
        for future in as_completed(futures):
            role = futures[future]
            try:
                result = future.result()
                if result:
                    expert_results.append(result)
            except Exception as e:
                logger.warning("Expert %s failed (turn %d): %s", role["id"], turn, e)

    if not expert_results:
        raise ValueError(f"All expert assessments failed (turn {turn})")

    # Phase 2: synthesis
    data = _synthesize_panel(
        llm, turn, companies, industry,
        expert_results, ctx["tier_constraint_block"],
        cumulative_arc_block=ctx["cumulative_arc_block"],
    )

    # Validate and clamp positions
    result_positions: dict[str, dict] = {}
    for sid in companies:
        p = data["positions"].get(sid, {})
        pos = p.get("position", "contested")
        if pos not in POSITION_TIERS:
            pos = "contested"
        mom = p.get("momentum", "→")
        if mom not in MOMENTUM_SYMBOLS:
            mom = "→"

        if previous_positions and sid in previous_positions:
            prev_pos = previous_positions[sid].get("position", "contested")
            if prev_pos in POSITION_TIERS and pos in POSITION_TIERS:
                prev_idx = POSITION_TIERS.index(prev_pos)
                new_idx = POSITION_TIERS.index(pos)
                if abs(new_idx - prev_idx) > 1:
                    clamped_idx = prev_idx + (1 if new_idx > prev_idx else -1)
                    pos = POSITION_TIERS[clamped_idx]
                    logger.warning(
                        "Clamped %s position jump: %s → %s (wanted %s)",
                        sid, prev_pos, pos, POSITION_TIERS[new_idx],
                    )

        result_positions[sid] = {
            "position": pos,
            "momentum": mom,
            "rationale": p.get("rationale", ""),
        }

    turn_narrative = data.get("turn_narrative", "") or ""
    if not turn_narrative.strip():
        # Synthesis returned empty narrative — likely truncation residue or
        # the LLM dropped the field. Reconstruct from expert key_observations
        # so the cascade doesn't have a hole that downstream readers cannot
        # interpret.
        logger.warning(
            "Synthesis returned empty turn_narrative (turn %d); "
            "rebuilding from expert key_observations as fallback",
            turn,
        )
        obs_lines = []
        for er in expert_results:
            obs = (er.get("key_observation") or "").strip()
            if obs:
                obs_lines.append(f"[{er.get('role', '')}] {obs}")
        if obs_lines:
            turn_narrative = (
                "(자동 합성 fallback — synthesis 응답이 비어있어 패널 "
                "key_observation 기반 재구성)\n" + "\n".join(obs_lines)
            )
        else:
            turn_narrative = (
                f"(turn {turn} 합성 narrative 누락 — 패널 응답에서도 "
                f"key_observation 미발견)"
            )

    return {
        "positions": result_positions,
        "interaction_analysis": data.get("interaction_analysis", ""),
        "turn_narrative": turn_narrative,
        "expert_results": expert_results,
    }
