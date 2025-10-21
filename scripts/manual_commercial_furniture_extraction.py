#!/usr/bin/env python3
"""
Manual Commercial Furniture Suppliers Extraction
Targeting specific high-value suppliers individually
"""

import json
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps')

def extract_single_business(business_name):
    """Extract a single business using the core extractor."""
    try:
        from bob.extractors.selenium_optimized import SeleniumExtractorOptimized

        print(f"🔍 Extracting: {business_name}")
        extractor = SeleniumExtractorOptimized(headless=True)
        result = extractor.extract_business_optimized(business_name, include_reviews=False, max_reviews=0)

        print(f"   Result keys: {list(result.keys()) if result else 'None'}")
        if result and result.get('success'):
            # The result itself contains the business data
            business_data = result

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
                'search_query': business_name,
                'quality_score': business_data.get('quality_score', 0)
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
    """Manual extraction of commercial furniture suppliers."""
    print("🔱 MANUAL COMMERCIAL FURNITURE SUPPLIERS EXTRACTION")
    print("=" * 60)

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
                'quality_score': existing_data.get('data_quality_score', 0)
            }
            existing_suppliers.append(existing_supplier)
            print(f"📋 Loaded existing supplier: {existing_supplier['name']} (Rating: {existing_supplier['rating']})")
    except:
        print("⚠️  No existing commercial furniture leads found")

    # Target high-value commercial furniture suppliers
    target_suppliers = [
        # Office Furniture Suppliers
        "Office Furniture Dubai",
        "Workspace Dubai",  # High-end office furniture
        "Office furniture store Dubai",

        # Hotel Furniture Suppliers
        "Hotel furniture supplier Dubai",
        "Hotel furniture Dubai",

        # Restaurant Furniture
        "Restaurant furniture Dubai",
        "Cafe furniture Dubai",

        # Commercial Wholesale
        "Commercial furniture Dubai",
        "Furniture manufacturer Dubai",

        # Abu Dhabi Suppliers
        "Office furniture Abu Dhabi"
    ]

    all_suppliers = existing_suppliers.copy()

    # Extract each supplier individually
    for target in target_suppliers:
        try:
            supplier = extract_single_business(target)
            if supplier:
                # Check if it's a commercial furniture supplier
                name_lower = supplier['name'].lower()
                category_lower = supplier['category'].lower() if supplier['category'] != 'N/A' else ''

                is_commercial = any(keyword in name_lower or keyword in category_lower
                                  for keyword in [
                                      'office', 'hotel', 'restaurant', 'cafe',
                                      'commercial', 'wholesale', 'manufacturer',
                                      'contract', 'project', 'supplier',
                                      'workspace', 'furniture'
                                  ])

                if is_commercial and supplier['rating'] >= 3.5:  # Minimum 3.5 rating
                    all_suppliers.append(supplier)
                    print(f"   ✅ Added commercial supplier: {supplier['name']}")
                else:
                    print(f"   ⚠️  Skipped non-commercial or low-rated: {supplier['name']}")

        except Exception as e:
            print(f"   ❌ Error processing {target}: {e}")
            continue

    # Remove duplicates
    unique_suppliers = []
    seen_names = set()

    for supplier in all_suppliers:
        name_lower = supplier['name'].lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_suppliers.append(supplier)

    # Sort by rating and take top 10
    unique_suppliers.sort(key=lambda x: x['rating'], reverse=True)
    final_suppliers = unique_suppliers[:10]

    print(f"\n📊 EXTRACTION COMPLETE:")
    print(f"   Total unique suppliers: {len(unique_suppliers)}")
    print(f"   Selected top suppliers: {len(final_suppliers)}")

    # Add revenue potential and strategic analysis
    for supplier in final_suppliers:
        # Revenue estimation
        base_revenue = 2000000  # AED 2M base

        rating_multiplier = 1.0 + (supplier['rating'] - 3.0) * 0.4
        reviews_multiplier = 1.0 + min(supplier['reviews_count'] / 100, 0.3)

        name_lower = supplier['name'].lower()
        if any(keyword in name_lower for keyword in ['wholesale', 'manufacturer']):
            commercial_multiplier = 1.4
        elif any(keyword in name_lower for keyword in ['contract', 'project', 'workspace']):
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
        if 'contract' in name_lower or 'project' in name_lower or 'workspace' in name_lower:
            strategic_factors.append("Large project experience")
        if supplier['website'] != 'N/A':
            strategic_factors.append("Professional web presence")
        if supplier['emails']:
            strategic_factors.append("Multiple contact channels")

        supplier['strategic_factors'] = strategic_factors
        supplier['strategic_value_score'] = len(strategic_factors)

    # Display final results
    print(f"\n🎯 PREMIUM COMMERCIAL FURNITURE SUPPLIERS (Top {len(final_suppliers)})")
    print("=" * 80)

    for i, supplier in enumerate(final_suppliers, 1):
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
            'actual_count': len(final_suppliers),
            'region': 'UAE',
            'categories': ['Office', 'Hotel', 'Restaurant', 'Retail'],
            'quality_threshold': '3.5+ rating',
            'tool': 'BOB Google Maps Ultimate V3.0'
        },
        'suppliers': final_suppliers,
        'summary': {
            'total_suppliers': len(final_suppliers),
            'premium_suppliers_4plus': len([s for s in final_suppliers if s['rating'] >= 4.0]),
            'average_rating': sum(s['rating'] for s in final_suppliers) / len(final_suppliers) if final_suppliers else 0,
            'total_estimated_revenue': sum(s['estimated_revenue_aed'] for s in final_suppliers),
            'suppliers_with_website': len([s for s in final_suppliers if s['website'] != 'N/A']),
            'dubai_suppliers': len([s for s in final_suppliers if 'dubai' in s['address'].lower()]),
            'abu_dhabi_suppliers': len([s for s in final_suppliers if 'abu dhabi' in s['address'].lower()])
        }
    }

    # Save to JSON file
    output_file = '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/commercial_furniture_suppliers_leads.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")
    print(f"📈 Total Revenue Potential: AED {output_data['summary']['total_estimated_revenue']:,.0f}")
    print(f"✅ Mission Complete: {len(final_suppliers)} commercial furniture suppliers extracted!")

    return output_data

if __name__ == "__main__":
    main()