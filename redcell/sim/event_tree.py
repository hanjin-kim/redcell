"""Event-branch tree expander + M-run Monte Carlo orchestration (Phase 2).

WEGO doctrine: every turn all players commit simultaneously, then the control
team resolves the turn. The tree branches ONLY on a turn's single pivotal
external event (fires / does not fire). The two children of a branch share the
same committed actions and the same non-pivotal events, so a sibling pair is a
clean matched counterfactual.

Competitor decisions and adjudication are NOT branched — they are
multi-dimensional with no well-defined counterfactual. Their variation is
observed across the M Monte Carlo trials instead (each trial = one tree with a
different stochastic seed).

Layering:
- campaign  = our strategy archetype (controlled)
- branch    = pivotal event (uncontrolled, cleanly binary)
- M trials  = competitor behaviour + adjudication noise (observed)
"""
from __future__ import annotations

import hashlib
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any

from .adjudicator import _adjudicate_turn, _initial_positions
from .branch_selector import decide_branch
from .event_deck import (
    create_event_deck_state,
    _build_event_effects,
    _draw_events,
    _event_deck_to_prompt,
)
from .scenario_cache import load_cached, save_cache
from .sim_utils import (
    _apply_cash_bookkeeping,
    _resolve_cash_costs,
)
from .tree_models import TreeNode, TreeResult

logger = logging.getLogger(__name__)

# Nominal share per ordinal position — keeps backward-compat TreeResult metrics
# (win_rate etc.) working until the position-native report rewrite (Phase 4).
_POS_NOMINAL = {
    "dominant": 0.55, "strong": 0.38, "contested": 0.25,
    "weak": 0.14, "marginal": 0.05,
}


@dataclass
class _TreeCtx:
    """Immutable shared context for one tree expansion."""

    companies: dict
    our_side: str
    sides: list
    industry: str
    structural_context: str
    rulebook: dict
    deck: list
    llm: Any
    max_turns: int
    branch_budget: int
    campaign_name: str
    power: dict
    init_shares: dict
    # Reassessment context — set per-trial in run_event_tree_simulation.
    available_campaigns: list = field(default_factory=list)  # bucket names for pivoting
    campaign_texts: dict = field(default_factory=dict)        # name -> full campaign strategy text
    seed_campaign_text: str = ""                                # original seed for our side
    cache_dir: Path | None = None                                # for per-turn LLM call cache
    # Industry-specific position-tier → per-turn revenue mapping. Loaded
    # from scenario.position_revenue. Falls back to adjudicator.POSITION_REVENUE
    # if not specified. Exposed to the brief renderer for audit.
    position_revenue: dict = field(default_factory=dict)
    # The user-supplied environment/risk frame (mirror of scenario.trigger_event).
    # Threaded into per-turn competitor strategy reassessment so each side can
    # adapt to the environment as the simulation unfolds.
    environment: str = ""


# ---------------------------------------------------------------------------
# Per-turn LLM call cache (memoization)
# ---------------------------------------------------------------------------
# Wraps `_deliberate_all` and `_adjudicate_turn` with disk-backed memoization
# keyed on the FULL input (state + prompts hash). This means:
#   - Re-runs after a mid-tree failure (e.g., T4 synthesis truncation) reload
#     T1-T3 outputs from cache; only T4-T5 hit LLM. Iteration goes from ~30
#     minutes to ~5-10 minutes when only the failure tail needs recomputation.
#   - Edits to deliberation_v2 / adjudicator prompts change the engine
#     signature → ALL cached calls invalidate automatically. No stale outputs.
#   - Pure prompt-irrelevant code edits (e.g., reporting layer) reuse all
#     cached outputs → instant repro.

_ENGINE_SIG_CACHE: str | None = None


def _engine_signature() -> str:
    """Short hash of the prompt code that drives deliberation + adjudication.

    Any edit to these prompts shifts the hash so the per-turn cache invalidates
    automatically. Computed once per process.
    """
    global _ENGINE_SIG_CACHE
    if _ENGINE_SIG_CACHE is not None:
        return _ENGINE_SIG_CACHE
    try:
        from . import adjudicator as adj
        from . import deliberation_v2 as dv
        blob = "".join([
            getattr(adj, "EXPERT_PROMPT", ""),
            getattr(adj, "SYNTHESIS_PROMPT", ""),
            getattr(dv, "PROPOSE_PROMPT", ""),
            getattr(dv, "CHALLENGE_PROMPT", ""),
            getattr(dv, "DEVILS_ADVOCATE_PROMPT", ""),
            getattr(dv, "BOARD_REVIEW_PROMPT", ""),
            getattr(dv, "STRATEGY_REASSESS_PROMPT", ""),
            getattr(dv, "COMPETITOR_REASSESS_PROMPT", ""),
        ])
    except Exception:
        blob = ""
    _ENGINE_SIG_CACHE = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12]
    return _ENGINE_SIG_CACHE


def _quantize_floats(obj: Any, ndigits: int = 4) -> Any:
    """Recursively round floats so FP precision drift doesn't break hash equality.

    Without this, the same logical cash value can serialize as
    ``0.41999999999999993`` in one run and ``0.42000000000000004`` in
    another (different addition order). Those serialize to different
    JSON strings → different hashes → cache miss even though the state
    is logically identical.
    """
    if isinstance(obj, float):
        return round(obj, ndigits)
    if isinstance(obj, dict):
        return {k: _quantize_floats(v, ndigits) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_quantize_floats(v, ndigits) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_quantize_floats(v, ndigits) for v in obj)
    return obj


def _hash_payload(payload: Any) -> str:
    """Stable 12-char hash of a JSON-serializable payload.

    Floats are quantized to 4 decimal places so FP precision drift in
    upstream arithmetic doesn't invalidate the cache for the same
    logical state.
    """
    quantized = _quantize_floats(payload)
    raw = json.dumps(quantized, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def _cached_deliberate(
    ctx: _TreeCtx, agents: dict, turn: int, init_shares: dict, cash: dict,
    power: dict, companies: dict, industry: str, events_prompt: str,
    positions: dict, branch_sig: str,
) -> dict:
    """Memoized wrapper for `_deliberate_all`.

    Key inputs include each agent's strategy + their deliberator's turn_history
    snapshot — that captures the agent's state evolution across the branch.
    """
    if ctx.cache_dir is None:
        return _deliberate_all(
            agents, turn, init_shares, cash, power, companies, industry,
            events_prompt, positions,
        )

    agent_state = {}
    for sid, agent in agents.items():
        delib = getattr(agent, "_deliberator", None)
        agent_state[sid] = {
            "strategy": getattr(agent, "_strategy", ""),
            "history": getattr(delib, "_turn_history", []) if delib else [],
        }
    payload = {
        "turn": turn,
        "engine_sig": _engine_signature(),
        "branch_sig": branch_sig,
        "init_shares": init_shares, "cash": cash, "power": power,
        "companies": companies, "industry": industry,
        "events_prompt": events_prompt, "positions": positions,
        "agent_state": agent_state,
    }
    key = f"deliberate_{_hash_payload(payload)}"
    cached = load_cached(key, "evt_turn", ctx.cache_dir)
    if cached is not None:
        return cached.get("campaigns", {})
    # Diagnostic: dump payload on cache miss so we can compare against the
    # payload that produced an earlier successful save. Toggle via env.
    import os as _os
    if _os.environ.get("STRATEGYFORGE_CACHE_DEBUG"):
        import sys as _sys
        dump_dir = Path(ctx.cache_dir) / "_miss_payloads"
        dump_dir.mkdir(parents=True, exist_ok=True)
        dump_path = dump_dir / f"deliberate_T{turn}_{_hash_payload(payload)}.json"
        try:
            dump_path.write_text(json.dumps(
                _quantize_floats(payload), ensure_ascii=False,
                indent=2, sort_keys=True, default=str,
            ), encoding="utf-8")
            print(f"[CACHE MISS DUMP] {dump_path}", file=_sys.stderr, flush=True)
        except Exception as _e:
            print(f"[CACHE MISS DUMP FAIL] {_e}", file=_sys.stderr, flush=True)

    campaigns = _deliberate_all(
        agents, turn, init_shares, cash, power, companies, industry,
        events_prompt, positions,
    )
    try:
        save_cache(key, "evt_turn", {"campaigns": campaigns}, ctx.cache_dir)
    except Exception as e:
        logger.warning("Deliberate cache save failed: %s", e)
    return campaigns


def _cached_decide_branch(
    ctx: _TreeCtx, turn: int, entering_positions: dict, fired_counts: dict,
    prior_branch_ids: list[str], branch_sig: str,
):
    """Memoized wrapper for `decide_branch`. Stabilizes which event the LLM
    picks for branching across reruns — without this, the cached adjudicator
    outputs would miss because branch decisions vary stochastically.
    """
    if ctx.cache_dir is None:
        return decide_branch(
            turn, entering_positions, ctx.companies, ctx.our_side,
            ctx.industry, ctx.deck, fired_counts, prior_branch_ids, ctx.llm,
        )

    payload = {
        "engine_sig": _engine_signature(),
        "branch_sig": branch_sig,
        "turn": turn,
        "entering_positions": entering_positions,
        "companies": ctx.companies, "our_side": ctx.our_side,
        "industry": ctx.industry,
        "fired_counts": fired_counts,
        "prior_branch_ids": list(prior_branch_ids),
        "deck_ids": [e.get("id") for e in (ctx.deck or [])],
    }
    key = f"branch_{_hash_payload(payload)}"
    cached = load_cached(key, "evt_turn", ctx.cache_dir)
    if cached is not None:
        data = cached.get("branch_point")
        if data is None:
            return None
        from .branch_selector import (
            BranchCandidate, BranchPoint,
        )
        cand_data = data["candidate"]
        cand = BranchCandidate(
            id=cand_data["id"], kind=cand_data["kind"],
            label=cand_data["label"],
            variant_a=cand_data["variant_a"],
            variant_b=cand_data["variant_b"],
        )
        return BranchPoint(
            turn=data["turn"], candidate=cand, reasoning=data["reasoning"],
        )

    bp = decide_branch(
        turn, entering_positions, ctx.companies, ctx.our_side,
        ctx.industry, ctx.deck, fired_counts, prior_branch_ids, ctx.llm,
    )
    try:
        if bp is None:
            save_cache(key, "evt_turn", {"branch_point": None}, ctx.cache_dir)
        else:
            save_cache(key, "evt_turn", {"branch_point": {
                "turn": bp.turn,
                "candidate": {
                    "id": bp.candidate.id, "kind": bp.candidate.kind,
                    "label": bp.candidate.label,
                    "variant_a": bp.candidate.variant_a,
                    "variant_b": bp.candidate.variant_b,
                },
                "reasoning": bp.reasoning,
            }}, ctx.cache_dir)
    except Exception as e:
        logger.warning("Branch cache save failed: %s", e)
    return bp


def _cached_adjudicate(
    ctx: _TreeCtx, turn: int, actions_detail: dict, previous_positions: dict,
    cash: dict, turn_events: list[dict], action_history: list[dict],
    branch_sig: str,
) -> dict:
    """Memoized wrapper for `_adjudicate_turn`."""
    if ctx.cache_dir is None:
        return _adjudicate_turn(
            llm=ctx.llm, turn=turn, companies=ctx.companies,
            actions_detail=actions_detail, previous_positions=previous_positions,
            cash=cash, industry=ctx.industry,
            structural_context=ctx.structural_context,
            turn_events=turn_events, action_history=action_history,
        )

    payload = {
        "turn": turn,
        "engine_sig": _engine_signature(),
        "branch_sig": branch_sig,
        "companies": ctx.companies, "industry": ctx.industry,
        "structural_context": ctx.structural_context,
        "actions_detail": actions_detail,
        "previous_positions": previous_positions, "cash": cash,
        "turn_events": [
            {"id": e.get("id"), "name": e.get("name"),
             "label_ko": e.get("label_ko", "")}
            for e in (turn_events or [])
        ],
        "action_history": action_history,
    }
    key = f"adjudicate_{_hash_payload(payload)}"
    cached = load_cached(key, "evt_turn", ctx.cache_dir)
    if cached is not None:
        return cached
    import os as _os
    if _os.environ.get("STRATEGYFORGE_CACHE_DEBUG"):
        import sys as _sys
        dump_dir = Path(ctx.cache_dir) / "_miss_payloads"
        dump_dir.mkdir(parents=True, exist_ok=True)
        dump_path = dump_dir / f"adjudicate_T{turn}_{_hash_payload(payload)}.json"
        try:
            dump_path.write_text(json.dumps(
                _quantize_floats(payload), ensure_ascii=False,
                indent=2, sort_keys=True, default=str,
            ), encoding="utf-8")
            print(f"[CACHE MISS DUMP] {dump_path}", file=_sys.stderr, flush=True)
        except Exception as _e:
            print(f"[CACHE MISS DUMP FAIL] {_e}", file=_sys.stderr, flush=True)
        if _os.environ.get("STRATEGYFORGE_CACHE_DEBUG_ABORT_ON_MISS"):
            raise RuntimeError(
                f"CACHE DEBUG abort: adjudicate T{turn} MISS (dump at {dump_path})"
            )

    result = _adjudicate_turn(
        llm=ctx.llm, turn=turn, companies=ctx.companies,
        actions_detail=actions_detail, previous_positions=previous_positions,
        cash=cash, industry=ctx.industry,
        structural_context=ctx.structural_context,
        turn_events=turn_events, action_history=action_history,
    )
    try:
        save_cache(key, "evt_turn", result, ctx.cache_dir)
    except Exception as e:
        logger.warning("Adjudicate cache save failed: %s", e)
    return result


# ---------------------------------------------------------------------------
# Per-turn building blocks
# ---------------------------------------------------------------------------

def _deliberate_all(
    agents: dict, turn: int, init_shares: dict, cash: dict, power: dict,
    companies: dict, industry: str, events_prompt: str, positions: dict,
) -> dict:
    """WEGO commit — every player deliberates in parallel, no peeking."""
    campaigns: dict = {}
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {
            executor.submit(
                agent.deliberate,
                turn=turn, shares=init_shares, cash=cash, power=power,
                companies=companies, industry=industry,
                current_events=events_prompt, positions=positions,
            ): sid
            for sid, agent in agents.items()
        }
        for future in as_completed(futures):
            sid = futures[future]
            try:
                campaigns[sid] = future.result()
            except Exception as e:
                logger.warning("Agent %s failed at turn %d: %s", sid, turn, e)
                campaigns[sid] = ("", {})
    return campaigns


def _reassess_our_campaign(
    ctx: _TreeCtx, parent: TreeNode, agents: dict,
    strategic_state: dict, turn: int,
) -> dict:
    """Ask our CEO whether to hold or pivot the campaign for this turn.

    Called once at the start of each turn (turn ≥ 2) for our side only.
    Mutates ``agents[ctx.our_side]._strategy`` in place if the verdict is
    pivot; returns an updated strategic_state dict to thread forward.

    Fail-safe: any error path returns the state unchanged (hold).
    """
    if turn < 2:
        return strategic_state

    if not ctx.available_campaigns:
        return strategic_state

    our_agent = agents.get(ctx.our_side)
    if our_agent is None:
        return strategic_state
    deliberator = getattr(our_agent, "_deliberator", None)
    if deliberator is None or not hasattr(deliberator, "reassess_campaign"):
        return strategic_state

    # Build trajectory summary from parent's path.
    path = parent.path_from_root() if parent is not None else []
    traj_lines: list[str] = []
    for n in path:
        if n.turn < 1:
            continue
        pos = n.positions.get(ctx.our_side, {}) if n.positions else {}
        cash_v = n.cash.get(ctx.our_side, 0.0) if n.cash else 0.0
        traj_lines.append(
            f"  T{n.turn}: pos={pos.get('position', '?')}"
            f"({pos.get('momentum', '→')}) cash={cash_v:.0%}"
        )
    trajectory_summary = "\n".join(traj_lines[-6:]) if traj_lines else "(none)"

    # Recent events (last 3 turns).
    recent_lines: list[str] = []
    for n in path[-3:]:
        for ev in (n.events or []):
            recent_lines.append(
                f"  T{n.turn}: {ev.get('label_ko', ev.get('name', '?'))}"
            )
    recent_str = "\n".join(recent_lines[-5:]) if recent_lines else "(none)"

    # Competitor moves last turn.
    comp_lines: list[str] = []
    if path:
        last = path[-1]
        for sid in ctx.sides:
            if sid == ctx.our_side:
                continue
            det = last.actions_detail.get(sid, {}) if last.actions_detail else {}
            atype = det.get("action_type", "")
            txt = (det.get("text", "") or "")[:60]
            comp_name = ctx.companies.get(sid, sid)
            comp_lines.append(f"  {comp_name}: {atype} — {txt}")
    comp_str = "\n".join(comp_lines) if comp_lines else "(none)"

    company_name = ctx.companies.get(ctx.our_side, ctx.our_side)

    try:
        result = deliberator.reassess_campaign(
            side=ctx.our_side,
            company_name=company_name,
            industry=ctx.industry,
            current_campaign=strategic_state.get("current_campaign_text", ""),
            seed_campaign=strategic_state.get("seed_campaign_text", ""),
            turns_on_current=strategic_state.get("turns_on_current", 1),
            trajectory_summary=trajectory_summary,
            recent_events=recent_str,
            competitor_moves=comp_str,
            available_campaigns=list(ctx.available_campaigns),
        )
    except Exception as e:
        logger.warning(
            "Campaign reassessment failed at turn %d for %s: %s",
            turn, ctx.our_side, e,
        )
        return strategic_state

    new_state = dict(strategic_state)
    if result.get("verdict") == "pivot" and result.get("new_campaign_name"):
        new_name = result["new_campaign_name"]
        new_text = ctx.campaign_texts.get(new_name, new_name)
        prev_name = new_state.get("campaign_name", "")
        our_agent._strategy = new_text
        new_state["campaign_name"] = new_name
        new_state["current_campaign_text"] = new_text
        new_state["pivoted_from"] = prev_name
        new_state["pivot_turn"] = turn
        new_state["pivot_trigger"] = result.get("trigger", "")
        new_state["pivot_rationale"] = result.get("rationale", "")
        new_state["pivot_cost_acknowledged"] = result.get("cost_acknowledged", "")
        new_state["turns_on_current"] = 1
        logger.info(
            "PIVOT at turn %d for %s: %s → %s (trigger=%s)",
            turn, ctx.our_side, prev_name, new_name, result.get("trigger"),
        )
    else:
        new_state["turns_on_current"] = new_state.get("turns_on_current", 0) + 1

    new_state["last_verdict"] = result.get("verdict", "hold")
    new_state["last_trigger"] = result.get("trigger", "none")
    new_state["last_rationale"] = result.get("rationale", "")
    return new_state


def _reassess_competitor_strategies(
    ctx: _TreeCtx, parent: TreeNode, agents: dict, turn: int,
) -> None:
    """Let each competitor side adapt its strategy in response to the
    environment + observed turn outcomes. Mutates ``agents[sid]._strategy``
    in place when a side chooses to adapt.

    Mirror of ``_reassess_our_campaign`` but for non-our sides: simpler
    because competitors don't have a pre-built campaign menu — they just
    free-form revise their strategy text.
    """
    if turn < 2:
        return
    if not ctx.environment:
        return

    # Build trajectory + recent events + our-actions blocks once; same
    # facts for every competitor reassess.
    path = parent.path_from_root() if parent is not None else []
    recent_events: list[str] = []
    for n in path[-3:]:
        for ev in (n.events or []):
            recent_events.append(
                f"  T{n.turn}: {ev.get('label_ko', ev.get('name', '?'))}"
            )
    recent_str = "\n".join(recent_events[-5:]) if recent_events else "(none)"

    # Our (the user's side) last-turn actions — competitors see this and
    # react.
    rival_lines: list[str] = []
    if path:
        last = path[-1]
        det = (last.actions_detail or {}).get(ctx.our_side, {}) or {}
        atype = det.get("action_type", "")
        txt = (det.get("text", "") or "")[:80]
        our_name = ctx.companies.get(ctx.our_side, ctx.our_side)
        if atype or txt:
            rival_lines.append(f"  {our_name}: {atype} — {txt}")
    rival_str = "\n".join(rival_lines) if rival_lines else "(none)"

    # Late import to keep cycle-safe; deliberation_v2 is already loaded
    # by upstream callers in practice.
    from . import deliberation_v2 as dv

    for sid in ctx.sides:
        if sid == ctx.our_side:
            continue
        agent = agents.get(sid)
        if agent is None:
            continue
        current_strategy = getattr(agent, "_strategy", "")
        company_name = ctx.companies.get(sid, sid)

        # This side's own trajectory snippet (last 3 turns).
        traj_lines: list[str] = []
        for n in path[-3:]:
            if n.turn < 1:
                continue
            pos = (n.positions or {}).get(sid, {}) if n.positions else {}
            cash_v = (n.cash or {}).get(sid, 0.0)
            traj_lines.append(
                f"  T{n.turn}: pos={pos.get('position', '?')}"
                f"({pos.get('momentum', '→')}) cash={cash_v:.0%}"
            )
        traj_str = "\n".join(traj_lines) if traj_lines else "(no trajectory yet)"

        try:
            result = dv.reassess_competitor_strategy(
                ctx.llm,
                side=sid,
                company_name=company_name,
                industry=ctx.industry,
                current_strategy=current_strategy,
                environment=ctx.environment,
                trajectory_summary=traj_str,
                recent_events=recent_str,
                rival_actions=rival_str,
            )
        except Exception as e:
            logger.warning(
                "Competitor reassess failed at turn %d for %s: %s",
                turn, sid, e,
            )
            continue

        verdict = result.get("verdict", "hold")
        rationale = (result.get("rationale", "") or "")[:120]
        if verdict == "adapt":
            new_strategy = result.get("new_strategy", "").strip()
            if new_strategy:
                agent._strategy = new_strategy
                logger.info(
                    "competitor-reassess T%d %s: ADAPT — %s",
                    turn, sid, rationale,
                )
            else:
                logger.info(
                    "competitor-reassess T%d %s: adapt-with-empty-strategy "
                    "(treated as hold)", turn, sid,
                )
        else:
            logger.info(
                "competitor-reassess T%d %s: hold — %s", turn, sid, rationale,
            )


def _build_actions(campaigns: dict, companies: dict) -> tuple[dict, dict, dict]:
    """Turn campaign tuples into (actions_text, actions_detail, impact_input)."""
    actions_text = {sid: campaigns.get(sid, ("", {}))[0] for sid in companies}
    actions_detail: dict = {}
    impact_input: dict = {}
    for sid in companies:
        _, delib = campaigns.get(sid, ("", {}))
        action_str = actions_text[sid]
        payload = delib.get("actions_payload", [])
        detail: dict = {
            "text": action_str,
            "action_type": delib.get("action_type", ""),
            "intensity": delib.get("intensity", 0.5),
        }
        if payload:
            detail["actions"] = payload
            impact_input[sid] = payload if len(payload) > 1 else payload[0]
        elif delib.get("action_type"):
            impact_input[sid] = {
                "action_type": delib["action_type"],
                "intensity": delib.get("intensity", 0.5),
            }
        else:
            impact_input[sid] = {"action_type": "", "intensity": 0.0}
        actions_detail[sid] = detail
    return actions_text, actions_detail, impact_input


def _inject_event_cash(cash: dict, events: list[dict], sides: list) -> dict:
    """Apply event cash effects to a copy of ``cash``."""
    out = dict(cash)
    if not events:
        return out
    effects = _build_event_effects(events, list(sides))
    for sid in out:
        delta = effects.get(sid, {}).get("cash_delta", 0.0)
        out[sid] = max(0.0, min(1.0, out[sid] + delta))
    return out


def _make_node(
    ctx: _TreeCtx, turn: int, prev_positions: dict, child_cash: dict,
    cash_deltas: dict, actions_text: dict, actions_detail: dict, campaigns: dict,
    events_for_adj: list[dict], parent: TreeNode, branch_meta: dict,
    strategic_state: dict | None = None,
    branch_sig: str = "",
) -> tuple[TreeNode, dict, dict]:
    """Adjudicate one outcome and append it as a child of ``parent``."""
    previous = prev_positions if turn > 1 else {}

    # Build cumulative action history (oldest first) from parent's path.
    # Gives the panel a multi-turn arc to reason about accumulated capex /
    # R&D / brand stocks, not just this turn's snapshot.
    action_history: list[dict] = []
    if parent is not None:
        for n in parent.path_from_root():
            if n.turn < 1:
                continue
            action_history.append({
                "turn": n.turn,
                "actions_detail": dict(n.actions_detail or {}),
                "positions": {sid: dict(p) for sid, p in (n.positions or {}).items()},
                "cash": dict(n.cash or {}),
                "events": list(n.events or []),
            })

    adjudication = _cached_adjudicate(
        ctx, turn=turn, actions_detail=actions_detail,
        previous_positions=previous, cash=child_cash,
        turn_events=events_for_adj, action_history=action_history,
        branch_sig=branch_sig,
    )
    new_positions = adjudication["positions"]
    new_cash = _apply_cash_bookkeeping(
        child_cash, cash_deltas, new_positions,
        position_revenue=(ctx.position_revenue or None),
    )
    shares = {
        sid: _POS_NOMINAL.get(
            new_positions.get(sid, {}).get("position", "contested"), 0.25,
        )
        for sid in ctx.companies
    }

    # Cash driver decomposition. Isomorphic to MBB control-team P&L:
    # starting − action_cost + events_delta + position_revenue = ending.
    # `position_revenue` is the deterministic mapping from the LLM panel's
    # awarded position tier (MBB equivalent: market team's awarded share ×
    # market size). Calling it "bookkeeping" hid that this is the model's
    # core economic identity, not a residual plug — renamed per consultant
    # review feedback.
    starting_cash = dict((parent.cash if parent is not None else {}) or {})
    cash_attribution: dict = {}
    for sid in ctx.companies:
        start = starting_cash.get(sid, 0.0)
        post_event = child_cash.get(sid, start)
        action_cost = (cash_deltas or {}).get(sid, 0.0) if isinstance(cash_deltas, dict) else 0.0
        end = new_cash.get(sid, post_event)
        events_delta = post_event - start
        # Net of starting + events + action, the remaining delta is the
        # position-tier-based revenue line (MBB share × market_size equivalent).
        position_revenue = end - post_event - action_cost
        cash_attribution[sid] = {
            "starting": round(start, 4),
            "events_delta": round(events_delta, 4),
            "action_cost": round(action_cost, 4),
            "position_revenue": round(position_revenue, 4),
            "ending": round(end, 4),
        }
    node = TreeNode(
        turn=turn,
        state={},
        actions=dict(actions_text),
        actions_detail={sid: dict(d) for sid, d in actions_detail.items()},
        market_eval=adjudication.get("turn_narrative", f"Turn {turn} resolved"),
        shares=shares,
        cash=dict(new_cash),
        deliberations={
            sid: campaigns.get(sid, ("", {}))[1] for sid in ctx.companies
        },
        events=[
            {"id": e["id"], "name": e["name"],
             "label_ko": e.get("label_ko", ""), "category": e.get("category", "")}
            for e in events_for_adj
        ],
        positions={sid: dict(p) for sid, p in new_positions.items()},
        adjudication={
            "interaction_analysis": adjudication.get("interaction_analysis", ""),
            "turn_narrative": adjudication.get("turn_narrative", ""),
            "expert_results": adjudication.get("expert_results", []),
        },
        branch=dict(branch_meta),
        scenario_type="event_tree",
        archetype_name=(strategic_state or {}).get("campaign_name") or ctx.campaign_name,
        strategic_state={ctx.our_side: dict(strategic_state)} if strategic_state else {},
        cash_attribution=cash_attribution,
        parent=parent,
        _our_side=ctx.our_side,
        _sides=ctx.sides,
    )
    parent.children.append(node)
    return node, new_positions, new_cash


def _fork_with_history(
    agents: dict, turn: int, actions_text: dict, actions_detail: dict,
    positions: dict, cash: dict, market_eval: str, events: list[dict],
) -> dict:
    """Fork every agent and feed it this turn's outcome — diverges per branch."""
    history_entry = {
        "turn": turn,
        "actions": dict(actions_text),
        "actions_detail": {sid: dict(d) for sid, d in actions_detail.items()},
        "positions": {sid: dict(p) for sid, p in positions.items()},
        "cash": dict(cash),
        "summary": market_eval,
        "events": [
            {"label_ko": e.get("label_ko", e["name"]),
             "description": e.get("description", "")}
            for e in events
        ],
    }
    forked = {sid: agent.fork() for sid, agent in agents.items()}
    for agent in forked.values():
        agent.update_history(history_entry)
    return forked


# ---------------------------------------------------------------------------
# Recursive expander
# ---------------------------------------------------------------------------

def _expand(
    ctx: _TreeCtx, parent: TreeNode, agents: dict, positions: dict, cash: dict,
    event_state, turn: int, branches_used: int, prior_branch_ids: list[str],
    strategic_state: dict | None = None, branch_sig: str = "",
) -> None:
    """Expand one turn at ``parent``, then recurse into the children.

    Turn 1 has no events (linear). From turn 2 the branch selector may fork the
    turn on a single pivotal event; the two children share the committed
    actions and non-pivotal events.

    ``strategic_state`` carries the per-branch campaign continuity record for
    our side. The reassessment phase (turn ≥ 2) consults it, may pivot the
    campaign, and threads the updated state to children.
    """
    if turn > ctx.max_turns:
        return

    # Strategic reassessment — turn ≥ 2 only. May mutate our agent's strategy.
    if strategic_state is None:
        strategic_state = {
            "campaign_name": ctx.campaign_name,
            "seed_campaign_text": ctx.seed_campaign_text,
            "current_campaign_text": ctx.seed_campaign_text,
            "pivoted_from": None,
            "pivot_turn": None,
            "pivot_trigger": "",
            "pivot_rationale": "",
            "pivot_cost_acknowledged": "",
            "turns_on_current": 1,
            "last_verdict": "initial",
            "last_trigger": "none",
            "last_rationale": "",
        }
    strategic_state = _reassess_our_campaign(
        ctx, parent, agents, strategic_state, turn,
    )
    _reassess_competitor_strategies(ctx, parent, agents, turn)

    has_events = turn > 1
    turn_es = event_state.fork() if has_events else event_state

    # Branch decision — only while branch budget remains.
    bp = None
    if has_events and branches_used < ctx.branch_budget:
        try:
            bp = _cached_decide_branch(
                ctx, turn, positions, turn_es.fired, prior_branch_ids,
                branch_sig,
            )
        except Exception as e:
            logger.warning("Branch decision failed (turn %d): %s", turn, e)

    pivotal_id = None
    pivotal_event = None
    if bp is not None:
        cid = bp.candidate.id
        pivotal_id = cid[4:] if cid.startswith("evt:") else cid
        pivotal_event = next(
            (e for e in ctx.deck if e["id"] == pivotal_id), None,
        )
        if pivotal_event is None:
            logger.warning(
                "Pivotal event %s not found in deck — turn %d stays linear",
                pivotal_id, turn,
            )
            bp = None
            pivotal_id = None

    # Draw non-pivotal events — shared by both children, pivotal withheld.
    non_pivotal: list[dict] = []
    if has_events:
        exclude = {pivotal_id} if pivotal_id else None
        non_pivotal = _draw_events(turn_es, turn, exclude_ids=exclude)

    # Cash entering deliberation — non-pivotal events are this turn's news.
    turn_cash = _inject_event_cash(cash, non_pivotal, ctx.sides)

    # WEGO — one shared commit, consumed by every child of this turn.
    events_prompt = _event_deck_to_prompt(non_pivotal)
    campaigns = _cached_deliberate(
        ctx, agents, turn, ctx.init_shares, turn_cash, ctx.power,
        ctx.companies, ctx.industry, events_prompt, positions,
        branch_sig=branch_sig,
    )
    actions_text, actions_detail, impact_input = _build_actions(
        campaigns, ctx.companies,
    )
    cash_deltas = _resolve_cash_costs(impact_input, ctx.rulebook, ctx.sides)

    # Resolve outcome(s).
    # children_specs: (node, agents, positions, cash, event_state,
    #                  branches_used, prior_branch_ids)
    children_specs: list[tuple] = []
    if bp is not None and pivotal_event is not None:
        label = bp.candidate.label

        # Child A — pivotal event fires.
        es_a = turn_es.fork()
        es_a.fired[pivotal_id] = es_a.fired.get(pivotal_id, 0) + 1
        cash_a = _inject_event_cash(turn_cash, [pivotal_event], ctx.sides)
        events_a = non_pivotal + [pivotal_event]
        meta_a = {
            "event_id": pivotal_id, "variant": "A", "fired": True,
            "label": f"{label} — 발효", "reasoning": bp.reasoning,
        }
        branch_sig_a = branch_sig + f"|T{turn}A:{pivotal_id[:8]}"
        node_a, pos_a, cash_after_a = _make_node(
            ctx, turn, positions, cash_a, cash_deltas,
            actions_text, actions_detail, campaigns, events_a, parent, meta_a,
            strategic_state=strategic_state, branch_sig=branch_sig_a,
        )
        agents_a = _fork_with_history(
            agents, turn, actions_text, actions_detail,
            pos_a, cash_after_a, node_a.market_eval, events_a,
        )

        # Child B — pivotal event does not fire.
        # We still mark the event as exhausted in ARM B's state so it
        # cannot re-draw on later turns — the "muted" decision *consumes*
        # the event's chance for this branch. Without this, the same
        # event re-appears in ARM B's later turns and contaminates the
        # matched counterfactual (regulatory event "doesn't fire" at T2
        # then mysteriously fires again at T4).
        es_b = turn_es.fork()
        max_occ_b = pivotal_event.get("max_occurrences", 1)
        es_b.fired[pivotal_id] = max(es_b.fired.get(pivotal_id, 0), max_occ_b)
        events_b = list(non_pivotal)
        meta_b = {
            "event_id": pivotal_id, "variant": "B", "fired": False,
            "label": f"{label} — 무산", "reasoning": bp.reasoning,
        }
        branch_sig_b = branch_sig + f"|T{turn}B:{pivotal_id[:8]}"
        node_b, pos_b, cash_after_b = _make_node(
            ctx, turn, positions, dict(turn_cash), cash_deltas,
            actions_text, actions_detail, campaigns, events_b, parent, meta_b,
            strategic_state=strategic_state, branch_sig=branch_sig_b,
        )
        agents_b = _fork_with_history(
            agents, turn, actions_text, actions_detail,
            pos_b, cash_after_b, node_b.market_eval, events_b,
        )

        new_prior = prior_branch_ids + [bp.candidate.id]
        children_specs = [
            (node_a, agents_a, pos_a, cash_after_a, es_a,
             branches_used + 1, new_prior, branch_sig_a),
            (node_b, agents_b, pos_b, cash_after_b, es_b,
             branches_used + 1, new_prior, branch_sig_b),
        ]
    else:
        node, new_pos, new_cash = _make_node(
            ctx, turn, positions, dict(turn_cash), cash_deltas,
            actions_text, actions_detail, campaigns, non_pivotal, parent, {},
            strategic_state=strategic_state, branch_sig=branch_sig,
        )
        agents_n = _fork_with_history(
            agents, turn, actions_text, actions_detail,
            new_pos, new_cash, node.market_eval, non_pivotal,
        )
        children_specs = [
            (node, agents_n, new_pos, new_cash, turn_es,
             branches_used, prior_branch_ids, branch_sig),
        ]

    # Recurse — siblings expanded in parallel. Each branch carries its own
    # copy of strategic_state so independent pivots downstream don't collide.
    if turn + 1 > ctx.max_turns:
        return
    if len(children_specs) == 1:
        spec = children_specs[0]
        _expand(ctx, spec[0], spec[1], spec[2], spec[3], spec[4],
                turn + 1, spec[5], spec[6],
                strategic_state=dict(strategic_state),
                branch_sig=spec[7])
    else:
        with ThreadPoolExecutor(max_workers=len(children_specs)) as executor:
            futures = [
                executor.submit(
                    _expand, ctx, spec[0], spec[1], spec[2], spec[3], spec[4],
                    turn + 1, spec[5], spec[6],
                    dict(strategic_state),
                    spec[7],
                )
                for spec in children_specs
            ]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.warning("Subtree expansion failed: %s", e)


# ---------------------------------------------------------------------------
# Per-tree checkpoint serialization (branch-aware, recursive)
# ---------------------------------------------------------------------------

def _node_to_dict(node: TreeNode) -> dict:
    return {
        "turn": node.turn,
        "actions": dict(node.actions),
        "actions_detail": dict(node.actions_detail),
        "market_eval": node.market_eval,
        "shares": dict(node.shares),
        "cash": dict(node.cash),
        "deliberations": dict(node.deliberations),
        "events": list(node.events),
        "positions": dict(node.positions),
        "adjudication": dict(node.adjudication),
        "branch": dict(node.branch),
        "scenario_type": node.scenario_type,
        "archetype_name": node.archetype_name,
        "strategic_state": dict(node.strategic_state) if node.strategic_state else {},
        "cash_attribution": dict(node.cash_attribution) if node.cash_attribution else {},
        "children": [_node_to_dict(c) for c in node.children],
    }


def _serialize_subtree(anchor: TreeNode) -> dict:
    """Serialize a job's whole tree (the anchor's children + descendants)."""
    return {"children": [_node_to_dict(c) for c in anchor.children]}


def _dict_to_node(
    data: dict, parent: TreeNode, our_side: str, sides: list,
) -> TreeNode:
    node = TreeNode(
        turn=data["turn"],
        state={},
        actions=dict(data.get("actions", {})),
        actions_detail=dict(data.get("actions_detail", {})),
        market_eval=data.get("market_eval", ""),
        shares=dict(data.get("shares", {})),
        cash=dict(data.get("cash", {})),
        deliberations=dict(data.get("deliberations", {})),
        events=list(data.get("events", [])),
        positions=dict(data.get("positions", {})),
        adjudication=dict(data.get("adjudication", {})),
        branch=dict(data.get("branch", {})),
        scenario_type=data.get("scenario_type", "event_tree"),
        archetype_name=data.get("archetype_name", ""),
        strategic_state=dict(data.get("strategic_state", {})),
        cash_attribution=dict(data.get("cash_attribution", {})),
        parent=parent,
        _our_side=our_side,
        _sides=sides,
    )
    for child_data in data.get("children", []):
        node.children.append(
            _dict_to_node(child_data, node, our_side, sides),
        )
    return node


def _deserialize_subtree(data: dict, ctx) -> TreeNode:
    """Rebuild a job's tree onto a fresh detached anchor."""
    from .simulation_setup import create_root_node

    anchor = create_root_node(ctx)
    for child_data in data.get("children", []):
        anchor.children.append(
            _dict_to_node(child_data, anchor, ctx.our_side, ctx.all_side_ids),
        )
    return anchor


# ---------------------------------------------------------------------------
# M-run orchestration
# ---------------------------------------------------------------------------

def run_event_tree_simulation(
    scenario: dict,
    strategy: str,
    our_side: str,
    llm,
    max_turns: int = 3,
    our_branch_factor: int = 2,
    n_runs: int = 5,
    branch_budget: int = 2,
    callback=None,
    cache_dir=None,
    regenerate: bool = False,
) -> TreeResult:
    """Event-branch tree simulation: M Monte Carlo trees per campaign.

    Each (campaign, trial) pair builds one event-branch tree. Trees share the
    deck and competitor strategies but use independent stochastic seeds, so
    competitor behaviour and adjudication noise vary across trials while a
    branch's sibling pair stays a matched event counterfactual.
    """
    from .simulation_setup import (
        build_agent_factory,
        build_simulation_context,
        create_root_node,
        load_or_generate_buckets,
        load_or_generate_run_inputs,
    )
    from .scenario_cache import load_cached, save_cache

    ctx = build_simulation_context(
        scenario, strategy, our_side, llm, max_depth_or_turns=max_turns,
        cache_dir=cache_dir, regenerate=regenerate, callback=callback,
    )
    our_side = ctx.our_side

    event_deck, competitor_strategies = load_or_generate_run_inputs(
        ctx, scenario, llm, regenerate,
    )
    make_agent = build_agent_factory(ctx, scenario, llm)
    buckets = load_or_generate_buckets(
        ctx, strategy, llm, our_branch_factor, regenerate, callback,
    )

    root = create_root_node(ctx)
    init_positions = _initial_positions(ctx.init_shares, ctx.companies)

    # Build the campaign catalog once — used both for jobs and as the pivot
    # pool the reassessment phase can choose from.
    campaign_texts: dict[str, str] = {}
    available_campaigns: list[str] = []
    for bucket in buckets:
        name = bucket.get("name", "default")
        direction = bucket.get("direction", strategy)
        text = (
            f"{strategy}\n[캠페인: {name}] {direction}\n"
            f"[Theory of winning] {bucket.get('theory_of_winning', '')}"
        )
        campaign_texts[name] = text
        if name not in available_campaigns:
            available_campaigns.append(name)

    # Jobs: one event tree per (campaign, trial).
    jobs: list[tuple] = []
    for name in available_campaigns:
        campaign_strategy = campaign_texts[name]
        for run_idx in range(n_runs):
            jobs.append((name, campaign_strategy, run_idx))

    total = len(jobs)
    if callback:
        callback(f"Building {total} event-tree trial(s)...", 0.1)

    progress_lock = Lock()
    done = [0]

    def _run_job(job: tuple) -> tuple:
        campaign_name, campaign_strategy, run_idx = job
        ckpt_key = f"{ctx.paths_hash}_{campaign_name}_{run_idx}"

        if not regenerate:
            cached = load_cached(ckpt_key, "evt_tree", ctx.cache_dir)
            if cached:
                logger.info(
                    "Event-tree trial from cache: %s/%d", campaign_name, run_idx,
                )
                return (campaign_name, run_idx, _deserialize_subtree(cached, ctx))

        agents = {our_side: make_agent(our_side, campaign_strategy)}
        for sid in ctx.all_side_ids:
            if sid != our_side:
                agents[sid] = make_agent(sid, competitor_strategies.get(sid, ""))

        anchor = create_root_node(ctx)
        tctx = _TreeCtx(
            companies=ctx.companies, our_side=our_side, sides=ctx.all_side_ids,
            industry=ctx.industry, structural_context=ctx.structural_context,
            rulebook=ctx.rulebook, deck=event_deck, llm=llm,
            max_turns=max_turns, branch_budget=branch_budget,
            campaign_name=campaign_name, power=ctx.power,
            init_shares=ctx.init_shares,
            available_campaigns=list(available_campaigns),
            campaign_texts=dict(campaign_texts),
            seed_campaign_text=campaign_strategy,
            cache_dir=ctx.cache_dir,
            position_revenue=dict(scenario.get("position_revenue") or {}),
            environment=scenario.get("trigger_event", "") or "",
        )
        # NEVER use Python's built-in hash() for cross-process determinism —
        # PYTHONHASHSEED is randomized per process by default, so the same
        # string yields a different int each run. That made the event-deck
        # RNG seed non-reproducible, which propagated into per-turn cash and
        # invalidated every downstream cache (deliberate/adjudicate) on every
        # probe rerun. Use hashlib for a stable integer seed instead.
        _seed_str = f"{ctx.paths_hash}_{campaign_name}_{run_idx}"
        _seed_int = int(
            hashlib.sha256(_seed_str.encode("utf-8")).hexdigest()[:16], 16,
        )
        event_state = create_event_deck_state(event_deck, _seed_int)
        _expand(
            tctx, anchor, agents, init_positions, dict(ctx.init_cash),
            event_state, turn=1, branches_used=0, prior_branch_ids=[],
        )
        save_cache(ckpt_key, "evt_tree", _serialize_subtree(anchor), ctx.cache_dir)
        return (campaign_name, run_idx, anchor)

    results: list[tuple] = []
    with ThreadPoolExecutor(max_workers=min(total, 4)) as executor:
        futures = {executor.submit(_run_job, job): job for job in jobs}
        for future in as_completed(futures):
            job = futures[future]
            try:
                results.append(future.result())
            except Exception as e:
                logger.warning("Event-tree trial failed (%s): %s", job[0], e)
            with progress_lock:
                done[0] += 1
                if callback:
                    callback(
                        f"Event-tree trials: {done[0]}/{total}",
                        0.1 + 0.9 * (done[0] / total),
                    )

    # Attach every trial's tree to the shared root.
    for _campaign_name, _run_idx, anchor in results:
        for child in anchor.children:
            child.parent = root
            root.children.append(child)

    if callback:
        callback("Event-tree simulation complete", 1.0)

    return TreeResult(
        strategy=strategy,
        our_side=our_side,
        companies=ctx.companies,
        root=root,
        depth=max_turns,
        rulebook=ctx.rulebook,
        non_actors=ctx.non_actors,
        side_personas=ctx.side_personas,
        closed_market=ctx.closed_market,
        simulation_constraints=scenario.get("simulation_constraints", []),
    )


def summarize_tree(result: TreeResult) -> str:
    """Human-readable structure summary — verification aid for Phase 2."""
    lines: list[str] = []
    roots = result.root.children
    leaves = result.leaves
    branch_nodes: list[TreeNode] = []

    def _walk(node: TreeNode) -> None:
        if node.branch:
            branch_nodes.append(node)
        for child in node.children:
            _walk(child)

    for child in roots:
        _walk(child)

    lines.append(f"Trees attached : {len(roots)} turn-1 root(s)")
    lines.append(f"Total leaves   : {len(leaves)}")
    lines.append(f"Branch nodes   : {len(branch_nodes)}")
    if branch_nodes:
        lines.append("Branches:")
        for bn in branch_nodes:
            b = bn.branch
            lines.append(
                f"  T{bn.turn} [{bn.archetype_name}] "
                f"{b.get('variant', '?')} {b.get('label', '')}"
            )

    def _render(node: TreeNode, indent: str) -> None:
        tag = ""
        if node.branch:
            tag = f" «{node.branch.get('variant', '?')}: {node.branch.get('label', '')}»"
        our = node.positions.get(result.our_side, {})
        pos = our.get("position", "?") if isinstance(our, dict) else "?"
        lines.append(f"{indent}T{node.turn} {result.our_company}={pos}{tag}")
        for child in node.children:
            _render(child, indent + "  ")

    lines.append("Structure:")
    for child in roots:
        _render(child, "  ")
    return "\n".join(lines)
