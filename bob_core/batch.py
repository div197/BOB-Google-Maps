"""bob_core.batch

Simple thread-pool batch scraper wrapper.
"""
from __future__ import annotations

import concurrent.futures as _fut
from typing import Iterable, List, Dict, Any
import asyncio
from tqdm import tqdm

from .scraper import GoogleMapsScraper

__all__ = ["batch_scrape", "async_batch_scrape"]


def batch_scrape(
    urls: Iterable[str], *, max_workers: int = 4, show_progress: bool = True
) -> List[Dict[str, Any]]:
    """Scrape *urls* concurrently and return list of results.

    Parameters
    ----------
    urls : Iterable[str]
        Google Maps URLs (must include `&hl=en`).
    max_workers : int, default 4
        Thread concurrency.
    show_progress : bool, default True
        Display a tqdm progress bar.
    """
    scraper = GoogleMapsScraper()
    results: List[Dict[str, Any]] = []
    url_list = list(urls)
    progress_iter = tqdm(url_list, desc="Scraping", unit="url") if show_progress else url_list

    with _fut.ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(scraper.scrape, u): u for u in progress_iter}
        for future in _fut.as_completed(futures):
            url = futures[future]
            if show_progress:
                progress_iter.update(0)  # keep bar responsive
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({
                    "url": url,
                    "success": False,
                    "error_message": str(exc),
                })

    if show_progress and hasattr(progress_iter, "close"):
        progress_iter.close()
    return results


async def async_batch_scrape(
    urls: Iterable[str], *, max_workers: int = 4
) -> List[Dict[str, Any]]:
    """Async wrapper that runs *batch_scrape* in a thread pool."""

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: batch_scrape(urls, max_workers=max_workers)
    ) 