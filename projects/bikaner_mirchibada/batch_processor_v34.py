#!/usr/bin/env python3
"""
🔱 BATCH PROCESSOR V3.4.1 - LARGE-SCALE EXTRACTION ENGINE
Phase 3: Process hundreds of businesses with rate limiting and error handling

Features:
  • Rate limiting (15-30s delays between extractions)
  • Batch progress tracking with detailed logging
  • Automatic error recovery and retry logic
  • Quality score aggregation and reporting
  • Export to JSON/CSV formats
  • Memory-efficient processing

Status: PRODUCTION-READY
Philosophy: Nishkaam Karma Yoga - Selfless action for data excellence
"""

import sys
import json
import csv
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bob import HybridExtractorOptimized
from extract_lalgarh_v34_unified import UnifiedExtractionV34


class BatchProcessorV34:
    """
    🔱 Batch Processing Engine

    Philosophy: Nishkaam Karma Yoga
    - Process each business with dedication and attention
    - No attachment to results, focus on process excellence
    - Systematic error handling and recovery
    """

    def __init__(self,
                 rate_limit_seconds: int = 20,
                 max_retries: int = 2,
                 verbose: bool = True):
        """
        Initialize batch processor.

        Args:
            rate_limit_seconds: Delay between extractions (default 20s)
            max_retries: Number of retries for failed extractions
            verbose: Enable detailed logging
        """
        self.rate_limit_seconds = rate_limit_seconds
        self.max_retries = max_retries
        self.verbose = verbose

        self.extractor = UnifiedExtractionV34()

        self.results = {
            "batch_version": "3.4.1",
            "batch_timestamp": datetime.now().isoformat(),
            "batch_settings": {
                "rate_limit_seconds": rate_limit_seconds,
                "max_retries": max_retries
            },
            "businesses": [],
            "summary": {
                "total_processed": 0,
                "successful": 0,
                "failed": 0,
                "average_quality_score": 0,
                "processing_time_seconds": 0
            }
        }

    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp and level"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level:8} {message}")

    def process_single_business(self,
                               business_name: str,
                               retry_count: int = 0) -> Optional[Dict]:
        """
        Extract single business with retry logic.

        Args:
            business_name: Name/query of business to extract
            retry_count: Current retry attempt

        Returns:
            Extraction result dict or None
        """
        try:
            self.log(f"Processing: {business_name}")

            # Extract business using unified module
            result = self.extractor.extract_business(business_name)

            if result:
                self.log(f"✅ SUCCESS: {business_name}", "SUCCESS")
                return result
            else:
                self.log(f"⚠️ FAILED: {business_name} (result is None)", "WARNING")
                return None

        except Exception as e:
            error_msg = str(e)[:60]
            self.log(f"❌ ERROR: {business_name} - {error_msg}", "ERROR")

            # Retry logic
            if retry_count < self.max_retries:
                wait_time = 5 * (retry_count + 1)  # Backoff: 5s, 10s, 15s
                self.log(f"⏸️ Retry {retry_count + 1}/{self.max_retries} in {wait_time}s...", "RETRY")
                time.sleep(wait_time)
                return self.process_single_business(business_name, retry_count + 1)
            else:
                self.log(f"❌ FINAL FAILURE: {business_name} (max retries exceeded)", "ERROR")
                return None

    def process_batch(self,
                     business_list: List[str],
                     delay_after_each: bool = True) -> Dict:
        """
        Process batch of businesses.

        Args:
            business_list: List of business names/queries
            delay_after_each: Apply rate limiting between extractions

        Returns:
            Batch results dictionary
        """
        print("\n" + "="*70)
        print("🔱 BATCH PROCESSOR V3.4.1 - NISHKAAM KARMA YOGA")
        print("="*70)
        print(f"Processing {len(business_list)} businesses...")
        print(f"Rate limit: {self.rate_limit_seconds}s | Max retries: {self.max_retries}")
        print("="*70 + "\n")

        start_time = time.time()

        for index, business_name in enumerate(business_list, 1):
            print(f"\n[{index}/{len(business_list)}] Processing business...")
            print("-"*70)

            # Process business
            result = self.process_single_business(business_name)

            # Store result
            if result:
                self.results["businesses"].append({
                    "index": index,
                    "business_name": business_name,
                    "status": "✅ SUCCESS",
                    "quality_score": result.get('quality_score', {}).get('final', 0),
                    "result": result
                })
                self.results["summary"]["successful"] += 1
            else:
                self.results["businesses"].append({
                    "index": index,
                    "business_name": business_name,
                    "status": "❌ FAILED",
                    "quality_score": 0,
                    "result": None
                })
                self.results["summary"]["failed"] += 1

            self.results["summary"]["total_processed"] = index

            # Rate limiting (except after last business)
            if delay_after_each and index < len(business_list):
                self.log(f"⏸️ Rate limiting: waiting {self.rate_limit_seconds}s...", "RATE_LIMIT")
                time.sleep(self.rate_limit_seconds)

        # Calculate summary statistics
        elapsed_time = time.time() - start_time
        self.results["summary"]["processing_time_seconds"] = round(elapsed_time, 2)

        # Calculate average quality score
        successful_results = [
            b for b in self.results["businesses"]
            if b["status"] == "✅ SUCCESS"
        ]

        if successful_results:
            avg_quality = sum(
                b["quality_score"] for b in successful_results
            ) / len(successful_results)
            self.results["summary"]["average_quality_score"] = round(avg_quality, 1)

        # Display summary
        self._display_summary()

        return self.results

    def _display_summary(self):
        """Display batch processing summary"""
        summary = self.results["summary"]
        total = summary["total_processed"]
        successful = summary["successful"]
        failed = summary["failed"]
        avg_quality = summary["average_quality_score"]
        processing_time = summary["processing_time_seconds"]

        print("\n" + "="*70)
        print("📊 BATCH PROCESSING SUMMARY")
        print("="*70)
        print(f"Total processed: {total}")
        print(f"Successful: {successful} ({100*successful/total:.1f}%)")
        print(f"Failed: {failed} ({100*failed/total:.1f}%)")
        print(f"Average quality score: {avg_quality}/100")
        print(f"Processing time: {processing_time}s ({processing_time/total:.1f}s per business)")
        print("="*70 + "\n")

    def save_results_json(self, filename: Optional[str] = None) -> Path:
        """Save batch results to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_results_{timestamp}.json"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        self.log(f"💾 Results saved to: {output_path}", "SAVE")
        return output_path

    def save_results_csv(self, filename: Optional[str] = None) -> Path:
        """Save batch results summary to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_results_{timestamp}.csv"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "Index",
                "Business Name",
                "Status",
                "Quality Score",
                "Emails Found",
                "GPS Status",
                "Hours Status",
                "Phone",
                "Address",
                "Website"
            ])

            # Data rows
            for business in self.results["businesses"]:
                index = business["index"]
                name = business["business_name"]
                status = business["status"]
                quality = business["quality_score"]

                result = business.get("result", {})
                core_data = result.get("core_data", {})
                enhancements = result.get("enhancements", {})

                emails = enhancements.get("emails", {}).get("count", 0)
                gps_status = enhancements.get("gps", {}).get("status", "N/A")
                hours_status = enhancements.get("hours", {}).get("status", "N/A")

                phone = core_data.get("phone", "N/A")
                address = core_data.get("address", "N/A")
                website = core_data.get("website", "N/A")

                writer.writerow([
                    index,
                    name,
                    status,
                    quality,
                    emails,
                    gps_status,
                    hours_status,
                    phone,
                    address,
                    website[:50] + "..." if len(website) > 50 else website
                ])

        self.log(f"📊 CSV results saved to: {output_path}", "SAVE")
        return output_path

    def get_results(self) -> Dict:
        """Return batch results"""
        return self.results


def main():
    """Main batch processing example"""

    # Sample business list for testing
    test_businesses = [
        "Lalgarh Palace Bikaner",
        "Gypsy Vegetarian Restaurant Jodhpur",
        "Bikaner Municipality Office",
    ]

    # Create processor
    processor = BatchProcessorV34(
        rate_limit_seconds=20,
        max_retries=1,
        verbose=True
    )

    # Process batch
    results = processor.process_batch(test_businesses, delay_after_each=True)

    # Save results
    processor.save_results_json()
    processor.save_results_csv()

    print("✨ Batch processing complete!")


if __name__ == "__main__":
    main()

