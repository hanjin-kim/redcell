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


def _turn_section(d: dict) -> str:
    trace = d.get("trace", [])
    side_map = _side_map(d)
    lines = ["## 2. 턴별 전개", ""]
    if not trace:
        return "\n".join(lines + ["*(시뮬 결과 없음)*"])

    for t in trace:
        turn_num = t["turn"]
        events = ", ".join(t.get("events", [])) or "—"
        lines.append(f"### Turn {turn_num}")
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


def render_brief(data: dict) -> str:
    parts = [_header(data), _summary(data), _turn_section(data), _our_drivers(data)]
    return "\n".join(parts)
