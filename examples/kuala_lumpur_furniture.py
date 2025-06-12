#!/usr/bin/env python3
"""examples.kuala_lumpur_furniture

Kuala Lumpur Furniture Showrooms Extraction
Demonstrates BOB's capability to extract furniture business data from Google Maps.

🔱 Made with Niṣkāma Karma Yoga principles 🔱

This example shows:
1. Single furniture manufacturer extraction
2. Batch extraction of 50 furniture showrooms
3. CSV export with comprehensive data
4. Business analytics and insights
"""

import asyncio
import csv
import json
import time
from typing import List, Dict, Any
from pathlib import Path

# BOB Core imports
import bob_core
from bob_core.scraper import GoogleMapsScraper
from bob_core.batch import batch_scrape, async_batch_scrape
from bob_core.analytics import analyze_business_data
from bob_core.export import export_to_csv, export_to_json

class KualaLumpurFurnitureExtractor:
    """Divine extractor for Kuala Lumpur furniture businesses."""
    
    def __init__(self):
        self.scraper = GoogleMapsScraper(headless=True)
        self.results = []
        self.start_time = time.time()
        
    async def extract_single_manufacturer(self) -> Dict[str, Any]:
        """Extract a single furniture manufacturer as a test."""
        print("🔍 EXTRACTING SINGLE FURNITURE MANUFACTURER")
        print("-" * 50)
        
        # Search for a specific furniture manufacturer in KL
        search_url = "https://maps.google.com/maps?q=furniture+manufacturer+kuala+lumpur&hl=en"
        
        print(f"🌐 Searching: {search_url}")
        
        try:
            result = await self.scraper.scrape_url(
                url=search_url,
                extract_reviews=True,
                max_reviews=10,
                business_only=False
            )
            
            if result['success']:
                business = result['business_info']
                print(f"✅ Found: {business.get('name', 'Unknown')}")
                print(f"📍 Address: {business.get('address', 'N/A')}")
                print(f"⭐ Rating: {business.get('rating', 'N/A')}")
                print(f"📞 Phone: {business.get('phone', 'N/A')}")
                print(f"🌐 Website: {business.get('website', 'N/A')}")
                print(f"💬 Reviews: {len(result.get('reviews', []))}")
                
                return result
            else:
                print(f"❌ Failed: {result.get('error_message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    async def extract_50_furniture_showrooms(self) -> List[Dict[str, Any]]:
        """Extract 50 furniture showrooms in Kuala Lumpur."""
        print("\n🏢 EXTRACTING 50 FURNITURE SHOWROOMS")
        print("-" * 50)
        
        # Generate search URLs for different furniture-related queries
        search_queries = [
            "furniture showroom kuala lumpur",
            "furniture store kuala lumpur", 
            "home furniture kuala lumpur",
            "office furniture kuala lumpur",
            "bedroom furniture kuala lumpur",
            "living room furniture kuala lumpur",
            "kitchen furniture kuala lumpur",
            "furniture outlet kuala lumpur",
            "furniture warehouse kuala lumpur",
            "custom furniture kuala lumpur"
        ]
        
        urls = []
        for query in search_queries:
            # Create multiple search variations
            base_url = f"https://maps.google.com/maps?q={query.replace(' ', '+')}&hl=en"
            urls.append(base_url)
            
            # Add location-specific searches
            for area in ["KLCC", "Bukit Bintang", "Mont Kiara", "Bangsar", "Petaling Jaya"]:
                area_url = f"https://maps.google.com/maps?q={query.replace(' ', '+')}+{area.replace(' ', '+')}&hl=en"
                urls.append(area_url)
        
        # Limit to 50 URLs
        urls = urls[:50]
        
        print(f"🔍 Processing {len(urls)} search queries...")
        print("📊 Extraction Progress:")
        
        try:
            # Use batch scraping for efficiency
            results = await async_batch_scrape(
                urls=urls,
                extract_reviews=True,
                max_reviews=5,
                business_only=False,
                max_workers=5,
                timeout=30
            )
            
            # Filter successful results
            successful_results = [r for r in results if r.get('success', False)]
            
            print(f"\n✅ Successfully extracted {len(successful_results)} businesses")
            print(f"❌ Failed extractions: {len(results) - len(successful_results)}")
            
            return successful_results
            
        except Exception as e:
            print(f"❌ Batch extraction error: {e}")
            return []
    
    def export_to_csv(self, results: List[Dict[str, Any]], filename: str = "kuala_lumpur_furniture.csv"):
        """Export results to CSV format."""
        print(f"\n📄 EXPORTING TO CSV: {filename}")
        print("-" * 50)
        
        if not results:
            print("❌ No results to export")
            return
        
        # Prepare CSV data
        csv_data = []
        for result in results:
            if not result.get('success'):
                continue
                
            business = result.get('business_info', {})
            reviews = result.get('reviews', [])
            
            row = {
                'name': business.get('name', ''),
                'rating': business.get('rating', ''),
                'category': business.get('category', ''),
                'address': business.get('address', ''),
                'phone': business.get('phone', ''),
                'website': business.get('website', ''),
                'hours': str(business.get('hours', {})),
                'price_range': business.get('price_range', ''),
                'review_count': len(reviews),
                'url': result.get('url', ''),
                'extraction_time': result.get('processing_time', 0),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result.get('timestamp', time.time())))
            }
            
            # Add review insights
            if reviews:
                row['latest_review'] = reviews[0].get('text', '')[:200] + '...' if len(reviews[0].get('text', '')) > 200 else reviews[0].get('text', '')
                row['latest_review_rating'] = reviews[0].get('rating', '')
            else:
                row['latest_review'] = ''
                row['latest_review_rating'] = ''
            
            csv_data.append(row)
        
        # Write to CSV
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if csv_data:
                    fieldnames = csv_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
                    
                    print(f"✅ Exported {len(csv_data)} businesses to {filename}")
                    print(f"📊 Columns: {', '.join(fieldnames)}")
                else:
                    print("❌ No valid data to export")
                    
        except Exception as e:
            print(f"❌ CSV export error: {e}")
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the extracted furniture business data."""
        print("\n📈 BUSINESS ANALYTICS")
        print("-" * 50)
        
        if not results:
            print("❌ No results to analyze")
            return {}
        
        successful_results = [r for r in results if r.get('success', False)]
        
        # Basic statistics
        total_businesses = len(successful_results)
        total_reviews = sum(len(r.get('reviews', [])) for r in successful_results)
        
        # Rating analysis
        ratings = []
        for result in successful_results:
            rating_str = result.get('business_info', {}).get('rating', '')
            if rating_str and 'star' in rating_str:
                try:
                    rating = float(rating_str.split()[0])
                    ratings.append(rating)
                except:
                    pass
        
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Category analysis
        categories = {}
        for result in successful_results:
            category = result.get('business_info', {}).get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
        
        # Location analysis
        locations = {}
        for result in successful_results:
            address = result.get('business_info', {}).get('address', '')
            if 'Kuala Lumpur' in address:
                # Extract area from address
                parts = address.split(',')
                if len(parts) >= 2:
                    area = parts[-2].strip()
                    locations[area] = locations.get(area, 0) + 1
        
        analysis = {
            'total_businesses': total_businesses,
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': {
                '5_stars': len([r for r in ratings if r >= 4.5]),
                '4_stars': len([r for r in ratings if 3.5 <= r < 4.5]),
                '3_stars': len([r for r in ratings if 2.5 <= r < 3.5]),
                'below_3': len([r for r in ratings if r < 2.5])
            },
            'top_categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]),
            'top_locations': dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])
        }
        
        # Print analysis
        print(f"📊 Total Businesses: {analysis['total_businesses']}")
        print(f"💬 Total Reviews: {analysis['total_reviews']}")
        print(f"⭐ Average Rating: {analysis['average_rating']}")
        print(f"🏆 Top Categories: {list(analysis['top_categories'].keys())[:3]}")
        print(f"📍 Top Locations: {list(analysis['top_locations'].keys())[:3]}")
        
        return analysis
    
    async def run_complete_extraction(self):
        """Run the complete furniture extraction process."""
        print("🔱" + "="*80)
        print("🏢 KUALA LUMPUR FURNITURE SHOWROOMS EXTRACTION 🏢")
        print("Following Niṣkāma Karma Yoga principles")
        print("="*80 + "🔱")
        
        # Step 1: Single manufacturer test
        single_result = await self.extract_single_manufacturer()
        
        # Step 2: Extract 50 showrooms
        batch_results = await self.extract_50_furniture_showrooms()
        
        # Step 3: Analyze results
        analysis = self.analyze_results(batch_results)
        
        # Step 4: Export to CSV
        if batch_results:
            self.export_to_csv(batch_results, "kuala_lumpur_furniture_showrooms.csv")
            
            # Also export as JSON for API testing
            with open("kuala_lumpur_furniture_showrooms.json", "w", encoding='utf-8') as f:
                json.dump({
                    'extraction_info': {
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'total_extracted': len(batch_results),
                        'extraction_time': time.time() - self.start_time
                    },
                    'analytics': analysis,
                    'businesses': batch_results
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Also exported JSON: kuala_lumpur_furniture_showrooms.json")
        
        print(f"\n🔱 EXTRACTION COMPLETED 🔱")
        print(f"⏱️ Total Time: {time.time() - self.start_time:.2f} seconds")
        print("🕉️ Made with divine precision for furniture industry insights 🕉️")

async def main():
    """Main execution function."""
    print("🕉️ Starting Kuala Lumpur Furniture Extraction...")
    print("🙏 Following the path of Niṣkāma Karma Yoga\n")
    
    extractor = KualaLumpurFurnitureExtractor()
    await extractor.run_complete_extraction()

if __name__ == "__main__":
    asyncio.run(main()) 