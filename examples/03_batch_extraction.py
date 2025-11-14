#!/usr/bin/env python3
"""
Example 3: Batch Business Extraction

This example demonstrates how to extract multiple businesses
efficiently using the batch processor.

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob.utils.batch_processor import BatchProcessor
import json


def main():
    """Extract multiple businesses in batch mode."""

    print("🔱 BOB Google Maps - Batch Extraction Example")
    print("=" * 60)

    # Create batch processor
    processor = BatchProcessor(
        headless=True,
        include_reviews=False,
        max_reviews=5,
        max_concurrent=3  # Process 3 businesses at a time
    )

    # Define list of businesses to extract
    businesses_to_extract = [
        "McDonald's Times Square New York",
        "Starbucks Pike Place Seattle",
        "Apple Store Fifth Avenue New York",
        "Whole Foods Market Austin",
        "Target Times Square New York"
    ]

    print(f"\n📋 Extracting {len(businesses_to_extract)} businesses:")
    for idx, business in enumerate(businesses_to_extract, 1):
        print(f"   {idx}. {business}")

    print("\n⏳ Starting batch extraction...")
    print(f"{'─' * 60}")

    # Process batch with retry logic
    results = processor.process_batch_with_retry(
        businesses_to_extract,
        max_retries=1,
        verbose=True  # Show progress
    )

    # Analyze results
    print(f"\n{'═' * 60}")
    print("📊 Batch Extraction Summary")
    print(f"{'═' * 60}")

    successful = sum(1 for r in results if r.get('success'))
    failed = len(results) - successful
    total_time = sum(r.get('extraction_time_seconds', 0) for r in results)
    avg_time = total_time / len(results) if results else 0
    avg_quality = sum(
        r.get('business', {}).get('data_quality_score', 0)
        for r in results if r.get('success')
    ) / successful if successful else 0

    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"⏱️ Total Time: {total_time:.2f}s")
    print(f"⏱️ Average Time: {avg_time:.2f}s per business")
    print(f"📊 Average Quality: {avg_quality:.1f}/100")

    # Show individual results
    print(f"\n{'─' * 60}")
    print("📋 Individual Results:")
    print(f"{'─' * 60}")

    for idx, result in enumerate(results, 1):
        if result.get('success'):
            business = result['business']
            status = "✅"
            info = f"{business.name} | Rating: {business.rating or 'N/A'} | Quality: {business.data_quality_score}/100"
        else:
            status = "❌"
            info = f"Failed: {result.get('error', 'Unknown error')}"

        print(f"{idx}. {status} {info}")

    # Save results to JSON
    output_file = "batch_extraction_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {output_file}")

    print(f"\n{'═' * 60}")
    print("✅ Batch extraction completed!")


if __name__ == "__main__":
    main()
