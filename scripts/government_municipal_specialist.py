#!/usr/bin/env python3
"""
🏛️ GOVERNMENT & MUNICIPAL PROJECTS SPECIALIST AGENT
UAE Government Entities Extraction - Interior Design Services Targeting

MISSION: Extract 6 premium government entities and municipal projects across UAE
requiring interior design services with complete contact information.

TARGET CATEGORIES:
- Municipalities
- Government departments
- Public projects
- Government project managers and decision-makers

QUALITY THRESHOLD: 4.0+ rating minimum
REVENUE POTENTIAL: AED 5-15M per government project

Created: October 9, 2025
Version: 1.0 Government Specialist
"""

import json
import time
from datetime import datetime
from bob.extractors import HybridExtractor


class GovernmentMunicipalSpecialist:
    """Specialist agent for UAE government entities and municipal projects extraction."""

    def __init__(self):
        self.version = "1.0 Government Specialist"
        self.mission_date = "October 9, 2025"
        self.extractor = HybridExtractor(use_cache=True, prefer_playwright=True)

        # Target government entities search strategy
        self.search_targets = [
            "Dubai Municipality Head Office",
            "Abu Dhabi Municipality",
            "Government Projects Department Dubai",
            "Public Works Authority UAE",
            "Municipality Office Sharjah",
            "Government Interior Design Projects"
        ]

        self.results = []
        self.revenue_analysis = {
            "total_potential_revenue": 0,
            "avg_project_value": 0,
            "high_value_leads": []
        }

    def extract_all_government_entities(self):
        """Extract all target government entities."""
        print(f"""
{'='*100}
🏛️ GOVERNMENT & MUNICIPAL PROJECTS SPECIALIST AGENT
{'='*100}
Mission Date: {self.mission_date}
Version: {self.version}
Target: 6 Premium Government Entities
Focus: Large-scale development projects requiring interior design
Revenue Potential: AED 5-15M per project
Quality Threshold: 4.0+ rating minimum
{'='*100}
        """)

        start_time = time.time()

        for i, target in enumerate(self.search_targets, 1):
            print(f"""
{'='*60}
🎯 TARGET {i}/6: {target}
{'='*60}
            """)

            try:
                # Extract government entity data
                result = self.extractor.extract_business(
                    target,
                    force_fresh=True,  # Get fresh data for government entities
                    include_reviews=True,
                    max_reviews=10
                )

                if result.get('success'):
                    # Analyze government entity for interior design potential
                    analysis = self._analyze_government_entity(result)
                    result['government_analysis'] = analysis

                    # Add to results if meets quality threshold
                    if analysis['quality_score'] >= 4.0:
                        self.results.append(result)
                        print(f"✅ QUALIFIED: {result['name']} (Rating: {result.get('rating', 'N/A')})")

                        # Update revenue analysis
                        self._update_revenue_analysis(analysis)
                    else:
                        print(f"❌ DISQUALIFIED: {result['name']} (Rating: {result.get('rating', 'N/A')} < 4.0)")
                else:
                    print(f"❌ EXTRACTION FAILED: {result.get('error', 'Unknown error')}")

            except Exception as e:
                print(f"❌ SYSTEM ERROR: {str(e)}")

            # Brief pause between extractions
            if i < len(self.search_targets):
                time.sleep(2)

        total_time = time.time() - start_time

        # Display mission summary
        self._display_mission_summary(total_time)

        # Save results
        self._save_government_leads()

        return self.results

    def _analyze_government_entity(self, entity):
        """Analyze government entity for interior design project potential."""
        analysis = {
            'entity_type': self._classify_entity_type(entity),
            'project_potential': self._assess_project_potential(entity),
            'contact_quality': self._assess_contact_quality(entity),
            'revenue_potential': self._estimate_revenue_potential(entity),
            'strategic_value': self._assess_strategic_value(entity),
            'quality_score': self._calculate_quality_score(entity),
            'target_contacts': self._extract_target_contacts(entity),
            'likely_projects': self._identify_likely_projects(entity)
        }

        return analysis

    def _classify_entity_type(self, entity):
        """Classify the type of government entity."""
        name = entity.get('name', '').lower()
        category = entity.get('category', '').lower()

        if 'municipality' in name:
            return 'Municipal Government'
        elif 'public works' in name or 'authority' in name:
            return 'Public Works Authority'
        elif 'government projects' in name or 'projects department' in name:
            return 'Projects Department'
        elif 'interior design' in name:
            return 'Government Design Services'
        else:
            return 'General Government Entity'

    def _assess_project_potential(self, entity):
        """Assess interior design project potential."""
        name = entity.get('name', '').lower()
        category = entity.get('category', '').lower()
        review_count = entity.get('review_count', 0)

        # High potential indicators
        high_potential_keywords = [
            'municipality', 'public works', 'government projects',
            'development', 'planning', 'infrastructure'
        ]

        potential_score = 0
        for keyword in high_potential_keywords:
            if keyword in name or keyword in category:
                potential_score += 2

        # Review volume indicates activity level
        if review_count > 100:
            potential_score += 2
        elif review_count > 50:
            potential_score += 1

        if potential_score >= 4:
            return 'HIGH'
        elif potential_score >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _assess_contact_quality(self, entity):
        """Assess quality of contact information."""
        contact_score = 0

        if entity.get('phone'):
            contact_score += 1
        if entity.get('website'):
            contact_score += 1
        if entity.get('emails'):
            contact_score += 2
        if entity.get('address'):
            contact_score += 1

        if contact_score >= 4:
            return 'EXCELLENT'
        elif contact_score >= 3:
            return 'GOOD'
        elif contact_score >= 2:
            return 'FAIR'
        else:
            return 'POOR'

    def _estimate_revenue_potential(self, entity):
        """Estimate revenue potential for interior design projects."""
        entity_type = self._classify_entity_type(entity)
        project_potential = self._assess_project_potential(entity)

        # Base revenue estimates by entity type
        revenue_estimates = {
            'Municipal Government': {'min': 10_000_000, 'max': 25_000_000},  # AED 10-25M
            'Public Works Authority': {'min': 8_000_000, 'max': 20_000_000},   # AED 8-20M
            'Projects Department': {'min': 5_000_000, 'max': 15_000_000},      # AED 5-15M
            'Government Design Services': {'min': 3_000_000, 'max': 10_000_000}, # AED 3-10M
            'General Government Entity': {'min': 2_000_000, 'max': 8_000_000}    # AED 2-8M
        }

        base_range = revenue_estimates.get(entity_type, {'min': 2_000_000, 'max': 8_000_000})

        # Adjust based on project potential
        multiplier = 1.0
        if project_potential == 'HIGH':
            multiplier = 1.5
        elif project_potential == 'MEDIUM':
            multiplier = 1.0
        else:
            multiplier = 0.7

        return {
            'min_revenue': int(base_range['min'] * multiplier),
            'max_revenue': int(base_range['max'] * multiplier),
            'avg_revenue': int((base_range['min'] + base_range['max']) / 2 * multiplier)
        }

    def _assess_strategic_value(self, entity):
        """Assess strategic value for government partnerships."""
        name = entity.get('name', '').lower()
        rating = float(entity.get('rating', 0))

        strategic_factors = {
            'dubai municipality': 10,  # Most strategic
            'abu dhabi municipality': 9,
            'public works': 8,
            'government projects': 8,
            'sharjah municipality': 7
        }

        base_score = 5  # Default strategic value
        for keyword, score in strategic_factors.items():
            if keyword in name:
                base_score = score
                break

        # Adjust based on rating
        if rating >= 4.5:
            base_score += 2
        elif rating >= 4.0:
            base_score += 1

        if base_score >= 9:
            return 'CRITICAL'
        elif base_score >= 7:
            return 'HIGH'
        elif base_score >= 5:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _calculate_quality_score(self, entity):
        """Calculate overall quality score (0-5)."""
        rating = float(entity.get('rating', 0))
        review_count = entity.get('review_count', 0)
        has_website = bool(entity.get('website'))
        has_phone = bool(entity.get('phone'))
        has_email = bool(entity.get('emails'))

        # Base score from rating
        score = rating

        # Bonus factors
        if review_count > 100:
            score += 0.2
        elif review_count > 50:
            score += 0.1

        if has_website:
            score += 0.2
        if has_phone:
            score += 0.2
        if has_email:
            score += 0.4

        # Cap at 5.0
        return min(score, 5.0)

    def _extract_target_contacts(self, entity):
        """Extract target contact information."""
        contacts = {
            'primary_phone': entity.get('phone'),
            'website': entity.get('website'),
            'emails': entity.get('emails', []),
            'address': entity.get('address'),
            'location': {
                'latitude': entity.get('latitude'),
                'longitude': entity.get('longitude')
            }
        }

        return contacts

    def _identify_likely_projects(self, entity):
        """Identify likely interior design projects."""
        entity_type = self._classify_entity_type(entity)

        project_types = {
            'Municipal Government': [
                'Government office buildings',
                'Public service centers',
                'Municipality facilities',
                'Community centers',
                'Administrative buildings'
            ],
            'Public Works Authority': [
                'Public infrastructure facilities',
                'Government service buildings',
                'Maintenance facilities',
                'Public utility buildings',
                'Transportation hubs'
            ],
            'Projects Department': [
                'New government developments',
                'Renovation projects',
                'Public space improvements',
                'Government facility upgrades',
                'Civic building projects'
            ],
            'Government Design Services': [
                'Interior design contracts',
                'Design consultancy projects',
                'Space planning projects',
                'Design oversight contracts',
                'Design standards development'
            ]
        }

        return project_types.get(entity_type, ['General government projects'])

    def _update_revenue_analysis(self, analysis):
        """Update revenue analysis with entity data."""
        revenue = analysis['revenue_potential']
        self.revenue_analysis['total_potential_revenue'] += revenue['avg_revenue']

        if revenue['avg_revenue'] >= 10_000_000:  # AED 10M+
            self.revenue_analysis['high_value_leads'].append(analysis)

    def _display_mission_summary(self, total_time):
        """Display comprehensive mission summary."""
        qualified_count = len(self.results)

        print(f"""
{'='*100}
🏛️ GOVERNMENT EXTRACTION MISSION COMPLETE
{'='*100}
Mission Duration: {total_time:.1f} seconds
Targets Processed: {len(self.search_targets)}
Qualified Entities: {qualified_count}
Quality Threshold: 4.0+ rating

REVENUE ANALYSIS:
  Total Potential Revenue: AED {self.revenue_analysis['total_potential_revenue']:,}
  Average Project Value: AED {self.revenue_analysis['total_potential_revenue'] // max(qualified_count, 1):,}
  High-Value Leads (≥AED 10M): {len(self.revenue_analysis['high_value_leads'])}

STRATEGIC BREAKDOWN:
""")

        # Count by strategic value
        strategic_counts = {}
        for result in self.results:
            strategic = result['government_analysis']['strategic_value']
            strategic_counts[strategic] = strategic_counts.get(strategic, 0) + 1

        for value, count in strategic_counts.items():
            print(f"  {value}: {count} entities")

        print(f"\n{'='*100}")

    def _save_government_leads(self):
        """Save government leads to JSON file."""
        filename = "government_municipal_projects_leads.json"

        # Prepare comprehensive report
        report_data = {
            'mission_metadata': {
                'mission_date': self.mission_date,
                'version': self.version,
                'specialist': 'Government & Municipal Projects Specialist Agent',
                'total_targets': len(self.search_targets),
                'qualified_entities': len(self.results),
                'quality_threshold': '4.0+ rating',
                'focus_area': 'UAE Government Entities requiring interior design services'
            },
            'revenue_analysis': {
                'total_potential_revenue_aed': self.revenue_analysis['total_potential_revenue'],
                'average_project_value_aed': self.revenue_analysis['total_potential_revenue'] // max(len(self.results), 1),
                'high_value_leads_count': len(self.revenue_analysis['high_value_leads']),
                'revenue_per_lead': self.revenue_analysis['total_potential_revenue'] // max(len(self.results), 1)
            },
            'government_entities': self.results,
            'strategic_recommendations': self._generate_strategic_recommendations()
        }

        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Government leads report saved to: {filename}")

    def _generate_strategic_recommendations(self):
        """Generate strategic recommendations for approaching government entities."""
        recommendations = {
            'priority_approach_order': [],
            'key_value_propositions': [],
            'contact_strategies': [],
            'partnership_opportunities': []
        }

        # Sort entities by strategic value
        sorted_entities = sorted(
            self.results,
            key=lambda x: (
                x['government_analysis']['strategic_value'],
                x['government_analysis']['revenue_potential']['avg_revenue']
            ),
            reverse=True
        )

        # Generate priority approach order
        for entity in sorted_entities:
            priority = {
                'entity_name': entity['name'],
                'strategic_value': entity['government_analysis']['strategic_value'],
                'revenue_potential': entity['government_analysis']['revenue_potential'],
                'contact_quality': entity['government_analysis']['contact_quality']
            }
            recommendations['priority_approach_order'].append(priority)

        # Generate key value propositions
        recommendations['key_value_propositions'] = [
            "Specialized expertise in government facility design and compliance",
            "Proven track record with municipal and public works projects",
            "Understanding of government procurement processes and requirements",
            "Ability to work within government budgets and timelines",
            "Experience with sustainable and accessible public space design"
        ]

        # Generate contact strategies
        recommendations['contact_strategies'] = [
            "Direct approach to facilities management departments",
            "Engagement through official government procurement portals",
            "Networking with municipal planning and development teams",
            "Participation in government vendor registration programs",
            "Collaboration with architecture firms serving government contracts"
        ]

        # Generate partnership opportunities
        recommendations['partnership_opportunities'] = [
            "Long-term facility maintenance and upgrade contracts",
            "Multiple project partnerships across different municipalities",
            "Design-build consortium opportunities",
            "Public-private partnership initiatives",
            "Government design standards consulting"
        ]

        return recommendations


def main():
    """Main execution function."""
    print("🏛️ Initializing Government & Municipal Projects Specialist Agent...")

    specialist = GovernmentMunicipalSpecialist()
    results = specialist.extract_all_government_entities()

    if results:
        print(f"""
🎯 MISSION SUCCESS!
Successfully extracted {len(results)} government entities requiring interior design services.
Ready for strategic business development and partnership outreach.

📊 Next Steps:
1. Review detailed government leads report
2. Prioritize by strategic value and revenue potential
3. Develop tailored proposals for each entity type
4. Initiate contact through appropriate government channels
5. Prepare for government procurement processes

💼 Expected ROI: AED {specialist.revenue_analysis['total_potential_revenue']:,} total potential revenue
        """)
    else:
        print("""
❌ MISSION INCOMPLETE
No qualified government entities met the quality threshold.
Consider expanding search criteria or reviewing target parameters.
        """)


if __name__ == "__main__":
    main()