#!/usr/bin/env python3
"""
BOB Parallel Extractor v4.3.0

Extract multiple businesses concurrently using asyncio.
Uses multiple browser instances for faster extraction.

⚠️ WARNING: Use responsibly! Parallel extraction is faster but:
- Uses more memory (~50MB per browser)
- May trigger rate limiting from Google
- Default is 2 parallel browsers (conservative)

Usage:
    from bob.utils.parallel_extractor import ParallelExtractor
    
    extractor = ParallelExtractor(max_concurrent=2)
    results = await extractor.extract_batch(urls)
"""

import asyncio
import time
import psutil
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from bob.extractors.playwright_optimized import PlaywrightExtractorOptimized


@dataclass
class ParallelConfig:
    """Configuration for parallel extraction."""
    max_concurrent: int = 2           # Max parallel browsers (conservative default)
    delay_between_starts: float = 3.0 # Seconds between starting each browser
    memory_limit_percent: float = 80  # Abort if memory usage exceeds this
    include_reviews: bool = True
    max_reviews: int = 5
    headless: bool = True
    
    def __post_init__(self):
        # Safety limits
        if self.max_concurrent > 5:
            print(f"⚠️ Reducing max_concurrent from {self.max_concurrent} to 5 (safety limit)")
            self.max_concurrent = 5


class ParallelExtractor:
    """
    Extract multiple businesses concurrently.
    
    Uses asyncio.Semaphore to limit concurrent extractions.
    Each extraction runs in its own browser instance.
    """
    
    def __init__(self, config: Optional[ParallelConfig] = None):
        """
        Initialize parallel extractor.
        
        Args:
            config: ParallelConfig instance (uses defaults if None)
        """
        self.config = config or ParallelConfig()
        self.stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "skipped_memory": 0,
            "start_time": None,
            "end_time": None,
        }
    
    def _check_memory(self) -> float:
        """Check current memory usage percentage."""
        return psutil.virtual_memory().percent
    
    async def _extract_single(
        self,
        url: str,
        semaphore: asyncio.Semaphore,
        index: int,
        total: int
    ) -> Dict[str, Any]:
        """
        Extract a single business with semaphore control.
        
        Args:
            url: Business URL or name
            semaphore: Asyncio semaphore for concurrency control
            index: Current index (for progress)
            total: Total businesses (for progress)
        
        Returns:
            Extraction result dictionary
        """
        async with semaphore:
            # Check memory before starting
            mem_usage = self._check_memory()
            if mem_usage > self.config.memory_limit_percent:
                print(f"   [{index}/{total}] ⚠️ Skipped (memory {mem_usage:.0f}%)")
                self.stats["skipped_memory"] += 1
                return {"success": False, "error": "Memory limit exceeded", "url": url}
            
            # Create fresh extractor for each business
            extractor = PlaywrightExtractorOptimized(headless=self.config.headless)
            
            try:
                result = await extractor.extract_business_optimized(
                    url,
                    include_reviews=self.config.include_reviews,
                    max_reviews=self.config.max_reviews
                )
                
                if result.get('success'):
                    self.stats["successful"] += 1
                    name = result.get('name', 'Unknown')[:35]
                    print(f"   [{index}/{total}] ✅ {name}")
                else:
                    self.stats["failed"] += 1
                    print(f"   [{index}/{total}] ❌ Failed")
                
                return result
                
            except Exception as e:
                self.stats["failed"] += 1
                print(f"   [{index}/{total}] ❌ Error: {str(e)[:40]}")
                return {"success": False, "error": str(e), "url": url}
    
    async def extract_batch(
        self,
        urls: List[str],
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Extract multiple businesses in parallel.
        
        Args:
            urls: List of business URLs or names
            progress_callback: Optional callback(current, total, result)
        
        Returns:
            List of extraction results
        """
        self.stats = {
            "total": len(urls),
            "successful": 0,
            "failed": 0,
            "skipped_memory": 0,
            "start_time": time.time(),
            "end_time": None,
        }
        
        print(f"\n🔱 BOB PARALLEL EXTRACTOR v4.3.0")
        print("=" * 60)
        print(f"📊 Total businesses: {len(urls)}")
        print(f"⚡ Max concurrent: {self.config.max_concurrent}")
        print(f"🧠 Memory limit: {self.config.memory_limit_percent}%")
        print(f"⏱️ Delay between starts: {self.config.delay_between_starts}s")
        print("=" * 60)
        
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        # Create tasks with staggered starts
        tasks = []
        for i, url in enumerate(urls, 1):
            # Stagger task creation to avoid all starting at once
            if i > 1:
                await asyncio.sleep(self.config.delay_between_starts)
            
            task = asyncio.create_task(
                self._extract_single(url, semaphore, i, len(urls))
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result),
                    "url": urls[i]
                })
            else:
                processed_results.append(result)
        
        self.stats["end_time"] = time.time()
        
        # Print summary
        self._print_summary()
        
        return processed_results
    
    def _print_summary(self):
        """Print extraction summary."""
        duration = self.stats["end_time"] - self.stats["start_time"]
        total = self.stats["total"]
        successful = self.stats["successful"]
        
        print("\n" + "=" * 60)
        print("📊 PARALLEL EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"   Total: {total}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {self.stats['failed']}")
        if self.stats['skipped_memory'] > 0:
            print(f"   Skipped (memory): {self.stats['skipped_memory']}")
        print(f"   Success Rate: {successful/total*100:.1f}%")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Avg Time: {duration/total:.1f}s per business")
        
        # Compare to sequential estimate
        seq_estimate = total * 15  # ~15s per business sequentially
        speedup = seq_estimate / duration if duration > 0 else 0
        print(f"   Speedup: ~{speedup:.1f}x vs sequential")
        print("=" * 60)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

async def extract_parallel(
    urls: List[str],
    max_concurrent: int = 2,
    include_reviews: bool = True
) -> List[Dict[str, Any]]:
    """
    Convenience function for parallel extraction.
    
    Args:
        urls: List of business URLs or names
        max_concurrent: Maximum parallel browsers
        include_reviews: Whether to extract reviews
    
    Returns:
        List of extraction results
    """
    config = ParallelConfig(
        max_concurrent=max_concurrent,
        include_reviews=include_reviews
    )
    extractor = ParallelExtractor(config)
    return await extractor.extract_batch(urls)


# ============================================================================
# CLI INTERFACE
# ============================================================================

async def main():
    """Demo of parallel extraction."""
    
    # Test businesses
    businesses = [
        "Starbucks Times Square NYC",
        "Apple Store Fifth Avenue NYC",
        "Empire State Building NYC",
        "Central Park NYC",
    ]
    
    config = ParallelConfig(
        max_concurrent=2,
        include_reviews=False,  # Faster for demo
        delay_between_starts=2.0
    )
    
    extractor = ParallelExtractor(config)
    results = await extractor.extract_batch(businesses)
    
    # Show results
    print("\n📋 Results:")
    for r in results:
        if r.get('success'):
            print(f"   ✅ {r.get('name')} - Quality: {r.get('quality_score')}/100")
        else:
            print(f"   ❌ {r.get('url', 'Unknown')[:40]} - {r.get('error', 'Failed')[:30]}")


if __name__ == "__main__":
    asyncio.run(main())
