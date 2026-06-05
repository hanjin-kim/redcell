"""Vendored simulation engine (extracted from strategyforge).

Single-source-of-truth for redcell's multi-LLM C-suite deliberation,
adjudication panel, event deck, and rulebook generation. Originally
authored as part of strategyforge; vendored into redcell so this package
has zero dependencies on the parent project.

Public entry point: ``run_event_tree_simulation`` (used by
``redcell.engine.run_linear_scenario`` with branch_budget=0).
"""
from .event_tree import run_event_tree_simulation

__all__ = ["run_event_tree_simulation"]
