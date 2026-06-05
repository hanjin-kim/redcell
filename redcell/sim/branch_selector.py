"""Branch selector — Phase 1 of the event-branching tree migration.

Decides, for a turn, whether to branch the simulation tree on the turn's single
most pivotal EXTERNAL EVENT, or keep the turn linear.

Only events are branched: an event has a clean binary occurrence space (fires /
does not fire), so the two children form a matched counterfactual pair.
Competitor decisions are NOT branched — they are multi-dimensional with no
well-defined counterfactual; their variation is observed across the M Monte
Carlo trials instead.

One LLM step: the selector picks the pivotal event from GROUNDED candidates
(eligible, non-exhausted deck events), or NONE. It selects by id — it cannot
invent (validated across probe v1-v4).
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

KIND_EVENT = "외부 이벤트"


@dataclass
class BranchCandidate:
    """One binary event fork the turn could branch on."""

    id: str          # "evt:<event_id>"
    kind: str        # KIND_EVENT
    label: str
    variant_a: str   # event fires
    variant_b: str   # event does not fire


@dataclass
class BranchPoint:
    """The selected branch for a turn (None means the turn stays linear)."""

    turn: int
    candidate: BranchCandidate
    reasoning: str


def _build_event_candidates(
    deck: list[dict], turn: int, fired_counts: dict[str, int],
) -> list[BranchCandidate]:
    """Deterministic — deck events eligible this turn and not yet exhausted."""
    candidates = []
    for ev in deck:
        eligible = ev.get("eligible_turns")
        if eligible and turn not in eligible:
            continue
        if fired_counts.get(ev["id"], 0) >= ev.get("max_occurrences", 1):
            continue
        label = ev.get("label_ko") or ev.get("name") or ev["id"]
        candidates.append(BranchCandidate(
            id=f"evt:{ev['id']}", kind=KIND_EVENT, label=label,
            variant_a=f"{label} — 발효", variant_b=f"{label} — 무산",
        ))
    return candidates


def _run_selector(
    turn: int, candidates: list[BranchCandidate], entering_block: str,
    prior_block: str, industry: str, our_company: str, llm,
) -> dict:
    """LLM step — pick the pivotal event (by id) from grounded candidates."""
    cand_block = "\n".join(
        f"  [{c.id}] {c.label}\n      A: {c.variant_a}\n      B: {c.variant_b}"
        for c in candidates
    )
    cand_ids = [c.id for c in candidates] + ["NONE"]
    schema = {
        "type": "object",
        "properties": {
            "chosen_id": {"type": "string", "enum": cand_ids},
            # DashScope's `strict: true` is *not* actually strict — required
            # fields can be silently omitted. The string enum ["yes","no"]
            # itself isn't load-bearing (boolean also works), but pairing it
            # with an explicit field list in the prompt below produces 100%
            # field-present rate across thinking/non-thinking variants
            # (verified in tmp_review/probe_branch_schema_repro.py).
            "materially_divergent": {"type": "string", "enum": ["yes", "no"]},
            "reasoning": {"type": "string", "maxLength": 300},
        },
        "required": ["chosen_id", "materially_divergent", "reasoning"],
        "additionalProperties": False,
    }
    system = f"""당신은 {industry} 경쟁 워게임의 CONTROL TEAM입니다.
우리 측은 {our_company}입니다. Turn {turn}의 이진 분기점을 정합니다.

아래 이벤트 후보에서 — 우리가 통제 못 하는 — 가장 결정적인 단일 외부 이벤트를
고르십시오. 목록에 없는 것을 지어내지 마십시오. 후보가 모두 사소하면
chosen_id="NONE" (이 턴은 분기 없이 선형).

이벤트 후보 (각 후보는 발효/무산 이진):
{cand_block}
  [NONE] 어느 이벤트도 경쟁 결과를 의미 있게 가르지 않음 — 분기 없음

Turn {turn} 진입 포지션:
{entering_block}

이미 분기에 쓴 이벤트 (중복 회피):
{prior_block}

JSON 출력 — 다음 세 필드 모두 반드시 포함:
- chosen_id: 위 id 중 하나 (NONE 포함)
- materially_divergent: "yes" 또는 "no" — 선택 이벤트의 발효/무산이 결과적으로 다른 outcome을 만드는가?
- reasoning: 한국어로 짧게 (한 문장)"""
    response = llm.complete(
        system=system, user="분기점을 JSON으로 고르십시오.",
        temperature=0.3, max_tokens=1100,
        response_format={"type": "json_schema",
                         "json_schema": {"name": "branch", "strict": True,
                                         "schema": schema}},
    )
    return json.loads(response) if response else {"chosen_id": "NONE"}


def decide_branch(
    turn: int,
    entering_positions: dict[str, dict],
    companies: dict[str, str],
    our_side: str,
    industry: str,
    deck: list[dict],
    fired_counts: dict[str, int],
    prior_branch_ids: list[str],
    llm,
) -> BranchPoint | None:
    """Decide whether Turn `turn` branches on a pivotal event.

    Returns a BranchPoint, or None if the turn stays linear (no eligible event,
    no materially divergent event, or no LLM available).
    """
    if llm is None:
        return None

    candidates = _build_event_candidates(deck, turn, fired_counts)
    if not candidates:
        return None

    entering_block = "\n".join(
        f"  {companies[s]}: {p.get('position', '')} {p.get('momentum', '')}"
        for s, p in entering_positions.items()
    )
    prior_block = "\n".join(f"  {bid}" for bid in prior_branch_ids) or "  (없음)"

    try:
        result = _run_selector(
            turn, candidates, entering_block, prior_block,
            industry, companies.get(our_side, our_side), llm,
        )
    except Exception as e:
        logger.error("Branch selector failed (turn %s): %s", turn, e)
        return None

    chosen_id = result.get("chosen_id", "NONE")
    if chosen_id == "NONE" or result.get("materially_divergent") != "yes":
        return None
    chosen = next((c for c in candidates if c.id == chosen_id), None)
    if chosen is None:
        return None
    return BranchPoint(turn=turn, candidate=chosen, reasoning=result.get("reasoning", ""))
