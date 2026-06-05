"""Brief renderer — scenario card format.

Pure function: takes the analyzed run dict, returns a markdown string.
NO statistical aggregate language ("robust", "mean ± stdev", "CI") — each
scenario is one conditional plausible future, not an estimate.
"""
from __future__ import annotations


def _fmt_pp(x: float) -> str:
    return f"{x * 100:+.1f}pp"


def _fmt_cash(x: float) -> str:
    return f"{x * 100:.1f}%"


def _final_cash(trace: list) -> float:
    return trace[-1].get("cash", 0.0) if trace else 0.0


def _final_position(trace: list) -> str:
    return trace[-1].get("position", "?") if trace else "?"


def _cash_delta(trace: list) -> float:
    if len(trace) < 2:
        return 0.0
    return trace[-1].get("cash", 0.0) - trace[0].get("cash", 0.0)


def _header(d: dict) -> str:
    return "\n".join([
        "# Red Team Brief — Adversary Scenario Set",
        "",
        "> **Scope:** Pre-workshop *thinking aid*. 사용자 전략을 "
        "*N개 distinct adversary scenarios*로 stress-test. 각 scenario에서 "
        "전략이 *어디서 깨질 수 있는지* 가설 발굴.",
        "",
        "> **What this is NOT:** statistical estimator. *Robust claim 없음*, "
        "*mean ± stdev 없음*, *p-value 없음*. 각 scenario는 *조건부 시나리오* — "
        "\"X가 fire한다면 trajectory는 이렇다\" — 인용용 추정치 아님.",
        "",
        f"**산업:** `{d.get('industry', '?')}`",
        "",
        f"**검증 대상 전략:**\n> {d.get('user_strategy', '')}",
        "",
        f"**사용자 worried risk (Scenario 1로 포함):**\n> {d.get('user_worried_risk', '')}",
        "",
    ])


def _summary(d: dict) -> str:
    scenarios = d.get("scenarios", [])
    lines = ["## 1. Cross-Scenario Summary", ""]
    lines.append(
        f"{len(scenarios)} adversary scenarios. 각 scenario에서 우리 측 "
        f"cash + position 변동 (단일 trial — *우선순위 판단용*, 통계 아님):"
    )
    lines.append("")
    lines.append("| # | Scenario | Axis | T-final cash | position | Δ cash |")
    lines.append("|---|---|---|---|---|---|")
    for s in scenarios:
        m, trace = s["move"], s.get("trace", [])
        lines.append(
            f"| {s['scenario_idx']+1} | {m['label_ko']} | `{m['axis']}` | "
            f"{_fmt_cash(_final_cash(trace))} | `{_final_position(trace)}` | "
            f"{_fmt_pp(_cash_delta(trace))} |"
        )
    lines.append("")
    return "\n".join(lines)


def _scenario_card(s: dict, rank: int) -> str:
    m, trace = s["move"], s.get("trace", [])
    a = s.get("analysis") or {}
    lines = [f"## {rank}. Scenario {s['scenario_idx']+1}: {m['label_ko']}", ""]
    lines.append(f"**Axis:** `{m['axis']}`")
    lines.append("")
    lines.append(f"**Primary stressor:** {m['primary_stressor']}")
    lines.append("")
    lines.append(f"**Secondary conditions:** {m['secondary_conditions']}")
    lines.append("")
    lines.append(f"**Expected failure mode (hypothesis):** {m['expected_failure_mode']}")
    lines.append("")

    if trace:
        lines.append("### Trajectory")
        lines.append("")
        lines.append("| Turn | Action | Position | Cash | Events fired |")
        lines.append("|------|--------|----------|------|--------------|")
        for n in trace:
            evs = ", ".join(n.get("events", [])) or "—"
            lines.append(
                f"| T{n['turn']} | `{(n.get('audit_action_type') or '')[:20]}`@"
                f"{n.get('audit_intensity', 0.5):.2f} | "
                f"`{n.get('position', '?')}` {n.get('momentum', '')} | "
                f"{_fmt_cash(n.get('cash', 0.0))} | {evs} |"
            )
        lines.append("")

    if a.get("axis_aligned_summary"):
        lines.append("### Axis-aligned analysis")
        lines.append("")
        lines.append(f"> {a['axis_aligned_summary']}")
        lines.append("")

    if a.get("cash_driver_per_turn"):
        lines.append("### Per-turn cash drivers")
        lines.append("")
        for dr in a["cash_driver_per_turn"]:
            lines.append(f"- {dr}")
        lines.append("")

    if a.get("observation_triggers"):
        lines.append("### Observation triggers (가설 강화/약화 신호)")
        lines.append("")
        for t in a["observation_triggers"]:
            if isinstance(t, dict):
                st = t.get("signal_type", "")
                ind = t.get("indicator", "")
                mark = "✅" if st == "strong_support" else "⚠"
                lines.append(f"- {mark} **{st}**: {ind}")
            else:
                lines.append(f"- {t}")
        lines.append("")

    if a.get("diligence_questions"):
        lines.append("### Diligence questions (워크숍 prep)")
        lines.append("")
        for i, q in enumerate(a["diligence_questions"], 1):
            lines.append(f"**Q{i}:** {q}")
            lines.append("")
    return "\n".join(lines)


def _caveats() -> str:
    return "\n".join([
        "## Caveats",
        "",
        "- **Single-trial per scenario** — 통계적 변동성 측정 아님. "
        "재실행 시 RNG로 일부 다른 events 발효 가능.",
        "- **No matched counterfactual** — \"event X fire vs not\" isolated "
        "effect 측정 안 함. 각 scenario는 *plausible future* 하나.",
        "- **Calibration is day-0** — 비용/revenue 매핑은 rulebook bootstrap. "
        "절대값보다 *상대 비교*·*방향성* (hypothesis prioritization).",
        "- **Output is *질문* not *결론*** — diligence question을 워크숍 prep "
        "checklist로. 인용 가능한 결론으로 사용 *금지*.",
        "",
    ])


def render_brief(data: dict) -> str:
    parts = [_header(data), _summary(data)]
    for i, s in enumerate(data.get("scenarios", []), start=2):
        parts.append(_scenario_card(s, rank=i))
    parts.append(_caveats())
    return "\n".join(parts)
