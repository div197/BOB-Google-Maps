#!/usr/bin/env python3
"""
Example 5: Export to Different Formats

This example demonstrates how to export extracted business data
to various formats (JSON, CSV, Excel, CRM formats).

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob import HybridExtractor
import json
import csv
from pathlib import Path


def main():
    """Extract and export business data to multiple formats."""

    print("🔱 BOB Google Maps - Export Formats Example")
    print("=" * 60)

    # Create output directory
    output_dir = Path("output_exports")
    output_dir.mkdir(exist_ok=True)

    # Extract a business
    extractor = HybridExtractor()
    business_query = "Apple Store Fifth Avenue New York"

    print(f"\n📍 Extracting: {business_query}")
    result = extractor.extract_business(business_query, include_reviews=True, max_reviews=5)

    if not result.get('success'):
        print(f"❌ Extraction failed: {result.get('error')}")
        return

    business = result['business']
    print(f"✅ Extracted: {business.name}")

    # Export to JSON
    print(f"\n{'─' * 60}")
    print("📄 Exporting to JSON...")

    json_file = output_dir / f"{business.name.replace(' ', '_')}_detailed.json"
    business_dict = {
        "name": business.name,
        "phone": business.phone,
        "emails": business.emails,
        "website": business.website,
        "address": business.address,
        "latitude": business.latitude,
        "longitude": business.longitude,
        "rating": business.rating,
        "review_count": business.review_count,
        "category": business.category,
        "price_range": business.price_range,
        "hours": business.hours,
        "place_id": business.place_id,
        "cid": business.cid,
        "data_quality_score": business.data_quality_score,
        "reviews": [
            {
                "reviewer": r.reviewer,
                "rating": r.rating,
                "text": r.text,
                "date": r.review_date
            }
            for r in business.reviews
        ] if business.reviews else [],
        "extraction_metadata": {
            "extracted_at": str(business.extracted_at),
            "extraction_time_seconds": result.get('extraction_time_seconds'),
            "extraction_method": result.get('method'),
            "extractor_version": business.extractor_version
        }
    }

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(business_dict, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON saved: {json_file}")

    # Export to CSV (basic info)
    print(f"\n📊 Exporting to CSV...")

    csv_file = output_dir / f"{business.name.replace(' ', '_')}_basic.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name', 'Phone', 'Email', 'Website', 'Address',
            'Rating', 'Reviews', 'Category', 'Quality Score'
        ])
        writer.writerow([
            business.name,
            business.phone or '',
            ', '.join(business.emails) if business.emails else '',
            business.website or '',
            business.address or '',
            business.rating or '',
            business.review_count or 0,
            business.category or '',
            business.data_quality_score
        ])

    print(f"✅ CSV saved: {csv_file}")

    # Export to CRM-friendly format (HubSpot style)
    print(f"\n🎯 Exporting to CRM format (HubSpot style)...")

    crm_file = output_dir / f"{business.name.replace(' ', '_')}_crm.json"
    crm_format = {
        "properties": {
            "company": business.name,
            "phone": business.phone or "",
            "website": business.website or "",
            "address": business.address or "",
            "city": "",  # Parse from address if needed
            "state": "",  # Parse from address if needed
            "zip": "",  # Parse from address if needed
            "rating": str(business.rating) if business.rating else "",
            "review_count": str(business.review_count) if business.review_count else "0",
            "industry": business.category or "",
            "notes": f"Extracted from Google Maps. Quality Score: {business.data_quality_score}/100"
        },
        "contacts": [
            {
                "email": email,
                "properties": {
                    "company": business.name,
                    "phone": business.phone or ""
                }
            }
            for email in (business.emails or [])
        ]
    }

    with open(crm_file, 'w', encoding='utf-8') as f:
        json.dump(crm_format, f, indent=2, ensure_ascii=False)

    print(f"✅ CRM format saved: {crm_file}")

    # Export summary
    print(f"\n{'═' * 60}")
    print("📦 Export Summary")
    print(f"{'═' * 60}")
    print(f"📄 JSON (Detailed): {json_file.name}")
    print(f"📊 CSV (Basic): {csv_file.name}")
    print(f"🎯 CRM Format: {crm_file.name}")
    print(f"\n📁 All files saved to: {output_dir.absolute()}")

    print(f"\n{'═' * 60}")
    print("✅ Export completed!")


if __name__ == "__main__":
    main()
