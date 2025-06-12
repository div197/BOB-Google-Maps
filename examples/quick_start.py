#!/usr/bin/env python3
"""
BOB Google Maps v0.5.0 - Quick Start Examples
===========================================

This script demonstrates the key features of BOB Google Maps v0.5.0:
- Business-only extraction (3.18x faster)
- Full extraction with reviews
- Batch processing capabilities
- Performance monitoring
- Error handling

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import bob_core
from bob_core.batch import batch_scrape
from bob_core.analytics import MarketAnalyzer, BusinessAnalyzer
from bob_core.export import export_data

def main():
    """Demonstrate BOB Google Maps v0.5.0 capabilities."""
    
    print("🙏 BOB Google Maps v0.5.0 - Quick Start Examples")
    print("=" * 50)
    
    # Test URL - Replace with your own Google Maps URL
    test_url = "https://maps.google.com/?q=restaurant+paris&hl=en"
    
    # Example 1: Business-Only Extraction (Fastest)
    print("\n⚡ Example 1: Business-Only Extraction (3.18x faster)")
    print("-" * 50)
    
    start_time = time.time()
    scraper_business = bob_core.GoogleMapsScraper(extract_reviews=False)
    result_business = scraper_business.scrape(test_url)
    business_time = time.time() - start_time
    
    if result_business['success']:
        business_info = result_business['business_info']
        print(f"✅ Business extracted in {business_time:.2f}s")
        print(f"   Name: {business_info.get('name', 'N/A')}")
        print(f"   Rating: {business_info.get('rating', 'N/A')}")
        print(f"   Address: {business_info.get('address', 'N/A')}")
        print(f"   Reviews: {result_business['reviews_count']} (business-only mode)")
    else:
        print(f"❌ Business extraction failed: {result_business.get('error', 'Unknown error')}")
    
    # Example 2: Dedicated Business-Only Method
    print("\n🎯 Example 2: Dedicated Business-Only Method")
    print("-" * 50)
    
    scraper = bob_core.GoogleMapsScraper()
    result_dedicated = scraper.scrape_business_only(test_url)
    
    if result_dedicated['success']:
        print("✅ Using dedicated scrape_business_only() method")
        print(f"   Business: {result_dedicated['business_info'].get('name', 'N/A')}")
    
    # Example 3: Limited Reviews (Balanced Speed)
    print("\n⚖️ Example 3: Limited Reviews (Balanced Speed)")
    print("-" * 50)
    
    start_time = time.time()
    scraper_limited = bob_core.GoogleMapsScraper(max_reviews=5)
    result_limited = scraper_limited.scrape(test_url)
    limited_time = time.time() - start_time
    
    if result_limited['success']:
        print(f"✅ Limited extraction in {limited_time:.2f}s")
        print(f"   Reviews extracted: {result_limited['reviews_count']}")
        print(f"   Speed vs business-only: {limited_time/business_time:.2f}x")
    
    # Example 4: Full Extraction (Most Comprehensive)
    print("\n📊 Example 4: Full Extraction (Most Comprehensive)")
    print("-" * 50)
    
    start_time = time.time()
    scraper_full = bob_core.GoogleMapsScraper(extract_reviews=True)
    result_full = scraper_full.scrape(test_url)
    full_time = time.time() - start_time
    
    if result_full['success']:
        print(f"✅ Full extraction in {full_time:.2f}s")
        print(f"   Reviews extracted: {result_full['reviews_count']}")
        print(f"   Speed comparison:")
        print(f"     - Business-only: {business_time:.2f}s (baseline)")
        print(f"     - Limited (5): {limited_time:.2f}s ({limited_time/business_time:.2f}x)")
        print(f"     - Full: {full_time:.2f}s ({full_time/business_time:.2f}x)")
        print(f"   Performance gain: {full_time/business_time:.2f}x faster with business-only")
    
    # Example 5: Batch Processing
    print("\n🔄 Example 5: Batch Processing")
    print("-" * 50)
    
    urls = [
        "https://maps.google.com/?q=restaurant+paris&hl=en",
        "https://maps.google.com/?q=cafe+london&hl=en"
    ]
    
    # Business-only batch (fastest for directories)
    print("Processing batch with business-only mode...")
    batch_results = batch_scrape(urls, extract_reviews=False, max_workers=2)
    
    successful_results = [r for r in batch_results if r['success']]
    print(f"✅ Batch completed: {len(successful_results)}/{len(urls)} successful")
    
    for i, result in enumerate(successful_results):
        business = result['business_info']
        print(f"   {i+1}. {business.get('name', 'N/A')} - {business.get('rating', 'N/A')}⭐")
    
    # Example 6: Analytics (if we have data)
    if successful_results:
        print("\n📈 Example 6: Business Analytics")
        print("-" * 50)
        
        try:
            # Market analysis
            analyzer = MarketAnalyzer(successful_results)
            market_analysis = analyzer.category_analysis()
            
            print("✅ Market Analysis:")
            print(f"   Categories found: {len(market_analysis.get('categories', []))}")
            
            # Individual business analysis
            if successful_results:
                business_analyzer = BusinessAnalyzer(successful_results[0])
                score = business_analyzer.overall_score()
                print(f"   First business score: {score:.2f}/10")
                
        except Exception as e:
            print(f"⚠️ Analytics unavailable: {str(e)}")
    
    # Example 7: Export Data
    if successful_results:
        print("\n💾 Example 7: Data Export")
        print("-" * 50)
        
        try:
            # Export to JSON
            export_data(successful_results, "example_results.json", format="json")
            print("✅ Data exported to example_results.json")
            
            # Export to CSV
            export_data(successful_results, "example_results.csv", format="csv")
            print("✅ Data exported to example_results.csv")
            
        except Exception as e:
            print(f"⚠️ Export failed: {str(e)}")
    
    # Example 8: Health Check
    print("\n🏥 Example 8: System Health Check")
    print("-" * 50)
    
    try:
        from bob_core.health_check import get_global_health_monitor
        health = get_global_health_monitor()
        status = health.get_system_status()
        
        print(f"✅ System Status: {status.get('status', 'Unknown')}")
        print(f"   Memory usage: {status.get('memory_usage_mb', 'N/A')} MB")
        print(f"   Active circuits: {status.get('active_circuits', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️ Health check unavailable: {str(e)}")
    
    # Performance Summary
    print("\n🎯 Performance Summary")
    print("=" * 50)
    print(f"Business-only extraction: ~{business_time:.1f}s (fastest)")
    if 'limited_time' in locals():
        print(f"Limited reviews (5): ~{limited_time:.1f}s (balanced)")
    if 'full_time' in locals():
        print(f"Full extraction: ~{full_time:.1f}s (comprehensive)")
        print(f"Speed improvement: {full_time/business_time:.2f}x faster with business-only")
    
    print("\n🙏 BOB Google Maps v0.5.0 - Production Ready!")
    print("Made with excellence following Niṣkāma Karma Yoga principles")

if __name__ == "__main__":
    main() 