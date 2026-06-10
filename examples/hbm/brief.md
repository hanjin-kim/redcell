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
| **SK Hynix** | 70.0% | 100.0% | +30.0pp | `dominant` |
| Samsung Electronics DS | 85.0% | 66.0% | -19.0pp | `contested` |
| Micron Technology | 60.0% | 29.2% | -30.8pp | `contested` |

## 2. 턴별 전개

### Turn 1  ([C-suite 토론 상세 →](brief_trace.md#turn-1))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Yield Optimization`@0.90 | `dominant` ↗ | 79.5% |
| Samsung Electronics DS | `Samsung Quality Catch-up`@0.80 | `strong` ↗ | 88.8% |
| Micron Technology | `Micron US Fab Expansion`@0.80 | `contested` ↗ | 54.2% |

**Adjudicator narrative:** SK Hynix 는 TSMC CoWoS 패키징 용량을 선점하며 HBM 시장의 핵심 병목을 장악하고 주도권을 강화했습니다. 삼성전자는 대규모 자본력을 투입해 기술 격차 해소에 나섰으나 HBM3E 인증 지연으로 인해 시장 점유율 방어에 어려움을 겪고 있습니다. Micron Technology 는 CHIPS Act 지원을 통해 자금 기반을 다졌지만 TSMC CoWoS 할당 부족으로 성장 잠재력이 제한받고 있습니다. 결과적으로 패키징 역량 확보 여부가 이번 턴의 승패를 가르는 가장 중요한 변수로 작용했습니다.

**경쟁 상호작용 분석:** SK Hynix 의 TSMC CoWoS 우선 할당 확보는 삼성전자의 자본력 투입과 Micron Technology 의 미국 내 생산 기지 확보 효과를 상쇄하며 생태계 지배력을 재편했습니다. 이로 인해 패키징 용량 확보 여부가 단순한 기술 경쟁을 넘어 자원 배분의 실질적 결정 요인으로 작용하고 있습니다.

### Turn 2  ([C-suite 토론 상세 →](brief_trace.md#turn-2))

**Events fired:** 중국 고급 패키징 장비 수출 금지, TSMC CoWoS 할당량 재조정

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Yield Optimization`@0.80 | `dominant` ↗ | 81.5% |
| Samsung Electronics DS | `Samsung Quality Catch-up`@0.80 | `strong` ↘ | 85.0% |
| Micron Technology | `Breakthrough R&D Bet`@0.90 | `contested` ↘ | 41.2% |

**Adjudicator narrative:** SK Hynix는 T1의 우위 기반을 바탕으로 TSMC CoWoS 할당권을 선점하고 HBM4 기술 표준을 장악하며 시장 지배력을 확정했습니다. 반면 Samsung Electronics DS는 T1의 자본력 확보가 있었으나, T2에 들어 TSMC CoWoS 할당 지연과 재인증 지연이 누적되어 성장 궤도가 둔화되었습니다. Micron Technology는 T1의 팹 확장 투자가 기술 역량 회복에 기여했으나, T2에 TSMC CoWoS 후순위 할당과 현금 소진 가속화로 인해 제품 가용성 한계가 경영 지속 가능성을 위협하는 상황으로 전락했습니다.

**경쟁 상호작용 분석:** SK Hynix가 TSMC CoWoS의 물리적 공급망을 선점하며 승자독식 구조를 완성한 반면, Samsung Electronics DS와 Micron Technology는 패키징 할당 지연으로 인해 공급망 권력에서 소외되었습니다. 특히 Micron Technology는 고강도 투자에도 불구하고 할당 후순위로 인해 수익 창출의 상한선이 현실적으로 제한되는 구조적 약점을 노출했습니다.

### Turn 3  ([C-suite 토론 상세 →](brief_trace.md#turn-3))

**Events fired:** 미국 칩스법 보조금 확대

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Capacity Ramp`@0.80 | `dominant` ↗ | 82.5% |
| Samsung Electronics DS | `Breakthrough R&D Bet`@0.90 | `strong` ↘ | 81.0% |
| Micron Technology | `Breakthrough R&D Bet`@0.90 | `contested` ↗ | 39.2% |

**Adjudicator narrative:** SK Hynix는 T1과 T2에서 지속된 수율 최적화 전략의 결실로 TSMC CoWoS 협력을 통해 HBM3E 12-Hi 양산 라인을 가동하며 시장 지배력을 강화했습니다. 반면 Samsung Electronics DS는 T1과 T2에서 집중된 R&D 투자가 HBM3E 12-Hi 인증 지연이라는 결과로 이어져 시장 주도권 확보에 실패했습니다. Micron Technology는 T2의 미국 공장 확장 전략이 CHIPS Act 보조금과 맞물려 비용 부담을 줄였으나, TSMC CoWoS 할당량 제약으로 인해 매출 성장에 한계를 맞이했습니다. 이로 인해 SK Hynix는 공급망 장악력을 바탕으로 타사들과의 격차를 더욱 벌리는 결과를 낳았습니다.

**경쟁 상호작용 분석:** SK Hynix의 TSMC CoWoS 선점 전략은 공급망 안정성을 확보하여 고객 전환 비용을 높이는 반면, Samsung Electronics DS와 Micron Technology는 인증 지연과 할당량 제약으로 인해 이 격차를 좁히지 못했습니다. 특히 SK Hynix의 양산 라인 가동률 유지가 시장 점유율 방어에 결정적인 역할을 한 반면, 타사들은 기술 로드맵 재설정과 제도적 수혜에만 의존하여 즉각적인 성과로 연결되지 못했습니다.

### Turn 4  ([C-suite 토론 상세 →](brief_trace.md#turn-4))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Yield Optimization`@0.85 | `dominant` ↗ | 91.1% |
| Samsung Electronics DS | `Breakthrough R&D Bet`@0.80 | `strong` ↘ | 79.0% |
| Micron Technology | `Aggressive Price Cut`@0.80 | `contested` ↘ | 35.2% |

**Adjudicator narrative:** SK Hynix는 T1부터 T3까지 지속된 수율 최적화와 용량 증설을 통해 NVIDIA Blackwell Ultra 계약이라는 결정적 우위를 점했으나, 청주 M15X 건설 등 대규모 Capex가 누적되면서 현금 흐름에 부담을 안게 되었습니다. 삼성전자는 T2부터 T3까지 기술 개발에 집중하며 R&D 파이프라인을 강화했으나, HBM3E 12-Hi 인증 지연과 파운드리 적자가 누적되어 시장 점유율 회복에 실패하며 위상이 하락했습니다. Micron Technology는 T2와 T3의 R&D 베팅과 CHIPS Act 보조금 수혜로 시장 진입 기반을 마련했으나, TSMC CoWoS 할당량 후순위와 낮은 현금 보유율이 확장 속도를 제한하며 여전히 경쟁 구도에서 뒤처지고 있습니다.

**경쟁 상호작용 분석:** SK Hynix의 파트너십 Lock-in 전략이 프리미엄 수익 구조를 고정시키는 동안, Micron Technology의 자금 강제 소모형 전략은 단기 점유율 방어에 그치며 장기 생존 위험을 키우고 있습니다. 삼성전자의 기술 개발 집중은 HBM3E 12-Hi 승격을 위한 검증 지연으로 인해 시장 진입 타이밍을 놓치며, 규제적 리스크와 TSMC CoWoS 할당량 재조정이 경쟁 구도를 더욱 복잡하게 만들고 있습니다.

### Turn 5  ([C-suite 토론 상세 →](brief_trace.md#turn-5))

**Events fired:** 삼성 파운드리 품질 스캔들

| 측 | Action | Position | Cash |
|---|---|---|---|
| **SK Hynix** | `SK Hynix Yield Optimization`@0.90 | `dominant` ↗ | 100.0% |
| Samsung Electronics DS | `Breakthrough R&D Bet`@0.75 | `contested` ↘ | 66.0% |
| Micron Technology | `Breakthrough R&D Bet`@0.70 | `contested` ↗ | 29.2% |

**Adjudicator narrative:** SK Hynix는 T1부터 T4까지 지속된 수율 최적화와 이천 M16 라인 가동률 향상이 T5에 이르러 현금 비율 91%라는 압도적 재무 건전성으로 이어졌습니다. 반면 삼성전자는 T2 이후 지속된 파운드리 품질 스캔들이 T3, T4의 R&D 베팅과 맞물려 자금 조달 비용을 급증시키고 HBM 양산 일정을 지연시켰습니다. Micron Technology는 T2-T3의 R&D 투자로 기술 신뢰도를 높였으나, T4의 공격적 가격 인하와 CoWoS 할당량 부족으로 인해 현금 소모가 가속화되며 성장에 한계를 겪고 있습니다.

**경쟁 상호작용 분석:** SK Hynix의 수율 극대화 전략은 현금 흐름을 강화하여 규제 리스크를 상쇄하는 반면, 삼성전자의 품질 문제는 자금 조달 비용을 높여 기술 개발을 지연시키고 있습니다. Micron Technology는 기술적 진전을 이루었으나, SK Hynix의 압도적 공급망 우위와 삼성의 자금난 사이에서 성장 속도가 제한받고 있습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 70.0% | -5.5pp | +0.0pp | +15.0pp | 79.5% |
| T2 | 79.5% | -12.0pp | -1.0pp | +15.0pp | 81.5% |
| T3 | 81.5% | -12.0pp | -2.0pp | +15.0pp | 82.5% |
| T4 | 82.5% | -6.3pp | +0.0pp | +15.0pp | 91.1% |
| T5 | 91.1% | -6.5pp | +2.0pp | +13.4pp | 100.0% |
