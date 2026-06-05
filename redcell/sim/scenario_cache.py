"""Scenario-level cache for rulebook, archetypes, and paths.

Tier 1 (setup): rulebook + archetypes + non_actors — keyed by scenario hash.
Tier 2 (paths): bookend + archetype paths — keyed by scenario hash + strategy + depth.

Cache invalidation is hash-based: any change to the scenario YAML content
invalidates the setup cache, and any strategy/depth change invalidates paths.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path(".redcell_cache")


def _compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def scenario_hash(scenario: dict) -> str:
    raw = json.dumps(scenario, sort_keys=True, default=str, ensure_ascii=False)
    return _compute_hash(raw)


def paths_hash(scenario: dict, strategy: str, max_depth: int) -> str:
    raw = json.dumps(scenario, sort_keys=True, default=str, ensure_ascii=False)
    raw += f"\n__strategy={strategy}\n__max_depth={max_depth}"
    return _compute_hash(raw)


def sim_result_hash(scenario: dict, strategy: str, turns: int, campaigns: int, runs: int) -> str:
    raw = json.dumps(scenario, sort_keys=True, default=str, ensure_ascii=False)
    raw += f"\n__strategy={strategy}\n__turns={turns}\n__campaigns={campaigns}\n__runs={runs}"
    return _compute_hash(raw)


def load_cached(key: str, tier: str, cache_dir: Path = DEFAULT_CACHE_DIR) -> dict | None:
    path = cache_dir / f"{tier}_{key}.json"
    import os, sys
    debug = os.environ.get("STRATEGYFORGE_CACHE_DEBUG")
    if not path.exists():
        if debug:
            print(f"[CACHE MISS] {tier}/{key}", file=sys.stderr, flush=True)
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if debug:
            print(f"[CACHE HIT]  {tier}/{key}", file=sys.stderr, flush=True)
        logger.info("Cache hit: %s (key=%s)", tier, key[:8])
        return data
    except Exception as e:
        logger.warning("Cache read failed for %s: %s", tier, e)
        return None


def save_cache(key: str, tier: str, data: dict, cache_dir: Path = DEFAULT_CACHE_DIR) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{tier}_{key}.json"
    try:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        logger.info("Cache saved: %s (key=%s)", tier, key[:8])
    except Exception as e:
        logger.warning("Cache write failed for %s: %s", tier, e)
