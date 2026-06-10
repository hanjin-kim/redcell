"""Brief renderer — single-trajectory output (v0.3).

The input is a redcell run dict ({user_strategy, environment, industry,
our_company, competitors, trace}). Each ``trace`` entry exposes every
side's per-turn data so we can show our team's actions AND competitor
reactions side by side.
"""
from __future__ import annotations


def _fmt_pp(x: float) -> str:
    return f"{x * 100:+.1f}pp"


def _fmt_cash(x: float) -> str:
    return f"{x * 100:.1f}%"


def _initial_cash(turn: dict, sid: str) -> float:
    attr = turn.get("sides", {}).get(sid, {}).get("cash_attribution", {})
    return attr.get("starting", turn.get("sides", {}).get(sid, {}).get("cash", 0.0))


def _final_pos(trace: list, sid: str) -> str:
    if not trace:
        return "?"
    return trace[-1].get("sides", {}).get(sid, {}).get("position", "?")


def _final_cash(trace: list, sid: str) -> float:
    if not trace:
        return 0.0
    return trace[-1].get("sides", {}).get(sid, {}).get("cash", 0.0)


def _cash_delta(trace: list, sid: str) -> float:
    if not trace:
        return 0.0
    first = _initial_cash(trace[0], sid)
    last = trace[-1].get("sides", {}).get(sid, {}).get("cash", 0.0)
    return last - first


def _side_map(d: dict) -> dict[str, str]:
    """side_id → display name."""
    m: dict[str, str] = {"side_a": d.get("our_company", "side_a")}
    competitors = d.get("competitors", [])
    # Naive — assume side_b/c... order matches competitors[] order
    for i, name in enumerate(competitors):
        m[f"side_{chr(ord('b') + i)}"] = name
    return m


def _header(d: dict) -> str:
    return "\n".join([
        "# Red Team Brief",
        "",
        "이 전략을 주어진 환경에서 수행할 때, 우리 측과 경쟁사가 어떻게 반응하고 "
        "어떤 risk가 emerging 되는지 트레이싱한 결과입니다.",
        "",
        f"**산업:** `{d.get('industry', '?')}`",
        "",
        f"**우리 회사:** {d.get('our_company', '?')}  ·  "
        f"**경쟁사:** {', '.join(d.get('competitors', [])) or '?'}",
        "",
        f"**검증 대상 전략:**\n> {d.get('user_strategy', '').strip()}",
        "",
        f"**주어진 환경:**\n> {d.get('environment', '').strip()}",
        "",
    ])


def _summary(d: dict) -> str:
    trace = d.get("trace", [])
    side_map = _side_map(d)
    lines = ["## 1. 시뮬레이션 결과 요약", ""]
    if not trace:
        lines.append("*(시뮬 결과 없음)*")
        return "\n".join(lines)
    lines.append("각 측의 시작 → 종료 변동:")
    lines.append("")
    lines.append("| 측 | 초기 cash | T-final cash | Δ cash | T-final position |")
    lines.append("|---|---|---|---|---|")
    sides = list(trace[-1].get("sides", {}).keys())
    for sid in sides:
        name = side_map.get(sid, sid)
        mark = "**" if sid == "side_a" else ""
        lines.append(
            f"| {mark}{name}{mark} | "
            f"{_fmt_cash(_initial_cash(trace[0], sid))} | "
            f"{_fmt_cash(_final_cash(trace, sid))} | "
            f"{_fmt_pp(_cash_delta(trace, sid))} | "
            f"`{_final_pos(trace, sid)}` |"
        )
    lines.append("")
    return "\n".join(lines)


def _turn_section(d: dict, trace_link: str | None = None) -> str:
    trace = d.get("trace", [])
    side_map = _side_map(d)
    lines = ["## 2. 턴별 전개", ""]
    if not trace:
        return "\n".join(lines + ["*(시뮬 결과 없음)*"])

    for t in trace:
        turn_num = t["turn"]
        events = ", ".join(t.get("events", [])) or "—"
        header = f"### Turn {turn_num}"
        if trace_link:
            header += f"  ([C-suite 토론 상세 →]({trace_link}#turn-{turn_num}))"
        lines.append(header)
        lines.append("")
        lines.append(f"**Events fired:** {events}")
        lines.append("")
        lines.append("| 측 | Action | Position | Cash |")
        lines.append("|---|---|---|---|")
        for sid, side in t.get("sides", {}).items():
            name = side_map.get(sid, sid)
            mark = "**" if sid == "side_a" else ""
            action = f"`{side.get('action_type', '')}`@{side.get('action_intensity', 0):.2f}"
            lines.append(
                f"| {mark}{name}{mark} | {action} | "
                f"`{side.get('position', '?')}` {side.get('momentum', '')} | "
                f"{_fmt_cash(side.get('cash', 0.0))} |"
            )
        lines.append("")
        narrative = t.get("narrative", "")
        if narrative:
            lines.append(f"**Adjudicator narrative:** {narrative}")
            lines.append("")
        interaction = t.get("interaction", "")
        if interaction:
            lines.append(f"**경쟁 상호작용 분석:** {interaction}")
            lines.append("")
    return "\n".join(lines)


def _our_drivers(d: dict) -> str:
    """Our side's per-turn cash drivers (action / events / position revenue)."""
    trace = d.get("trace", [])
    lines = ["## 3. 우리 측 현금 동인", ""]
    lines.append("매 턴 cash identity: "
                 "`starting + action_cost + events_delta + position_revenue = ending`")
    lines.append("")
    lines.append("| Turn | Start | Action | Events | Position rev | End |")
    lines.append("|------|-------|--------|--------|--------------|-----|")
    for t in trace:
        side = t.get("sides", {}).get("side_a", {})
        attr = side.get("cash_attribution") or {}
        if not attr:
            continue
        lines.append(
            f"| T{t['turn']} | "
            f"{_fmt_cash(attr.get('starting', 0.0))} | "
            f"{_fmt_pp(attr.get('action_cost', 0.0))} | "
            f"{_fmt_pp(attr.get('events_delta', 0.0))} | "
            f"{_fmt_pp(attr.get('position_revenue', 0.0))} | "
            f"{_fmt_cash(attr.get('ending', 0.0))} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_brief(data: dict, *, trace_link: str | None = None) -> str:
    """Render the headline brief. If ``trace_link`` (relative path to a
    companion trace.md) is given, each turn header gets a link to its
    anchor in that file."""
    parts = [
        _header(data),
        _summary(data),
        _turn_section(data, trace_link=trace_link),
        _our_drivers(data),
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------
# Trace renderer — per-turn × per-side C-suite deliberation dump
# ----------------------------------------------------------------------

def _role_block(role_key: str, role_data: dict) -> list[str]:
    """One role's propose/challenge data → 2-3 markdown lines."""
    actions = role_data.get("actions") or []
    actions_str = ", ".join(
        f"`{a.get('action', '?')}`@{a.get('allocation', 0):.2f}"
        for a in actions
    ) or "—"
    out = [f"- **{role_key}**: {actions_str}"]
    risk = (role_data.get("risk") or "").strip()
    reason = (role_data.get("reason") or "").strip()
    cf = (role_data.get("changed_from") or "").strip()
    cb = (role_data.get("changed_because") or "").strip()
    dissent = (role_data.get("dissent_argument") or "").strip()
    if reason:
        out.append(f"  - rationale: {reason}")
    if risk:
        out.append(f"  - risk: {risk}")
    if cf and cb:
        out.append(f"  - changed `{cf}` → because: {cb}")
    if dissent:
        out.append(f"  - dissent: {dissent}")
    return out


def _deliberation_block(d: dict) -> list[str]:
    """Render one side's deliberation (phases 1-3)."""
    lines: list[str] = []
    phase1 = d.get("phase1") or {}
    phase2 = d.get("phase2") or {}
    phase3 = d.get("phase3") or {}
    da = d.get("devils_advocate") or ""
    majority = d.get("majority_action") or ""
    changes = d.get("position_changes") or []

    if phase1:
        lines.append("##### Phase 1 — 독립 제안")
        lines.append("")
        for role_key in phase1:
            lines.extend(_role_block(role_key, phase1[role_key]))
        lines.append("")

    if phase2:
        lines.append(f"##### Phase 2 — 비판적 검토 (다수안: `{majority or '?'}`"
                     + (f", DA: `{da}`" if da else "") + ")")
        lines.append("")
        for role_key in phase2:
            lines.extend(_role_block(role_key, phase2[role_key]))
        lines.append("")
        if changes:
            lines.append("**Position changes:**")
            for c in changes:
                lines.append(f"- {c}")
            lines.append("")

    if phase3:
        lines.append("##### Phase 3 — CEO 종합")
        lines.append("")
        decision = (phase3.get("decision") or "").strip()
        reasoning = (phase3.get("reasoning") or "").strip()
        if decision:
            lines.append(f"**Decision:** {decision}")
            lines.append("")
        if reasoning:
            lines.append(f"**Reasoning:** {reasoning}")
            lines.append("")
    return lines


def _expert_block(experts: list) -> list[str]:
    """Render the adjudicator panel's 3 experts + their key observations."""
    if not experts:
        return []
    lines = ["#### Adjudicator panel (3 experts)", ""]
    for er in experts:
        role = er.get("role") or er.get("role_id") or "?"
        obs = (er.get("key_observation") or "").strip()
        lines.append(f"**{role}**: {obs}")
        lines.append("")
        assessments = er.get("assessments") or {}
        for sid, a in assessments.items():
            lines.append(
                f"- {sid}: `{a.get('position', '?')}` "
                f"{a.get('momentum', '')} — {(a.get('rationale') or '').strip()}"
            )
        lines.append("")
    return lines


def render_trace(data: dict) -> str:
    """Per-turn × per-side C-suite deliberation dump. Each turn has an
    anchor (``#turn-N``) the brief can link to."""
    trace = data.get("trace", [])
    side_map = _side_map(data)
    lines = [
        "# Deliberation Trace",
        "",
        "각 턴의 C-suite 토론 (CEO/CFO/CTO/CMO/COO 제안 / 검토 / 종합) 과 "
        "adjudicator 패널 평가를 펼친 trace 입니다. 헤드라인 결과는 "
        "[브리프](.) 참조.",
        "",
        f"**산업:** `{data.get('industry', '?')}`  ·  "
        f"**우리 회사:** {data.get('our_company', '?')}",
        "",
        f"**검증 대상 전략:**\n> {data.get('user_strategy', '').strip()}",
        "",
        f"**주어진 환경:**\n> {data.get('environment', '').strip()}",
        "",
    ]

    if not trace:
        lines.append("*(시뮬 결과 없음)*")
        return "\n".join(lines)

    for t in trace:
        turn_num = t["turn"]
        events = ", ".join(t.get("events", [])) or "—"
        # Anchor for cross-link from brief.
        lines.append(f'<a id="turn-{turn_num}"></a>')
        lines.append(f"## Turn {turn_num}")
        lines.append("")
        lines.append(f"**Events fired:** {events}")
        lines.append("")

        for sid, side in t.get("sides", {}).items():
            name = side_map.get(sid, sid)
            mark = "**" if sid == "side_a" else ""
            lines.append(f"### {mark}{name}{mark} ({sid})")
            lines.append("")
            lines.append(
                f"- Final action: "
                f"`{side.get('action_type', '?')}`"
                f"@{side.get('action_intensity', 0):.2f}"
            )
            lines.append(f"- Position: `{side.get('position', '?')}` "
                         f"{side.get('momentum', '')}")
            lines.append(f"- Cash: {_fmt_cash(side.get('cash', 0.0))}")
            rat = (side.get("rationale") or "").strip()
            if rat:
                lines.append(f"- Adjudicator rationale: {rat}")
            lines.append("")
            # Deliberation phases
            delib = (t.get("deliberations") or {}).get(sid) or {}
            lines.extend(_deliberation_block(delib))

        # Adjudicator panel
        lines.extend(_expert_block(t.get("experts") or []))

        narrative = (t.get("narrative") or "").strip()
        if narrative:
            lines.append("#### Adjudicator synthesis")
            lines.append("")
            lines.append(f"> {narrative}")
            lines.append("")
        interaction = (t.get("interaction") or "").strip()
        if interaction:
            lines.append(f"**Interaction analysis:** {interaction}")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)
