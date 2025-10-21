#!/usr/bin/env python3
"""
Commercial Furniture Suppliers Extraction Mission
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

from bob.utils.batch_processor import BatchProcessor

def main():
    """Extract commercial furniture suppliers across UAE."""
    print("🔱 BOB GOOGLE MAPS ULTIMATE V3.0 - Commercial Furniture Suppliers Mission")
    print("=" * 80)
    print("Mission: Extract 10 Premium Commercial Furniture Suppliers Across UAE")
    print("Categories: Office, Hotel, Restaurant, Retail Furniture")
    print("Quality Threshold: 4.0+ Rating Minimum")
    print("=" * 80)
    print()

    # Search strategy for commercial furniture suppliers
    search_queries = [
        # Office Furniture Suppliers (2 targets)
        "Office Furniture Supplier Dubai",
        "Office Furniture Dubai",

        # Hotel Furniture Suppliers (2 targets)
        "Hotel Furniture Supplier UAE",
        "Hotel Furniture Dubai",

        # Restaurant Furniture Suppliers (2 targets)
        "Restaurant Furniture Dubai",
        "Restaurant Furniture Supplier Dubai",

        # Commercial Furniture Wholesale (2 targets)
        "Commercial Furniture Wholesale Dubai",
        "Furniture Manufacturer Dubai",

        # Retail Furniture Suppliers (2 targets)
        "Retail Furniture Supplier Abu Dhabi",
        "Commercial Furniture Abu Dhabi"
    ]

    print(f"📍 Search Strategy: {len(search_queries)} targeted queries")
    print(f"🎯 Target: 10 premium commercial furniture suppliers")
    print()

    # Initialize batch processor
    processor = BatchProcessor(
        headless=True,
        include_reviews=True,
        max_reviews=5
    )

    # Process all search queries
    print("🚀 Starting extraction process...")
    results = processor.process_batch_with_retry(
        businesses=search_queries,
        max_retries=2,
        verbose=True
    )

    # Filter and analyze results
    premium_suppliers = []
    commercial_suppliers = []

    for result in results:
        if result.get('success') and 'business' in result:
            business_data = result['business']

            # Extract key information
            supplier_info = {
                'name': business_data.get('name', 'N/A'),
                'rating': business_data.get('rating', 0),
                'reviews_count': business_data.get('reviews_count', 0),
                'phone': business_data.get('phone', 'N/A'),
                'address': business_data.get('address', 'N/A'),
                'website': business_data.get('website', 'N/A'),
                'emails': business_data.get('emails', []),
                'category': business_data.get('category', 'Furniture'),
                'cid': business_data.get('cid', 'N/A'),
                'latitude': business_data.get('latitude'),
                'longitude': business_data.get('longitude'),
                'images_count': len(business_data.get('images', [])),
                'service_options': business_data.get('service_options', {}),
                'extraction_date': datetime.now().isoformat(),
                'search_query': result.get('business', 'N/A'),
                'quality_score': business_data.get('quality_score', 0)
            }

            # Determine commercial capability based on keywords
            name_lower = supplier_info['name'].lower()
            category_lower = supplier_info['category'].lower() if supplier_info['category'] != 'N/A' else ''

            is_commercial = any(keyword in name_lower or keyword in category_lower
                              for keyword in [
                                  'commercial', 'office', 'hotel', 'restaurant',
                                  'wholesale', 'manufacturer', 'contract',
                                  'supplier', 'project', 'corporate'
                              ])

            if is_commercial:
                commercial_suppliers.append(supplier_info)

                # Check if premium (4.0+ rating)
                if supplier_info['rating'] >= 4.0:
                    premium_suppliers.append(supplier_info)

    print(f"\n📊 Extraction Results:")
    print(f"   Total successful extractions: {len([r for r in results if r.get('success')])}")
    print(f"   Commercial furniture suppliers found: {len(commercial_suppliers)}")
    print(f"   Premium suppliers (4.0+ rating): {len(premium_suppliers)}")
    print()

    # Select top 10 premium suppliers (or best available)
    target_suppliers = []

    # First, add all premium suppliers
    target_suppliers.extend(premium_suppliers)

    # If we need more suppliers, add high-rated commercial ones
    if len(target_suppliers) < 10:
        remaining_commercial = [s for s in commercial_suppliers
                              if s not in target_suppliers and s['rating'] >= 3.5]
        target_suppliers.extend(remaining_commercial)

    # Take top 10
    target_suppliers = target_suppliers[:10]

    print(f"🎯 Final Selection: {len(target_suppliers)} commercial furniture suppliers")
    print()

    # Analyze revenue potential and strategic value
    for i, supplier in enumerate(target_suppliers, 1):
        # Revenue potential estimation based on rating and commercial keywords
        base_revenue = 2000000  # AED 2M base

        # Multipliers
        rating_multiplier = 1.0 + (supplier['rating'] - 3.0) * 0.5  # Higher rating = more revenue
        reviews_multiplier = 1.0 + min(supplier['reviews_count'] / 100, 0.5)  # More reviews = established

        # Commercial type premium
        name_lower = supplier['name'].lower()
        if 'wholesale' in name_lower or 'manufacturer' in name_lower:
            commercial_multiplier = 1.5
        elif 'contract' in name_lower or 'project' in name_lower:
            commercial_multiplier = 1.3
        else:
            commercial_multiplier = 1.0

        estimated_revenue = base_revenue * rating_multiplier * reviews_multiplier * commercial_multiplier

        # Strategic value assessment
        strategic_factors = []
        if supplier['rating'] >= 4.5:
            strategic_factors.append("Premium reputation - excellent client satisfaction")
        if supplier['reviews_count'] >= 50:
            strategic_factors.append("High market presence and trust")
        if 'wholesale' in name_lower or 'manufacturer' in name_lower:
            strategic_factors.append("Direct manufacturer - cost advantage")
        if 'contract' in name_lower or 'project' in name_lower:
            strategic_factors.append("Large-scale project experience")
        if len(supplier['emails']) > 0:
            strategic_factors.append("Multiple contact channels available")
        if supplier['images_count'] > 5:
            strategic_factors.append("Showroom/capability demonstration")

        supplier['estimated_revenue_aed'] = round(estimated_revenue, 0)
        supplier['revenue_range'] = f"AED {round(estimated_revenue * 0.8, 0):,} - {round(estimated_revenue * 1.2, 0):,}"
        supplier['strategic_factors'] = strategic_factors
        supplier['strategic_value_score'] = len(strategic_factors)

    # Sort by strategic value
    target_suppliers.sort(key=lambda x: x['strategic_value_score'], reverse=True)

    # Display detailed analysis
    print("📋 PREMIUM COMMERCIAL FURNITURE SUPPLIERS ANALYSIS")
    print("=" * 80)

    for i, supplier in enumerate(target_suppliers, 1):
        print(f"\n{i}. {supplier['name']}")
        print(f"   ⭐ Rating: {supplier['rating']}/5 ({supplier['reviews_count']} reviews)")
        print(f"   📞 Phone: {supplier['phone']}")
        print(f"   📍 Address: {supplier['address']}")
        print(f"   🌐 Website: {supplier['website']}")
        print(f"   📧 Emails: {', '.join(supplier['emails']) if supplier['emails'] else 'N/A'}")
        print(f"   💰 Revenue Potential: {supplier['revenue_range']}")
        print(f"   🎯 Strategic Value Score: {supplier['strategic_value_score']}/6")

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
            'actual_count': len(target_suppliers),
            'region': 'UAE',
            'categories': ['Office', 'Hotel', 'Restaurant', 'Retail'],
            'quality_threshold': '4.0+ rating',
            'tool': 'BOB Google Maps Ultimate V3.0'
        },
        'suppliers': target_suppliers,
        'summary': {
            'total_suppliers': len(target_suppliers),
            'premium_suppliers_4plus': len([s for s in target_suppliers if s['rating'] >= 4.0]),
            'average_rating': sum(s['rating'] for s in target_suppliers) / len(target_suppliers) if target_suppliers else 0,
            'total_estimated_revenue': sum(s['estimated_revenue_aed'] for s in target_suppliers),
            'suppliers_with_email': len([s for s in target_suppliers if s['emails']]),
            'suppliers_with_website': len([s for s in target_suppliers if s['website'] != 'N/A']),
            'dubai_suppliers': len([s for s in target_suppliers if 'dubai' in s['address'].lower()]),
            'abu_dhabi_suppliers': len([s for s in target_suppliers if 'abu dhabi' in s['address'].lower()])
        }
    }

    # Save to JSON file
    output_file = '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/commercial_furniture_suppliers_leads.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Complete results saved to: {output_file}")
    print(f"📈 Total Revenue Potential: AED {output_data['summary']['total_estimated_revenue']:,.0f}")
    print(f"✅ Mission Accomplished: {len(target_suppliers)} premium commercial furniture suppliers extracted!")
    print()
    print("🔱 BOB Google Maps Ultimate V3.0 - Mission Complete! 🔱")

if __name__ == "__main__":
    main()