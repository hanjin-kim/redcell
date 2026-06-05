"""Action models and types."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .scenario import MarketSegment


# Known action categories for fallback/analytics (not an enum — just constants)
KNOWN_CATEGORIES = {
    "PRICE_CUT", "PRICE_INCREASE", "PRODUCT_LAUNCH", "MARKETING_BLITZ",
    "RD_INVEST", "MARKET_ENTRY", "MARKET_EXIT", "ACQUISITION",
    "PARTNERSHIP", "DEFEND_POSITION", "HOLD",
}


class StrategicAction(BaseModel, frozen=True):
    """A strategic decision made by an agent."""

    action_id: str
    turn: int
    commander_id: str
    entity_id: str  # Business unit performing the action
    action_type: str = "HOLD"  # Coarse category (free string, not enum)
    strategy_description: str = ""  # Natural language: "Launch $25K compact EV with Blade Battery"
    target_segment: MarketSegment | None = None
    target_competitor_id: str | None = None
    intensity: float = Field(default=0.5, ge=0.0, le=1.0)
    investment_amount: float = 0.0
    reasoning: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


# Backward compat: ActionType alias for imports that still reference it
ActionType = str
