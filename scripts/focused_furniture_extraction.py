#!/usr/bin/env python3
"""
Focused Commercial Furniture Suppliers Extraction
Processing smaller batches for better reliability
"""

import json
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps')

from bob.utils.batch_processor import BatchProcessor

def extract_suppliers_batch(search_queries, batch_name):
    """Extract suppliers for a batch of queries."""
    print(f"\n🔱 Processing {batch_name} ({len(search_queries)} queries)")
    print("-" * 50)

    processor = BatchProcessor(
        headless=True,
        include_reviews=False,  # Faster extraction without reviews
        max_reviews=0
    )

    results = processor.process_batch_with_retry(
        businesses=search_queries,
        max_retries=1,
        verbose=True
    )

    # Filter successful results
    suppliers = []
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
                'extraction_date': datetime.now().isoformat(),
                'search_query': result.get('business', 'N/A'),
                'quality_score': business_data.get('quality_score', 0)
            }

            suppliers.append(supplier_info)
            print(f"   ✅ {supplier_info['name']} (Rating: {supplier_info['rating']})")

    return suppliers

def main():
    """Extract commercial furniture suppliers in focused batches."""
    print("🔱 FOCUSED COMMERCIAL FURNITURE SUPPLIERS EXTRACTION")
    print("=" * 60)

    # Load existing commercial furniture leads
    existing_leads = []
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
                'search_query': 'Existing data',
                'quality_score': existing_data.get('data_quality_score', 0)
            }
            existing_leads.append(existing_supplier)
            print(f"📋 Loaded {len(existing_leads)} existing commercial furniture lead(s)")
    except:
        print("⚠️  No existing commercial furniture leads found")

    # Focused search strategy
    search_batches = [
        {
            'name': 'Office Furniture Dubai',
            'queries': [
                'Office Furniture Dubai',
                'Office Furniture Store Dubai'
            ]
        },
        {
            'name': 'Hotel Furniture Suppliers',
            'queries': [
                'Hotel Furniture Supplier Dubai',
                'Hotel Furniture Dubai'
            ]
        },
        {
            'name': 'Restaurant Furniture',
            'queries': [
                'Restaurant Furniture Dubai',
                'Cafe Furniture Dubai'
            ]
        },
        {
            'name': 'Commercial Wholesale',
            'queries': [
                'Commercial Furniture Wholesale Dubai',
                'Furniture Manufacturer Dubai'
            ]
        },
        {
            'name': 'Abu Dhabi Suppliers',
            'queries': [
                'Office Furniture Abu Dhabi',
                'Commercial Furniture Abu Dhabi'
            ]
        }
    ]

    all_suppliers = existing_leads.copy()

    # Process each batch
    for batch in search_batches:
        try:
            suppliers = extract_suppliers_batch(batch['queries'], batch['name'])
            all_suppliers.extend(suppliers)

            print(f"   Found {len(suppliers)} suppliers in this batch")

        except Exception as e:
            print(f"   ❌ Error in {batch['name']}: {e}")
            continue

    # Remove duplicates based on name
    unique_suppliers = []
    seen_names = set()

    for supplier in all_suppliers:
        name_lower = supplier['name'].lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_suppliers.append(supplier)

    # Filter for commercial furniture suppliers
    commercial_suppliers = []
    for supplier in unique_suppliers:
        name_lower = supplier['name'].lower()
        category_lower = supplier['category'].lower() if supplier['category'] != 'N/A' else ''

        # Check if it's a commercial furniture supplier
        is_commercial = any(keyword in name_lower or keyword in category_lower
                          for keyword in [
                              'office', 'hotel', 'restaurant', 'cafe',
                              'commercial', 'wholesale', 'manufacturer',
                              'contract', 'project', 'supplier'
                          ])

        if is_commercial:
            commercial_suppliers.append(supplier)

    # Sort by rating (highest first) and take top 10
    commercial_suppliers.sort(key=lambda x: x['rating'], reverse=True)
    target_suppliers = commercial_suppliers[:10]

    print(f"\n📊 FINAL RESULTS:")
    print(f"   Total unique suppliers found: {len(unique_suppliers)}")
    print(f"   Commercial furniture suppliers: {len(commercial_suppliers)}")
    print(f"   Target suppliers (top 10): {len(target_suppliers)}")

    # Add revenue potential and strategic analysis
    for supplier in target_suppliers:
        # Revenue estimation
        base_revenue = 2000000  # AED 2M base

        rating_multiplier = 1.0 + (supplier['rating'] - 3.0) * 0.4
        reviews_multiplier = 1.0 + min(supplier['reviews_count'] / 100, 0.3)

        name_lower = supplier['name'].lower()
        if any(keyword in name_lower for keyword in ['wholesale', 'manufacturer']):
            commercial_multiplier = 1.4
        elif any(keyword in name_lower for keyword in ['contract', 'project']):
            commercial_multiplier = 1.2
        else:
            commercial_multiplier = 1.0

        estimated_revenue = base_revenue * rating_multiplier * reviews_multiplier * commercial_multiplier
        supplier['estimated_revenue_aed'] = round(estimated_revenue, 0)
        supplier['revenue_range'] = f"AED {round(estimated_revenue * 0.8, 0):,} - {round(estimated_revenue * 1.2, 0):,}"

        # Strategic factors
        strategic_factors = []
        if supplier['rating'] >= 4.5:
            strategic_factors.append("Premium reputation")
        if supplier['reviews_count'] >= 50:
            strategic_factors.append("High market trust")
        if 'wholesale' in name_lower or 'manufacturer' in name_lower:
            strategic_factors.append("Direct manufacturer advantage")
        if 'contract' in name_lower or 'project' in name_lower:
            strategic_factors.append("Large project experience")
        if supplier['website'] != 'N/A':
            strategic_factors.append("Professional web presence")

        supplier['strategic_factors'] = strategic_factors
        supplier['strategic_value_score'] = len(strategic_factors)

    # Display final results
    print(f"\n🎯 PREMIUM COMMERCIAL FURNITURE SUPPLIERS (Top {len(target_suppliers)})")
    print("=" * 80)

    for i, supplier in enumerate(target_suppliers, 1):
        print(f"\n{i}. {supplier['name']}")
        print(f"   ⭐ Rating: {supplier['rating']}/5 ({supplier['reviews_count']} reviews)")
        print(f"   📞 {supplier['phone']}")
        print(f"   📍 {supplier['address']}")
        print(f"   🌐 {supplier['website']}")
        print(f"   💰 Revenue Potential: {supplier['revenue_range']}")
        print(f"   🎯 Strategic Score: {supplier['strategic_value_score']}/6")

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
            'tool': 'BOB Google Maps Ultimate V3.0'
        },
        'suppliers': target_suppliers,
        'summary': {
            'total_suppliers': len(target_suppliers),
            'premium_suppliers_4plus': len([s for s in target_suppliers if s['rating'] >= 4.0]),
            'average_rating': sum(s['rating'] for s in target_suppliers) / len(target_suppliers) if target_suppliers else 0,
            'total_estimated_revenue': sum(s['estimated_revenue_aed'] for s in target_suppliers),
            'suppliers_with_website': len([s for s in target_suppliers if s['website'] != 'N/A']),
            'dubai_suppliers': len([s for s in target_suppliers if 'dubai' in s['address'].lower()]),
            'abu_dhabi_suppliers': len([s for s in target_suppliers if 'abu dhabi' in s['address'].lower()])
        }
    }

    # Save to JSON file
    output_file = '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/commercial_furniture_suppliers_leads.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")
    print(f"📈 Total Revenue Potential: AED {output_data['summary']['total_estimated_revenue']:,.0f}")
    print(f"✅ Mission Complete: {len(target_suppliers)} commercial furniture suppliers extracted!")

    return output_data

if __name__ == "__main__":
    main()