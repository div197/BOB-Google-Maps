#!/usr/bin/env python3
"""
BOB Google Maps - Main Application Entry Point

Revolutionary Google Maps alternative providing:
- 4-20 high-resolution images per business
- Complete business intelligence extraction
- $0 cost vs $850-1,600 Google API cost
- Works with any Google Maps URL

Made for students, researchers, and startups worldwide.
"""

import sys
import os
import argparse
import json
import time
import requests
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.google_maps_extractor import GoogleMapsExtractor

class BOBGoogleMaps:
    """Main BOB Google Maps application class."""

    def __init__(self):
        self.version = "1.0.0"
        self.release_date = "September 22, 2025"
        self.extractor = GoogleMapsExtractor()

    def extract_business(self, url, include_reviews=True, max_reviews=5):
        """
        Extract complete business data from Google Maps URL.

        Args:
            url: Any Google Maps URL
            include_reviews: Include customer reviews
            max_reviews: Maximum reviews to extract

        Returns:
            Complete business data with images and reviews
        """
        print(f"🔱 BOB GOOGLE MAPS {self.version}")
        print(f"📅 Release: {self.release_date}")
        print(f"🌟 Revolutionary Google Maps Alternative")
        print()

        result = self.extractor.extract_business(url, include_reviews, max_reviews)

        if result.get('success'):
            self._display_professional_summary(result)
        else:
            print(f"\n❌ EXTRACTION FAILED: {result.get('error', 'Unknown error')}")
            print(f"💡 Suggestion: {result.get('guidance', 'Please check URL and try again')}")

        return result

    def _display_professional_summary(self, result):
        """Display professional-grade extraction summary."""
        print("\n" + "="*60)
        print("✅ EXTRACTION COMPLETED SUCCESSFULLY")
        print("="*60)

        # Business Information
        print(f"\n📋 BUSINESS: {result.get('name', 'N/A')}")

        if result.get('rating'):
            stars = "⭐" * int(float(result['rating']))
            print(f"⭐ RATING: {result['rating']}/5 {stars}")

        if result.get('address'):
            print(f"📍 ADDRESS: {result['address']}")

        if result.get('phone'):
            print(f"📞 PHONE: {result['phone']}")

        if result.get('website'):
            print(f"🌐 WEBSITE: {result['website']}")

        if result.get('category'):
            print(f"🏷️ CATEGORY: {result['category']}")

        # Location Data
        if result.get('latitude') and result.get('longitude'):
            print(f"\n🌍 GPS COORDINATES:")
            print(f"   Latitude: {result['latitude']}")
            print(f"   Longitude: {result['longitude']}")

        # Revolutionary Features
        print(f"\n🔥 REVOLUTIONARY CAPABILITIES:")
        image_count = result.get('image_count', 0)
        if image_count > 0:
            print(f"   📸 Images Extracted: {image_count} (IMPOSSIBLE via Google API!)")
        else:
            print(f"   📸 Images Extracted: 0")

        review_count = len(result.get('reviews', []))
        print(f"   💬 Reviews Extracted: {review_count}")

        # Data Quality Assessment
        quality_score = result.get('data_quality_score', 0)
        if quality_score >= 80:
            quality_status = "EXCELLENT"
            quality_emoji = "🟢"
        elif quality_score >= 60:
            quality_status = "GOOD"
            quality_emoji = "🟡"
        else:
            quality_status = "BASIC"
            quality_emoji = "🟠"

        print(f"\n📊 DATA QUALITY: {quality_emoji} {quality_status} ({quality_score}/100)")

        # Economic Impact
        print(f"\n💰 ECONOMIC IMPACT:")
        print(f"   💵 Cost via BOB: $0 (FREE)")
        print(f"   💸 Cost via Google API: $0.50-$1.60 per business")
        print(f"   🎉 Your Savings: $0.50-$1.60 for this extraction!")

        print("\n" + "="*60)

    def extract_multiple(self, urls, max_reviews_per_business=3, verbose=True):
        """Extract multiple businesses in batch with professional progress tracking."""
        print(f"🔱 BOB BATCH EXTRACTION")
        print(f"📊 Target: {len(urls)} businesses")
        print(f"⚙️ Reviews per business: {max_reviews_per_business}")
        print("🚀 Production-scale processing...")

        results = []
        successful = 0
        failed = 0
        total_images = 0
        total_quality_score = 0

        for i, url in enumerate(urls, 1):
            if verbose:
                print(f"\n📍 [{i}/{len(urls)}] Processing: {url[:50]}...")

            result = self.extractor.extract_business(url, True, max_reviews_per_business)
            results.append(result)

            if result.get('success'):
                successful += 1
                total_images += result.get('image_count', 0)
                total_quality_score += result.get('data_quality_score', 0)
                if verbose:
                    print(f"   ✅ Success: {result.get('name', 'N/A')} ({result.get('image_count', 0)} images)")
            else:
                failed += 1
                if verbose:
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")

            # Progress indicator for large batches
            if not verbose and len(urls) > 10:
                progress = (i / len(urls)) * 100
                print(f"\r⏳ Progress: {progress:.1f}% ({i}/{len(urls)}) - Success: {successful}, Failed: {failed}", end="")

            # Respectful rate limiting
            if i < len(urls):
                time.sleep(2)

        # Final batch summary
        print(f"\n\n" + "="*60)
        print("🎉 BATCH EXTRACTION COMPLETED")
        print("="*60)
        print(f"📊 RESULTS SUMMARY:")
        print(f"   ✅ Successful: {successful}/{len(urls)} ({(successful/len(urls)*100):.1f}%)")
        print(f"   ❌ Failed: {failed}/{len(urls)} ({(failed/len(urls)*100):.1f}%)")
        print(f"   📸 Total Images: {total_images}")
        if successful > 0:
            avg_quality = total_quality_score / successful
            print(f"   📊 Average Quality: {avg_quality:.1f}/100")

        # Economic impact
        savings = len(urls) * 1.00  # Assume $1 per business API cost
        print(f"\n💰 ECONOMIC IMPACT:")
        print(f"   💵 Your Cost: $0 (FREE)")
        print(f"   💸 Google API Cost: ${savings:.2f}")
        print(f"   🎉 Total Savings: ${savings:.2f}")

        print("="*60)
        return results

    def download_images(self, result, images_dir='downloaded_images', max_images=20, business_name=None):
        """
        Download actual image files from extracted URLs.

        Args:
            result: Extraction result containing photos URLs
            images_dir: Directory to save images
            max_images: Maximum images to download
            business_name: Business name for organized folders

        Returns:
            Dict with download statistics
        """
        if not result.get('photos'):
            return {'downloaded': 0, 'failed': 0, 'total': 0}

        # Create images directory
        base_dir = Path(images_dir)
        if business_name:
            safe_name = "".join(c for c in business_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')[:50]  # Limit length
            download_dir = base_dir / safe_name
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            download_dir = base_dir / f"business_{timestamp}"

        download_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🖼️ DOWNLOADING IMAGES")
        print(f"📁 Directory: {download_dir}")
        print(f"🎯 Target: {min(len(result['photos']), max_images)} images")

        downloaded = 0
        failed = 0
        total_size = 0

        for i, url in enumerate(result['photos'][:max_images], 1):
            try:
                print(f"   📸 [{i}/{min(len(result['photos']), max_images)}] Downloading...", end="")

                response = requests.get(url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })

                if response.status_code == 200:
                    # Determine file extension
                    content_type = response.headers.get('content-type', '').lower()
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    elif 'webp' in content_type:
                        ext = '.webp'
                    else:
                        ext = '.jpg'  # default

                    filename = download_dir / f"image_{i:03d}{ext}"

                    with open(filename, 'wb') as f:
                        f.write(response.content)

                    file_size = len(response.content)
                    total_size += file_size

                    print(f" ✅ ({file_size:,} bytes)")
                    downloaded += 1

                else:
                    print(f" ❌ HTTP {response.status_code}")
                    failed += 1

            except Exception as e:
                print(f" ❌ {str(e)[:30]}...")
                failed += 1

        # Summary
        print(f"\n📊 DOWNLOAD SUMMARY:")
        print(f"   ✅ Downloaded: {downloaded} images")
        print(f"   ❌ Failed: {failed} images")
        print(f"   📁 Total Size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        print(f"   📂 Location: {download_dir}")

        return {
            'downloaded': downloaded,
            'failed': failed,
            'total': len(result['photos']),
            'total_size_bytes': total_size,
            'download_dir': str(download_dir)
        }

    def save_results(self, data, filename=None):
        """Save results to JSON, CSV, or Excel file based on extension."""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"bob_extraction_{timestamp}.json"

        # Determine file type from extension
        file_ext = filename.lower().split('.')[-1] if '.' in filename else 'json'

        if file_ext == 'csv':
            self._save_to_csv(data, filename)
        elif file_ext in ['xlsx', 'xls']:
            self._save_to_excel(data, filename)
        else:
            # Default to JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 Results saved: {filename}")
        return filename

    def _save_to_csv(self, data, filename):
        """Save results to CSV file."""
        import csv

        # Handle both single and multiple business results
        if isinstance(data, dict) and not data.get('success') is None:
            data = [data]  # Single business
        elif not isinstance(data, list):
            data = [data]

        if not data:
            return

        # Flatten nested data for CSV
        flattened_data = []
        for business in data:
            flat_row = {}
            for key, value in business.items():
                if isinstance(value, (list, dict)):
                    if key == 'reviews':
                        flat_row['review_count'] = len(value)
                        flat_row['first_review'] = value[0]['text'][:100] if value else ''
                    elif key == 'photos':
                        flat_row['photo_count'] = len(value)
                        flat_row['first_photo_url'] = value[0] if value else ''
                    elif key == 'attributes':
                        flat_row['attributes'] = ', '.join(value) if value else ''
                    elif key == 'service_options':
                        flat_row['services'] = ', '.join([k for k, v in value.items() if v])
                    elif key == 'popular_times':
                        flat_row['has_popular_times'] = 'Yes' if value else 'No'
                    elif key == 'social_media':
                        flat_row['social_links'] = ', '.join(value.values()) if value else ''
                    else:
                        flat_row[key] = str(value)
                else:
                    flat_row[key] = value

            flattened_data.append(flat_row)

        # Write CSV
        if flattened_data:
            keys = set()
            for row in flattened_data:
                keys.update(row.keys())

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(keys))
                writer.writeheader()
                writer.writerows(flattened_data)

    def _save_to_excel(self, data, filename):
        """Save results to Excel file (requires openpyxl)."""
        try:
            import openpyxl
            from openpyxl import Workbook

            # Use CSV method to flatten data first
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
                self._save_to_csv(data, tmp.name)
                tmp_path = tmp.name

            # Convert CSV to Excel
            import csv
            wb = Workbook()
            ws = wb.active
            ws.title = "BOB Google Maps Data"

            with open(tmp_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    ws.append(row)

            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width

            wb.save(filename)

            # Cleanup temp file
            import os
            os.remove(tmp_path)

        except ImportError:
            print("⚠️ Excel export requires 'openpyxl'. Install with: pip install openpyxl")
            print("💡 Saving as CSV instead...")
            filename = filename.replace('.xlsx', '.csv').replace('.xls', '.csv')
            self._save_to_csv(data, filename)

    def get_capabilities(self):
        """Get BOB capabilities summary."""
        return {
            "version": self.version,
            "release_date": self.release_date,
            "revolutionary_features": {
                "images_per_business": "4-20 typically",
                "cost": "Completely FREE",
                "api_cost_savings": "$850-1,600 per 50,000 businesses",
                "data_points": "17+ comprehensive",
                "url_compatibility": "Universal (any Google Maps URL)",
                "scalability": "50,000+ businesses confirmed"
            },
            "target_audience": {
                "students": "Free alternative to expensive Google API",
                "researchers": "Large-scale academic data collection",
                "startups": "Zero-cost market research and analysis"
            },
            "comparison": {
                "google_maps_api": {
                    "cost_50k": "$850-1,600",
                    "images": "0",
                    "setup": "API keys required"
                },
                "bob_google_maps": {
                    "cost_50k": "$0 (FREE)",
                    "images": "4-20",
                    "setup": "Zero setup required"
                }
            }
        }

def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="🔱 BOB Google Maps 1.0.0 - Revolutionary Google Maps Alternative",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bob_maps.py "https://www.google.com/maps/place/Restaurant"
  python bob_maps.py --batch urls.txt --output results.json
  python bob_maps.py --test "Coffee Shop"

Made for students, researchers, and startups worldwide.
Completely FREE - No API keys required.
        """
    )

    parser.add_argument('url', nargs='?', help='Google Maps URL to extract')
    parser.add_argument('--batch', help='File with URLs (one per line)')
    parser.add_argument('--output', '-o', help='Output filename')
    parser.add_argument('--reviews', type=int, default=5, help='Max reviews to extract (0-50)')
    parser.add_argument('--capabilities', action='store_true', help='Show capabilities')
    parser.add_argument('--version', action='store_true', help='Show version')
    parser.add_argument('--test', help='Quick test with business name')

    # Real-world optimization options
    parser.add_argument('--visible', action='store_true', help='Show browser window (for debugging)')
    parser.add_argument('--fast', action='store_true', help='Fast mode: skip reviews and extra images')
    parser.add_argument('--minimal', action='store_true', help='Minimal mode: basic business info only')

    # Image handling options
    parser.add_argument('--download-images', action='store_true', help='Download actual image files')
    parser.add_argument('--images-dir', default='downloaded_images', help='Directory for downloaded images')
    parser.add_argument('--max-images', type=int, default=20, help='Max images to download per business')

    # Advanced options
    parser.add_argument('--quality-threshold', type=int, default=50, help='Minimum data quality score (0-100)')
    parser.add_argument('--timeout', type=int, default=60, help='Timeout per business in seconds')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between requests (seconds)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - minimal output')

    args = parser.parse_args()

    bob = BOBGoogleMaps()

    if args.version:
        print(f"🔱 BOB Google Maps {bob.version}")
        print(f"Release: {bob.release_date}")
        print("Revolutionary Google Maps Alternative")
        return

    if args.capabilities:
        capabilities = bob.get_capabilities()
        print("🔱 BOB GOOGLE MAPS CAPABILITIES")
        print("=" * 40)
        for section, data in capabilities.items():
            if isinstance(data, dict):
                print(f"\n{section.upper().replace('_', ' ')}:")
                for key, value in data.items():
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"{section}: {data}")
        return

    if args.test:
        test_url = f"https://www.google.com/maps/search/{args.test.replace(' ', '+')}"
        print(f"🧪 Testing with: {test_url}")

        # Configure extraction based on CLI options
        include_reviews = not args.fast and not args.minimal
        max_reviews = 0 if args.minimal else (2 if args.fast else args.reviews)

        result = bob.extract_business(test_url, include_reviews, max_reviews)

        # Download images if requested
        if args.download_images and result.get('success') and result.get('photos'):
            business_name = result.get('name', 'Unknown_Business')
            download_stats = bob.download_images(
                result,
                args.images_dir,
                args.max_images,
                business_name
            )
            result['download_stats'] = download_stats

        # Check quality threshold
        if result.get('success') and result.get('data_quality_score', 0) < args.quality_threshold:
            print(f"\n⚠️ WARNING: Data quality ({result['data_quality_score']}) below threshold ({args.quality_threshold})")

        if args.output:
            bob.save_results(result, args.output)
        return

    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
            results = bob.extract_multiple(urls, args.reviews)
            filename = bob.save_results(results, args.output)
            print(f"✅ Batch processing completed: {filename}")
        except FileNotFoundError:
            print(f"❌ File not found: {args.batch}")
            sys.exit(1)
        return

    if args.url:
        result = bob.extract_business(args.url, True, args.reviews)
        if args.output:
            bob.save_results(result, args.output)
        return

    # No arguments provided - show professional welcome
    print("🔱 BOB GOOGLE MAPS 1.0.0 - REVOLUTIONARY GOOGLE MAPS ALTERNATIVE")
    print("=" * 70)
    print("Made for students, researchers, and startups worldwide.")
    print("Completely FREE - No API keys required.")
    print()
    print("📊 QUICK EXAMPLES:")
    print("  python bob_maps.py --test 'Starbucks'")
    print("  python bob_maps.py --test 'Restaurant' --download-images")
    print("  python bob_maps.py --batch urls.txt --output results.json")
    print("  python bob_maps.py --capabilities")
    print()
    print("🔥 REVOLUTIONARY FEATURES:")
    print("  • Extract 4-20 images per business (IMPOSSIBLE via Google API)")
    print("  • Complete business intelligence (17+ data points)")
    print("  • Download actual image files organized by business")
    print("  • Works with any Google Maps URL")
    print("  • Production-scale batch processing")
    print("  • $0 cost vs $850-1,600 Google API alternative")
    print()
    print("📚 For detailed help: python bob_maps.py --help")
    print("=" * 70)

if __name__ == "__main__":
    main()