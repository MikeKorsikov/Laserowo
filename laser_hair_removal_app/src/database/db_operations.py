# db_operations.py

import sqlite3
import pysqlcipher3.dbapi2 as sqlcipher
import os
from pathlib import Path
import yaml
import logging
from typing import List, Dict, Optional, Tuple

class DatabaseOperations:
    """Handles CRUD operations for the encrypted SQLite database."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with paths to config and database files."""
        self.config_path = Path(config_path)
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(__name__)
        self.conn = None
        
    def connect(self) -> None:
        """Establish a secure connection to the encrypted database."""
        try:
            config = self._load_config()
            encryption_key = config.get('encryption_key')
            if not encryption_key:
                raise ValueError("Database encryption key not found in config")
            
            self.conn = sqlcipher.connect(str(self.db_path))
            self.conn.execute(f"PRAGMA key = '{encryption_key}'")
            self.logger.info("Database connection established")
        except sqlcipher.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Configuration or connection error: {e}")
            raise
    
    def _load_config(self) -> dict:
        """Load database configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('database', {})
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing config file: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")
            self.conn = None
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute a query and return results as a list of dictionaries."""
        try:
            if not self.conn:
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results
            self.conn.commit()
            return []
        except sqlcipher.Error as e:
            self.logger.error(f"Query execution error: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()
    
    # CRUD Operations for clients
    def add_client(self, full_name: str, phone_number: str, email: str = None, dob: str = None, notes: str = None) -> int:
        """Add a new client and return the client_id."""
        query = "INSERT INTO clients (full_name, phone_number, email, dob, notes) VALUES (?, ?, ?, ?, ?)"
        params = (full_name, phone_number, email, dob, notes)
        self.execute_query(query, params)
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    
    def get_client(self, client_id: int) -> Optional[Dict]:
        """Retrieve a client by client_id."""
        query = "SELECT * FROM clients WHERE client_id = ?"
        results = self.execute_query(query, (client_id,))
        return results[0] if results else None
    
    def update_client(self, client_id: int, full_name: str = None, phone_number: str = None, email: str = None, 
                     dob: str = None, is_blacklisted: bool = None, is_active: bool = None, notes: str = None) -> bool:
        """Update client details."""
        updates = []
        params = []
        if full_name: updates.append("full_name = ?"); params.append(full_name)
        if phone_number: updates.append("phone_number = ?"); params.append(phone_number)
        if email: updates.append("email = ?"); params.append(email)
        if dob: updates.append("dob = ?"); params.append(dob)
        if is_blacklisted is not None: updates.append("is_blacklisted = ?"); params.append(is_blacklisted)
        if is_active is not None: updates.append("is_active = ?"); params.append(is_active)
        if notes: updates.append("notes = ?"); params.append(notes)
        if not updates:
            return False
        params.append(client_id)
        query = f"UPDATE clients SET {', '.join(updates)} WHERE client_id = ?"
        self.execute_query(query, tuple(params))
        return True
    
    def delete_client(self, client_id: int) -> bool:
        """Deactivate a client (soft delete by setting is_active to False)."""
        query = "UPDATE clients SET is_active = FALSE WHERE client_id = ?"
        self.execute_query(query, (client_id,))
        return True
    
    # Additional CRUD operations can be added for other tables (e.g., appointments, services) as needed

    def __enter__(self):
        """Context manager entry for using with statement."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit to ensure connection is closed."""
        self.disconnect()

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/app.log'),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    setup_logging()
    with DatabaseOperations(config_path="config/secrets.yaml", db_path="data/database.db") as db:
        # Example usage
        client_id = db.add_client("John Doe", "+48 123 456 789", "john@example.com", "1990-05-15")
        print(f"Added client with ID: {client_id}")
        client = db.get_client(client_id)
        print(f"Retrieved client: {client}")