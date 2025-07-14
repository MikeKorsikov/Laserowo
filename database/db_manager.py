# db_manager.py

"""
Database manager for SQLite operations
"""

import sqlite3
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from app.config import DATABASE_FILE_PATH
from app.database.schema import ALL_TABLES, SAMPLE_SERVICES, SAMPLE_TREATMENT_AREAS

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_FILE_PATH
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def create_tables(self):
        """Create all database tables"""
        if not self.connection:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            for table_sql in ALL_TABLES:
                cursor.execute(table_sql)
            self.connection.commit()
            logger.info("All tables created successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def execute_query(self, query: str, params: Tuple = None) -> sqlite3.Cursor:
        """Execute a query with optional parameters"""
        if not self.connection:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            raise
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[sqlite3.Row]:
        """Fetch a single row from the database"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[sqlite3.Row]:
        """Fetch all rows from the database"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def get_table_count(self, table_name: str) -> int:
        """Get the number of rows in a table"""
        result = self.fetch_one(f"SELECT COUNT(*) as count FROM {table_name}")
        return result['count'] if result else 0
    
    def insert_sample_data(self):
        """Insert sample data if tables are empty"""
        try:
            # Insert sample services if table is empty
            if self.get_table_count('services') == 0:
                for service_data in SAMPLE_SERVICES:
                    self.execute_query(
                        "INSERT INTO services (service_name, description, base_price, estimated_duration_minutes) VALUES (?, ?, ?, ?)",
                        service_data
                    )
                logger.info("Sample services inserted")
            
            # Insert sample treatment areas if table is empty
            if self.get_table_count('treatment_areas') == 0:
                for area_data in SAMPLE_TREATMENT_AREAS:
                    self.execute_query(
                        "INSERT INTO treatment_areas (area_name) VALUES (?)",
                        area_data
                    )
                logger.info("Sample treatment areas inserted")
                
        except sqlite3.Error as e:
            logger.error(f"Error inserting sample data: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Global database manager instance
db_manager = DatabaseManager()