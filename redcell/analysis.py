"""Per-scenario analysis layer — Red Team v2.1.

After each adversary scenario's simulation completes, run an LLM pass to:
  1. Generate an *axis-aligned* summary (fixes narrative-axis drift)
  2. Identify the *primary cash drivers* per turn (causal hygiene)
  3. Produce *observation triggers* for the diligence question (what to
     watch for that would strengthen / weaken the hypothesis)
  4. Produce 2-3 *specific* diligence questions (not generic placeholders)

Per Codex (2026-05-27 brutal blind 3.7/5 review):
- Weakest #1: narrative-axis mismatch
- Weakest #2: numeric change causal explanation missing
- Weakest #3: "Expected vs Observed" verification trigger absent

This module supplies the synthesis layer that closes those gaps.
"""
import json
from .llm import parse_llm_json


ANALYSIS_PROMPT = """당신은 *Red Team facilitator*입니다. 한 시나리오의 시뮬레이션 trace를
*정직히* 재해석해주십시오.

==========================
🔴 GROUNDING DISCIPLINE — *반드시 준수*
==========================

1. **Trace-bound facts only**: 아래 trace_block에 *literal로 명시된 events
   /actions/numbers*만 인용 가능. **명시되지 않은 event를 발화했다고
   언급하면 안 됨**. 예: trace의 T5 events가 ["A"]면, T5에서 B가 발화했다고
   주장 금지.

2. **Axis 효과가 안 보이면 솔직히 그렇게 말함**: 이 시나리오의 axis가
   *trace에 분명한 신호가 없으면*, "*이 axis는 trace에서 명확히
   나타나지 않음, 다른 events가 primary driver*"라고 *정직히* 명시.
   axis hypothesis를 *지지하기 위해 trace를 왜곡하지 말 것*.

3. **Cash arithmetic rules (엔진 결정성)**:
   - 한 턴의 *총 action cash delta*는 **`[-12.0pp, +5.0pp]`로 clamp**됨.
     stack 합계가 cap을 넘으면 column엔 cap 값 표시.
   - Position revenue per turn: dominant=+12pp, strong=+8pp, contested=+5pp,
     weak=+3pp, marginal=+1pp.
   - Cash identity: starting + action_cost + events_delta + position_revenue = ending.
   - **Driver 합계 ≠ 실제 cash 변화면 cap 발효 또는 산술 오류** — 양심적으로
     인정해야 함.

==========================
Scenario context
==========================
Adversary axis: {axis}
Primary stressor: {primary_stressor}
Secondary conditions: {secondary_conditions}
Expected failure mode (hypothesis): {expected_failure_mode}

==========================
시뮬레이션 trace (5 turns) — *literal facts*
==========================
{trace_block}

==========================
당신 job — 4가지 출력
==========================

1. **axis_aligned_summary** (한국어 2-3문장):
   *{axis}* axis의 stressor가 trace에 *어떻게 실제로 나타났는지*.
   - trace의 *명시된* events만 인용
   - axis 신호가 *trace에 분명히 안 보이면* "*이 axis는 명확히
     materialize하지 않음, [실제 driver]가 primary*"라고 솔직히 명시
   - 다른 events가 cash 변동의 primary driver였다면 *그것을 인정*

2. **cash_driver_per_turn** (각 turn 1줄):
   각 turn의 cash 변화를 *trace 숫자에 부합*하게 분해.
   - 형식: "T2: cash 46.0→32.0 (-14pp). action stack [-12pp cap 발효]
     + events [-3pp] + position [+1pp] = -14pp ✓"
   - 합계가 안 맞으면 *cap 발효* 또는 *산술 미정 (LLM 한계)* 명시
   - trace에 없는 event 인용 금지

3. **observation_triggers** (3-5개):
   이 axis가 *실제로 materialize 한다면* 무엇이 관찰되는가 — *forward-looking*.
   - `axis_aligned_summary`에서 "*axis materialize 안 함*"이라고 결론 냈다면,
     trigger도 *"if it WERE to materialize"* framing이어야 함. 현재 trace에서
     *"strong_support 신호 보임"*이라고 단정 금지 — 그건 summary와 모순.
   - 가능 framing:
     - "If axis materializes: [관찰 가능 신호 X]" (predictive)
     - "Trace에 [신호 Y]가 보였으나 *axis-attributable인지 ambiguous*" (정직)
   - axis가 trace에 명확히 나타난 경우만 "strong_support: 현재 X 관찰됨" OK.

4. **diligence_questions** (3개):
   *수치/임계/방향 명시*한 구체 질문. Generic 금지.
   axis가 materialize 안 했다면 *조건부 framing*: "*만약 [axis stressor]가
   진짜 발생한다면*, [측정 가능 X]는 어떻게 변하나?"

==========================
출력 형식
==========================
JSON only. 5개 key 모두 포함:
{{
  "axis_aligned_summary": "...",
  "cash_driver_per_turn": ["T1: cash X→Y (Zpp). actions [...] + events [...] + position [...] = Zpp", ...],
  "observation_triggers": [
    {{"signal_type": "strong_support", "indicator": "..."}},
    {{"signal_type": "weakening_signal", "indicator": "..."}},
    ...
  ],
  "diligence_questions": ["Q1 ...", "Q2 ...", "Q3 ..."]
}}
"""


def _format_trace_block(trace: list) -> str:
    """Format trace with explicit starting+ending cash per turn so the LLM
    can reconcile arithmetic. cash_attribution.starting is what's missing
    from the simpler 'cash' field that only shows ending."""
    lines = []
    for n in trace:
        attr = n.get("cash_attribution", {}).get("side_a", {})
        starting = (attr.get("starting", 0) * 100) if attr else 0
        ending = (attr.get("ending", n.get("cash", 0)) * 100) if attr else (n.get("cash", 0) * 100)
        ev = attr.get("events_delta", 0) * 100 if attr else 0
        ac = attr.get("action_cost", 0) * 100 if attr else 0
        pr = attr.get("position_revenue", 0) * 100 if attr else 0
        net = ev + ac + pr
        events_str = ", ".join(n.get("events", [])) or "—"
        lines.append(
            f"T{n['turn']}: "
            f"action=`{n.get('audit_action_type','')}` @{n.get('audit_intensity',0):.2f} | "
            f"position=`{n.get('position','?')}` | "
            f"cash {starting:.1f}%→{ending:.1f}% ({(ending - starting):+.1f}pp); "
            f"components: events Δ {ev:+.1f}pp, actions {ac:+.1f}pp, "
            f"position rev {pr:+.1f}pp, sum {net:+.1f}pp | "
            f"events_fired={events_str}"
        )
    return "\n".join(lines)


def analyze_scenario(llm, *, scenario: dict) -> dict:
    """Run per-scenario LLM analysis. Returns 4-field dict.

    `scenario` must have:
      - move: {axis, primary_stressor, secondary_conditions, expected_failure_mode}
      - trace: list of turn dicts
    """
    move = scenario["move"]
    trace = scenario.get("trace", [])
    if not trace:
        return {
            "axis_aligned_summary": "(no trace — scenario empty)",
            "cash_driver_per_turn": [],
            "observation_triggers": [],
            "diligence_questions": [],
        }

    prompt = ANALYSIS_PROMPT.format(
        axis=move["axis"],
        primary_stressor=move["primary_stressor"],
        secondary_conditions=move["secondary_conditions"],
        expected_failure_mode=move["expected_failure_mode"],
        trace_block=_format_trace_block(trace),
    )
    response = llm.complete(
        system=prompt,
        user="Output JSON only.",
        temperature=0.5,
        max_tokens=8192,
        enable_thinking=False,
    )
    data = parse_llm_json(response)
    if not data:
        raise ValueError(
            f"scenario_analysis: unparseable response. "
            f"raw[:300]={(response or '')[:300]!r}"
        )
    required = {"axis_aligned_summary", "cash_driver_per_turn",
                "observation_triggers", "diligence_questions"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(
            f"scenario_analysis missing keys: {missing}. got: {list(data.keys())}"
        )
    return data
