#!/usr/bin/env python3
"""
D Corner Living - Database ORM Layer

SQLite database operations for business intelligence.
Handles centralized storage with mission-based data integration.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path

from ..entities.business import BusinessIntelligence, BusinessType, PotentialValue, ApproachStrategy


class DatabaseManager:
    """
    Centralized database manager for D Corner Living business intelligence.
    Handles all CRUD operations and data integration.
    """

    def __init__(self, db_path: str = "data/cache/dcorner_master.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable dict-like row access

    def create_tables(self):
        """Create database schema if not exists"""
        cursor = self.connection.cursor()

        # Main businesses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                business_id TEXT PRIMARY KEY,
                google_cid TEXT UNIQUE,
                business_name TEXT NOT NULL,
                business_type TEXT,
                primary_phone TEXT,
                emails TEXT,
                website TEXT,
                social_media TEXT,
                address TEXT,
                city TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                logistics_zone TEXT,
                business_size TEXT,
                estimated_revenue TEXT,
                years_in_business INTEGER,
                employee_count INTEGER,
                google_rating REAL,
                review_count INTEGER,
                trust_score INTEGER,
                lead_score INTEGER,
                potential_value TEXT,
                product_match TEXT,
                approach_strategy TEXT,
                specialties TEXT,
                current_suppliers TEXT,
                project_frequency TEXT,
                decision_makers TEXT,
                extraction_date TEXT,
                last_updated TEXT,
                extraction_source TEXT,
                data_quality_score INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Missions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                mission_id TEXT PRIMARY KEY,
                mission_name TEXT NOT NULL,
                mission_type TEXT NOT NULL,
                target_business_type TEXT,
                geographic_scope TEXT,
                search_terms TEXT,
                status TEXT DEFAULT 'PLANNING',
                start_date TEXT,
                end_date TEXT,
                businesses_extracted INTEGER DEFAULT 0,
                high_quality_leads INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Extraction logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extraction_logs (
                log_id TEXT PRIMARY KEY,
                mission_id TEXT,
                business_name TEXT,
                extraction_status TEXT,
                error_message TEXT,
                extraction_time_seconds REAL,
                data_quality_score INTEGER,
                extracted_at TEXT,
                FOREIGN KEY (mission_id) REFERENCES missions(mission_id)
            )
        ''')

        # Lead scoring history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lead_scoring_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id TEXT,
                lead_score INTEGER,
                scoring_date TEXT,
                scoring_factors TEXT,
                FOREIGN KEY (business_id) REFERENCES businesses(business_id)
            )
        ''')

        self.connection.commit()

    def insert_business(self, business: BusinessIntelligence) -> bool:
        """
        Insert or update business in database.

        Args:
            business: BusinessIntelligence object

        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()

            # Convert complex fields to JSON
            business_dict = business.to_dict()

            cursor.execute('''
                INSERT OR REPLACE INTO businesses (
                    business_id, google_cid, business_name, business_type,
                    primary_phone, emails, website, social_media,
                    address, city, country, latitude, longitude, logistics_zone,
                    business_size, estimated_revenue, years_in_business, employee_count,
                    google_rating, review_count, trust_score, lead_score,
                    potential_value, product_match, approach_strategy,
                    specialties, current_suppliers, project_frequency, decision_makers,
                    extraction_date, last_updated, extraction_source, data_quality_score,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                business.business_id,
                business.google_cid,
                business.business_name,
                business_dict.get('business_type'),
                business.primary_phone,
                json.dumps(business.emails),
                business.website,
                json.dumps(business.social_media),
                business.address,
                business.city,
                business.country,
                business.latitude,
                business.longitude,
                business.logistics_zone,
                business_dict.get('business_size'),
                business_dict.get('estimated_revenue'),
                business.years_in_business,
                business.employee_count,
                business.google_rating,
                business.review_count,
                business.trust_score,
                business.lead_score,
                business_dict.get('potential_value'),
                json.dumps(business.product_match),
                business_dict.get('approach_strategy'),
                json.dumps(business.specialties),
                json.dumps(business.current_suppliers),
                business.project_frequency,
                json.dumps(business_dict.get('decision_makers')),
                business.extraction_date.isoformat(),
                business.last_updated.isoformat(),
                business.extraction_source,
                business.data_quality_score,
                datetime.now().isoformat()
            ))

            self.connection.commit()
            return True

        except Exception as e:
            print(f"Error inserting business: {e}")
            return False

    def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve business by ID.

        Args:
            business_id: Unique business identifier

        Returns:
            Business data dictionary or None if not found
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM businesses WHERE business_id = ?', (business_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def get_businesses_by_type(self, business_type: BusinessType, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve businesses by type, sorted by lead score.

        Args:
            business_type: Type of businesses to retrieve
            limit: Maximum number of results

        Returns:
            List of business dictionaries
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM businesses
            WHERE business_type = ?
            ORDER BY lead_score DESC, data_quality_score DESC
            LIMIT ?
        ''', (business_type.value, limit))

        return [dict(row) for row in cursor.fetchall()]

    def get_high_priority_leads(self, min_score: int = 60, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve high-priority leads based on lead score.

        Args:
            min_score: Minimum lead score threshold
            limit: Maximum number of results

        Returns:
            List of high-priority business dictionaries
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM businesses
            WHERE lead_score >= ? AND data_quality_score >= 70
            ORDER BY lead_score DESC, google_rating DESC
            LIMIT ?
        ''', (min_score, limit))

        return [dict(row) for row in cursor.fetchall()]

    def get_businesses_by_location(self, city: str, business_type: Optional[BusinessType] = None) -> List[Dict[str, Any]]:
        """
        Retrieve businesses by location.

        Args:
            city: City name to filter by
            business_type: Optional business type filter

        Returns:
            List of business dictionaries
        """
        cursor = self.connection.cursor()

        if business_type:
            cursor.execute('''
                SELECT * FROM businesses
                WHERE city = ? AND business_type = ?
                ORDER BY lead_score DESC
            ''', (city, business_type.value))
        else:
            cursor.execute('''
                SELECT * FROM businesses
                WHERE city = ?
                ORDER BY lead_score DESC
            ''', (city,))

        return [dict(row) for row in cursor.fetchall()]

    def search_businesses(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search businesses by name or specialty.

        Args:
            query: Search query string
            limit: Maximum number of results

        Returns:
            List of matching business dictionaries
        """
        cursor = self.connection.cursor()
        search_pattern = f"%{query}%"

        cursor.execute('''
            SELECT * FROM businesses
            WHERE business_name LIKE ? OR specialties LIKE ?
            ORDER BY lead_score DESC
            LIMIT ?
        ''', (search_pattern, search_pattern, limit))

        return [dict(row) for row in cursor.fetchall()]

    def get_mission_statistics(self) -> Dict[str, Any]:
        """
        Get overall database statistics.

        Returns:
            Dictionary with statistics
        """
        cursor = self.connection.cursor()

        # Total businesses
        cursor.execute('SELECT COUNT(*) as total FROM businesses')
        total_businesses = cursor.fetchone()['total']

        # Business type breakdown
        cursor.execute('''
            SELECT business_type, COUNT(*) as count
            FROM businesses
            GROUP BY business_type
        ''')
        by_type = {row['business_type']: row['count'] for row in cursor.fetchall()}

        # High-quality leads
        cursor.execute('SELECT COUNT(*) as count FROM businesses WHERE lead_score >= 60')
        high_quality_leads = cursor.fetchone()['count']

        # Geographic distribution
        cursor.execute('''
            SELECT city, COUNT(*) as count
            FROM businesses
            GROUP BY city
        ''')
        by_city = {row['city']: row['count'] for row in cursor.fetchall()}

        # Average quality scores
        cursor.execute('''
            SELECT AVG(data_quality_score) as avg_quality,
                   AVG(lead_score) as avg_lead_score
            FROM businesses
        ''')
        scores = cursor.fetchone()

        return {
            'total_businesses': total_businesses,
            'by_business_type': by_type,
            'high_quality_leads': high_quality_leads,
            'by_city': by_city,
            'average_data_quality': round(scores['avg_quality'] or 0, 1),
            'average_lead_score': round(scores['avg_lead_score'] or 0, 1)
        }

    def create_mission(self, mission_data: Dict[str, Any]) -> bool:
        """
        Create a new mission record.

        Args:
            mission_data: Mission configuration data

        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                INSERT INTO missions (
                    mission_id, mission_name, mission_type, target_business_type,
                    geographic_scope, search_terms, status, start_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                mission_data['mission_id'],
                mission_data['mission_name'],
                mission_data['mission_type'],
                mission_data.get('target_business_type'),
                mission_data.get('geographic_scope'),
                json.dumps(mission_data.get('search_terms', [])),
                mission_data.get('status', 'PLANNING'),
                mission_data.get('start_date', datetime.now().isoformat())
            ))

            self.connection.commit()
            return True

        except Exception as e:
            print(f"Error creating mission: {e}")
            return False

    def update_mission_progress(self, mission_id: str, businesses_extracted: int, high_quality_leads: int) -> bool:
        """
        Update mission progress.

        Args:
            mission_id: Mission identifier
            businesses_extracted: Number of businesses extracted
            high_quality_leads: Number of high-quality leads found

        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                UPDATE missions
                SET businesses_extracted = ?, high_quality_leads = ?, updated_at = ?
                WHERE mission_id = ?
            ''', (businesses_extracted, high_quality_leads, datetime.now().isoformat(), mission_id))

            self.connection.commit()
            return True

        except Exception as e:
            print(f"Error updating mission: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()