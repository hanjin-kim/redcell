"""Company agent: wraps DeliberationV2 for any company in a Markov game.

Each company gets an independent agent that:
1. Observes current market state
2. Internally anticipates competitor moves (game-theoretic reasoning)
3. Produces a campaign (list of actions with action_type + intensity)

The agent is parameterized by side_id, strategy, and persona — it can represent
any company in the simulation, not just "our side".
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .state_adapter import (
    SimulationStateAdapter,
    _build_delib_dict,
)

if TYPE_CHECKING:
    from .deliberation_v2 import DeliberationV2

logger = logging.getLogger(__name__)


class CompanyAgent:
    """Independent decision-making agent for one company.

    Wraps DeliberationV2 to produce campaigns given current state.
    Each agent deliberates independently — competitor anticipation is
    inherent in the C-suite deliberation prompt, not externally injected.
    """

    def __init__(
        self,
        side_id: str,
        company_name: str,
        deliberator: DeliberationV2,
        strategy: str = "",
    ) -> None:
        self.side_id = side_id
        self.company_name = company_name
        self._deliberator = deliberator
        self._strategy = strategy

    def deliberate(
        self,
        turn: int,
        shares: dict[str, float],
        cash: dict[str, float],
        power: dict[str, float],
        companies: dict[str, str],
        industry: str,
        current_events: str = "",
        positions: dict[str, dict] | None = None,
    ) -> tuple[str, dict]:
        """Produce a campaign for this turn given current state.

        Returns (action_str, delib_dict) where delib_dict contains:
        - actions_payload: [{action_type, intensity, text}, ...]
        - phase1/phase2/phase3: full deliberation trace
        - decision/reasoning: summary
        """
        adapter = SimulationStateAdapter(
            turn=turn,
            shares=shares,
            cash=cash,
            power=power,
            companies=companies,
            industry=industry,
            positions=positions,
        )

        self._deliberator._strategic_direction[self.side_id] = self._strategy
        if current_events:
            self._deliberator._current_events = current_events

        actions, phases = self._deliberator.deliberate_side(self.side_id, adapter)

        if not actions:
            logger.warning("Agent %s produced no actions at turn %d", self.side_id, turn)
            return "", {}

        action_str = "; ".join(
            a.strategy_description or a.action_type for a in actions
        )
        delib = _build_delib_dict(actions, phases)
        return action_str, delib

    def update_history(self, turn_snapshot: dict) -> None:
        """Feed a completed turn's result into the deliberator's history.

        Expected format: {turn, actions: {side: str}, shares: {side: float}, summary: str}
        """
        current = list(self._deliberator._turn_history or [])
        current.append(turn_snapshot)
        self._deliberator.set_turn_history(current)

    def fork(self) -> CompanyAgent:
        """Thread-safe copy sharing the LLM client."""
        return CompanyAgent(
            side_id=self.side_id,
            company_name=self.company_name,
            deliberator=self._deliberator.fork(),
            strategy=self._strategy,
        )
