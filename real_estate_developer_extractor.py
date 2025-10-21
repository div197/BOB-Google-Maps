#!/usr/bin/env python3
"""
Real Estate Developers Lead Extraction - BOB Google Maps Ultimate V3.0
Specialized tool for extracting premium real estate developers across UAE

Target: 10 NEW real estate development companies
Focus: Large-scale residential and commercial projects
Quality threshold: 4.0+ rating minimum
"""

import json
import sys
import os
from datetime import datetime
from bob import HybridExtractorOptimized

class RealEstateDeveloperExtractor:
    def __init__(self):
        """Initialize the extractor with BOB Ultimate V3.0."""
        self.extractor = HybridExtractorOptimized()
        self.developers = []
        self.extraction_stats = {
            'total_searches': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'high_quality_leads': 0
        }

    def extract_developer(self, search_query, location_focus=""):
        """
        Extract a real estate developer using BOB Ultimate V3.0.

        Args:
            search_query (str): Search query for the developer
            location_focus (str): Specific location focus

        Returns:
            dict: Developer data or None if extraction failed
        """
        self.extraction_stats['total_searches'] += 1

        try:
            print(f"🔍 Extracting: {search_query}")

            # Use BOB Ultimate V3.0 for extraction
            result = self.extractor.extract_business(
                search_query,
                include_reviews=True,
                max_reviews=10
            )

            if result and result.get('success'):
                # The result is already the business data dictionary
                business = result

                # Quality threshold check (4.0+ rating)
                if business.get('rating') and business['rating'] >= 4.0:
                    developer_data = {
                        'extractor_version': 'BOB Ultimate V3.0',
                        'extraction_date': datetime.now().isoformat(),
                        'search_query': search_query,
                        'location_focus': location_focus,

                        # Core Business Information
                        'company_name': business.get('name'),
                        'rating': business.get('rating'),
                        'review_count': business.get('review_count'),
                        'address': business.get('address'),
                        'phone': business.get('phone'),
                        'website': business.get('website'),
                        'emails': business.get('emails', []),  # Will be enhanced later if available
                        'category': business.get('category'),

                        # Location Data
                        'latitude': business.get('latitude'),
                        'longitude': business.get('longitude'),
                        'place_id': business.get('cid'),

                        # Rich Media
                        'photos_count': len(business.get('photos', [])),
                        'photos': business.get('photos', [])[:5],  # Top 5 photos

                        # Customer Reviews Analysis
                        'reviews_count': len(business.get('reviews', [])),
                        'recent_reviews': [
                            {
                                'reviewer': review.get('reviewer_name', review.get('reviewer', 'N/A')),
                                'rating': review.get('rating_text', str(review.get('rating', 'N/A'))),
                                'text': (review.get('review_text', review.get('text', ''))[:200] + "...") if len(review.get('review_text', review.get('text', ''))) > 200 else review.get('review_text', review.get('text', '')),
                                'date': review.get('review_date', review.get('date', 'N/A'))
                            }
                            for review in business.get('reviews', [])[:5]
                        ],

                        # Quality Metrics
                        'data_quality_score': business.get('data_quality_score', 85),

                        # Interior Design Potential Analysis
                        'interior_design_potential': {
                            'revenue_potential_aed': self._estimate_revenue_potential(business),
                            'project_types': self._analyze_project_types(business),
                            'partnership_value': self._assess_partnership_value(business),
                            'contact_priority': self._determine_contact_priority(business)
                        }
                    }

                    self.extraction_stats['successful_extractions'] += 1
                    self.extraction_stats['high_quality_leads'] += 1

                    print(f"✅ Successfully extracted: {business.get('name')} (Rating: {business.get('rating')})")
                    return developer_data
                else:
                    print(f"⚠️  Low rating ({business.get('rating')}) - Skipping: {business.get('name')}")
                    self.extraction_stats['failed_extractions'] += 1
                    return None
            else:
                print(f"❌ Failed to extract: {search_query}")
                self.extraction_stats['failed_extractions'] += 1
                return None

        except Exception as e:
            print(f"❌ Exception extracting {search_query}: {str(e)}")
            self.extraction_stats['failed_extractions'] += 1
            return None

    def _estimate_revenue_potential(self, business):
        """Estimate interior design revenue potential (AED 5-10M per developer)."""
        base_potential = 5000000  # AED 5M base

        # Rating multiplier
        rating = business.get('rating', 0)
        if rating >= 4.8:
            multiplier = 2.0  # AED 10M
        elif rating >= 4.5:
            multiplier = 1.5  # AED 7.5M
        else:
            multiplier = 1.0  # AED 5M

        # Review count influence
        if business.get('review_count', 0) >= 100:
            multiplier *= 1.2

        return int(base_potential * multiplier)

    def _analyze_project_types(self, business):
        """Analyze likely project types based on business category and reviews."""
        project_types = []

        category = business.get('category', '')
        category_lower = category.lower() if category else ""

        if 'villa' in category_lower or 'residential' in category_lower:
            project_types.append('Luxury Villas')
        if 'apartment' in category_lower or 'tower' in category_lower:
            project_types.append('High-Rise Apartments')
        if 'commercial' in category_lower or 'office' in category_lower:
            project_types.append('Commercial Buildings')
        if 'mixed' in category_lower:
            project_types.append('Mixed-Use Developments')

        # Analyze reviews for project type clues
        reviews = business.get('reviews', [])
        if reviews:
            review_text = ' '.join([review.get('review_text', review.get('text', '')).lower() for review in reviews[:5]])
            if 'villa' in review_text:
                project_types.append('Luxury Villas')
            if 'apartment' in review_text or 'tower' in review_text:
                project_types.append('High-Rise Apartments')
            if 'commercial' in review_text or 'office' in review_text:
                project_types.append('Commercial Buildings')

        return list(set(project_types)) if project_types else ['Mixed-Use Developments']

    def _assess_partnership_value(self, business):
        """Assess strategic partnership value."""
        rating = business.get('rating', 0)
        review_count = business.get('review_count', 0)

        if rating >= 4.8 and review_count >= 50:
            return 'HIGH - Premium developer with excellent reputation'
        elif rating >= 4.5:
            return 'MEDIUM - Quality developer with good market presence'
        else:
            return 'STANDARD - Reliable developer for project pipeline'

    def _determine_contact_priority(self, business):
        """Determine contact priority based on developer quality."""
        rating = business.get('rating', 0)

        if rating >= 4.8:
            return 'IMMEDIATE - Top-tier developer, high-value target'
        elif rating >= 4.5:
            return 'HIGH - Quality developer, strong potential'
        else:
            return 'MEDIUM - Standard developer, steady pipeline'

    def extract_multiple_developers(self, search_queries):
        """Extract multiple real estate developers."""
        print("🏗️  REAL ESTATE DEVELOPERS LEAD EXTRACTION - BOB ULTIMATE V3.0")
        print("=" * 70)
        print(f"🎯 Target: 10 premium real estate developers")
        print(f"📊 Quality threshold: 4.0+ rating minimum")
        print(f"💰 Revenue potential: AED 5-10M per developer")
        print("=" * 70)

        for query in search_queries:
            if len(self.developers) >= 10:  # Stop when we have 10 developers
                break

            developer = self.extract_developer(query['query'], query.get('location', ''))
            if developer:
                self.developers.append(developer)
                print(f"📊 Progress: {len(self.developers)}/10 developers extracted")

        return self.developers

    def save_results(self, filename="real_estate_developers_leads.json"):
        """Save extraction results to JSON file."""
        # Create comprehensive report
        report_data = {
            'extraction_metadata': {
                'extractor_version': 'BOB Google Maps Ultimate V3.0',
                'extraction_date': datetime.now().isoformat(),
                'mission': 'Real Estate Developers Lead Extraction',
                'target_count': 10,
                'actual_count': len(self.developers),
                'quality_threshold': '4.0+ rating',
                'location_focus': 'UAE (Dubai, Abu Dhabi, etc.)'
            },
            'extraction_statistics': self.extraction_stats,
            'developers': self.developers,
            'strategic_analysis': self._generate_strategic_analysis()
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Results saved to: {filename}")
        return filename

    def _generate_strategic_analysis(self):
        """Generate strategic analysis of extracted developers."""
        if not self.developers:
            return {}

        total_revenue_potential = sum(dev['interior_design_potential']['revenue_potential_aed']
                                    for dev in self.developers)

        high_value_developers = [dev for dev in self.developers
                               if dev['interior_design_potential']['revenue_potential_aed'] >= 7500000]

        project_types = {}
        for dev in self.developers:
            for ptype in dev['interior_design_potential']['project_types']:
                project_types[ptype] = project_types.get(ptype, 0) + 1

        return {
            'total_revenue_potential_aed': total_revenue_potential,
            'average_revenue_potential_aed': total_revenue_potential // len(self.developers),
            'high_value_developers_count': len(high_value_developers),
            'project_type_distribution': project_types,
            'recommended_approach': {
                'immediate_contacts': len([dev for dev in self.developers
                                         if 'IMMEDIATE' in dev['interior_design_potential']['contact_priority']]),
                'high_priority_contacts': len([dev for dev in self.developers
                                             if 'HIGH' in dev['interior_design_potential']['contact_priority']]),
                'total_market_opportunity': f"AED {total_revenue_potential:,}".replace(',', ',')
            }
        }

def main():
    """Main extraction function."""
    # Define search strategy for real estate developers
    search_queries = [
        {'query': 'Emaar Properties Dubai', 'location': 'Dubai'},
        {'query': 'Damac Properties Dubai', 'location': 'Dubai'},
        {'query': 'Aldar Properties Abu Dhabi', 'location': 'Abu Dhabi'},
        {'query': 'Meraas Dubai', 'location': 'Dubai'},
        {'query': 'Nakheel Dubai', 'location': 'Dubai'},
        {'query': 'Dubai Properties', 'location': 'Dubai'},
        {'query': 'Emaar Beachfront Dubai', 'location': 'Dubai'},
        {'query': 'Damac Hills Dubai', 'location': 'Dubai'},
        {'query': 'Yas Island Abu Dhabi', 'location': 'Abu Dhabi'},
        {'query': 'Dubai South Properties', 'location': 'Dubai'},
        {'query': 'Meydan Dubai', 'location': 'Dubai'},
        {'query': 'Al Habtoor Group Dubai', 'location': 'Dubai'}
    ]

    # Initialize extractor
    extractor = RealEstateDeveloperExtractor()

    # Extract developers
    developers = extractor.extract_multiple_developers(search_queries)

    # Save results
    if developers:
        filename = extractor.save_results()

        # Print summary
        print(f"\n🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
        print(f"📊 Total Developers Extracted: {len(developers)}")
        print(f"💰 Total Revenue Potential: AED {sum(dev['interior_design_potential']['revenue_potential_aed'] for dev in developers):,}")
        print(f"📈 Average Quality Score: {sum(dev['data_quality_score'] for dev in developers) // len(developers)}/100")
        print(f"📁 Results saved: {filename}")

        # Show top 3 developers by revenue potential
        top_developers = sorted(developers,
                              key=lambda x: x['interior_design_potential']['revenue_potential_aed'],
                              reverse=True)[:3]

        print(f"\n🏆 TOP 3 DEVELOPERS BY REVENUE POTENTIAL:")
        for i, dev in enumerate(top_developers, 1):
            potential = dev['interior_design_potential']['revenue_potential_aed']
            print(f"{i}. {dev['company_name']} - AED {potential:,}")
    else:
        print("\n❌ No developers extracted. Please check search queries.")

if __name__ == "__main__":
    main()