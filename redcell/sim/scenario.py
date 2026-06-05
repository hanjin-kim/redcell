"""Scenario and company models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MarketSegment(BaseModel, frozen=True):
    """A market segment node (replaces HexCoord from wargame)."""

    industry: str
    segment: str
    region: str = "global"

    @property
    def key(self) -> str:
        return f"{self.industry}:{self.segment}:{self.region}"


class CompanyProfile(BaseModel, frozen=True):
    """Static company information."""

    id: str
    name: str
    industry: str
    market_cap_tier: str = "large"  # startup, mid, large, mega
    strengths: list[str] = []
    weaknesses: list[str] = []


class BusinessUnitConfig(BaseModel, frozen=True):
    """Initial state of a business unit within a company."""

    id: str
    name: str
    segment: MarketSegment
    market_share: float = Field(ge=0.0, le=1.0)
    revenue_index: float = 1.0
    competitive_power: float = 50.0
    brand_loyalty: float = 50.0
    r_and_d: float = Field(default=0.5, ge=0.0, le=1.0)
    cash_reserves: float = Field(default=0.5, ge=0.0, le=1.0)


class CommanderConfig(BaseModel, frozen=True):
    """Agent configuration for a commander."""

    id: str
    name: str
    role: str  # "CEO", "VP", "BU_Head"
    unit_id: str = ""
    personality: dict[str, float] = {}  # aggression, risk_tolerance, innovation_focus


class Side(BaseModel, frozen=True):
    """One side in the simulation (a company/alliance)."""

    id: str
    company: CompanyProfile
    business_units: list[BusinessUnitConfig] = []
    commanders: list[CommanderConfig] = []


class Scenario(BaseModel, frozen=True):
    """Complete simulation scenario."""

    name: str
    description: str
    domain: str = "competitive"
    industry: str
    time_unit: str = "quarter"  # quarter, half_year, year
    time_horizon: int = 12  # number of turns
    sides: list[Side]
    market_segments: list[MarketSegment] = []
    market_connections: dict[str, list[str]] = {}
    initial_conditions: dict = {}
    trigger_event: str = ""
