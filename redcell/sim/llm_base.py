"""Base LLM adapter with circuit breaker pattern and optional disk cache.

Circuit breaker states: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing recovery).
After MAX_FAILURES consecutive errors, the circuit opens and all calls raise
CircuitOpenError until the reset timeout expires.

Disk cache: when ``cache_dir`` is set, request/response pairs are stored on disk
keyed by a hash of (model, system, user, temperature, enable_thinking). Subsequent
calls with the same inputs return the cached response instantly. Useful for
iterating on probe scripts without re-running expensive LLM calls.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CircuitOpenError(Exception):
    """Raised when the circuit breaker is open."""


class BaseLLMAdapter(ABC):
    """Base adapter with circuit breaker and retry logic."""

    def __init__(self, max_failures: int = 10, reset_timeout: float = 120.0, cache_dir: str | None = None):
        self._failure_count = 0
        self._max_failures = max_failures
        self._state = "CLOSED"
        self._last_failure_time: float = 0
        self._reset_timeout = reset_timeout
        self._cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    def _cache_key(self, system: str, user: str, temperature: float, **kwargs) -> str:
        enable_thinking = kwargs.get("enable_thinking", None)
        blob = json.dumps({
            "model": self.model_name,
            "system": system,
            "user": user,
            "temperature": temperature,
            "enable_thinking": enable_thinking,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode()).hexdigest()[:16]

    def _cache_get(self, key: str) -> str | None:
        if not self._cache_dir:
            return None
        path = os.path.join(self._cache_dir, f"{key}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            logger.debug("Cache HIT: %s", key)
            return data["response"]
        return None

    def _cache_put(self, key: str, system: str, user: str, response: str) -> None:
        if not self._cache_dir:
            return
        path = os.path.join(self._cache_dir, f"{key}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"system": system, "user": user, "response": response}, f, ensure_ascii=False, indent=2)

    def complete(
        self,
        system: str,
        user: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        **kwargs,
    ) -> str:
        cache_key = self._cache_key(system, user, temperature, **kwargs)
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached

        if self._state == "OPEN":
            if time.time() - self._last_failure_time > self._reset_timeout:
                self._state = "HALF_OPEN"
                logger.info("Circuit half-open for %s, testing recovery", self.model_name)
            else:
                raise CircuitOpenError(f"Circuit open for {self.model_name}")

        try:
            result = self._do_complete(system, user, temperature=temperature, max_tokens=max_tokens, **kwargs)
            self._on_success()
            self._cache_put(cache_key, system, user, result)
            return result
        except CircuitOpenError:
            raise
        except Exception as e:
            self._on_failure(e)
            raise

    def _on_success(self) -> None:
        if self._state == "HALF_OPEN":
            logger.info("Circuit recovered for %s", self.model_name)
        self._failure_count = 0
        self._state = "CLOSED"

    def _on_failure(self, error: Exception) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        logger.warning(
            "LLM failure %d/%d for %s: %s",
            self._failure_count, self._max_failures, self.model_name, error,
        )
        if self._failure_count >= self._max_failures:
            self._state = "OPEN"
            logger.error("Circuit OPEN for %s after %d failures", self.model_name, self._max_failures)

    @abstractmethod
    def _do_complete(
        self, system: str, user: str, temperature: float = 0.3, max_tokens: int = 1024, **kwargs,
    ) -> str: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    @property
    @abstractmethod
    def model_name(self) -> str: ...

    @property
    @abstractmethod
    def cost_tier(self) -> str: ...
