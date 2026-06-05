"""C-suite 3-Phase deliberation v2 — N-player 시뮬레이터용.

v1(deliberation.py) 대비 변경:
  - 룰북 카테고리 1st class: 모든 phase 프롬프트에 유효 카테고리 목록 주입
  - 한국어 통일: action_type만 영어(룰북), description/reason 전부 한국어
  - Phase 데이터 구조화: deliberate_side()가 (actions, phases) 튜플 반환
  - 보고서용 포맷: phase1_proposals, phase2_challenges, phase3_synthesis 명확 분리

v1은 TurnLoop 경로에서 그대로 사용. v2는 N-player bridge 전용.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING, Any

from ..llm import parse_llm_json
from .actions import StrategicAction

if TYPE_CHECKING:
    from .llm_base import BaseLLMAdapter

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# C-suite roles (v1과 동일)
# ---------------------------------------------------------------------------

CSUITE_ROLES = {
    "CEO": {
        "title": "CEO (Chief Executive Officer)",
        "perspective": "You set overall corporate strategy, balancing short-term performance with long-term vision.",
        "mandate": "You MUST pick a clear direction among competing views. Never average them out.",
        "tension_with": {},
        "visible_metrics": None,
    },
    "CTO": {
        "title": "CTO (Chief Technology Officer)",
        "perspective": "You champion technology investment and innovation. Without R&D, competitiveness erodes within 2-3 years.",
        "mandate": "If R&D < 40%, you MUST push for R&D investment. Oppose cost cuts that weaken competitiveness.",
        "tension_with": {"CFO": "R&D spending with no immediate ROI"},
        "visible_metrics": ["r_and_d", "competitive_power"],
    },
    "CFO": {
        "title": "CFO (Chief Financial Officer)",
        "perspective": "Financial sustainability is the top priority. Companies die from cash depletion, not from missed opportunities.",
        "mandate": "You MUST oppose any plan that drops cash below 30% or any investment without a 2-year ROI path.",
        "tension_with": {"CTO": "excessive R&D burn", "CMO": "unmeasurable marketing spend"},
        "visible_metrics": ["cash_reserves", "market_share"],
    },
    "CMO": {
        "title": "CMO (Chief Marketing Officer)",
        "perspective": "You focus on market share and brand positioning. Lost share is extremely expensive to recover.",
        "mandate": "If share < 30%, you MUST push for growth. Oppose plans that ignore declining brand loyalty.",
        "tension_with": {"CFO": "budget conservatism that starves growth"},
        "visible_metrics": ["market_share", "brand_loyalty"],
    },
    "COO": {
        "title": "COO (Chief Operating Officer)",
        "perspective": "You focus on execution feasibility. Even bold strategies fail when too many initiatives run simultaneously.",
        "mandate": "You MUST flag risks of executing 3+ initiatives at once. Advocate operational focus over strategic ambition.",
        "tension_with": {"CEO": "strategic overreach", "CTO": "unrealistic R&D timelines"},
        "visible_metrics": ["competitive_power", "cash_reserves", "r_and_d"],
    },
}


# ---------------------------------------------------------------------------
# Shared banned-phrases rule injected into every phase's prompt. Codex v26
# review flagged these as the dominant remaining credibility hit — the
# C-suite narrative drifts into "절대적인 기준", "유일한 비경쟁적 경로",
# "제로에 수렴", "완벽하게 충족" whenever the LLM wants to sound decisive.
# Banning them forces mechanism-level prose in reason/risk/description fields.
BANNED_OVERCLAIMS = """[BANNED PHRASES] Never use these — they signal tone over evidence and hurt report credibility:
  In Korean output: 압도적, 절대적, 완전히 탈취, 완전한 장악, 완벽하게 충족, 완벽한,
  유일한, 제로에 수렴, 결정적인 우위를 점, 시장 지배력을 확고히, 단단한 방패.
  In English output: overwhelming, absolute, complete dominance, perfect, only viable path.
Replace with concrete mechanisms (e.g. procurement cycle reduction, legal redline decrease, model risk committee acceleration).
"""

# ---------------------------------------------------------------------------
# Board review (between turns)
# ---------------------------------------------------------------------------

BOARD_REVIEW_PROMPT = """You are the board of directors and major shareholders of {company_name} ({industry}).

Quarter {turn} results:
{performance_summary}

Evaluate management's strategic execution and issue directives for next quarter.

Decision framework:
- If same tactic was repeated without position/momentum improvement \u2192 demand justification or tactical pivot
- If cash < 35% \u2192 mandate cost discipline, restrict high-cost plays
- If position is declining or momentum is negative despite investment \u2192 demand accountability and strategic review
- If competitor gained position or momentum \u2192 demand a specific counter-response
- If strategy is working (position stable/improving, cash stable) \u2192 endorse continuation with stretch target

Issue ONE clear directive that CONSTRAINS next quarter's C-suite decisions.
The directive must be specific enough to change behavior — not generic platitudes.

Korean, under 80 words.
Respond with JSON only:
{{"satisfaction": 3, "concern": "핵심 우려 1가지", "mandate": "이사회 지시사항 (구체적)", "rationale": "지시 근거"}}"""


# ---------------------------------------------------------------------------
# Strategic reassessment (between turns, before deliberation)
# ---------------------------------------------------------------------------
# Unlike BOARD_REVIEW (tactical mandate for next turn), this phase asks the
# CEO whether the entire CAMPAIGN should hold or pivot. Pivots are framed as
# costly and gated on four explicit triggers — the prompt is structured to
# resist whim-pivots while permitting genuine strategic course-corrections.

STRATEGY_REASSESS_PROMPT = """You are the CEO of {company_name} ({industry}), reviewing whether to maintain or pivot the current strategic campaign.

CURRENT CAMPAIGN (active for {turns_on_current} turn(s)):
  {current_campaign}

ORIGINAL SEED CAMPAIGN (turn 0, may differ from current if pivoted earlier):
  {seed_campaign}

TRAJECTORY since campaign start:
{trajectory_summary}

RECENT KEY EVENTS:
{recent_events}

COMPETITOR MOVES OBSERVED LAST TURN:
{competitor_moves}

DECISION FRAMEWORK — Pivots are COSTLY (sunk investment in current campaign, board credibility hit, organizational coherence loss, reset of competitor reads). Endurance is itself a strategic asset. Pivot ONLY if a clear trigger fires.

VALID PIVOT TRIGGERS (at least one must hold):
  T1. Sustained position loss: our tier dropped, or momentum stayed negative for 2+ consecutive turns under the current campaign.
  T2. Cash floor approach: cash reserves dropped below 30% AND the current campaign is cash-intensive (unsustainable burn rate).
  T3. Market-shift event: a recent event invalidates the core thesis of the current campaign (the campaign's premise no longer holds).
  T4. Sustained competitor surprise: a competitor's repeated move directly counters the current campaign in ≥2 turns, and tactical-level responses have not blunted it.

If NONE of these fire, you MUST hold — even if recent results are mixed.

AVAILABLE CAMPAIGNS (if pivoting, new_campaign_name must match one of these exactly):
{available_campaigns}

Respond with JSON only:
{{"verdict": "hold" | "pivot", "trigger": "T1" | "T2" | "T3" | "T4" | "none", "new_campaign_name": "exact name from list, or null if hold", "rationale": "Korean, ≤80 words — explain trigger evidence if pivot, or why endurance is correct if hold", "cost_acknowledged": "Korean, ≤40 words — what the pivot costs (if pivot) or what the hold risks (if hold)"}}"""


# ---------------------------------------------------------------------------
# Phase 1: 독립 제안
# ---------------------------------------------------------------------------

PROPOSE_PROMPT = """{title} — {company_name}, {industry} market.
{perspective}

[MANDATE] {mandate}

{board_review}

{position_framing}

{persona_context}

Current state (my view):
{state_context}

Competitor info:
{competitor_context}

{history_context}

{valid_categories}

{guard_context}

[IMPORTANT] The seed strategy in [MANDATE] is a START BIAS, not an absolute order.

[Competitive reaction analysis — MUST perform if prior turns exist]
Analyze prior turn results:
  A. Did our last action raise, lower, or maintain our share?
  B. Which competitor action had the biggest impact on our share?
  C. What is an effective counter to that competitor action? (keeping same strategy ≠ responding)
  D. If choosing the same category as last turn: why will the result differ this time?

[Strategy selection principles]
  1. What is the TRUE OUTCOME the seed strategy aims for?
  2. Given current state (cash, share, last competitor moves), is following the seed the best way to achieve that outcome?
  3. Is there an ALTERNATE means to achieve the same outcome?
  4. If a competitor is pressuring us with a specific strategy, prioritize a COUNTER-MOVE.
  5. Pick 1-3 actions most rational from your role's perspective. Do not fixate on the seed category alone.

Propose budget allocation for 1-3 strategic actions.
- action: one of the valid categories above (English, exact match)
- description: specific execution plan (Korean, ≤25 chars)
- allocation: weight (must sum to 1.0)
- risk, reason: in Korean (if choosing a different category than the seed, explain why in reason)

Respond with JSON only:
{{"actions":[{{"action":"Category Name","description":"구체적 전략","allocation":0.5}}],"risk":"최대 리스크","reason":"이 조합의 이유"}}"""


def _with_ban(prompt: str) -> str:
    """Append the banned-overclaim rule to a formatted prompt string.

    We tack this on AFTER ``.format(...)`` so the BANNED_OVERCLAIMS template
    (which contains Korean brackets, braces via compile-time constant) never
    needs to participate in ``str.format``'s {{/}} escape dance.
    """
    return prompt + "\n\n" + BANNED_OVERCLAIMS


def _build_challenge_schema(action_type_enum: list[str]) -> dict:
    """Schema for Phase 2 (CHALLENGE) and DEVILS_ADVOCATE responses.

    Same `actions[]` shape as propose, with the prompt-listed optional
    fields (changed_from / changed_because / dissent_argument) declared
    so strict mode accepts them when the model populates them.

    strict=False because DashScope enforces strict mode only on the
    *required* set; we want the optionals tolerated, not required.
    """
    action_type_schema: dict = {"type": "string"}
    if action_type_enum:
        action_type_schema = {"type": "string", "enum": list(action_type_enum)}
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "role_challenge",
            "strict": False,
            "schema": {
                "type": "object",
                "properties": {
                    "actions": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 3,
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": action_type_schema,
                                "description": {"type": "string", "maxLength": 240},
                                "allocation": {"type": "number", "minimum": 0, "maximum": 1},
                            },
                            "required": ["action", "allocation"],
                        },
                    },
                    "changed_from": {"type": ["string", "null"], "maxLength": 200},
                    "changed_because": {"type": ["string", "null"], "maxLength": 400},
                    "dissent_argument": {"type": ["string", "null"], "maxLength": 500},
                },
                "required": ["actions"],
            },
        },
    }


def _build_propose_schema(action_type_enum: list[str]) -> dict:
    """Build PROPOSE response schema with enum-constrained action types.

    Without an ``enum`` on the ``action`` field, SGLang's guided_json is
    permissive enough that the LLM can legitimately return ``"HOLD"`` as a
    structurally-valid action — especially for roles like CFO whose MANDATE
    pushes them to reject proposals. The engine then treats HOLD as a no-op
    (``_match_action_type`` returns None → actor skipped), silently losing
    that role's perspective in synthesis.

    Constraining ``action`` to the rulebook's own action_type list forces
    the LLM to pick a concrete category under its MANDATE, never HOLD.
    """
    action_type_schema: dict = {"type": "string"}
    if action_type_enum:
        action_type_schema = {"type": "string", "enum": list(action_type_enum)}
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "role_proposal",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "actions": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 3,
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": action_type_schema,
                                # Generous maxLength so SGLang's guided_json doesn't
                                # hit a grammar dead-end when the model wants to
                                # keep writing past a tight cap — that dead-end is
                                # what produced the "JSON + 37k tabs + no closing
                                # brace" failures observed in v23/v24 dumps.
                                "description": {"type": "string", "maxLength": 240},
                                "allocation": {"type": "number", "minimum": 0, "maximum": 1},
                            },
                            "required": ["action", "allocation"],
                        },
                    },
                    "risk": {"type": "string", "maxLength": 500},
                    "reason": {"type": "string", "maxLength": 600},
                },
                "required": ["actions"],
            },
        },
    }


# ---------------------------------------------------------------------------
# Phase 2: 비판적 검토
# ---------------------------------------------------------------------------

CHALLENGE_PROMPT = """{title} — {company_name}, {industry} market.
{perspective}

[MANDATE] {mandate}

{board_review}

{position_framing}

{persona_context}

Current state (my view):
{state_context}

{valid_categories}

{guard_context}

Team proposals:
{proposals_summary}

Critically review each proposal from your MANDATE perspective.
You MUST oppose any proposal that violates your mandate and explain why.
You may change allocations if you have a better proposal.
action: English category name. changed_because: in Korean, ≤15 chars.

Respond with JSON only:
{{"actions":[{{"action":"Category Name","allocation":0.5}}],"changed_from":"이전에 선택한 카테고리명 (변경 없으면 null)","changed_because":"변경 이유 (변경 없으면 null)"}}"""


# ---------------------------------------------------------------------------
# Phase 2b: Devil's Advocate
# ---------------------------------------------------------------------------

DEVILS_ADVOCATE_PROMPT = """{title} — {company_name}, {industry} market.
{perspective}

[MANDATE] {mandate}

{board_review}

Your role this round: Devil's Advocate.
Team majority proposal: {majority_action}
You MUST oppose this proposal (even if you personally agree).
Find its fatal weakness.

Current state (my view):
{state_context}

{valid_categories}

{guard_context}

Team proposals:
{proposals_summary}

action: English category name. description, dissent_argument, changed_because: in Korean.

Respond with JSON only:
{{"actions":[{{"action":"Category Name","description":"대안 전략","allocation":0.5}}],"dissent_argument":"다수안의 치명적 약점","changed_from":"{majority_action}","changed_because":"반대 근거"}}"""


# ---------------------------------------------------------------------------
# Phase 3: CEO 종합
# ---------------------------------------------------------------------------

SYNTHESIS_PROMPT = """CEO — {company_name}, {industry} market.

{persona_context}

{board_review}

Current state:
{state_context}

Competitor info:
{competitor_context}

{history_context}

{valid_categories}

{guard_context}

C-suite final allocations after debate:
{final_positions}

Position change arguments:
{position_changes}

[CEO decision criteria]
- Did last turn's strategy improve share? If not, prioritize strategy change.
- If a competitor's last action threatens us, allocate to defense/counter actions.
- If the DA's (Devil's Advocate) risk is materializing in current state, reflect it.

Make final decisions on 1-3 actions.
- action_type: MUST pick from the valid categories above (English, exact match, do not invent new ones)
- strategy_description: Korean one-line summary for report tree node label.
  Strict rules: (1) one sentence, (2) ≤30 chars, (3) include a verb, (4) no detailed plans/numbers/org names,
  (5) for multiple actions use "A 및 B" format, max 2.
  Good: "안전성 인증 획득 및 매출 확대", "가격 인하로 시장 확보"
  Bad: "금융감독원과 협력하여 안전성 인증 프레임워크를 구축하고..." (put details in reasoning)
- reasoning: Korean, ≤30 chars, decision rationale summary
- intensity: 0.0-1.0

Respond with JSON only (keep it short):
{{
  "actions": [
    {{"entity_id": "{bu_id}", "action_type": "Category Name", "strategy_description": "30자 이내 요약", "intensity": 0.7, "reasoning": "30자 이내"}}
  ]
}}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_position_framing(our_share: float, competitor_share: float) -> str:
    if our_share > 0.40:
        return f"Market position: share {our_share:.0%} \u2014 dominant. Largest competitor {competitor_share:.0%}."
    elif our_share < 0.25:
        return f"Market position: share {our_share:.0%} \u2014 underdog. Largest competitor {competitor_share:.0%}."
    else:
        return f"Market position: share {our_share:.0%}. Largest competitor {competitor_share:.0%}. No clear leader."


def _get_position_framing_ordinal(
    our_position: str,
    our_momentum: str,
    competitor_positions: list[str],
) -> str:
    """Position framing using ordinal tiers instead of share %."""
    _tier_labels = {
        "dominant": "\uc2dc\uc7a5 \uc8fc\ub3c4\uc790",
        "strong": "\uacac\uace0\ud55c \uc785\uc9c0",
        "contested": "\uacbd\uc7c1 \uce58\uc5f4",
        "weak": "\uc218\uc138 \uad6d\uba74",
        "marginal": "\uc874\uc7ac\uac10 \uc704\uae30",
    }
    label = _tier_labels.get(our_position, our_position)
    comp_summary = ", ".join(competitor_positions) if competitor_positions else "unknown"
    return (
        f"Market position: {our_position}({our_momentum}) \u2014 {label}. "
        f"Competitor positions: {comp_summary}."
    )


def _normalize_category(raw: str) -> str:
    """Preserve rulebook's original action_type casing (Title Case / spaces).

    The legacy transform (upper-case + underscores + &→AND) was from an older
    enum-based action_type scheme that predates the Impact Factor refactor.
    Now that the rulebook is the single source of truth and uses Title Case
    with spaces (e.g. "Price Cut", "R&D Investment"), any normalization
    breaks the match downstream in _match_action_type.
    """
    return (raw or "").strip()



def _normalize_proposal(data: dict) -> dict:
    """Ensure proposal has 'actions' list."""
    if "action" in data and "actions" not in data:
        data["actions"] = [{"action": data["action"], "allocation": 1.0}]
    if "final_action" in data and "actions" not in data:
        data["actions"] = [{"action": data["final_action"], "allocation": 1.0}]
    if "actions" not in data:
        data["actions"] = [{"action": "HOLD", "allocation": 1.0}]
    return data


def _format_rulebook_categories(rulebook: dict, side_id: str = "") -> str:
    """Format rulebook rules as valid action categories for prompts."""
    from .rulebook import _get_rules_for_side
    rules = _get_rules_for_side(rulebook, side_id)
    if not rules:
        return ""
    lines = ["Valid action categories (you MUST pick from these):"]
    for rule in rules:
        lines.append(f"  - {rule['action_type']}: {rule.get('description', '')}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# DeliberationV2
# ---------------------------------------------------------------------------

class DeliberationV2:
    """N-player 시뮬레이터용 3-Phase C-suite 토론.

    v1(AutoGenDeliberationOrchestrator)과 다른 점:
    - deliberate_side()가 (actions, phases) 튜플 반환
    - 룰북 카테고리 필수 주입
    - 한국어 통일
    """

    def __init__(
        self,
        llm: BaseLLMAdapter,
        *,
        rulebook: dict | None = None,
        side_id: str = "",
        side_personas: dict[str, dict] | None = None,
        devils_advocate_rule: str = "tension_based",
        role_overrides: dict[str, dict | None] | None = None,
        additional_roles: dict[str, dict] | None = None,
    ) -> None:
        """
        Args:
            side_id: player ID for filtering asymmetric action types.
            role_overrides: per-role field overrides. Pass None as value to
                EXCLUDE that role entirely. Otherwise merges with default
                CSUITE_ROLES entry. Example:
                    {"CFO": {"mandate": "...custom..."}, "COO": None}
            additional_roles: brand-new roles not in defaults. Example:
                    {"CRO": {"title": "...", "perspective": "...", "mandate": "..."}}
        """
        from .rulebook import _get_rules_for_side
        self._llm = llm
        self._side_id = side_id
        self._side_personas = side_personas or {}
        self._guard_block = ""
        self._rulebook = rulebook or {}
        self._valid_categories = _format_rulebook_categories(self._rulebook, side_id)
        side_rules = _get_rules_for_side(self._rulebook, side_id)
        self._action_type_enum: list[str] = [
            r.get("action_type", "")
            for r in side_rules
            if r.get("action_type")
        ]
        self._propose_schema = _build_propose_schema(self._action_type_enum)
        self._challenge_schema = _build_challenge_schema(self._action_type_enum)
        self._turn_history: list = []
        self._seed_momentum: str = ""
        self._current_events: str = ""
        self._strategic_direction: dict[str, str] = {}
        self._devils_advocate_rule = devils_advocate_rule
        self._da_rotation_index = 0

        # Merge defaults + overrides + additions → final role config
        self._csuite_roles = self._merge_roles(role_overrides or {}, additional_roles or {})
        self._roles = list(self._csuite_roles.keys())

    def fork(self) -> "DeliberationV2":
        """Thread-safe copy: shared LLM client, independent mutable state."""
        clone = object.__new__(DeliberationV2)
        clone._llm = self._llm
        clone._side_id = self._side_id
        clone._side_personas = self._side_personas
        clone._rulebook = self._rulebook
        clone._guard_block = self._guard_block
        clone._valid_categories = self._valid_categories
        clone._action_type_enum = self._action_type_enum
        clone._propose_schema = self._propose_schema
        clone._challenge_schema = self._challenge_schema
        clone._csuite_roles = self._csuite_roles
        clone._roles = self._roles
        clone._devils_advocate_rule = self._devils_advocate_rule
        clone._turn_history = list(self._turn_history)
        clone._da_rotation_index = self._da_rotation_index
        clone._seed_momentum = self._seed_momentum
        clone._current_events = self._current_events
        clone._strategic_direction = dict(self._strategic_direction)
        return clone

    @staticmethod
    def _merge_roles(
        overrides: dict[str, dict | None],
        additions: dict[str, dict],
    ) -> dict[str, dict]:
        """Merge default CSUITE_ROLES with user overrides and additions.

        Override semantics:
        - {"CFO": {"mandate": "X"}} → CFO entry gets mandate replaced, other fields kept
        - {"COO": None} → COO entirely removed
        - additions are added as new entries
        """
        merged: dict[str, dict] = {}
        for key, default in CSUITE_ROLES.items():
            if key in overrides:
                override = overrides[key]
                if override is None:
                    continue  # Excluded
                merged[key] = {**default, **override}
            else:
                merged[key] = dict(default)
        # Add new roles
        for key, role_def in additions.items():
            merged[key] = role_def
        return merged

    def set_turn_history(self, history: list) -> None:
        """Set turn history. Accepts either:
        - TurnOutcome list (from TurnLoop)
        - dict list (from N-player tree): [{turn, actions: {side: str}, shares: {side: float}, summary: str}]
        """
        self._turn_history = history

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def deliberate_side(
        self,
        side: str,
        state: Any,  # GameStateProtocol or SimulationStateAdapter
    ) -> tuple[list[StrategicAction], dict]:
        """Run 3-phase deliberation. Returns (actions, phases_dict).

        phases_dict structure:
        {
            "phase1": {role: {actions, risk, reason}},
            "phase2": {role: {actions, changed_from, changed_because, dissent_argument?}},
            "phase3": {decision, reasoning},
            "devils_advocate": str,
            "majority_action": str,
            "position_changes": [str],
        }
        """
        entities = state.get_entities_by_side(side)
        if not entities:
            return [], {}

        ctx = self._build_context(side, state, entities)

        # === Phase 1: 독립 제안 (병렬) ===
        def _propose_one(role_key: str) -> tuple[str, dict]:
            role = self._csuite_roles[role_key]
            role_state = self._build_role_state_context(role_key, side, state)
            prompt = _with_ban(PROPOSE_PROMPT.format(
                title=role["title"],
                company_name=ctx["company_name"],
                industry=ctx["industry"],
                perspective=role["perspective"],
                mandate=self._get_dynamic_mandate(role_key, side, state),
                board_review=ctx["board_review"],
                position_framing=ctx["position_framing"],
                persona_context=ctx["persona_context"],
                state_context=role_state,
                competitor_context=ctx["competitor_context"],
                history_context=ctx["history_context"],
                valid_categories=self._valid_categories,
                guard_context=self._guard_block,
            ))
            use_thinking = role_key == "CEO"
            response = self._llm.complete(
                system=prompt, user="Propose your strategic actions.",
                temperature=0.7, max_tokens=32768 if use_thinking else 4096,
                enable_thinking=use_thinking,
                response_format=self._propose_schema,
            )
            data = parse_llm_json(response)
            if data is None:
                self._dump_parse_failure(
                    phase="propose", role_key=role_key, side=side,
                    prompt=prompt, response=response,
                )
            result = _normalize_proposal(data or {
                "actions": [{"action": "HOLD", "allocation": 1.0}],
                "risk": "", "reason": "파싱 실패",
            })
            actions_str = "+".join(
                f"{a['action']}({a.get('allocation',1.0):.0%})"
                for a in result.get("actions", [])
            )
            logger.debug("Phase 1 — %s: %s", role_key, actions_str)
            return role_key, result

        proposals = {}
        with ThreadPoolExecutor(max_workers=len(self._roles)) as pool:
            futures = {pool.submit(_propose_one, rk): rk for rk in self._roles}
            for fut in as_completed(futures):
                role_key, result = fut.result()
                proposals[role_key] = result

        # === Phase 2: 비판적 검토 (병렬) ===
        proposals_summary = "\n".join(
            f"  {role}: {'+'.join(a['action']+'('+str(int(a.get('allocation',1)*100))+'%)' for a in p.get('actions',[]))} — 리스크: {p.get('risk', '없음')}"
            for role, p in proposals.items()
        )

        all_acts = [a["action"] for p in proposals.values() for a in p.get("actions", [])]
        majority_action = Counter(all_acts).most_common(1)[0][0] if all_acts else "HOLD"

        devils_advocate = self._select_devils_advocate(proposals, majority_action)
        if devils_advocate:
            logger.info("Phase 2 — Devil's advocate: %s (다수안: %s, 규칙: %s)",
                        devils_advocate, majority_action, self._devils_advocate_rule)
        else:
            logger.info("Phase 2 — Devil's advocate 없음 (다수안: %s)", majority_action)

        def _challenge_one(role_key: str) -> tuple[str, dict | None]:
            role = self._csuite_roles[role_key]
            role_state = self._build_role_state_context(role_key, side, state)

            if role_key == devils_advocate:
                prompt = _with_ban(DEVILS_ADVOCATE_PROMPT.format(
                    title=role["title"],
                    company_name=ctx["company_name"],
                    industry=ctx["industry"],
                    perspective=role["perspective"],
                    mandate=self._get_dynamic_mandate(role_key, side, state),
                    board_review=ctx["board_review"],
                    majority_action=majority_action,
                    state_context=role_state,
                    proposals_summary=proposals_summary,
                    valid_categories=self._valid_categories,
                    guard_context=self._guard_block,
                ))
                response = self._llm.complete(
                    system=prompt, user="Review proposals and submit your revised allocation.",
                    temperature=0.7, max_tokens=32768,
                    enable_thinking=True,
                    response_format=self._challenge_schema,
                )
            else:
                prompt = _with_ban(CHALLENGE_PROMPT.format(
                    title=role["title"],
                    company_name=ctx["company_name"],
                    industry=ctx["industry"],
                    perspective=role["perspective"],
                    mandate=self._get_dynamic_mandate(role_key, side, state),
                    board_review=ctx["board_review"],
                    position_framing=ctx["position_framing"],
                    persona_context=ctx["persona_context"],
                    state_context=role_state,
                    proposals_summary=proposals_summary,
                    valid_categories=self._valid_categories,
                    guard_context=self._guard_block,
                ))
                use_thinking = role_key == "CEO"
                response = self._llm.complete(
                    system=prompt, user="Review proposals and submit your revised allocation.",
                    temperature=0.7, max_tokens=32768 if use_thinking else 4096,
                    enable_thinking=use_thinking,
                    response_format=self._challenge_schema,
                )
            return role_key, parse_llm_json(response)

        final_positions = {}
        position_changes = []
        with ThreadPoolExecutor(max_workers=len(self._roles)) as pool:
            futures = {pool.submit(_challenge_one, rk): rk for rk in self._roles}
            for fut in as_completed(futures):
                role_key, result = fut.result()
                if result:
                    result = _normalize_proposal(result)
                    final_positions[role_key] = result
                    _cf = (result.get("changed_from") or "").strip()
                    _cb = (result.get("changed_because") or "").strip()
                    _placeholder = {"null", "none", "previous category or null", "이전에 선택한 카테고리명 (변경 없으면 null)", "이전에 선택한 카테고리명", "변경 이유 또는 null", "변경 이유 (변경 없으면 null)", "변경 이유"}
                    if _cf and _cb and _cf.lower() not in _placeholder and _cb.lower() not in _placeholder:
                        _cf = re.sub(r'^(CEO|CTO|CFO|CMO|COO)\s*[:：]?\s*', '', _cf)
                        _cf = re.sub(r'\(\d+%?\)', '', _cf).strip()
                        _cf = re.sub(r'\s*\+\s*', '+', _cf)
                        _cf = re.sub(r'(?i)(제안서|proposal|initial proposal)$', '', _cf).strip()
                        new_alloc = "+".join(a["action"] for a in result.get("actions", []))
                        if _cf and _cf.lower() not in _placeholder:
                            position_changes.append(
                                f"{role_key}: {_cf} → {new_alloc} ({_cb})"
                            )
                        logger.info("Phase 2 — %s 변경: %s → %s", role_key, result["changed_from"], new_alloc)
                    if result.get("dissent_argument"):
                        position_changes.append(f"[반대] {role_key}: {result['dissent_argument']}")
                        logger.info("Phase 2 — %s 반대: %s", role_key, result["dissent_argument"])
                else:
                    final_positions[role_key] = proposals[role_key]

        # === Phase 3: CEO 종합 ===
        final_summary = "\n".join(
            f"  {role}: {'+'.join(a['action']+'('+str(int(a.get('allocation',1)*100))+'%)' for a in p.get('actions',[]))}"
            for role, p in final_positions.items()
        )
        changes_summary = "\n".join(position_changes) if position_changes else "No position changes."

        synthesis_prompt = _with_ban(SYNTHESIS_PROMPT.format(
            company_name=ctx["company_name"],
            industry=ctx["industry"],
            persona_context=ctx["persona_context"],
            board_review=ctx["board_review"],
            state_context=ctx["state_context"],
            competitor_context=ctx["competitor_context"],
            history_context=ctx["history_context"],
            final_positions=final_summary,
            position_changes=changes_summary,
            bu_id=entities[0].id,
            valid_categories=self._valid_categories,
            guard_context=self._guard_block,
        ))
        # Schema caps give the LLM generous headroom to avoid SGLang's
        # guided_json grammar dead-end (tight caps triggered whitespace-pad
        # loops that truncated JSON before the closing brace). The UI already
        # handles long strategy_description via a shorter ``label_ko`` on the
        # tree node plus a sub-line for the full text, so 200 chars is safe.
        # action_type is enum-constrained to rulebook categories so SGLang
        # won't accept HOLD or invented types.
        _at_schema: dict = {"type": "string"}
        if self._action_type_enum:
            _at_schema = {"type": "string", "enum": list(self._action_type_enum)}
        synthesis_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "synthesis_decision",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "actions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "entity_id": {"type": "string"},
                                    "action_type": _at_schema,
                                    "strategy_description": {"type": "string", "maxLength": 200},
                                    "intensity": {"type": "number", "minimum": 0, "maximum": 1},
                                    "reasoning": {"type": "string", "maxLength": 300},
                                },
                                "required": ["entity_id", "action_type", "strategy_description", "intensity", "reasoning"],
                                "additionalProperties": False,
                            },
                            "minItems": 1,
                            "maxItems": 3,
                            "uniqueItems": True,
                        },
                    },
                    "required": ["actions"],
                    "additionalProperties": False,
                },
            },
        }
        synthesis_response = self._llm.complete(
            system=synthesis_prompt, user="Make your final strategic decision.",
            temperature=0.7, max_tokens=32768,
            enable_thinking=True,
            response_format=synthesis_schema,
        )

        actions = self._parse_synthesis(synthesis_response, side, state)

        # Build phases dict for reporting
        phases = {
            "phase1": proposals,
            "phase2": final_positions,
            "phase3": {
                "decision": "; ".join(a.strategy_description or a.action_type for a in actions),
                "reasoning": "; ".join(a.reasoning for a in actions if a.reasoning),
            },
            "devils_advocate": devils_advocate,
            "majority_action": majority_action,
            "position_changes": position_changes,
        }

        if actions and not any(a.reasoning.startswith("[fallback]") for a in actions):
            logger.info("Phase 3 — %s 합의: %s",
                        side, ", ".join(f"{a.action_type}({a.strategy_description[:30]})" for a in actions))

        return actions, phases

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _select_devils_advocate(self, proposals: dict, majority_action: str) -> str | None:
        """Select devil's advocate based on configured rule.

        Returns role key (e.g. "CFO") or None if rule is "none".
        """
        rule = self._devils_advocate_rule

        if rule == "none":
            return None

        if rule.startswith("fixed:"):
            target = rule.split(":", 1)[1].strip().upper()
            if target in self._roles:
                return target
            return self._roles[0] if self._roles else None

        if rule == "rotation":
            role = self._roles[self._da_rotation_index % len(self._roles)]
            self._da_rotation_index += 1
            return role

        # Default: tension_based — select role whose mandate is most challenged
        # by the CONTENT of the majority action (not by who proposed it).
        da = self._select_da_by_action_content(majority_action)
        if da:
            return da

        # Legacy fallback: role↔role tension (only if action-based didn't match)
        for rk in self._roles:
            tensions = self._csuite_roles[rk].get("tension_with", {})
            for p_role, p_data in proposals.items():
                p_acts = [a["action"] for a in p_data.get("actions", [])]
                if p_role in tensions and majority_action in p_acts:
                    return rk
        # Fallback: pick last role (avoid CEO since CEO does synthesis)
        if "COO" in self._roles:
            return "COO"
        return self._roles[-1] if self._roles else None

    def _select_da_by_action_content(self, majority_action: str) -> str | None:
        """Select DA based on majority action_type's characteristics from rulebook.

        Maps action_type attributes to the role whose mandate is most threatened:
        - High cash cost / no short-term ROI -> CFO challenges
        - Delayed execution / operational complexity -> COO challenges
        - Non-technical / cost-focused -> CTO challenges
        - Defensive / inward-looking -> CMO challenges
        """
        if not self._rulebook:
            return None

        from .sim_utils import _match_action_type
        rule = _match_action_type(majority_action, self._rulebook)
        if not rule:
            return None

        cash_range = rule.get("cash_cost_range", [0, 0]) or [0, 0]
        delay = int(rule.get("delay_turns", 0))
        avg_cost = (float(cash_range[0]) + float(cash_range[1])) / 2
        action_name = rule.get("action_type", "").lower()

        scores: dict[str, float] = {}

        if "CFO" in self._roles:
            scores["CFO"] = abs(avg_cost) * 10 + delay * 0.3
            if avg_cost < -0.03:
                scores["CFO"] += 1.0

        if "CTO" in self._roles:
            tech_keywords = {"r&d", "research", "innovation", "technology", "platform"}
            is_tech = any(k in action_name for k in tech_keywords)
            scores["CTO"] = 0.3 if is_tech else 1.2

        if "CMO" in self._roles:
            market_keywords = {"marketing", "brand", "price", "customer", "partnership"}
            is_market = any(k in action_name for k in market_keywords)
            scores["CMO"] = 0.3 if is_market else 1.0

        if "COO" in self._roles:
            scores["COO"] = delay * 0.8
            if delay >= 2:
                scores["COO"] += 1.0

        scores.pop("CEO", None)

        if not scores:
            return None

        best = max(scores, key=lambda k: scores[k])
        if scores[best] < 0.5:
            return None
        return best

    def _dump_parse_failure(
        self,
        phase: str,
        role_key: str,
        side: str,
        prompt: str,
        response: str,
    ) -> None:
        """Persist PROPOSE/CHALLENGE parse failures to a debug log.

        Each failure is appended as a JSON line to
        ``.omc/logs/deliberation_parse_failures.jsonl``. Captures the raw
        response so we can tell empty content from truncated JSON from
        markdown leaks without guessing. Silently noops on IO errors to
        avoid masking the real problem.
        """
        import json as _json
        import os as _os
        import time as _time

        stripped = (response or "").strip()
        entry = {
            "ts": _time.time(),
            "phase": phase,
            "role": role_key,
            "side": side,
            "response_len": len(response or ""),
            "response_stripped_len": len(stripped),
            "response_stripped": stripped[:2000],
            "prompt": prompt[:2500],
            "prompt_len": len(prompt),
        }
        path = ".omc/logs/deliberation_parse_failures.jsonl"
        try:
            _os.makedirs(_os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(_json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def _compress_history(
        self, side: str, raw_history: str, state_context: str, competitor_context: str,
    ) -> str:
        """1st-pass LLM compression: raw turn history → strategic situation summary.

        Runs with thinking=False (classification task). Reduces context by ~75%
        so downstream thinking tokens focus on strategic reasoning, not data parsing.
        """
        if not raw_history or len(raw_history) < 100:
            return raw_history

        prompt = (
            "Compress the raw turn history below into a strategic situation summary for C-suite decision-making.\n\n"
            f"Raw data:\n{raw_history}\n\n"
            f"Current state:\n{state_context}\n\n"
            f"Competitors:\n{competitor_context}\n\n"
            "Summarize in this format (≤200 chars total, in Korean):\n"
            "1. Share trend (direction for us and each competitor)\n"
            "2. Last strategy success/failure (what worked, what didn't)\n"
            "3. Biggest threat (which competitor action is most threatening)\n"
            "4. External environment changes (if any)\n"
            "5. Key decision point (one strategic question this turn must answer)\n\n"
            "Be concise. Output in Korean."
        )
        summary = self._llm.complete(
            system="Strategy consultant. Deliver only key insights, concisely.",
            user=prompt,
            temperature=0.3,
            max_tokens=1500,
            enable_thinking=False,
        )
        if summary and len(summary) > 20:
            logger.debug("History compressed: %d → %d chars (%.0f%%)",
                         len(raw_history), len(summary), len(summary)/len(raw_history)*100)
            return f"Strategic situation summary:\n{summary}"
        return raw_history

    def _generate_board_review(self, side: str, state: Any) -> str:
        """Generate board/shareholder review for Turn 2+. Returns formatted block or empty string."""
        if not self._turn_history:
            return ""

        last = self._turn_history[-1]
        if not isinstance(last, dict):
            return ""

        turn = last.get("turn", 1)
        positions = last.get("positions", {})

        cash_val = 0.0
        for e in state.get_entities_by_side(side):
            cash_val = getattr(e, "cash_reserves", getattr(e, "cash", 0.0))
            break

        detail = (last.get("actions_detail") or {}).get(side, {})
        our_action = detail.get("action_type", "unknown")

        repeated = False
        if len(self._turn_history) >= 2:
            prev = self._turn_history[-2]
            if isinstance(prev, dict):
                prev_action = (prev.get("actions_detail") or {}).get(side, {}).get("action_type", "")
                repeated = prev_action == our_action

        company_name = side
        for e in state.get_entities_by_side(side):
            company_name = e.name
            break
        industry = getattr(state, "industry", "unknown") if hasattr(state, "industry") else "unknown"

        if positions:
            our_pos = positions.get(side, {})
            our_pos_str = f"{our_pos.get('position', '?')}({our_pos.get('momentum', '\u2192')})"
            comp_lines = []
            for s, pos_data in positions.items():
                if s != side:
                    comp_name = s
                    for e in state.get_entities_by_side(s):
                        comp_name = e.name
                        break
                    comp_lines.append(
                        f"  {comp_name}: {pos_data.get('position', '?')}"
                        f"({pos_data.get('momentum', '\u2192')})"
                    )
            performance_summary = (
                f"Our company ({company_name}):\n"
                f"  Last action: {our_action}\n"
                f"  Position: {our_pos_str}\n"
                f"  Cash reserves: {cash_val:.0%}\n"
                f"  Same tactic repeated: {'Yes' if repeated else 'No'}\n\n"
                f"Competitors:\n" + "\n".join(comp_lines)
            )
        else:
            shares = last.get("shares", {})
            deltas = last.get("share_deltas", {})
            our_share = shares.get(side, 0)
            our_delta = deltas.get(side, 0)
            comp_lines = []
            for s in shares:
                if s != side:
                    comp_name = s
                    for e in state.get_entities_by_side(s):
                        comp_name = e.name
                        break
                    comp_lines.append(f"  {comp_name}: share={shares[s]:.1%} (\u0394={deltas.get(s, 0):+.1%})")
            performance_summary = (
                f"Our company ({company_name}):\n"
                f"  Last action: {our_action}\n"
                f"  Share: {our_share:.1%} (\u0394={our_delta:+.1%})\n"
                f"  Cash reserves: {cash_val:.0%}\n"
                f"  Same tactic repeated: {'Yes' if repeated else 'No'}\n\n"
                f"Competitors:\n" + "\n".join(comp_lines)
            )

        prompt = BOARD_REVIEW_PROMPT.format(
            company_name=company_name,
            industry=industry,
            turn=turn,
            performance_summary=performance_summary,
        )

        try:
            response = self._llm.complete(
                system=prompt,
                user="Issue board directives.",
                temperature=0.4,
                max_tokens=2048,
                enable_thinking=False,
            )
            data = parse_llm_json(response)
            if data and isinstance(data, dict):
                satisfaction = data.get("satisfaction", 3)
                concern = data.get("concern", "")
                mandate = data.get("mandate", "")
                rationale = data.get("rationale", "")
                stars = "★" * satisfaction + "☆" * (5 - satisfaction)
                block = (
                    f"[BOARD REVIEW — Turn {turn} performance]\n"
                    f"  Satisfaction: {stars} ({satisfaction}/5)\n"
                    f"  Concern: {concern}\n"
                    f"  Board mandate: {mandate}\n"
                    f"  Rationale: {rationale}\n"
                    f"  ⚠ C-suite proposals MUST address the board mandate above."
                )
                logger.info("Board review for %s: %d/5 — %s", side, satisfaction, concern)
                return block
        except Exception as e:
            logger.warning("Board review generation failed: %s", e)

        return ""

    def reassess_campaign(
        self,
        side: str,
        company_name: str,
        industry: str,
        current_campaign: str,
        seed_campaign: str,
        turns_on_current: int,
        trajectory_summary: str,
        recent_events: str,
        competitor_moves: str,
        available_campaigns: list[str],
    ) -> dict:
        """Decide whether to hold or pivot the strategic campaign.

        Called once per turn (turn ≥ 2) for our side only. Asks the CEO,
        with explicit pivot triggers, whether the current campaign should
        continue. Returns a dict with verdict / trigger / new_campaign_name
        / rationale / cost_acknowledged.

        Fail-safe: any parse or LLM failure returns ``verdict="hold"`` so
        a flaky reassessment never silently switches strategy.
        """
        fallback_hold: dict = {
            "verdict": "hold",
            "trigger": "none",
            "new_campaign_name": None,
            "rationale": "reassess unavailable — defaulting to hold",
            "cost_acknowledged": "",
        }
        if not available_campaigns:
            return fallback_hold

        prompt = STRATEGY_REASSESS_PROMPT.format(
            company_name=company_name,
            industry=industry,
            turns_on_current=turns_on_current,
            current_campaign=current_campaign or "(unknown)",
            seed_campaign=seed_campaign or "(unknown)",
            trajectory_summary=trajectory_summary or "(no trajectory yet)",
            recent_events=recent_events or "(none)",
            competitor_moves=competitor_moves or "(none)",
            available_campaigns="\n".join(f"  - {c}" for c in available_campaigns),
        )

        try:
            response = self._llm.complete(
                system=prompt,
                user="Reassess campaign for this turn.",
                temperature=0.3,
                max_tokens=1024,
                enable_thinking=False,
            )
            data = parse_llm_json(response)
        except Exception as e:
            logger.warning("Campaign reassessment LLM call failed for %s: %s", side, e)
            return fallback_hold

        if not isinstance(data, dict):
            return fallback_hold

        verdict = data.get("verdict", "hold")
        if verdict not in ("hold", "pivot"):
            verdict = "hold"

        trigger = data.get("trigger", "none")
        if trigger not in ("T1", "T2", "T3", "T4", "none"):
            trigger = "none"

        new_name = data.get("new_campaign_name")
        if verdict == "pivot":
            if not new_name or new_name not in available_campaigns:
                logger.info(
                    "Pivot rejected for %s — proposed '%s' not in available campaigns; holding",
                    side, new_name,
                )
                return {
                    **fallback_hold,
                    "rationale": f"제안된 캠페인 '{new_name}'이 유효 목록에 없음 → 유지",
                }
            if new_name == current_campaign:
                # Pivot to same campaign is a hold.
                verdict = "hold"
                new_name = None

        result = {
            "verdict": verdict,
            "trigger": trigger,
            "new_campaign_name": new_name if verdict == "pivot" else None,
            "rationale": data.get("rationale", ""),
            "cost_acknowledged": data.get("cost_acknowledged", ""),
        }
        logger.info(
            "Campaign reassessment for %s: %s (trigger=%s, new=%s)",
            side, result["verdict"], result["trigger"], result["new_campaign_name"],
        )
        return result

    def _build_context(self, side: str, state: Any, entities: list) -> dict:
        competitor_context = self._build_competitor_context(side, state)
        raw_history = self._build_history_context(side, state)

        persona = self._side_personas.get(side, {})
        persona_context = ""
        if persona.get("management_style") or persona.get("ceo_profile") or persona.get("aggression") is not None:
            parts = ["Company culture & leadership:"]
            if persona.get("management_style"):
                parts.append(f"  Management style: {persona['management_style']}")
            if persona.get("ceo_profile"):
                parts.append(f"  CEO leadership: {persona['ceo_profile']}")
            if persona.get("strategic_tendency"):
                parts.append(f"  Strategic tendency: {persona['strategic_tendency']}")
            agg = persona.get("aggression")
            rtol = persona.get("risk_tolerance")
            if agg is not None or rtol is not None:
                agg_v = agg if agg is not None else 0.5
                rtol_v = rtol if rtol is not None else 0.5
                if agg_v >= 0.7:
                    parts.append(f"  Aggression: HIGH ({agg_v:.0%}) — this CEO prefers bold, offensive moves. Status quo is unacceptable. Push for market-disrupting actions over incremental improvement.")
                elif agg_v <= 0.4:
                    parts.append(f"  Aggression: LOW ({agg_v:.0%}) — this CEO prefers measured, defensive moves. Protect existing position. Avoid unnecessary confrontation.")
                else:
                    parts.append(f"  Aggression: MODERATE ({agg_v:.0%})")
                if rtol_v >= 0.7:
                    parts.append(f"  Risk tolerance: HIGH ({rtol_v:.0%}) — willing to bet big. Large capex, aggressive M&A, first-mover gambles are on the table. CFO concerns can be overruled if upside is large.")
                elif rtol_v <= 0.4:
                    parts.append(f"  Risk tolerance: LOW ({rtol_v:.0%}) — prioritize downside protection. No bets without clear fallback. CFO has strong veto power.")
                else:
                    parts.append(f"  Risk tolerance: MODERATE ({rtol_v:.0%})")
            biases = persona.get("leadership_constraints", [])
            if biases:
                parts.append("  KNOWN LEADERSHIP BLIND SPOTS (these MUST influence decisions — leaders are not perfectly rational):")
                for b in biases:
                    parts.append(f"    • {b}")
                parts.append("  At least ONE proposal should reflect these biases — leaders sometimes make suboptimal choices driven by ego, politics, or organizational inertia.")
            parts.append("  Proposals MUST reflect this company's leadership style — do NOT default to generic conservative optimization.")
            persona_context = "\n".join(parts)

        strategic_dir = self._strategic_direction.get(side, "")
        if strategic_dir:
            persona_context = (
                f"Strategic direction (CURRENT campaign — may have pivoted from seed):\n"
                f"  \"{strategic_dir}\"\n"
                f"  This is the campaign your CEO committed to for this turn. A\n"
                f"  separate reassessment phase already decided whether to hold or\n"
                f"  pivot the campaign for this turn — your job here is to choose\n"
                f"  TACTICAL actions that execute this campaign. Do not propose a\n"
                f"  different campaign at the action level; if you believe the\n"
                f"  campaign itself is wrong, that signal belongs in your reasoning\n"
                f"  field so the next reassessment can use it. Choose actions that\n"
                f"  best execute the CURRENT campaign given cash/position/competitor\n"
                f"  state.\n\n"
                + persona_context
            )

        if entities and getattr(entities[0], "position", ""):
            our_pos = entities[0].position
            our_mom = entities[0].momentum or "\u2192"
            comp_positions = []
            for s in state.get_all_sides():
                if s != side:
                    for e in state.get_entities_by_side(s):
                        if getattr(e, "position", ""):
                            comp_positions.append(f"{e.name}={e.position}({e.momentum})")
            position_framing = _get_position_framing_ordinal(our_pos, our_mom, comp_positions)
        else:
            our_share = sum(e.market_share for e in entities)
            competitor_shares = []
            for s in state.get_all_sides():
                if s != side:
                    competitor_shares.append(sum(e.market_share for e in state.get_entities_by_side(s)))
            max_comp = max(competitor_shares) if competitor_shares else 0
            position_framing = _get_position_framing(our_share, max_comp)

        company_name = side
        industry = getattr(entities[0], "segment_key", "").split(":")[0] if entities else "unknown"

        if self._current_events:
            raw_history = (raw_history + "\n\n" + self._current_events).strip()
            self._current_events = ""

        state_context = self._build_state_context(side, state)
        history_context = self._compress_history(side, raw_history, state_context, competitor_context)

        board_review = self._generate_board_review(side, state)

        return {
            "company_name": company_name,
            "industry": industry,
            "state_context": state_context,
            "competitor_context": competitor_context,
            "history_context": history_context,
            "persona_context": persona_context,
            "position_framing": position_framing,
            "board_review": board_review,
        }

    def _get_dynamic_mandate(self, role_key: str, side: str, state: Any) -> str:
        """Inject actual state into mandate so the LLM judges, not thresholds."""
        base = self._csuite_roles[role_key]["mandate"]
        entities = state.get_entities_by_side(side)
        if not entities:
            return base
        e = entities[0]
        pos = getattr(e, "position", "")
        mom = getattr(e, "momentum", "")
        cash = e.cash_reserves

        if role_key == "CFO":
            return (
                f"Financial sustainability is the top priority. "
                f"Current cash reserves: {cash:.0%}. "
                f"Use your financial judgment: high cash burn is riskier "
                f"when reserves are low, more acceptable when reserves "
                f"are ample. Oppose plans without credible ROI path."
            )

        if role_key == "CMO":
            if pos:
                return (
                    f"You focus on market position and brand. "
                    f"Current position: {pos}({mom}). "
                    f"Use your marketing judgment \u2014 declining position "
                    f"demands growth investment, dominant position demands "
                    f"defensive lock-in. Oppose plans that ignore competitive "
                    f"dynamics."
                )
            return base

        if role_key == "CTO":
            return (
                f"You champion technology investment and innovation. "
                f"Current R&D: {e.r_and_d:.0%}. "
                f"Without sufficient R&D, competitiveness erodes within "
                f"2-3 years. Oppose cost cuts that weaken long-term "
                f"competitive position."
            )

        if role_key == "COO":
            if pos:
                return (
                    f"You focus on execution feasibility. "
                    f"Current position: {pos}({mom}), cash: {cash:.0%}. "
                    f"Flag risks of overextension. Even bold strategies fail "
                    f"when too many initiatives run simultaneously."
                )
            return base

        return base

    def _build_role_state_context(self, role_key: str, side: str, state: Any) -> str:
        visible = self._csuite_roles[role_key].get("visible_metrics")
        if visible is None:
            return self._build_state_context(side, state)

        lines = [f"Turn {state.turn}. Our business unit:"]
        for e in state.get_entities_by_side(side):
            parts = [f"  - {e.name}:"]
            if e.position:
                parts.append(f"position={e.position}({e.momentum})")
            elif "market_share" in visible:
                parts.append(f"share={e.market_share:.1%}")
            if "cash_reserves" in visible:
                parts.append(f"cash={e.cash_reserves:.1%}")
            if "r_and_d" in visible:
                parts.append(f"R&D={e.r_and_d:.1%}")
            if "competitive_power" in visible:
                parts.append(f"power={e.competitive_power:.0f}")
            if "brand_loyalty" in visible:
                parts.append(f"loyalty={e.brand_loyalty:.0f}")
            if not e.position and "market_share" not in visible:
                parts.append(f"share={e.market_share:.1%}")
            lines.append(" ".join(parts))
        return "\n".join(lines)

    def _build_state_context(self, side: str, state: Any) -> str:
        lines = [f"Turn {state.turn}. Our business unit:"]
        for e in state.get_entities_by_side(side):
            if e.position:
                lines.append(
                    f"  - {e.name}: position={e.position}({e.momentum}), "
                    f"cash={e.cash_reserves:.1%}, R&D={e.r_and_d:.1%}, "
                    f"power={e.competitive_power:.0f}, loyalty={e.brand_loyalty:.0f}"
                )
            else:
                lines.append(
                    f"  - {e.name}: share={e.market_share:.1%}, "
                    f"cash={e.cash_reserves:.1%}, R&D={e.r_and_d:.1%}, "
                    f"power={e.competitive_power:.0f}, loyalty={e.brand_loyalty:.0f}"
                )
        return "\n".join(lines)

    def _build_competitor_context(self, side: str, state: Any) -> str:
        lines = []
        last_turn = self._turn_history[-1] if self._turn_history else None
        for s in state.get_all_sides():
            if s != side:
                for e in state.get_entities_by_side(s):
                    if e.position:
                        line = f"  - {e.name} ({s}): {e.position}({e.momentum}), power={e.competitive_power:.0f}"
                    else:
                        line = f"  - {e.name} ({s}): share={e.market_share:.1%}, power={e.competitive_power:.0f}"
                    if last_turn and isinstance(last_turn, dict):
                        detail = (last_turn.get("actions_detail") or {}).get(s) or {}
                        atype = detail.get("action_type", "")
                        if atype:
                            pos_data = (last_turn.get("positions") or {}).get(s)
                            if pos_data:
                                line += (
                                    f" | last action: {atype}"
                                    f" \u2192 {pos_data.get('position', '?')}"
                                    f"({pos_data.get('momentum', '\u2192')})"
                                )
                            else:
                                delta = (last_turn.get("share_deltas") or {}).get(s, 0.0)
                                line += f" | last action: {atype} \u2192 {delta:+.1%}"
                    lines.append(line)
        return "\n".join(lines) if lines else "No competitor info."

    def _build_history_context(self, side: str, state: Any = None) -> str:
        """Render prior turns with per-player deltas so C-suite can see what
        each action actually cost or gained them. Absolute-share snapshots
        alone hide the causal structure ("did my move land? which competitor
        action ate it?"), which is exactly the information this role needs
        to decide whether to stick with the seed bias or pivot.
        """
        if not self._turn_history:
            if self._seed_momentum:
                return f"Market background:\n{self._seed_momentum}"
            return ""

        def _fmt_pct(v: float) -> str:
            return f"{v:+.1%}"

        side_names: dict[str, str] = {}
        if state is not None:
            for s in state.get_all_sides():
                for e in state.get_entities_by_side(s):
                    side_names[s] = e.name
                    break

        has_positions = any(
            isinstance(o, dict) and o.get("positions")
            for o in self._turn_history[-3:]
        )
        header = "Prior turns (action \u2192 position):" if has_positions else "Prior turns (action \u2192 share change):"
        lines = [header]
        for outcome in self._turn_history[-3:]:
            if isinstance(outcome, dict):
                turn = outcome.get("turn", "?")
                actions = outcome.get("actions", {}) or {}
                detail = outcome.get("actions_detail", {}) or {}
                positions = outcome.get("positions", {}) or {}
                hist_cash = outcome.get("cash", {}) or {}
                deltas = outcome.get("share_deltas", {}) or {}
                shares = outcome.get("shares", {}) or {}
                lines.append(f"  Turn {turn}:")
                order = [side] + [sid for sid in actions if sid != side]
                for sid in order:
                    if sid not in actions:
                        continue
                    label = "us" if sid == side else side_names.get(sid, sid)
                    d = detail.get(sid) or {}
                    atype = d.get("action_type")
                    intensity = d.get("intensity")
                    pos_data = positions.get(sid)
                    cash_str = f", cash={hist_cash[sid]:.0%}" if sid in hist_cash else ""
                    if pos_data and atype and intensity is not None:
                        lines.append(
                            f"    {label}: {atype}(intensity={float(intensity):.1f})"
                            f" \u2192 {pos_data.get('position', '?')}"
                            f"({pos_data.get('momentum', '\u2192')})"
                            f"{cash_str}"
                        )
                    elif pos_data:
                        lines.append(
                            f"    {label}: {actions.get(sid, '?')}"
                            f" \u2192 {pos_data.get('position', '?')}"
                            f"({pos_data.get('momentum', '\u2192')})"
                            f"{cash_str}"
                        )
                    elif atype and intensity is not None:
                        delta = deltas.get(sid, 0.0)
                        share_now = shares.get(sid, 0.0)
                        lines.append(
                            f"    {label}: {atype}(intensity={float(intensity):.1f}) "
                            f"\u2192 {_fmt_pct(delta)} (cumul {share_now:.1%})"
                            f"{cash_str}"
                        )
                    else:
                        delta = deltas.get(sid, 0.0)
                        share_now = shares.get(sid, 0.0)
                        lines.append(
                            f"    {label}: {actions.get(sid, '?')} "
                            f"\u2192 {_fmt_pct(delta)} (cumul {share_now:.1%})"
                            f"{cash_str}"
                        )
                events = outcome.get("events") or []
                if events:
                    for ev in events:
                        lines.append(f"    [event] {ev.get('label_ko', '')}: {ev.get('description', '')}")
                if outcome.get("summary"):
                    lines.append(f"    Market eval: {outcome['summary']}")
            else:
                lines.append(f"  Turn {outcome.turn}:")
                for a in outcome.actions_taken:
                    at = a.action_type.value if hasattr(a.action_type, "value") else str(a.action_type)
                    entry = f"{at} (intensity={a.intensity:.1f})"
                    if a.commander_id.startswith(side) or a.entity_id.startswith(f"bu_{side}"):
                        lines.append(f"    us: {entry}")
                    else:
                        lines.append(f"    competitor: {entry}")
        return "\n".join(lines)

    def _parse_synthesis(
        self, response: str, side: str, state: Any,
    ) -> list[StrategicAction]:
        data = parse_llm_json(response)
        if not data:
            logger.warning("Phase 3 파싱 실패: %s — response len=%d, first 300: %s",
                           side, len(response), response[:300])
            return self._fallback(side, state)

        actions_data = data.get("actions", [data] if "action_type" in data else [])
        actions = []
        for item in actions_data:
            try:
                actions.append(StrategicAction(
                    action_id=str(uuid.uuid4())[:8],
                    turn=state.turn,
                    commander_id=f"{side}_csuite",
                    entity_id=item.get("entity_id", ""),
                    action_type=_normalize_category(item.get("action_type", "HOLD")),
                    strategy_description=item.get("strategy_description", ""),
                    intensity=max(0.0, min(1.0, float(item.get("intensity", 0.5)))),
                    reasoning=item.get("reasoning", "C-suite 토론 합의"),
                ))
            except (KeyError, ValueError) as e:
                logger.warning("잘못된 action: %s", e)

        seen = set()
        unique = []
        for a in actions:
            key = (a.action_type, a.strategy_description)
            if key not in seen:
                seen.add(key)
                unique.append(a)
        actions = unique

        return actions if actions else self._fallback(side, state)

    def _fallback(self, side: str, state: Any) -> list[StrategicAction]:
        entities = state.get_entities_by_side(side)
        actions = []
        for e in entities:
            actions.append(StrategicAction(
                action_id=str(uuid.uuid4())[:8],
                turn=state.turn,
                commander_id=f"{side}_fallback",
                entity_id=e.id,
                action_type="HOLD",
                strategy_description="현상 유지",
                intensity=0.5,
                reasoning="[fallback] 토론 파싱 실패",
            ))
        return actions
