"""TreeNode and TreeResult data classes for tree-based simulation."""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# TreeNode — N-player capable with backward-compat properties
# ---------------------------------------------------------------------------

@dataclass
class TreeNode:
    """A node in the simulation tree.

    Supports N players via ``shares`` / ``cash`` / ``deliberations`` dicts
    keyed by side_id.  Backward-compat scalar properties (``our_share``,
    ``comp_share``, ``our_action``, ``comp_action``, etc.) are resolved
    using ``_our_side`` stored on each node.
    """

    turn: int
    state: dict
    actions: dict  # side_id -> action description (free text, kept for backward-compat rendering)
    market_eval: str
    shares: dict = field(default_factory=dict)       # side_id -> float (direct pp model)
    rest_share: float = 0.0                          # rest-of-market share
    cash: dict = field(default_factory=dict)          # side_id -> float
    deliberations: dict = field(default_factory=dict) # side_id -> delib dict
    # side_id -> {"text": str, "action_type": str, "intensity": float}
    # Populated by the Impact Factor pipeline; downstream analytics (payoff
    # matrix grouping, pattern detection) should prefer action_type from here
    # over free-text clustering from .actions.
    actions_detail: dict = field(default_factory=dict)
    parent: TreeNode | None = field(default=None, repr=False)
    children: list[TreeNode] = field(default_factory=list)
    scenario_type: str = ""  # "bookend_best", "bookend_worst", "archetype", "montecarlo", ""
    archetype_name: str = ""  # e.g. "Price War", "Alliance Formation"
    share_deltas: dict = field(default_factory=dict)      # side_id -> float (turn-over-turn change)
    pending_effects: list = field(default_factory=list)  # deferred share deltas from delay_turns
    events: list = field(default_factory=list)  # exogenous events injected this turn
    positions: dict = field(default_factory=dict)  # side_id -> {position, momentum, rationale}
    adjudication: dict = field(default_factory=dict)  # interaction_analysis, turn_narrative
    # Event-branch metadata (event-tree migration). Empty on linear/markov nodes.
    # {event_id, variant: "A"|"B", fired: bool, label, reasoning}
    branch: dict = field(default_factory=dict)
    # Per-side strategic state — tracks campaign continuity vs pivot across turns.
    # {side_id: {campaign_name, pivoted_from, pivot_reason, pivot_turn, turns_on_current}}
    # Empty dict on legacy nodes; populated by the reassessment phase.
    strategic_state: dict = field(default_factory=dict)
    # Per-side cash delta decomposition — driver attribution for the Red Team
    # brief. Isomorphic to MBB control-team P&L: starting − action_cost
    # + event_delta + position_revenue = ending. position_revenue is the
    # deterministic mapping from the LLM panel's awarded position tier
    # (MBB equivalent: market team's awarded share × market size). Calling
    # it "bookkeeping" would hide that this is the model's core economic
    # identity, not a residual plug.
    # {side_id: {starting, events_delta, action_cost, position_revenue, ending}}
    cash_attribution: dict = field(default_factory=dict)
    _our_side: str = field(default="", repr=False)
    _sides: list[str] = field(default_factory=list, repr=False)

    # ------------------------------------------------------------------
    # Backward-compat scalar properties
    # ------------------------------------------------------------------

    def _our(self) -> str:
        return self._our_side

    def _comp(self) -> str:
        """First side that is not ours."""
        for s in self._sides:
            if s != self._our_side:
                return s
        # fallback: any key in actions/shares that isn't ours
        for k in list(self.actions.keys()) + list(self.shares.keys()):
            if k != self._our_side:
                return k
        return ""

    @property
    def our_action(self) -> str:
        return self.actions.get(self._our(), "")

    @property
    def comp_action(self) -> str:
        return self.actions.get(self._comp(), "")

    @property
    def our_share(self) -> float:
        return self.shares.get(self._our(), 0.0)

    @property
    def comp_share(self) -> float:
        return self.shares.get(self._comp(), 0.0)

    @property
    def our_cash(self) -> float:
        return self.cash.get(self._our(), 0.0)

    @property
    def comp_cash(self) -> float:
        return self.cash.get(self._comp(), 0.0)

    @property
    def our_deliberation(self) -> dict:
        return self.deliberations.get(self._our(), {})

    @property
    def comp_deliberation(self) -> dict:
        return self.deliberations.get(self._comp(), {})

    # ------------------------------------------------------------------
    # Tree navigation helpers
    # ------------------------------------------------------------------

    def path_from_root(self) -> list[TreeNode]:
        """Return path from root to this node."""
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent
        return list(reversed(path))

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def leaf_count(self) -> int:
        if self.is_leaf:
            return 1
        return sum(c.leaf_count() for c in self.children)

    def all_leaves(self) -> list[TreeNode]:
        if self.is_leaf:
            return [self]
        leaves = []
        for c in self.children:
            leaves.extend(c.all_leaves())
        return leaves


# ---------------------------------------------------------------------------
# TreeResult — N-player metrics with backward-compat properties
# ---------------------------------------------------------------------------

@dataclass
class TreeResult:
    """Complete tree simulation result."""

    strategy: str
    our_side: str
    companies: dict  # side_id -> company_name
    root: TreeNode
    depth: int
    rulebook: dict = field(default_factory=dict)  # Industry competition rulebook
    non_actors: list[str] = field(default_factory=list)  # Phase 2f: per-scenario denylist of non-player entities
    side_personas: dict = field(default_factory=dict)  # side_id -> {management_style, strategic_tendency, aggression}
    closed_market: bool = False
    simulation_constraints: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Backward-compat scalar properties
    # ------------------------------------------------------------------

    @property
    def our_company(self) -> str:
        return self.companies.get(self.our_side, self.our_side)

    @property
    def comp_company(self) -> str:
        for k, v in self.companies.items():
            if k != self.our_side:
                return v
        return "Competitor"

    @property
    def branch_factor(self) -> int:
        """Not applicable for N-player scenario-fan approach."""
        return 0

    # ------------------------------------------------------------------
    # Tree accessors
    # ------------------------------------------------------------------

    @property
    def leaves(self) -> list[TreeNode]:
        return self.root.all_leaves()

    # ------------------------------------------------------------------
    # Backward-compat metrics (2-player semantics: our_share vs comp)
    # ------------------------------------------------------------------

    @property
    def win_rate(self) -> float:
        """Fraction of leaves where our share is strictly highest among all sides."""
        leaves = self.leaves
        if not leaves:
            return 0.0
        wins = sum(
            1 for l in leaves
            if l.shares and l.our_share >= max(l.shares.values())
        )
        return wins / len(leaves)

    @property
    def rank_distribution(self) -> dict:
        """Fraction of leaves at each rank position for our side.

        Returns e.g. {1: 0.4, 2: 0.35, 3: 0.25} for a 3-player game.
        """
        leaves = self.leaves
        if not leaves:
            return {}
        rank_counts: dict[int, int] = {}
        for leaf in leaves:
            if not leaf.shares:
                continue
            sorted_shares = sorted(leaf.shares.values(), reverse=True)
            our_val = leaf.shares.get(self.our_side, 0.0)
            rank = sorted_shares.index(our_val) + 1
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        return {rank: count / len(leaves) for rank, count in rank_counts.items()}

    @property
    def improvement_rate(self) -> float:
        """Fraction of leaves where our share improved vs the root."""
        leaves = self.leaves
        if not leaves:
            return 0.0
        initial = self.root.our_share
        improved = sum(1 for l in leaves if l.our_share > initial)
        return improved / len(leaves)

    @property
    def mean_share(self) -> float:
        shares = [l.our_share for l in self.leaves]
        return sum(shares) / len(shares) if shares else 0.0

    @property
    def share_range(self) -> tuple:
        shares = [l.our_share for l in self.leaves]
        return (min(shares), max(shares)) if shares else (0.0, 0.0)
