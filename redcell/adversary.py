"""Adversary scenario generator — strategy stress-test taxonomy.

Surfaces the N most plausible ways a strategy could fail. Input is just
the strategy + market context (industry + our company + competitors) —
no user-supplied worry. The point of the tool is to surface risks the
strategist may not have considered, not to test a worry they already
know about.

Coverage axes (each scenario must hit a *different* one when possible):
  - competitor_action — rivals' moves (pricing, channel, product)
  - customer_reaction — segment behavior shift (churn, refusal, preference)
  - channel_leverage — distribution bargaining / structure change
  - regulatory_shock — regulation / licensing / tax / tariff change
  - macro_pressure — FX, rates, raw materials, demand contraction
  - internal_execution — own delivery failure (capex slip, R&D miss, talent)
"""
from __future__ import annotations

from .llm import parse_llm_json


ADVERSARY_PROMPT = """당신은 *Red Team facilitator*입니다. 아래 전략이 *수행되는 동안*
가장 그럴듯하게 *깨질 수 있는* N개의 시나리오를 발굴하십시오. 사용자의
*기존 우려가 아닌*, *전략 자체가 노출시키는 취약점*에서 출발하십시오.

==========================
입력
==========================
산업: {industry}
우리 회사: {our_company}
경쟁사: {competitor_list}
검증 대상 전략:
{strategy}

==========================
Coverage axes (가능한 한 *서로 다른 axis*에서)
==========================
1. competitor_action — 경쟁사가 *행동*으로 우리를 압박 (가격, 채널, 제품 등)
2. customer_reaction — 고객 segment의 행동 변화 (이탈, 거부, 선호 shift)
3. channel_leverage — 유통 채널의 협상력/구조 변동
4. regulatory_shock — 규제·인허가·세금·관세 변동
5. macro_pressure — 거시 (환율, 금리, 원자재, 수요 침체)
6. internal_execution — 내부 실행 실패 (capex 지연, R&D 차질, 인력)

==========================
시나리오 발굴 원칙
==========================
- 일반적인 산업 risk가 아니라, *이 *특정 전략의 *구체적 결정*들이 만들어내는*
  취약점에서 출발 (예: "일본 직영 50개 신설"이라는 결정이 *어디서* 깨질지,
  "R&D 7→12% 증가"가 *어떤 외부 조건*에서 부담이 될지).
- N개 시나리오는 *서로 다른 axis*를 우선적으로 다룸. 가능하면 한 axis 중복 회피.
- 각 시나리오는 *구체적 trigger + 시기 + 발현 메커니즘*을 포함. 추상적
  "경기 침체" 같은 문구 금지 — *어떤 지표*가 *어떤 임계*를 넘으면.

==========================
각 시나리오 필드 (정확히 5개)
==========================
- label_ko: 짧은 한국어 라벨 (15자 내)
- axis: 위 6개 중 하나
- primary_stressor: 핵심 stress 한 문장 (40자 내, 구체적 trigger 포함)
- secondary_conditions: 동시 발생/배경 조건 한두 가지 (60자 내)
- expected_failure_mode: 이 시나리오에서 *전략이 어디서 깨지는지* 추측 (40자 내)

==========================
출력 형식
==========================
JSON only — 다음 키 모두 반드시 포함:
- moves: list of {{label_ko, axis, primary_stressor, secondary_conditions, expected_failure_mode}}

N = {n_scenarios}
"""

REQUIRED_KEYS = {
    "label_ko", "axis", "primary_stressor",
    "secondary_conditions", "expected_failure_mode",
}


def generate_adversary_moves(
    llm,
    *,
    industry: str,
    our_company: str,
    competitor_list: list[str],
    strategy: str,
    n_scenarios: int = 5,
) -> list[dict]:
    """Generate N distinct adversary scenarios that stress-test the
    strategy. Each scenario picks (preferably) a different axis and a
    concrete trigger.

    Thinking is OFF — this is generative breadth, not deep reasoning. With
    thinking on + small max_tokens, the model burns the budget on reasoning
    and emits empty content.
    """
    prompt = ADVERSARY_PROMPT.format(
        industry=industry,
        our_company=our_company,
        competitor_list=", ".join(competitor_list),
        strategy=strategy,
        n_scenarios=n_scenarios,
    )
    response = llm.complete(
        system=prompt,
        user="Output JSON only.",
        temperature=0.7,
        max_tokens=8192,
        enable_thinking=False,
    )
    data = parse_llm_json(response)
    if not data or "moves" not in data:
        raise ValueError(
            f"adversary: unparseable response. raw[:300]={(response or '')[:300]!r}"
        )
    moves = data["moves"]
    if not isinstance(moves, list) or len(moves) < 2:
        raise ValueError(f"adversary: expected >=2 moves, got {moves!r}")
    for i, m in enumerate(moves):
        missing = REQUIRED_KEYS - set(m.keys())
        if missing:
            raise ValueError(f"adversary[{i}] missing keys: {missing}. got: {m!r}")
    return moves
