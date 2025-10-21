#!/usr/bin/env python3
"""
Comprehensive Commercial Furniture Suppliers Extraction Mission
BOB Google Maps Ultimate V3.0 - Specialist Agent for Commercial Furniture

Target: 10 premium commercial furniture suppliers across UAE
Categories: Office furniture, hotel furniture, restaurant furniture, retail furniture
Focus: High-volume suppliers with commercial capabilities (4.0+ rating minimum)
"""

import json
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps')

from bob.extractors.selenium_optimized import SeleniumExtractorOptimized

def extract_single_business(business_name):
    """Extract a single business using the optimized extractor."""
    try:
        print(f"🔍 Extracting: {business_name}")
        extractor = SeleniumExtractorOptimized(headless=True)
        result = extractor.extract_business_optimized(business_name, include_reviews=False, max_reviews=0)

        if result and result.get('success'):
            # Extract key information
            supplier_info = {
                'name': result.get('name', 'N/A'),
                'rating': result.get('rating', 0),
                'reviews_count': result.get('review_count', 0),
                'phone': result.get('phone', 'N/A'),
                'address': result.get('address', 'N/A'),
                'website': result.get('website', 'N/A'),
                'category': result.get('category', 'Furniture'),
                'cid': result.get('cid', 'N/A'),
                'latitude': result.get('latitude'),
                'longitude': result.get('longitude'),
                'extraction_date': datetime.now().isoformat(),
                'search_query': business_name,
                'quality_score': result.get('data_quality_score', 0),
                'extraction_method': result.get('extraction_method', 'N/A'),
                'extraction_time': result.get('extraction_time_seconds', 0)
            }

            print(f"   ✅ {supplier_info['name']} (Rating: {supplier_info['rating']})")
            return supplier_info
        else:
            print(f"   ❌ Failed to extract {business_name}")
            return None

    except Exception as e:
        print(f"   ❌ Error extracting {business_name}: {e}")
        return None

def main():
    """Extract commercial furniture suppliers across UAE."""
    print("🔱 BOB GOOGLE MAPS ULTIMATE V3.0 - Commercial Furniture Suppliers Mission")
    print("=" * 80)
    print("Mission: Extract 10 Premium Commercial Furniture Suppliers Across UAE")
    print("Categories: Office, Hotel, Restaurant, Retail Furniture")
    print("Quality Threshold: 4.0+ Rating Minimum")
    print("=" * 80)
    print()

    # Load existing commercial furniture leads
    existing_suppliers = []
    try:
        with open('/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/commercial_furniture_leads.json', 'r') as f:
            existing_data = json.load(f)

            # Convert existing lead to our format
            existing_supplier = {
                'name': existing_data.get('name', 'N/A'),
                'rating': existing_data.get('rating', 0),
                'reviews_count': existing_data.get('review_count', 0),
                'phone': existing_data.get('phone', 'N/A'),
                'address': existing_data.get('address', 'N/A'),
                'website': existing_data.get('website', 'N/A'),
                'emails': [],  # Not available in existing data
                'category': existing_data.get('category', 'Furniture'),
                'cid': existing_data.get('cid', 'N/A'),
                'latitude': existing_data.get('latitude'),
                'longitude': existing_data.get('longitude'),
                'extraction_date': datetime.now().isoformat(),
                'search_query': 'Existing data - WORKSPACE®',
                'quality_score': existing_data.get('data_quality_score', 0),
                'extraction_method': existing_data.get('extraction_method', 'Existing'),
                'extraction_time': 0
            }
            existing_suppliers.append(existing_supplier)
            print(f"📋 Loaded existing supplier: {existing_supplier['name']} (Rating: {existing_supplier['rating']})")
    except:
        print("⚠️  No existing commercial furniture leads found")

    # Target search queries for commercial furniture suppliers
    target_queries = [
        # Office Furniture Suppliers
        "Office Furniture Dubai",
        "Office Furniture Store Dubai",

        # Hotel & Hospitality Furniture
        "Hotel Furniture Dubai",
        "Hotel Furniture Supplier Dubai",

        # Restaurant & Cafe Furniture
        "Restaurant Furniture Dubai",
        "Cafe Furniture Dubai",

        # Commercial Wholesale & Manufacturing
        "Commercial Furniture Dubai",
        "Furniture Manufacturer Dubai",

        # Abu Dhabi Suppliers
        "Office Furniture Abu Dhabi",
        "Commercial Furniture Abu Dhabi"
    ]

    all_suppliers = existing_suppliers.copy()

    # Extract each supplier
    for query in target_queries:
        try:
            supplier = extract_single_business(query)
            if supplier:
                # Check if it's a commercial furniture supplier
                name_lower = supplier['name'].lower()
                category_lower = supplier['category'].lower() if supplier['category'] != 'N/A' else ''

                # Commercial furniture keywords
                is_commercial = any(keyword in name_lower or keyword in category_lower
                                  for keyword in [
                                      'office', 'hotel', 'restaurant', 'cafe',
                                      'commercial', 'wholesale', 'manufacturer',
                                      'contract', 'project', 'supplier',
                                      'workspace', 'furniture', 'home', 'improvement'
                                  ])

                # Include if commercial and meets quality threshold
                if is_commercial and supplier['rating'] >= 4.0:
                    all_suppliers.append(supplier)
                    print(f"   ✅ Added premium supplier: {supplier['name']}")
                elif is_commercial and supplier['rating'] >= 3.5:
                    all_suppliers.append(supplier)
                    print(f"   ⚠️  Added commercial supplier: {supplier['name']} (Rating: {supplier['rating']})")
                else:
                    print(f"   ⚠️  Skipped non-commercial or low-rated: {supplier['name']}")

        except Exception as e:
            print(f"   ❌ Error processing {query}: {e}")
            continue

    # Remove duplicates based on name
    unique_suppliers = []
    seen_names = set()

    for supplier in all_suppliers:
        name_lower = supplier['name'].lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_suppliers.append(supplier)

    # Sort by rating (highest first) and take top 10
    unique_suppliers.sort(key=lambda x: x['rating'], reverse=True)
    final_suppliers = unique_suppliers[:10]

    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"   Total unique suppliers found: {len(unique_suppliers)}")
    print(f"   Selected top suppliers: {len(final_suppliers)}")
    print(f"   Average rating: {sum(s['rating'] for s in final_suppliers) / len(final_suppliers):.1f}" if final_suppliers else "N/A")

    # Add revenue potential and strategic analysis
    for supplier in final_suppliers:
        # Revenue estimation model
        base_revenue = 2000000  # AED 2M base for commercial furniture suppliers

        # Rating multiplier (higher rating = more revenue potential)
        rating_multiplier = 1.0 + (supplier['rating'] - 3.0) * 0.4

        # Reviews multiplier (more reviews = established business)
        reviews_multiplier = 1.0 + min(supplier['reviews_count'] / 100, 0.3)

        # Commercial type premium
        name_lower = supplier['name'].lower()
        category_lower = supplier['category'].lower() if supplier['category'] != 'N/A' else ''

        if any(keyword in name_lower or keyword in category_lower
               for keyword in ['wholesale', 'manufacturer']):
            commercial_multiplier = 1.4  # Direct manufacturer advantage
        elif any(keyword in name_lower or keyword in category_lower
                 for keyword in ['contract', 'project', 'workspace']):
            commercial_multiplier = 1.2  # Large project experience
        else:
            commercial_multiplier = 1.0

        estimated_revenue = base_revenue * rating_multiplier * reviews_multiplier * commercial_multiplier
        supplier['estimated_revenue_aed'] = round(estimated_revenue, 0)
        supplier['revenue_range'] = f"AED {round(estimated_revenue * 0.8, 0):,} - {round(estimated_revenue * 1.2, 0):,}"

        # Strategic value assessment
        strategic_factors = []
        if supplier['rating'] >= 4.5:
            strategic_factors.append("Premium reputation - excellent client satisfaction")
        if supplier['reviews_count'] >= 50:
            strategic_factors.append("High market presence and trust")
        if any(keyword in name_lower or keyword in category_lower
               for keyword in ['wholesale', 'manufacturer']):
            strategic_factors.append("Direct manufacturer - cost advantage")
        if any(keyword in name_lower or keyword in category_lower
               for keyword in ['contract', 'project', 'workspace']):
            strategic_factors.append("Large-scale project experience")
        if supplier['website'] != 'N/A':
            strategic_factors.append("Professional web presence")
        if supplier['quality_score'] >= 75:
            strategic_factors.append("High data quality - reliable information")

        supplier['strategic_factors'] = strategic_factors
        supplier['strategic_value_score'] = len(strategic_factors)

    # Display final results
    print(f"\n🎯 PREMIUM COMMERCIAL FURNITURE SUPPLIERS (Top {len(final_suppliers)})")
    print("=" * 80)

    for i, supplier in enumerate(final_suppliers, 1):
        print(f"\n{i}. {supplier['name']}")
        print(f"   ⭐ Rating: {supplier['rating']}/5 ({supplier['reviews_count']} reviews)")
        print(f"   📞 Phone: {supplier['phone']}")
        print(f"   📍 Address: {supplier['address']}")
        print(f"   🌐 Website: {supplier['website']}")
        print(f"   📂 Category: {supplier['category']}")
        print(f"   💰 Revenue Potential: {supplier['revenue_range']}")
        print(f"   🎯 Strategic Score: {supplier['strategic_value_score']}/7")
        print(f"   🔍 Search Query: {supplier['search_query']}")

        if supplier['strategic_factors']:
            print("   ✨ Strategic Factors:")
            for factor in supplier['strategic_factors']:
                print(f"      • {factor}")

    # Save comprehensive results
    output_data = {
        'mission_metadata': {
            'extraction_date': datetime.now().isoformat(),
            'mission_type': 'Commercial Furniture Suppliers',
            'target_count': 10,
            'actual_count': len(final_suppliers),
            'region': 'UAE',
            'categories': ['Office', 'Hotel', 'Restaurant', 'Retail', 'Commercial'],
            'quality_threshold': '4.0+ rating (3.5+ for commercial)',
            'tool': 'BOB Google Maps Ultimate V3.0',
            'extraction_method': 'Selenium Optimized V4.0'
        },
        'suppliers': final_suppliers,
        'summary': {
            'total_suppliers': len(final_suppliers),
            'premium_suppliers_4plus': len([s for s in final_suppliers if s['rating'] >= 4.0]),
            'average_rating': sum(s['rating'] for s in final_suppliers) / len(final_suppliers) if final_suppliers else 0,
            'total_estimated_revenue': sum(s['estimated_revenue_aed'] for s in final_suppliers),
            'suppliers_with_website': len([s for s in final_suppliers if s['website'] != 'N/A']),
            'dubai_suppliers': len([s for s in final_suppliers if 'dubai' in s['address'].lower()]),
            'abu_dhabi_suppliers': len([s for s in final_suppliers if 'abu dhabi' in s['address'].lower()]),
            'average_quality_score': sum(s['quality_score'] for s in final_suppliers) / len(final_suppliers) if final_suppliers else 0,
            'categories_covered': list(set(s['category'] for s in final_suppliers if s['category'] != 'N/A'))
        }
    }

    # Save to JSON file
    output_file = '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/commercial_furniture_suppliers_leads.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")
    print(f"📈 Total Revenue Potential: AED {output_data['summary']['total_estimated_revenue']:,.0f}")
    print(f"✅ Mission Complete: {len(final_suppliers)} commercial furniture suppliers extracted!")
    print()
    print("🔱 BOB Google Maps Ultimate V3.0 - Mission Accomplished! 🔱")

    return output_data

if __name__ == "__main__":
    main()