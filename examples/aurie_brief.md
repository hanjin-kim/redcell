# Red Team Brief

이 전략을 주어진 환경에서 수행할 때, 우리 측과 경쟁사가 어떻게 반응하고 어떤 risk가 emerging 되는지 트레이싱한 결과입니다.

**산업:** `kbeauty_premium_skincare`

**우리 회사:** AURIE  ·  **경쟁사:** Shiseido, Amore Pacific

**검증 대상 전략:**
> 프리미엄-아시아 듀얼 트랙: 고가 anti-aging SKU 집중 + 일본 직영 채널 50개
신설 + 동남아 멀티브랜드 확장 + 중국 의존도 35→20% 축소.
R&D 매출 비중 7%→12% 증가, 면세 30%→15% 축소, D2C 자체몰 25% 비중 확보.
24개월 KPI: EBIT 마진 12→15%, 일본 매출 비중 8→18%, 중국 매출 35→20%.

**주어진 환경:**
> Shiseido가 2025 Q4에 발표한 한국 mass-premium 30% 가격 인하를 2026 Q1부터
실제 집행 — Olive Young / Lotte 면세 / 백화점 동시 적용, AURIE 핵심
anti-aging SKU 가격대(₩80-150K)에 직접 침투. 동남아 (베트남/태국) 시장에서도
Shiseido 채널 확장과 동시 진행.

## 1. 시뮬레이션 결과 요약

각 측의 시작 → 종료 변동:

| 측 | 초기 cash | T-final cash | Δ cash | T-final position |
|---|---|---|---|---|
| **AURIE** | 55.0% | 19.8% | -35.2pp | `weak` |
| Shiseido | 75.0% | 84.3% | +9.3pp | `dominant` |
| Amore Pacific | 62.0% | 64.0% | +2.0pp | `strong` |

## 2. 턴별 전개

### Turn 1

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Clinical Data Push`@0.80 | `contested` ↘ | 48.0% |
| Shiseido | `Aggressive Price Cut`@0.90 | `dominant` ↑ | 78.5% |
| Amore Pacific | `Clinical Data Push`@0.75 | `strong` → | 64.8% |

**Adjudicator narrative:** 시세이도는 풍부한 현금 자원을 활용하여 가격 인하 공세를 펼치며 중규모 브랜드인 AURIE의 수익성을 압박하고 시장 점유율을 잠식했습니다. AURIE는 규제 강화 흐름에 맞춰 임상 데이터 투자를 단행했으나, 이로 인한 현금 소모가 시세이도의 가격 공세로 인한 수익 감소분을 상쇄하지 못해 생존 리스크가 고조되었습니다. 아모레퍼시픽은 기존 브랜드 포트폴리오와 내부 시너지를 통해 안정적 입지를 유지했으나, 해외 시장 성장 정체와 규제 비용 증가로 인해 뚜렷한 성장 모멘텀을 확보하지는 못했습니다.

**경쟁 상호작용 분석:** 시세이도의 공격적 가격 공세는 AURIE의 현금 소모를 가속화하여 R&D 투자 지속성을 위협하는 동시에, 아모레퍼시픽의 시너지 전략도 규제 비용 상승으로 인해 그 효과가 상쇄되는 구조를 형성했습니다. 이로 인해 AURIE는 규제 준수 모션을 취하면서도 시장 점유율 방어에 어려움을 겪고, 시세이도는 현금력을 앞세워 시장 구조를 재편하고 있습니다.

### Turn 2

**Events fired:** 중국 수입 규제 강화 및 자국 브랜드 우대, MZ 세대 미니멀리즘 트렌드 전환

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Clinical Data Push`@0.80 | `contested` → | 41.4% |
| Shiseido | `Bold R&D Bet`@0.80 | `dominant` ↑ | 74.5% |
| Amore Pacific | `Aggressive Price Cut`@0.80 | `strong` ↘ | 63.0% |

**Adjudicator narrative:** T1에서 Shiseido가 가격 인하를 감행한 이후, T2에는 막대한 자본력을 바탕으로 규제 비용을 흡수하며 프리미엄 전략을 유지하는 데 성공했습니다. Amore Pacific은 T1의 가격 인하 전략을 이어받아 단기 점유율 방어에 나섰으나, 이로 인한 마진 압박과 브랜드 가치 하락 우려가 누적되어 상승세를 잃었습니다. AURIE는 T1 임상 데이터 추진의 효과가 규제 강화로 인해 진입 장벽으로 작용하기 시작했으나, T1부터 누적된 현금 고갈로 인해 시장 점유율 추락을 막지 못해 중립적 흐름을 유지하고 있습니다.

**경쟁 상호작용 분석:** Shiseido의 막대한 현금 보유력은 Amore Pacific의 가격 인하 공세를 무력화시키며 시장 주도권을 확고히 했습니다. 반면 AURIE는 규제 강화라는 외부 환경 변화로 인해 기술적 진입 장벽은 높았으나, 누적된 현금 부족으로 이를 성장 동력으로 전환하지 못해 정체 상태에 머물렀습니다.

### Turn 3

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Aggressive Price Cut`@0.80 | `weak` ↓ | 36.8% |
| Shiseido | `Mass-Premium Infiltration`@0.80 | `dominant` ↑ | 74.5% |
| Amore Pacific | `Clinical Data Push`@0.75 | `strong` → | 64.2% |

**Adjudicator narrative:** AURIE는 T1과 T2 동안 임상 데이터에 집중하며 자산을 소진해 왔고, T3에 들어선 가격 공세로 인해 그 누적된 현금 부족이 치명적인 약점으로 드러났습니다. Shiseido는 T2의 R&D 투자 성과를 바탕으로 T3에 가격 경쟁력을 결합하여, AURIE의 자생적 성장 동력을 완전히 차단하는 데 성공했습니다. Amore Pacific은 T2의 가격 인하로 일시적인 마진 압박을 겪었으나, T3에 임상 데이터의 신뢰도를 앞세워 시장에서의 안정적 위치를 재확인했습니다.

**경쟁 상호작용 분석:** Shiseido의 압도적인 현금 흐름을 바탕으로 한 T3의 가격 공세는 AURIE의 제한된 자원을 고갈시켜 시장 점유율 방어에 실패하게 만들었습니다. 반면 Amore Pacific은 임상 데이터라는 기술적 장벽을 유지하며 가격 전쟁의 직접적인 타격을 최소화하는 전략적 균형점을 찾았습니다.

### Turn 4

**Events fired:** 글로벌 물류 병목 현상 심화

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Clinical Data Push`@0.80 | `marginal` ↓ | 22.8% |
| Shiseido | `Clinical Data Push`@0.80 | `dominant` ↑ | 78.3% |
| Amore Pacific | `Olive Young Expansion`@0.70 | `strong` → | 64.5% |

**Adjudicator narrative:** AURIE는 T1부터 T3까지 임상 데이터와 일본 직영 확장이라는 이중 투자를 감행하며 현금 소진을 가속화했고, T4의 규제 강화와 물류 병목 현상은 유동성 임계점을 돌파하여 시장 지위를 한 단계 하락시켰습니다. Shiseido는 풍부한 현금 보유량을 바탕으로 T2-T3의 R&D 및 가격 공세가 만든 우위를 T4의 외부 충격에서도 방어하며, 오히려 경쟁사의 약점을 이용해 유통망과 점유율을 더욱 공고히 했습니다. Amore Pacific은 다각화된 포트폴리오와 채널 전략으로 특정 국가의 무역 장벽 리스크를 분산시키며, T3의 임상 데이터 투자 효과를 유지한 채 안정적인 수익 구조를 고수했습니다. 결과적으로 AURIE의 구조적 취약점이 노출되는 동안 Shiseido는 시장 지배력을 강화하고 Amore Pacific은 균형 잡힌 성장을 이어갔습니다.

**경쟁 상호작용 분석:** AURIE의 과도한 현금 소진과 Shiseido의 자본 우위가 맞물려 시장 격차가 극대화되었습니다. Shiseido는 AURIE의 유동성 위기를 기회로 삼아 오프라인 채널을 확장하는 반면, Amore Pacific은 리스크 분산 전략으로 중립적인 위치를 유지하며 양측의 공방을 견뎌냈습니다.

### Turn 5

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `D2C NPS Optimization`@0.80 | `weak` ↘ | 19.8% |
| Shiseido | `Olive Young Expansion`@0.80 | `dominant` ↑ | 84.3% |
| Amore Pacific | `Clinical Data Push`@0.80 | `strong` ↗ | 64.0% |

**Adjudicator narrative:** AURIE 는 T1 에서 T4 에 걸쳐 임상 데이터 투자와 가격 인하를 반복하며 현금을 급격히 소진했고, 이로 인해 T5 에는 중국 규제 강화와 물류 병목 현상이라는 외부 충격에 완전히 무력화되었습니다. Shiseido 는 T2 의 R&D 베팅과 T4 의 임상 데이터 투자를 통해 규제 장벽을 우회하는 동시에, 풍부한 현금으로 시장 지배력을 확장하며 AURIE 의 추락을 가속화했습니다. Amore Pacific 은 T3 의 임상 데이터와 T4 의 올리브영 확장을 통해 프리미엄 이미지를 유지하며, 현금 소모가 심한 경쟁사들과의 격차에서 벗어나 안정적 성장을 이어갔습니다.

**경쟁 상호작용 분석:** AURIE 의 현금 고갈은 중국 규제와 물류 병목이라는 외부 리스크를 감당하지 못하게 하여 시장에서의 생존을 위협하는 구조적 약점으로 작용했습니다. 반면 Shiseido 와 Amore Pacific 은 각각 자본력과 기술적 우위를 바탕으로 이러한 시장 환경에서 오히려 경쟁사들을 압도하며 지위를 강화했습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 55.0% | -12.0pp | +0.0pp | +5.0pp | 48.0% |
| T2 | 48.0% | -5.6pp | -6.0pp | +5.0pp | 41.4% |
| T3 | 41.4% | -7.6pp | +0.0pp | +3.0pp | 36.8% |
| T4 | 36.8% | -12.0pp | -3.0pp | +1.0pp | 22.8% |
| T5 | 22.8% | -6.0pp | +0.0pp | +3.0pp | 19.8% |
