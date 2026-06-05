"""Adversary moves generator — scenario taxonomy.

Converts a single worried_risk into N distinct adversary moves across
multiple axes (competitor action, customer reaction, channel leverage,
regulatory shock, macro pressure, internal execution).
"""
from __future__ import annotations

from .llm import parse_llm_json


ADVERSARY_PROMPT = """당신은 *Red Team facilitator*입니다. 사용자가 걱정하는 단일
risk 한 줄을 *서로 다른 axis*의 N개 adversary moves로 변환하십시오.

==========================
사용자 입력
==========================
산업: {industry}
우리 회사: {our_company}
경쟁사: {competitor_list}
우리 전략: {strategy}

사용자가 걱정하는 risk (한 줄):
{worried_risk}

==========================
Coverage axes (서로 다른 axis 우선)
==========================
1. competitor_action — 경쟁사가 *행동*으로 우리를 압박 (가격, 채널, 제품 등)
2. customer_reaction — 고객 segment의 행동 변화 (이탈, 거부, 선호 shift)
3. channel_leverage — 유통 채널의 협상력/구조 변동
4. regulatory_shock — 규제·인허가·세금·관세 변동
5. macro_pressure — 거시 (환율, 금리, 원자재, 수요 침체)
6. internal_execution — 내부 실행 실패 (capex 지연, R&D 차질, 인력)

==========================
출력 요구사항
==========================
- 사용자 worry는 *첫 scenario*에 포함하되 *명확하게 표현* (사용자가 표현한 그대로)
- 나머지 (N-1)개는 *서로 다른 axis*에서 (한 axis 중복 가능하나 *피하기*)
- 각 scenario는 다음 5개 필드:
  - label_ko: 짧은 한국어 라벨 (15자 내)
  - axis: 위 6개 중 하나
  - primary_stressor: 핵심 stress 한 문장 (30자 내)
  - secondary_conditions: 동시 발생/배경 조건 한두 가지 (50자 내)
  - expected_failure_mode: 이 시나리오에서 *우리 전략이* 어디서 *깨질 수 있는지* 추측 (40자 내)

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
    worried_risk: str,
    n_scenarios: int = 5,
) -> list[dict]:
    """Generate N distinct adversary moves. First carries the user's worry;
    the rest cover other axes the user may not have considered.

    Thinking is OFF — this is generative breadth, not deep reasoning; with
    thinking on + small max_tokens, the model burns the budget on reasoning
    and emits empty content.
    """
    prompt = ADVERSARY_PROMPT.format(
        industry=industry,
        our_company=our_company,
        competitor_list=", ".join(competitor_list),
        strategy=strategy,
        worried_risk=worried_risk,
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
