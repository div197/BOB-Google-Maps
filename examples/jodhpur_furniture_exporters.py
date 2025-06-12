#!/usr/bin/env python3
"""
BOB Google Maps - Jodhpur Furniture Exporters Directory
=====================================================

Complete example of collecting and scraping furniture exporters in Jodhpur.
Demonstrates data collection strategies and comprehensive scraping.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import bob_core
from bob_core.batch import batch_scrape
from bob_core.export import export_data
from typing import List, Dict, Any


def generate_furniture_search_urls() -> List[str]:
    """Generate comprehensive search URLs for furniture exporters in Jodhpur."""
    
    # Base location
    location = "jodhpur rajasthan"
    
    # Different business types and variations
    business_types = [
        "furniture exporters",
        "furniture manufacturers", 
        "wooden furniture exporters",
        "handicraft furniture exporters",
        "antique furniture exporters",
        "modern furniture exporters",
        "furniture wholesale dealers",
        "furniture suppliers",
        "export furniture",
        "furniture trading company"
    ]
    
    # Generate URLs
    urls = []
    for business_type in business_types:
        # Create Google Maps search URL
        search_query = f"{business_type} {location}".replace(" ", "+")
        url = f"https://maps.google.com/maps?q={search_query}&hl=en"
        urls.append(url)
    
    print(f"✅ Generated {len(urls)} search URLs for furniture exporters")
    return urls


def scrape_furniture_exporters() -> List[Dict[str, Any]]:
    """Scrape all furniture exporters in Jodhpur."""
    
    print("🪑 Starting Jodhpur Furniture Exporters Directory Creation")
    print("=" * 60)
    
    # Step 1: Generate search URLs
    urls = generate_furniture_search_urls()
    
    # Step 2: Batch scrape (business-only for speed)
    print(f"\n🔍 Scraping {len(urls)} search queries...")
    start_time = time.time()
    
    results = batch_scrape(
        urls, 
        extract_reviews=False,  # Business-only for speed
        max_workers=3  # Conservative to avoid rate limiting
    )
    
    scrape_time = time.time() - start_time
    
    # Step 3: Filter and deduplicate results
    unique_businesses = {}
    successful_count = 0
    
    for result in results:
        if result['success']:
            successful_count += 1
            business = result['business_info']
            name = business.get('name', 'Unknown')
            
            # Only include businesses with valid names
            if name != 'Unknown' and name.strip():
                # Use name as key for deduplication
                if name not in unique_businesses:
                    unique_businesses[name] = result
    
    unique_results = list(unique_businesses.values())
    
    print(f"\n📊 Scraping Results:")
    print(f"   URLs processed: {len(urls)}")
    print(f"   Successful scrapes: {successful_count}")
    print(f"   Unique businesses found: {len(unique_results)}")
    print(f"   Time taken: {scrape_time:.2f} seconds")
    
    return unique_results


def analyze_furniture_directory(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze the furniture exporters directory."""
    
    if not results:
        return {"error": "No data to analyze"}
    
    print(f"\n📈 Directory Analysis")
    print("-" * 30)
    
    # Extract business info
    businesses = []
    categories = set()
    phone_count = 0
    website_count = 0
    
    for result in results:
        business = result.get('business_info', {})
        if business:
            businesses.append(business)
            
            # Collect categories
            category = business.get('category', 'Unknown')
            if category and category != 'Unknown':
                categories.add(category)
            
            # Count contact info
            if business.get('phone', 'Unavailable') != 'Unavailable':
                phone_count += 1
            
            if business.get('website', 'Unavailable') != 'Unavailable':
                website_count += 1
    
    analysis = {
        'total_businesses': len(businesses),
        'unique_categories': len(categories),
        'categories': list(categories),
        'businesses_with_phone': phone_count,
        'businesses_with_website': website_count,
        'phone_coverage': round((phone_count / len(businesses)) * 100, 1) if businesses else 0,
        'website_coverage': round((website_count / len(businesses)) * 100, 1) if businesses else 0
    }
    
    print(f"✅ Analysis Results:")
    print(f"   Total businesses: {analysis['total_businesses']}")
    print(f"   Unique categories: {analysis['unique_categories']}")
    print(f"   Phone coverage: {analysis['phone_coverage']}%")
    print(f"   Website coverage: {analysis['website_coverage']}%")
    
    if categories:
        print(f"   Categories found:")
        for category in sorted(categories):
            print(f"     - {category}")
    
    return analysis


def export_furniture_directory(results: List[Dict[str, Any]]):
    """Export furniture directory in multiple formats."""
    
    if not results:
        print("❌ No data to export")
        return
    
    print(f"\n💾 Exporting Furniture Directory")
    print("-" * 35)
    
    timestamp = int(time.time())
    base_filename = f"jodhpur_furniture_exporters_{timestamp}"
    
    try:
        # Export to JSON (full data)
        json_file = f"{base_filename}.json"
        export_data(results, json_file, format="json")
        print(f"✅ JSON exported: {json_file}")
        
        # Export to CSV (flattened for spreadsheets)
        csv_file = f"{base_filename}.csv"
        export_data(results, csv_file, format="csv")
        print(f"✅ CSV exported: {csv_file}")
        
        # Create a business summary file
        summary_file = f"{base_filename}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("JODHPUR FURNITURE EXPORTERS DIRECTORY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total businesses: {len(results)}\n\n")
            
            for i, result in enumerate(results, 1):
                business = result.get('business_info', {})
                f.write(f"{i}. {business.get('name', 'N/A')}\n")
                f.write(f"   Category: {business.get('category', 'N/A')}\n")
                f.write(f"   Address: {business.get('address', 'N/A')}\n")
                f.write(f"   Phone: {business.get('phone', 'N/A')}\n")
                f.write(f"   Website: {business.get('website', 'N/A')}\n")
                f.write("\n")
        
        print(f"✅ Summary exported: {summary_file}")
        
        # Create a contact list (phones only)
        contact_file = f"{base_filename}_contacts.txt"
        with open(contact_file, 'w', encoding='utf-8') as f:
            f.write("JODHPUR FURNITURE EXPORTERS - CONTACT LIST\n")
            f.write("=" * 50 + "\n\n")
            
            for result in results:
                business = result.get('business_info', {})
                name = business.get('name', 'N/A')
                phone = business.get('phone', 'N/A')
                
                if phone != 'N/A' and phone != 'Unavailable':
                    f.write(f"{name}: {phone}\n")
        
        print(f"✅ Contact list exported: {contact_file}")
        
    except Exception as e:
        print(f"❌ Export failed: {str(e)}")


def main():
    """Main function to create Jodhpur furniture exporters directory."""
    
    print("🕉️ BOB Google Maps - Jodhpur Furniture Exporters")
    print("🙏 Made with Niṣkāma Karma Yoga principles")
    print("=" * 60)
    
    try:
        # Step 1: Scrape furniture exporters
        results = scrape_furniture_exporters()
        
        if not results:
            print("❌ No furniture exporters found. Please check your internet connection.")
            return
        
        # Step 2: Analyze the directory
        analysis = analyze_furniture_directory(results)
        
        # Step 3: Export the directory
        export_furniture_directory(results)
        
        # Step 4: Display sample results
        print(f"\n🎯 Sample Furniture Exporters:")
        print("-" * 35)
        
        for i, result in enumerate(results[:5], 1):  # Show first 5
            business = result.get('business_info', {})
            print(f"{i}. {business.get('name', 'N/A')}")
            print(f"   📍 {business.get('address', 'N/A')}")
            print(f"   📞 {business.get('phone', 'N/A')}")
            print(f"   🌐 {business.get('website', 'N/A')}")
            print()
        
        if len(results) > 5:
            print(f"... and {len(results) - 5} more businesses")
        
        print(f"\n🎉 SUCCESS! Created comprehensive directory of {len(results)} furniture exporters in Jodhpur!")
        print("📁 Check the exported files for complete data.")
        
    except Exception as e:
        print(f"❌ Error creating directory: {str(e)}")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main() 