#!/usr/bin/env python3
"""
Example 6: Export to Multiple Formats

Export extraction results to CSV, Excel, and SQLite.
"""

import asyncio
import json
from pathlib import Path
from bob import PlaywrightExtractorOptimized
from bob.utils.exporters import (
    export_to_csv,
    export_to_sqlite,
    export_to_json,
    export_all_formats,
)


async def main():
    """Extract and export to multiple formats."""
    
    print("🔱 BOB Google Maps v4.3.0 - Multi-Format Export")
    print("=" * 60)
    
    extractor = PlaywrightExtractorOptimized(headless=True)
    
    # Extract some businesses
    queries = [
        "Starbucks Times Square NYC",
        "Apple Store Fifth Avenue NYC",
        "Empire State Building NYC",
    ]
    
    results = []
    
    print(f"\n📋 Extracting {len(queries)} businesses...\n")
    
    for query in queries:
        print(f"   Extracting: {query}...")
        result = await extractor.extract_business_optimized(query, include_reviews=False)
        
        if result.get('success'):
            results.append(result)
            print(f"   ✅ {result.get('name')}")
        
        await asyncio.sleep(2)
    
    if not results:
        print("❌ No successful extractions")
        return
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("\n" + "=" * 60)
    print("📁 EXPORTING TO MULTIPLE FORMATS")
    print("=" * 60)
    
    # Export to JSON
    json_path = export_to_json(results, "output/businesses.json")
    
    # Export to CSV (spreadsheet compatible)
    csv_path = export_to_csv(results, "output/businesses.csv")
    
    # Export to SQLite (database)
    db_path = export_to_sqlite(results, "output/businesses.db")
    
    # Try Excel if openpyxl is installed
    try:
        from bob.utils.exporters import export_to_excel
        excel_path = export_to_excel(results, "output/businesses.xlsx")
    except ImportError:
        print("⚠️ Excel export skipped (install openpyxl for Excel support)")
    
    print("\n" + "=" * 60)
    print("✅ EXPORT COMPLETE")
    print("=" * 60)
    print(f"   📄 JSON:   output/businesses.json")
    print(f"   📊 CSV:    output/businesses.csv")
    print(f"   🗄️ SQLite: output/businesses.db")
    
    # Quick demo: Read from SQLite
    import sqlite3
    conn = sqlite3.connect("output/businesses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, rating, phone FROM businesses")
    rows = cursor.fetchall()
    conn.close()
    
    print("\n📊 Data from SQLite:")
    for row in rows:
        print(f"   • {row[0]} - Rating: {row[1]} - Phone: {row[2]}")


if __name__ == "__main__":
    asyncio.run(main())
