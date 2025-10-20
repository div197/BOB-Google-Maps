#!/usr/bin/env python3
"""
D Corner Living - Mission Execution Engine

Orchestrates business intelligence missions using BOB Google Maps.
Handles mission planning, execution, and data integration.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import BOB Google Maps
from bob import extract_business

# Import D Corner Living models
from models.entities.business import BusinessIntelligence
from models.orm.database import DatabaseManager


class MissionExecutor:
    """
    Executes business intelligence missions for D Corner Living.
    Coordinates BOB Google Maps extraction with database integration.
    """

    def __init__(self, project_root: Path):
        """
        Initialize mission executor.

        Args:
            project_root: Root path of D Corner Living project
        """
        self.project_root = project_root
        self.db_manager = DatabaseManager()
        self.mission_templates_dir = project_root / "missions" / "templates"
        self.active_missions_dir = project_root / "missions" / "active"
        self.completed_missions_dir = project_root / "missions" / "completed"
        self.raw_data_dir = project_root / "data" / "raw"
        self.processed_data_dir = project_root / "data" / "processed"

        # Ensure directories exist
        for directory in [self.active_missions_dir, self.completed_missions_dir,
                          self.raw_data_dir, self.processed_data_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def load_mission(self, mission_file: Path) -> Dict[str, Any]:
        """
        Load mission configuration from file.

        Args:
            mission_file: Path to mission JSON file

        Returns:
            Mission configuration dictionary
        """
        try:
            with open(mission_file, 'r', encoding='utf-8') as f:
                mission = json.load(f)
            return mission
        except Exception as e:
            print(f"Error loading mission {mission_file}: {e}")
            return {}

    def execute_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a complete business intelligence mission.

        Args:
            mission: Mission configuration dictionary

        Returns:
            Mission execution results
        """
        mission_id = mission['mission_id']
        mission_name = mission['mission_name']

        print(f"🎯 Executing Mission: {mission_name}")
        print(f"📊 Mission ID: {mission_id}")
        print(f"🗺️  Geographic Scope: {mission['geographic_scope']}")
        print(f"🔍 Search Terms: {len(mission['search_terms'])} keywords")
        print("=" * 70)

        # Update mission status to active
        self._update_mission_status(mission_id, "ACTIVE")

        # Create mission-specific directories
        mission_raw_dir = self.raw_data_dir / f"mission_{mission_id}"
        mission_processed_dir = self.processed_data_dir / f"mission_{mission_id}"
        mission_raw_dir.mkdir(exist_ok=True)
        mission_processed_dir.mkdir(exist_ok=True)

        # Initialize execution tracking
        execution_results = {
            'mission_id': mission_id,
            'mission_name': mission_name,
            'start_time': datetime.now().isoformat(),
            'search_terms': mission['search_terms'],
            'target_criteria': mission.get('target_criteria', {}),
            'extractions': [],
            'successful_extractions': 0,
            'failed_extractions': 0,
            'high_quality_leads': 0,
            'businesses_integrated': 0,
            'total_extraction_time': 0,
            'errors': []
        }

        # Execute extractions for each search term
        start_time = time.time()

        for i, search_term in enumerate(mission['search_terms'], 1):
            print(f"\n[{i}/{len(mission['search_terms'])}] Processing: {search_term}")

            try:
                # Extract business using BOB Google Maps
                result = self._extract_business_data(
                    search_term,
                    mission.get('extraction_settings', {})
                )

                if result.get('success'):
                    # Process and integrate the extracted data
                    processed_business = self._process_extracted_data(result, mission)

                    if processed_business:
                        # Save raw data
                        raw_filename = f"raw_{i}_{search_term.replace(' ', '_').lower()}_{int(time.time())}.json"
                        raw_filepath = mission_raw_dir / raw_filename

                        with open(raw_filepath, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2, ensure_ascii=False)

                        # Save processed data
                        processed_filename = f"processed_{i}_{search_term.replace(' ', '_').lower()}_{int(time.time())}.json"
                        processed_filepath = mission_processed_dir / processed_filename

                        with open(processed_filepath, 'w', encoding='utf-8') as f:
                            json.dump(processed_business, f, indent=2, ensure_ascii=False)

                        # Integrate into database
                        if self._integrate_business_data(processed_business, mission):
                            execution_results['businesses_integrated'] += 1

                            # Check if it's a high-quality lead
                            if processed_business['lead_score'] >= mission.get('quality_filters', {}).get('min_lead_score', 60):
                                execution_results['high_quality_leads'] += 1

                        execution_results['successful_extractions'] += 1
                        execution_results['extractions'].append({
                            'search_term': search_term,
                            'status': 'SUCCESS',
                            'business_name': result.get('name', 'Unknown'),
                            'lead_score': processed_business['lead_score'],
                            'data_quality_score': processed_business['data_quality_score'],
                            'raw_file': str(raw_filepath),
                            'processed_file': str(processed_filepath)
                        })

                        print(f"   ✅ {result.get('name', 'Unknown')} - Lead Score: {processed_business['lead_score']}/100")

                    else:
                        execution_results['failed_extractions'] += 1
                        execution_results['extractions'].append({
                            'search_term': search_term,
                            'status': 'PROCESSING_FAILED',
                            'error': 'Failed to process extracted data'
                        })
                        print(f"   ❌ Processing failed for {search_term}")

                else:
                    execution_results['failed_extractions'] += 1
                    error_msg = result.get('error', 'Unknown error')
                    execution_results['errors'].append(f"{search_term}: {error_msg}")
                    execution_results['extractions'].append({
                        'search_term': search_term,
                        'status': 'EXTRACTION_FAILED',
                        'error': error_msg
                    })
                    print(f"   ❌ Extraction failed: {error_msg}")

            except Exception as e:
                execution_results['failed_extractions'] += 1
                error_msg = str(e)
                execution_results['errors'].append(f"{search_term}: {error_msg}")
                execution_results['extractions'].append({
                    'search_term': search_term,
                    'status': 'SYSTEM_ERROR',
                    'error': error_msg
                })
                print(f"   ❌ System error: {error_msg}")

            # Add delay between requests
            if i < len(mission['search_terms']):
                delay = mission.get('extraction_settings', {}).get('delay_between_requests', 2)
                time.sleep(delay)

        # Calculate execution metrics
        execution_results['end_time'] = datetime.now().isoformat()
        execution_results['total_extraction_time'] = time.time() - start_time
        execution_results['success_rate'] = (execution_results['successful_extractions'] / len(mission['search_terms'])) * 100

        # Update mission database record
        self.db_manager.update_mission_progress(
            mission_id,
            execution_results['successful_extractions'],
            execution_results['high_quality_leads']
        )

        # Move mission to completed
        self._move_mission_to_completed(mission_id, execution_results)
        self._update_mission_status(mission_id, "COMPLETED")

        # Generate mission report
        self._generate_mission_report(execution_results, mission_processed_dir)

        print(f"\n🎉 Mission Completed!")
        print(f"📊 Results Summary:")
        print(f"   Total Extractions: {len(mission['search_terms'])}")
        print(f"   Successful: {execution_results['successful_extractions']}")
        print(f"   Failed: {execution_results['failed_extractions']}")
        print(f"   High-Quality Leads: {execution_results['high_quality_leads']}")
        print(f"   Success Rate: {execution_results['success_rate']:.1f}%")
        print(f"   Total Time: {execution_results['total_extraction_time']:.1f} seconds")
        print(f"   Avg per Business: {execution_results['total_extraction_time']/len(mission['search_terms']):.1f} seconds")

        return execution_results

    def _extract_business_data(self, search_term: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract business data using BOB Google Maps.

        Args:
            search_term: Search query for business
            settings: Extraction settings

        Returns:
            Extraction result from BOB Google Maps
        """
        try:
            return extract_business(
                search_term,
                include_reviews=settings.get('include_reviews', True),
                max_reviews=settings.get('max_reviews', 5)
            )
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'search_term': search_term
            }

    def _process_extracted_data(self, raw_data: Dict[str, Any], mission: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process raw extraction data into business intelligence.

        Args:
            raw_data: Raw data from BOB Google Maps
            mission: Mission configuration

        Returns:
            Processed business intelligence data
        """
        try:
            # Generate business ID
            business_id = f"{mission['mission_id']}_{raw_data.get('cid', 'unknown')}_{int(time.time())}"

            # Create BusinessIntelligence object
            business = BusinessIntelligence.from_raw_extraction(raw_data, business_id)

            # Apply mission-specific filters
            if not self._meets_quality_criteria(business, mission.get('quality_filters', {})):
                return None

            # Calculate scores
            business.calculate_data_quality_score()
            business.calculate_lead_score()

            return business.to_dict()

        except Exception as e:
            print(f"   ⚠️ Processing error: {e}")
            return None

    def _meets_quality_criteria(self, business: BusinessIntelligence, quality_filters: Dict[str, Any]) -> bool:
        """
        Check if business meets mission quality criteria.

        Args:
            business: BusinessIntelligence object
            quality_filters: Quality filter criteria

        Returns:
            True if business meets criteria, False otherwise
        """
        # Rating filter
        if 'min_rating' in quality_filters and business.google_rating < quality_filters['min_rating']:
            return False

        # Review count filter
        if 'min_reviews' in quality_filters and business.review_count < quality_filters['min_reviews']:
            return False

        # Contact completeness filter
        contact_filters = quality_filters.get('contact_completeness', {})
        if contact_filters.get('require_phone') and not business.primary_phone:
            return False
        if contact_filters.get('require_email') and not business.emails:
            return False
        if contact_filters.get('require_website') and not business.website:
            return False

        return True

    def _integrate_business_data(self, business_data: Dict[str, Any], mission: Dict[str, Any]) -> bool:
        """
        Integrate processed business data into central database.

        Args:
            business_data: Processed business intelligence data
            mission: Mission configuration

        Returns:
            True if integration successful, False otherwise
        """
        try:
            # Reconstruct BusinessIntelligence object
            business = BusinessIntelligence(
                business_id=business_data['business_id'],
                google_cid=business_data['google_cid'],
                business_name=business_data['business_name'],
                business_type=business_data['business_type'],
                primary_phone=business_data['primary_phone'],
                emails=business_data['emails'],
                website=business_data['website'],
                address=business_data['address'],
                city=business_data['city'],
                country=business_data['country'],
                latitude=business_data['latitude'],
                longitude=business_data['longitude'],
                google_rating=business_data['google_rating'],
                review_count=business_data['review_count']
            )

            return self.db_manager.insert_business(business)

        except Exception as e:
            print(f"   ⚠️ Database integration error: {e}")
            return False

    def _generate_mission_report(self, results: Dict[str, Any], output_dir: Path):
        """
        Generate comprehensive mission report.

        Args:
            results: Mission execution results
            output_dir: Directory to save report
        """
        report = {
            'mission_summary': {
                'mission_id': results['mission_id'],
                'mission_name': results['mission_name'],
                'execution_date': results['start_time'],
                'total_duration_seconds': results['total_extraction_time'],
                'success_rate_percent': results['success_rate']
            },
            'extraction_metrics': {
                'total_search_terms': len(results['search_terms']),
                'successful_extractions': results['successful_extractions'],
                'failed_extractions': results['failed_extractions'],
                'high_quality_leads': results['high_quality_leads'],
                'businesses_integrated': results['businesses_integrated']
            },
            'quality_metrics': {
                'average_lead_score': 0,
                'average_data_quality_score': 0,
                'contact_completeness_rate': 0
            },
            'top_leads': [],
            'errors': results['errors'],
            'detailed_extractions': results['extractions']
        }

        # Calculate quality metrics from successful extractions
        successful_extractions = [ex for ex in results['extractions'] if ex['status'] == 'SUCCESS']
        if successful_extractions:
            avg_lead_score = sum(ex.get('lead_score', 0) for ex in successful_extractions) / len(successful_extractions)
            avg_quality_score = sum(ex.get('data_quality_score', 0) for ex in successful_extractions) / len(successful_extractions)

            report['quality_metrics']['average_lead_score'] = round(avg_lead_score, 1)
            report['quality_metrics']['average_data_quality_score'] = round(avg_quality_score, 1)

        # Get top leads from database
        top_leads = self.db_manager.get_high_priority_leads(min_score=70, limit=10)
        report['top_leads'] = top_leads

        # Save report
        report_file = output_dir / f"mission_report_{results['mission_id']}_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"   📋 Mission report saved: {report_file}")

    def _update_mission_status(self, mission_id: str, status: str):
        """Update mission status in database"""
        # This would update the missions table in the database
        pass

    def _move_mission_to_completed(self, mission_id: str, results: Dict[str, Any]):
        """Move mission file and results to completed directory"""
        # This would move mission files and create completion record
        pass


def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python mission_executor.py <mission_file.json>")
        sys.exit(1)

    mission_file = Path(sys.argv[1])
    if not mission_file.exists():
        print(f"Mission file not found: {mission_file}")
        sys.exit(1)

    # Initialize mission executor
    project_root = Path(__file__).parent.parent.parent
    executor = MissionExecutor(project_root)

    # Load and execute mission
    mission = executor.load_mission(mission_file)
    if not mission:
        print("Failed to load mission configuration")
        sys.exit(1)

    # Execute mission
    results = executor.execute_mission(mission)

    # Output summary
    print(f"\n🎯 Mission '{mission['mission_name']}' completed successfully!")
    print(f"📊 Results: {results['successful_extractions']}/{len(mission['search_terms'])} businesses extracted")
    print(f"⭐ High-quality leads: {results['high_quality_leads']}")


if __name__ == "__main__":
    main()