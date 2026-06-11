# Red Team Brief

이 전략을 주어진 환경에서 수행할 때, 우리 측과 경쟁사가 어떻게 반응하고 어떤 risk가 emerging 되는지 트레이싱한 결과입니다.

**산업:** `semiconductor_memory_hbm`

**우리 회사:** SK Hynix  ·  **경쟁사:** Samsung Electronics DS, Micron Technology

**검증 대상 전략:**
> HBM4 양산 우선 + HBM3E 12-Hi capacity 유지 듀얼 트랙:
- 청주 M15X 라인 ramp 가속 (HBM3E 12-Hi 추가 capacity 50%)
- HBM4 양산 일정 2027 H1 → 2026 H2로 6개월 앞당김
- TSMC CoWoS 패키징 multi-year allocation 재계약
- R&D 비중 매출의 12 → 16%, 차세대 HBM4E 선행 투자
- DRAM 일반 commodity 비중 60% → 45% 축소, HBM/DDR5 server-grade 집중
24개월 KPI: HBM 매출 점유 53 → 60%, NVIDIA HBM4 launch supplier 1순위 사수.

**주어진 환경:**
> NVIDIA가 2026 H2 Blackwell Ultra (B200) 출하 가속하며 HBM3E 12-Hi 수요 폭증.
동시에 supplier 다변화 명목으로 Samsung HBM3E 12-Hi 재qualification 검토 + Micron
12-Hi 비중 확대 의지 시그널. HBM4 qualification 라운드도 2026 H1부터 NVIDIA가 주도.
TSMC CoWoS-L 패키징 capacity가 2026 +100% 확대 약속이나 NVIDIA + AMD + 클라우드
자체 ASIC가 모두 경쟁. 미국 CHIPS Act 2차 보조금 + 한국 K-Chips 세액공제 변동이
capex 인센티브에 영향.

## 1. 시뮬레이션 결과 요약

각 측의 시작 → 종료 변동:

| 측 | 초기 cash | T-final cash | Δ cash | T-final position |
|---|---|---|---|---|
| **SK Hynix** | 70.0% | 76.4% | +6.4pp | `dominant` |
| Samsung Electronics DS | 85.0% | 79.7% | -5.3pp | `strong` |
| Micron Technology | 60.0% | 50.2% | -9.8pp | `strong` |

## 2. 턴별 전개

### Turn 1  ([C-suite 토론 상세 →](brief_trace.md#turn-1))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `Next-Gen R&D Bet`@0.85 | `dominant` ↗ | 73.0% |
| Samsung Electronics DS | `CoWoS Allocation Push`@0.80 | `strong` → | 90.7% |
| Micron Technology | `Regulatory Subsidy Hunt`@0.80 | `contested` ↑ | 57.2% |

**Adjudicator narrative:** SK Hynix 는 TSMC CoWoS 패키징 용량이라는 절대 병목 자원을 선점하여 HBM3E 12-Hi 공급을 독점함으로써 시장 점유율 53% 를 유지하며 압도적 우위를 점했습니다. 삼성전자는 풍부한 자본과 보조금을 바탕으로 TSMC CoWoS 할당을 확보하려 노력했으나, HBM3E 12-Hi 인증 지연으로 인해 NVIDIA 신뢰 회복 비용이 발생하며 성장세가 정체되었습니다. 마이크론은 HBM3E 12-Hi 공급 자격을 획득하고 보조금 혜택을 받으며 입지를 넓혔으나, TSMC CoWoS 후순위 할당과 R&D 격차로 인해 추격 속도가 제한받고 있습니다.

**경쟁 상호작용 분석:** SK Hynix 의 선제적 양산과 TSMC CoWoS 용량 선점이 시장 지형을 결정짓는 핵심 변수로 작용하며, 이는 삼성과 마이크론의 추격 속도를 현금 효율성보다 초기 물량 확보 여부에 따라 제한하고 있습니다. 삼성의 막대한 자본력은 규제 리스크를 상쇄하지만 기술 인증 지연이 시장 진입 장벽으로 작용하여 SK Hynix 의 선점 효과를 따라잡지 못하고 있습니다.

### Turn 2  ([C-suite 토론 상세 →](brief_trace.md#turn-2))

**Events fired:** DRAM 일반 가격 폭락

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix NVIDIA Lock-in`@0.90 | `dominant` → | 72.4% |
| Samsung Electronics DS | `Samsung Custom HBM Pitch`@0.80 | `strong` ↘ | 84.7% |
| Micron Technology | `Next-Gen R&D Bet`@0.80 | `contested` → | 48.2% |

**Adjudicator narrative:** SK Hynix는 T1의 Next-Gen R&D 베팅을 통해 HBM3E 12-Hi 선점과 TSMC CoWoS 우선 확보라는 강력한 기반을 마련했으나, 이번 턴에 일반 DRAM 가격 급락과 독과점 규제 강화로 인해 현금 흐름이 압박받으며 모멘텀이 정체되었습니다. Samsung Electronics DS는 T1의 CoWoS 할당 추진으로 높은 현금 보유력을 유지했으나, HBM3E 12-Hi 자격 인증 지연과 파운드리 적자가 누적되며 시장 진입 타이밍을 놓쳐 하락세를 면치 못했습니다. Micron Technology는 T1의 Regulatory Subsidy Hunt를 통해 CHIPS Act 보조금과 공장 확장을 이루었으나, TSMC CoWoS 용량 할당 부족이라는 구조적 병목으로 인해 고성장 모멘텀을 발휘하지 못하고 기존 지위를 유지하는 데 그쳤습니다.

**경쟁 상호작용 분석:** NVIDIA의 공급망 다변화 전략이 SK Hynix의 독점 모델을 약화시키려 하지만, TSMC CoWoS 용량 부족이라는 공통 병목 변수가 모든 플레이어의 성장을 동시에 제한하고 있습니다. SK Hynix는 기술 선점과 우선 할당으로 우위를 지켰으나, 일반 DRAM 가격 하락과 규제 압력으로 인해 그 이득이 상쇄되는 양상을 보입니다. 반면 Micron Technology와 Samsung Electronics DS는 각각 보조금과 현금력을 바탕으로 성장하려 했으나, 패키징 용량 할당 지연으로 인해 시장 진입 속도가 둔화되었습니다.

### Turn 3  ([C-suite 토론 상세 →](brief_trace.md#turn-3))

**Events fired:** 마이크론 일본 공장 조기 완공

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `Next-Gen R&D Bet`@0.80 | `dominant` → | 73.4% |
| Samsung Electronics DS | `Samsung HBM Leapfrog`@0.80 | `strong` ↘ | 80.7% |
| Micron Technology | `Micron US Fab Expansion`@0.75 | `strong` ↗ | 50.2% |

**Adjudicator narrative:** T1과 T2 동안 SK Hynix가 Next-Gen R&D와 NVIDIA Lock-in을 통해 우위를 점했으나, T3에 들어서는 현금 소모 증가와 반독점 규제 강화로 인해 지배력 유지에 집중되는 국면이 되었습니다. Samsung Electronics DS는 T2의 Custom HBM Pitch와 파운드리 통합 노력에도 불구하고 HBM3E 12-Hi 자격 승인 지연이라는 누적된 병목 현상이 T3까지 성장 모멘텀을 저하시키고 있습니다. 반면 Micron Technology는 T2의 Next-Gen R&D 투자와 T3의 공장 증설 및 인증 통과가 시너지를 일으켜, 과거 패키징 자원 부족이라는 약점을 극복하고 점유율을 빠르게 확대하는 전환점을 맞이했습니다.

**경쟁 상호작용 분석:** NVIDIA의 공급망 다변화 전략이 SK Hynix의 독점 지위를 약화시키는 동시에 Micron Technology와 Samsung Electronics DS에게 새로운 기회를 제공하며 시장 구조를 재편하고 있습니다. 특히 Micron Technology의 공장 증설과 인증 통과가 패키징 병목 현상을 완화한 반면, Samsung Electronics DS의 인증 지연은 경쟁사 대비 성장 속도를 상대적으로 늦추는 요인으로 작용했습니다.

### Turn 4  ([C-suite 토론 상세 →](brief_trace.md#turn-4))

**Events fired:** 엔비디아 블랙웰 울트라 수요 폭발

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Yield Optimization`@0.80 | `dominant` ↗ | 81.4% |
| Samsung Electronics DS | `CoWoS Allocation Push`@0.70 | `strong` ↘ | 81.7% |
| Micron Technology | `Next-Gen R&D Bet`@0.80 | `strong` ↗ | 52.2% |

**Adjudicator narrative:** SK Hynix는 T1부터 T3까지 지속된 Next-Gen R&D 베팅과 NVIDIA Lock-in 전략으로 Blackwell Ultra 수요 폭증에 대응하며 기술적 우위를 점했습니다. 반면 Samsung Electronics DS는 T2와 T3에 걸쳐 공격적 가격 인하와 CoWoS 선점을 시도했으나, HBM3E 인증 지연과 Foundry 적자 누적으로 인해 수익성 방어에 어려움을 겪고 있습니다. Micron Technology는 T3의 미국 공장 확장으로 성장 궤도에 올랐으나, T2의 낮은 현금 보유율이 누적된 재정적 부담으로 작용하여 고강도 투자 지속에 제약을 받고 있습니다.

**경쟁 상호작용 분석:** SK Hynix의 기술 선점이 시장 주도권을 공고히 하는 동안, Samsung Electronics DS의 가격 공세는 SK Hynix의 마진을 압박했으나 HBM3E 인증 지연으로 인해 그 효과가 제한되었습니다. Micron Technology는 보조금과 확장으로 성장세를 회복했으나, TSMC CoWoS 할당 노력에도 불구하고 패키징 병목이 성장을 저해하고 있습니다.

### Turn 5  ([C-suite 토론 상세 →](brief_trace.md#turn-5))

**Events fired:** 엔비디아 공급망 다변화 강제, AI 데이터센터 자본지출 조정

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Capacity Ramp`@0.85 | `dominant` ↘ | 76.4% |
| Samsung Electronics DS | `Next-Gen R&D Bet`@0.90 | `strong` ↗ | 79.7% |
| Micron Technology | `Next-Gen R&D Bet`@0.75 | `strong` ↑ | 50.2% |

**Adjudicator narrative:** SK Hynix는 T1-T4 동안 HBM4 및 Blackwell B200 수요에 대응하며 우위를 유지해 왔으나, 이번 턴에서 NVIDIA의 할당량 축소 요구와 ASML 장비 비용 상승으로 인해 성장이 둔화되었습니다. 반면 Samsung Electronics DS는 T2-T3 동안의 HBM3E 인증 지연과 CoWoS 할당 부족을 극복하고, 이번 턴에 SK Hynix의 할당 감소분을 수혜받아 회복세로 전환했습니다. Micron Technology는 T3-T4 동안의 Boise FAB 확장과 R&D 투자를 통해 입지를 다졌으나, TSMC CoWoS 용량 제약과 기술 격차로 인해 강세만 유지하고 있을 뿐 지배적인 도약은 어렵습니다.

**경쟁 상호작용 분석:** NVIDIA의 공급망 다변화 정책은 SK Hynix의 독점적 지위를 약화시키면서 삼성전자가 TSMC CoWoS 용량 제한 속에서 기회를 포착할 수 있는 틈을 만들었습니다. 동시에 Micron Technology는 미국의 공공 보조금과 기술 신뢰도 향상을 통해 시장 점유율을 빠르게 확대하고 있으나, 패키징 용량 제약과 기술 격차로 인해 SK Hynix의 우위를 완전히 대체하지는 못하고 있습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 70.0% | -12.0pp | +0.0pp | +15.0pp | 73.0% |
| T2 | 73.0% | -10.6pp | -5.0pp | +15.0pp | 72.4% |
| T3 | 72.4% | -12.0pp | -2.0pp | +15.0pp | 73.4% |
| T4 | 73.4% | -12.0pp | +5.0pp | +15.0pp | 81.4% |
| T5 | 81.4% | -12.0pp | -8.0pp | +15.0pp | 76.4% |
