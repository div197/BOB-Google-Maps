"""bob_core.cli

Command-line interface for BOB Google Maps.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .scraper import GoogleMapsScraper
from .batch import batch_scrape
from .analytics import BusinessAnalyzer, MarketAnalyzer


def _single(args: argparse.Namespace) -> None:  # noqa: D401
    scraper = GoogleMapsScraper(
        headless=not args.no_headless, 
        backend=args.backend
    )
    result = scraper.scrape(args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _batch(args: argparse.Namespace) -> None:  # noqa: D401
    input_path = Path(args.file)
    urls = [l.strip() for l in input_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    results = batch_scrape(urls, max_workers=args.workers)
    print(json.dumps(results, ensure_ascii=False, indent=2))


def _analyze(args: argparse.Namespace) -> None:  # noqa: D401
    """Analyze scraped data for business intelligence."""
    input_path = Path(args.file)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    
    if isinstance(data, list):
        # Multiple businesses - market analysis
        analyzer = MarketAnalyzer(data)
        analysis = {
            "market_analysis": analyzer.category_analysis(),
            "opportunities": analyzer.market_opportunities()
        }
    else:
        # Single business analysis
        analyzer = BusinessAnalyzer(data)
        analysis = {
            "business_score": analyzer.overall_score()
        }
        
        if data.get("reviews"):
            from .analytics import ReviewAnalyzer
            review_analyzer = ReviewAnalyzer(data["reviews"])
            analysis.update({
                "sentiment": review_analyzer.sentiment_analysis(),
                "ratings": review_analyzer.rating_analysis(),
                "keywords": review_analyzer.keyword_analysis()
            })
    
    print(json.dumps(analysis, ensure_ascii=False, indent=2))


def main() -> None:  # noqa: D401
    parser = argparse.ArgumentParser(prog="bob", description="BOB Google Maps CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    single = sub.add_parser("gmaps", help="Scrape single Google Maps URL")
    single.add_argument("url", help="Google Maps URL with &hl=en")
    single.add_argument("--no-headless", action="store_true", help="Show browser UI")
    single.add_argument("--backend", choices=["selenium", "playwright", "auto"], 
                       default="auto", help="Browser backend")
    single.set_defaults(func=_single)

    batch = sub.add_parser("batch", help="Batch scrape URLs from file (one per line)")
    batch.add_argument("file", help="Path to text file of URLs")
    batch.add_argument("--workers", type=int, default=4, help="Concurrency level")
    batch.set_defaults(func=_batch)

    analyze = sub.add_parser("analyze", help="Analyze scraped data for insights")
    analyze.add_argument("file", help="Path to JSON file with scraped data")
    analyze.set_defaults(func=_analyze)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main() 