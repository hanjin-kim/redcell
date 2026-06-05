"""Shared setup logic for tree and Markov simulators.

Extracts common initialization code: state extraction, structural context,
rulebook caching, guard blocks, side personas, root node creation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .tree_models import TreeNode, TreeResult
from .rulebook import _generate_rulebook, _rulebook_to_prompt
from .state import _extract_initial_state
from .scenario_cache import (
    scenario_hash, paths_hash, load_cached, save_cache,
)

logger = logging.getLogger(__name__)


@dataclass
class SimulationContext:
    """All shared state produced by the setup phase."""

    companies: dict[str, str]
    all_side_ids: list[str]
    init_shares: dict[str, float]
    init_cash: dict[str, float]
    init_rest_share: float
    power: dict[str, float]
    sides_data: list[dict]
    industry: str
    structural_context: str
    rulebook: dict
    non_actors: list[str]
    side_personas: dict
    closed_market: bool
    our_side: str
    strategy: str
    cache_dir: Path
    scenario_hash: str
    paths_hash: str


def build_simulation_context(
    scenario: dict,
    strategy: str,
    our_side: str,
    llm: Any,
    max_depth_or_turns: int,
    cache_dir: Path | None = None,
    regenerate: bool = False,
    callback=None,
) -> SimulationContext:
    """Build the full shared simulation context (state, rulebook, guards, personas)."""

    companies, init_shares, init_cash, power, sides_data, init_rest_share = (
        _extract_initial_state(scenario)
    )
    all_side_ids = list(companies.keys())
    industry = scenario.get("industry", "unknown")
    closed_market = scenario.get("closed_market", False)

    # Resolve our_side: accept either side_id ("side_a") or company name ("SK Hynix")
    if our_side not in companies:
        name_to_id = {name.lower(): sid for sid, name in companies.items()}
        resolved = name_to_id.get(our_side.lower())
        if not resolved:
            for sid, name in companies.items():
                if our_side.lower() in name.lower() or name.lower() in our_side.lower():
                    resolved = sid
                    break
        if resolved:
            our_side = resolved
        else:
            raise ValueError(
                f"Cannot resolve our_side='{our_side}'. "
                f"Available: {list(companies.values())} (ids: {all_side_ids})"
            )

    # Structural context
    structural_context = _build_structural_context(scenario, sides_data)

    # Cache layer
    _cache_dir = Path(cache_dir) if cache_dir else Path(".redcell_cache")
    _s_hash = scenario_hash(scenario)
    _p_hash = paths_hash(scenario, strategy, max_depth_or_turns)

    # Rulebook (from cache or generated)
    setup_cached = None if regenerate else load_cached(_s_hash, "setup", _cache_dir)

    if setup_cached:
        if callback:
            callback("Rulebook loaded from cache", 0.0)
        rulebook = setup_cached["rulebook"]
        non_actors = setup_cached.get("non_actors", [])
    else:
        if callback:
            callback("Generating industry rulebook...", 0.0)
        rulebook = _generate_rulebook(llm, scenario, our_side)
        from .state import _generate_non_actor_list
        non_actors = _generate_non_actor_list(llm, scenario, companies)

    if "intensity_jitter" in scenario and "intensity_jitter" not in rulebook:
        rulebook["intensity_jitter"] = scenario["intensity_jitter"]

    # Append rulebook to structural context
    rulebook_prompt = _rulebook_to_prompt(rulebook)
    if rulebook_prompt:
        structural_context += f"\n\n{rulebook_prompt}"

    # Guard block
    guard_block = _build_guard_block(companies, our_side, non_actors)
    structural_context += "\n\n" + guard_block

    # Simulation constraints
    sim_constraints = scenario.get("simulation_constraints", [])
    if sim_constraints:
        constraint_lines = ["SIMULATION CONSTRAINTS (hard rules — violations invalidate the scenario):"]
        for sc in sim_constraints:
            constraint_lines.append(f"- {sc}")
        structural_context += "\n\n" + "\n".join(constraint_lines)

    # Side personas
    side_personas = _extract_side_personas(sides_data)

    return SimulationContext(
        companies=companies,
        all_side_ids=all_side_ids,
        init_shares=init_shares,
        init_cash=init_cash,
        init_rest_share=init_rest_share,
        power=power,
        sides_data=sides_data,
        industry=industry,
        structural_context=structural_context,
        rulebook=rulebook,
        non_actors=non_actors,
        side_personas=side_personas,
        closed_market=closed_market,
        our_side=our_side,
        strategy=strategy,
        cache_dir=_cache_dir,
        scenario_hash=_s_hash,
        paths_hash=_p_hash,
    )


def save_setup_cache(ctx: SimulationContext, extra: dict | None = None) -> None:
    """Save setup cache (rulebook + non_actors + extra data)."""
    data = {
        "rulebook": ctx.rulebook,
        "non_actors": ctx.non_actors,
    }
    if extra:
        data.update(extra)
    save_cache(ctx.scenario_hash, "setup", data, ctx.cache_dir)


def create_root_node(ctx: SimulationContext) -> TreeNode:
    """Create the turn-0 root TreeNode from simulation context."""
    return TreeNode(
        turn=0,
        state={},
        actions={
            sid: ctx.strategy if sid == ctx.our_side else "(initial)"
            for sid in ctx.all_side_ids
        },
        market_eval="Starting positions",
        shares=dict(ctx.init_shares),
        rest_share=ctx.init_rest_share,
        cash=dict(ctx.init_cash),
        _our_side=ctx.our_side,
        _sides=ctx.all_side_ids,
    )


def load_or_generate_run_inputs(
    ctx: SimulationContext, scenario: dict, llm: Any, regenerate: bool = False,
) -> tuple[list[dict], dict[str, str]]:
    """Load (or generate) the event deck + competitor strategies for a run.

    Both are cached together in the setup tier, keyed by scenario hash.
    Shared by the Markov and event-tree orchestrators.
    """
    setup_cached = None if regenerate else load_cached(
        ctx.scenario_hash, "setup", ctx.cache_dir,
    )
    needs_save = False

    if setup_cached and "event_deck" in setup_cached:
        event_deck = setup_cached["event_deck"]
    else:
        from .rulebook import _generate_event_deck
        event_deck = _generate_event_deck(llm, scenario, ctx.rulebook)
        needs_save = True

    if setup_cached and "competitor_strategies" in setup_cached:
        competitor_strategies: dict[str, str] = setup_cached["competitor_strategies"]
    else:
        from .strategic_setup import (
            _generate_competitor_strategies,
        )
        competitor_strategies = _generate_competitor_strategies(
            llm, ctx.our_side, ctx.companies, ctx.init_shares, ctx.industry,
            ctx.sides_data, trigger_event=scenario.get("trigger_event", ""),
        )
        needs_save = True

    if needs_save:
        save_setup_cache(ctx, extra={
            "archetypes": [],
            "event_deck": event_deck,
            "competitor_strategies": competitor_strategies,
        })
    return event_deck, competitor_strategies


def build_agent_factory(ctx: SimulationContext, scenario: dict, llm: Any):
    """Return a ``make_agent(side_id, strategy) -> CompanyAgent`` factory.

    Captures C-suite config, guard block, and seed momentum so both
    orchestrators construct agents identically.
    """
    from .deliberation_v2 import DeliberationV2
    from .company_agent import CompanyAgent

    interview_meta = scenario.get("_interview", {})
    csuite_cfg = interview_meta.get("csuite_config", {})
    da_rule = csuite_cfg.get("devils_advocate_rule", "tension_based")
    role_overrides = csuite_cfg.get("role_overrides") or {}
    additional_roles = csuite_cfg.get("additional_roles") or {}
    additional_context = scenario.get("_additional_context", "")
    trigger_event = scenario.get("trigger_event", "")

    guard_lines = (
        ctx.structural_context.split("SIMULATION GUARD RULES")[1].split("\n\n")[0]
        if "SIMULATION GUARD RULES" in ctx.structural_context else ""
    )

    def make_agent(sid: str, agent_strategy: str) -> "CompanyAgent":
        delib = DeliberationV2(
            llm=llm,
            rulebook=ctx.rulebook,
            side_id=sid,
            side_personas=ctx.side_personas,
            devils_advocate_rule=da_rule,
            role_overrides=role_overrides if sid == ctx.our_side else {},
            additional_roles=additional_roles if sid == ctx.our_side else {},
        )
        delib._guard_block = guard_lines
        delib._strategic_direction = {sid: agent_strategy}

        momentum_parts = []
        if trigger_event:
            momentum_parts.append(f"촉발 이벤트: {trigger_event}")
        if additional_context:
            momentum_parts.append(additional_context)
        if momentum_parts:
            delib._seed_momentum = "\n".join(momentum_parts)

        return CompanyAgent(
            side_id=sid,
            company_name=ctx.companies[sid],
            deliberator=delib,
            strategy=agent_strategy,
        )

    return make_agent


def load_or_generate_buckets(
    ctx: SimulationContext, strategy: str, llm: Any, our_branch_factor: int,
    regenerate: bool = False, callback=None,
) -> list[dict]:
    """Load (or generate) the campaign strategic buckets — cached for consistency."""
    import hashlib
    campaign_key = hashlib.sha256(
        f"{ctx.scenario_hash}_{strategy}_{our_branch_factor}".encode()
    ).hexdigest()[:16]
    campaign_cached = None if regenerate else load_cached(
        campaign_key, "campaigns", ctx.cache_dir,
    )

    if campaign_cached and "buckets" in campaign_cached:
        buckets = campaign_cached["buckets"]
        if callback:
            names = ", ".join(b.get("name", "?") for b in buckets)
            callback(f"Campaign options (cached): {names}", 0.1)
        return buckets

    if callback:
        callback("Generating campaign options...", 0.05)

    from .strategic_setup import (
        _extract_common_core,
        _generate_strategic_buckets,
    )

    common_core = _extract_common_core(
        llm, strategy, ctx.our_side, ctx.companies, ctx.init_shares, ctx.industry,
    )
    buckets = _generate_strategic_buckets(
        llm, strategy, ctx.our_side, ctx.companies, ctx.init_shares, ctx.industry,
        common_core, n_buckets=our_branch_factor,
    )
    save_cache(campaign_key, "campaigns", {"buckets": buckets}, ctx.cache_dir)

    if callback:
        names = ", ".join(b.get("name", "?") for b in buckets)
        callback(f"Campaign options: {names}", 0.1)
    return buckets


def _build_structural_context(scenario: dict, sides_data: list[dict]) -> str:
    """Build structural advantages/disadvantages context string."""
    lines = []
    for sd in sides_data:
        name = sd.get("company", {}).get("name", sd["id"])
        for adv in sd.get("structural_advantages", []):
            lines.append(f"  {name} (+): {adv}")
        for dis in sd.get("structural_disadvantages", []):
            lines.append(f"  {name} (-): {dis}")
    additional_context = scenario.get("_additional_context", "")
    result = "\n".join(lines)
    if additional_context:
        result += f"\n\nRECENT CONTEXT (treat as ground truth):\n{additional_context}"
    return result


def _build_guard_block(
    companies: dict[str, str], our_side: str, non_actors: list[str]
) -> str:
    """Build the simulation guard rules string."""
    player_names = list(companies.values())
    our_company = companies[our_side]
    guard_lines = [
        "SIMULATION GUARD RULES (apply to ALL output fields):",
        f"SCOPED ACTORS: Only these entities may be the SUBJECT of an action: {', '.join(player_names)}.",
        "All other entities (partners, suppliers, products, regulators, standards) "
        "are mechanisms — they may appear as objects or context but NEVER as the "
        "grammatical subject performing a strategic action.",
    ]
    if non_actors:
        guard_lines.append(
            "NON-ACTOR ENTITIES (must NOT be action subjects): "
            + ", ".join(non_actors[:40])
        )
    guard_lines.extend([
        f"ORIENTATION: {our_company} is '우리' (our side). NEVER refer to "
        f"{our_company} as '경쟁사' or 'competitor'. Only companies other than "
        f"{our_company} are 경쟁사.",
        "PROPER NOUNS: Every proper noun appearing in the context above MUST be "
        "copied CHARACTER-FOR-CHARACTER into your output.",
    ])
    return "\n".join(guard_lines)


def _extract_side_personas(sides_data: list[dict]) -> dict:
    """Extract persona dicts from commander data."""
    side_personas: dict = {}
    for sd in sides_data:
        sid = sd["id"]
        cmds = sd.get("commanders", [])
        cmd = cmds[0] if cmds else {}
        personality = cmd.get("personality", {}) or {}
        aggression = personality.get("aggression") if personality else cmd.get("aggression")
        risk_tolerance = personality.get("risk_tolerance") if personality else cmd.get("risk_tolerance")
        leadership_constraints = personality.get("leadership_constraints", []) if personality else []
        if cmd.get("management_style") or cmd.get("ceo_profile") or aggression is not None:
            side_personas[sid] = {
                "management_style": cmd.get("management_style", ""),
                "ceo_profile": cmd.get("ceo_profile", ""),
                "strategic_tendency": cmd.get("strategic_tendency", ""),
                "aggression": aggression,
                "risk_tolerance": risk_tolerance,
                "leadership_constraints": leadership_constraints,
            }
    return side_personas
