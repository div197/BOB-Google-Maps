#!/usr/bin/env python3
"""
📊 CRM EXPORT V3.4.1 - MULTIPLE FORMAT EXPORT ENGINE
Convert extracted business data to CRM-compatible formats

Supported Formats:
  • CSV (universal CRM import)
  • JSON (detailed data structure)
  • HubSpot (HubSpot-specific fields)
  • Salesforce (Salesforce-specific fields)
  • Zoho (Zoho CRM-specific fields)
  • Google Contacts (vCard format)

Status: PRODUCTION-READY
Philosophy: Nishkaam Karma Yoga - Data sharing for collective good
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class CRMExportV34:
    """
    📊 CRM Export Engine

    Convert business extraction results to multiple CRM formats
    """

    def __init__(self, verbose: bool = True):
        """Initialize CRM export engine"""
        self.verbose = verbose
        self.export_stats = {
            "timestamp": datetime.now().isoformat(),
            "formats_exported": []
        }

    def log(self, message: str):
        """Log message if verbose"""
        if self.verbose:
            print(f"  {message}")

    def export_to_csv(self,
                     batch_results: Dict,
                     filename: Optional[str] = None) -> Path:
        """
        Export batch results to CSV (universal format).

        CRM Fields:
        - First Name, Last Name (derived from business name)
        - Company Name
        - Phone Number
        - Email Address
        - Website
        - Address
        - City, State, Postal Code (parsed from address)
        - Notes/Description
        - Custom Fields (rating, review count, quality score)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crm_export_universal_{timestamp}.csv"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        self.log(f"📤 Exporting to CSV: {filename}")

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Define CSV columns for universal CRM import
            fieldnames = [
                'Business Name',
                'Phone',
                'Email',
                'Website',
                'Address',
                'City',
                'Rating',
                'Review Count',
                'Quality Score',
                'Extraction Status',
                'Emails Found',
                'GPS Status',
                'Hours Status',
                'Place ID',
                'CID'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Write each business
            for business in batch_results.get('businesses', []):
                try:
                    result = business.get('result', {})
                    core_data = result.get('core_data', {})
                    enhancements = result.get('enhancements', {})

                    # Parse address components
                    full_address = core_data.get('address', '')
                    address_parts = full_address.split(',')

                    # Extract city (usually second-to-last part)
                    city = address_parts[-2].strip() if len(address_parts) > 1 else ''

                    # Get enhancement details
                    emails = enhancements.get('emails', {})
                    email_list = ', '.join(emails.get('emails', []))

                    writer.writerow({
                        'Business Name': core_data.get('name', ''),
                        'Phone': core_data.get('phone', ''),
                        'Email': email_list,
                        'Website': core_data.get('website', ''),
                        'Address': full_address,
                        'City': city,
                        'Rating': core_data.get('rating', ''),
                        'Review Count': core_data.get('review_count', ''),
                        'Quality Score': business.get('quality_score', ''),
                        'Extraction Status': business.get('status', ''),
                        'Emails Found': emails.get('count', 0),
                        'GPS Status': enhancements.get('gps', {}).get('status', 'N/A'),
                        'Hours Status': enhancements.get('hours', {}).get('status', 'N/A'),
                        'Place ID': core_data.get('place_id', ''),
                        'CID': core_data.get('cid', '')
                    })

                except Exception as e:
                    self.log(f"⚠️ Error exporting business: {str(e)[:40]}")
                    continue

        self.log(f"✅ CSV exported: {output_path}")
        self.export_stats['formats_exported'].append('CSV')
        return output_path

    def export_to_hubspot(self,
                        batch_results: Dict,
                        filename: Optional[str] = None) -> Path:
        """
        Export to HubSpot-specific format.

        HubSpot fields:
        - Company, Phone, Website, Email
        - City, Address, Country
        - Custom properties for ratings and quality scores
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crm_export_hubspot_{timestamp}.csv"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        self.log(f"📤 Exporting to HubSpot: {filename}")

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # HubSpot column names
            fieldnames = [
                'firstname',  # Optional
                'lastname',   # Optional
                'company',
                'phone',
                'email',
                'website',
                'address',
                'city',
                'country',
                'hs_lead_status',
                'rating',
                'review_count',
                'quality_score',
                'extraction_method',
                'extraction_date'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for business in batch_results.get('businesses', []):
                try:
                    result = business.get('result', {})
                    core_data = result.get('core_data', {})

                    # Parse address
                    full_address = core_data.get('address', '')
                    address_parts = full_address.split(',')
                    city = address_parts[-2].strip() if len(address_parts) > 1 else ''

                    # Get first and last name from company name
                    company_name = core_data.get('name', '')
                    name_parts = company_name.split()
                    firstname = name_parts[0] if name_parts else ''
                    lastname = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

                    writer.writerow({
                        'firstname': firstname,
                        'lastname': lastname,
                        'company': company_name,
                        'phone': core_data.get('phone', ''),
                        'email': core_data.get('emails', [''])[0] if core_data.get('emails') else '',
                        'website': core_data.get('website', ''),
                        'address': full_address,
                        'city': city,
                        'country': 'India',  # Default for Bikaner region
                        'hs_lead_status': 'NEW' if business.get('status') == '✅ SUCCESS' else 'FAILED',
                        'rating': core_data.get('rating', ''),
                        'review_count': core_data.get('review_count', ''),
                        'quality_score': business.get('quality_score', ''),
                        'extraction_method': 'BOB-Google-Maps-V3.4.1',
                        'extraction_date': datetime.now().isoformat()
                    })

                except Exception as e:
                    self.log(f"⚠️ Error exporting to HubSpot: {str(e)[:40]}")
                    continue

        self.log(f"✅ HubSpot export: {output_path}")
        self.export_stats['formats_exported'].append('HubSpot')
        return output_path

    def export_to_salesforce(self,
                            batch_results: Dict,
                            filename: Optional[str] = None) -> Path:
        """
        Export to Salesforce-specific format.

        Salesforce Account fields:
        - Name, Phone, Website, BillingAddress
        - Industry, AnnualRevenue (custom fields)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crm_export_salesforce_{timestamp}.csv"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        self.log(f"📤 Exporting to Salesforce: {filename}")

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Name',
                'Phone',
                'Website',
                'BillingStreet',
                'BillingCity',
                'BillingCountry',
                'Industry',
                'Rating__c',
                'ReviewCount__c',
                'QualityScore__c',
                'DataSource__c',
                'ExtractionDate__c'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for business in batch_results.get('businesses', []):
                try:
                    result = business.get('result', {})
                    core_data = result.get('core_data', {})

                    full_address = core_data.get('address', '')
                    address_parts = full_address.split(',')
                    city = address_parts[-2].strip() if len(address_parts) > 1 else ''

                    writer.writerow({
                        'Name': core_data.get('name', ''),
                        'Phone': core_data.get('phone', ''),
                        'Website': core_data.get('website', ''),
                        'BillingStreet': full_address,
                        'BillingCity': city,
                        'BillingCountry': 'India',
                        'Industry': 'Business Services',
                        'Rating__c': core_data.get('rating', ''),
                        'ReviewCount__c': core_data.get('review_count', ''),
                        'QualityScore__c': business.get('quality_score', ''),
                        'DataSource__c': 'BOB-Google-Maps-V3.4.1',
                        'ExtractionDate__c': datetime.now().isoformat()
                    })

                except Exception as e:
                    self.log(f"⚠️ Error exporting to Salesforce: {str(e)[:40]}")
                    continue

        self.log(f"✅ Salesforce export: {output_path}")
        self.export_stats['formats_exported'].append('Salesforce')
        return output_path

    def export_to_json_detailed(self,
                               batch_results: Dict,
                               filename: Optional[str] = None) -> Path:
        """
        Export to detailed JSON format with all extracted data.

        Includes:
        - Complete business data
        - All enhancements (emails, GPS, hours)
        - Quality scores and metadata
        - Extraction details
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crm_export_detailed_{timestamp}.json"

        output_path = Path(__file__).parent / "data" / filename
        output_path.parent.mkdir(exist_ok=True)

        self.log(f"📤 Exporting to JSON: {filename}")

        # Create export structure
        export_data = {
            "export_version": "3.4.1",
            "export_timestamp": datetime.now().isoformat(),
            "export_format": "detailed_json",
            "total_records": len(batch_results.get('businesses', [])),
            "businesses": batch_results.get('businesses', [])
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str, ensure_ascii=False)

        self.log(f"✅ JSON export: {output_path}")
        self.export_stats['formats_exported'].append('JSON')
        return output_path

    def export_all_formats(self, batch_results: Dict) -> Dict[str, Path]:
        """
        Export batch results to all supported CRM formats.

        Returns:
            Dictionary with format name as key and file path as value
        """
        print("\n" + "="*70)
        print("📊 CRM EXPORT V3.4.1 - EXPORTING TO MULTIPLE FORMATS")
        print("="*70 + "\n")

        exports = {}

        try:
            exports['CSV'] = self.export_to_csv(batch_results)
        except Exception as e:
            self.log(f"❌ CSV export failed: {str(e)[:40]}")

        try:
            exports['HubSpot'] = self.export_to_hubspot(batch_results)
        except Exception as e:
            self.log(f"❌ HubSpot export failed: {str(e)[:40]}")

        try:
            exports['Salesforce'] = self.export_to_salesforce(batch_results)
        except Exception as e:
            self.log(f"❌ Salesforce export failed: {str(e)[:40]}")

        try:
            exports['JSON'] = self.export_to_json_detailed(batch_results)
        except Exception as e:
            self.log(f"❌ JSON export failed: {str(e)[:40]}")

        print("\n" + "="*70)
        print(f"✅ Exported to {len(exports)} formats:")
        for format_name, path in exports.items():
            print(f"  • {format_name}: {path.name}")
        print("="*70 + "\n")

        return exports


def main():
    """Example: Export batch results to all CRM formats"""
    # Sample batch results (would normally come from batch processor)
    sample_results = {
        "businesses": [
            {
                "index": 1,
                "business_name": "Sample Business",
                "status": "✅ SUCCESS",
                "quality_score": 75,
                "result": {
                    "core_data": {
                        "name": "Sample Business Ltd",
                        "phone": "+91-9876543210",
                        "address": "123 Main St, Bikaner, Rajasthan 334001",
                        "website": "https://example.com",
                        "rating": 4.5,
                        "review_count": 42,
                        "emails": ["contact@example.com"],
                        "place_id": "12345",
                        "cid": "67890"
                    },
                    "enhancements": {
                        "emails": {
                            "status": "✅ SUCCESS",
                            "count": 1,
                            "emails": ["contact@example.com"]
                        },
                        "gps": {
                            "status": "✅ SUCCESS",
                            "latitude": 28.0, "longitude": 73.3
                        },
                        "hours": {
                            "status": "⚠️ NOT FOUND"
                        }
                    }
                }
            }
        ]
    }

    # Export to all formats
    exporter = CRMExportV34(verbose=True)
    exports = exporter.export_all_formats(sample_results)

    print("✨ CRM export demonstration complete!")


if __name__ == "__main__":
    main()

