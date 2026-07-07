"""In-memory batch/rate/cache utilities."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Process items in fixed-size async batches with retry."""

    @staticmethod
    async def process_batch(
        items: List[Any],
        processor: Callable[[Any], Any],
        batch_size: int = 10,
        delay: float = 0.1,
        max_retries: int = 3,
    ) -> List[Any]:
        results: List[Any] = []
        failed: List[Tuple[int, Any]] = []

        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            outcomes = await asyncio.gather(
                *(processor(item) for item in batch), return_exceptions=True
            )
            for offset, outcome in enumerate(outcomes):
                if isinstance(outcome, Exception):
                    failed.append((len(results), batch[offset]))
                    results.append(None)
                else:
                    results.append(outcome)
            if i + batch_size < len(items):
                await asyncio.sleep(delay)

        if failed and max_retries > 0:
            logger.warning("Retrying %d failed items", len(failed))
            retry_results = await BatchProcessor.process_batch(
                [item for _, item in failed],
                processor,
                batch_size,
                delay,
                max_retries - 1,
            )
            for (idx, _), retry_value in zip(failed, retry_results):
                results[idx] = retry_value

        return results


class CacheManager:
    """Simple in-memory TTL cache."""

    def __init__(self, default_ttl: int = 60) -> None:
        self._cache: Dict[str, Tuple[Any, float, int]] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if not entry:
            return None
        value, timestamp, ttl = entry
        if time.time() - timestamp < ttl:
            return value
        self._cache.pop(key, None)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self._cache[key] = (value, time.time(), ttl or self._default_ttl)

    def clear(self, key: Optional[str] = None) -> None:
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()