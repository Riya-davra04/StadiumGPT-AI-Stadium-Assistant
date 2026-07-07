"""Batch processing utilities for efficiency"""

import asyncio
from typing import List, Any, Callable, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Process items in batches for efficiency"""
    
    @staticmethod
    async def process_batch(
        items: List[Any],
        processor: Callable,
        batch_size: int = 10,
        delay: float = 0.1,
        max_retries: int = 3
    ) -> List[Any]:
        """
        Process items in batches to avoid overwhelming resources
        
        Args:
            items: List of items to process
            processor: Async function to process each item
            batch_size: Number of items per batch
            delay: Delay between batches in seconds
            max_retries: Maximum retries for failed items
        """
        results = []
        failed_items = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            tasks = [processor(item) for item in batch]
            
            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                for idx, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        failed_items.append((batch[idx], result))
                        results.append(None)
                    else:
                        results.append(result)
            except Exception as e:
                logger.error(f"Batch processing error: {e}")
            
            # Delay between batches
            if i + batch_size < len(items):
                await asyncio.sleep(delay)
        
        # Retry failed items
        if failed_items and max_retries > 0:
            logger.warning(f"Retrying {len(failed_items)} failed items")
            retry_results = await BatchProcessor.process_batch(
                [item for item, _ in failed_items],
                processor,
                batch_size,
                delay,
                max_retries - 1
            )
            # Replace None results with retry results
            result_idx = 0
            for i, (_, retry_result) in enumerate(zip(failed_items, retry_results)):
                # Find the first None in results and replace it
                for j, r in enumerate(results):
                    if r is None:
                        results[j] = retry_result
                        break
        
        return results
    
    @staticmethod
    async def throttle(
        func: Callable,
        limit: int = 10,
        period: float = 1.0
    ) -> Callable:
        """Throttle function calls to limit rate"""
        semaphore = asyncio.Semaphore(limit)
        
        async def throttled(*args, **kwargs):
            async with semaphore:
                await asyncio.sleep(period / limit)
                return await func(*args, **kwargs)
        
        return throttled

class CacheManager:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 60):
        self.cache = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.utcnow().timestamp() - timestamp < self.default_ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        self.cache[key] = (value, datetime.utcnow().timestamp())
    
    def clear(self, key: Optional[str] = None):
        """Clear cache"""
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()