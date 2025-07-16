# db_setup.py

import sqlite3
import pysqlcipher3.dbapi2 as sqlcipher
import os
from pathlib import Path
import yaml
import logging

class DatabaseSetup:
    """Initializes the SQLite database with SQLCipher encryption and creates tables."""
    
    def __init__(self, config_path: str, db_path: str, schema_path: str):
        """Initialize with paths to config, database, and schema files."""
        self.config_path = Path(config_path)
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> dict:
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
    
    def initialize_database(self) -> None:
        """Create and initialize the encrypted SQLite database."""
        try:
            # Ensure data directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load database encryption key from config
            config = self.load_config()
            encryption_key = config.get('encryption_key')
            if not encryption_key:
                raise ValueError("Database encryption key not found in config")
            
            # Connect to database with SQLCipher
            conn = sqlcipher.connect(str(self.db_path))
            conn.execute(f"PRAGMA key = '{encryption_key}'")
            
            # Read and execute schema SQL
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()
            
            conn.executescript(schema_sql)
            conn.commit()
            self.logger.info(f"Database initialized successfully at {self.db_path}")
            
        except sqlcipher.Error as e:
            self.logger.error(f"Database error: {e}")
            raise
        except FileNotFoundError:
            self.logger.error(f"Schema file not found: {self.schema_path}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

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
    db_setup = DatabaseSetup(
        config_path="config/secrets.yaml",
        db_path="data/database.db",
        schema_path="src/database/migrations/init_schema.sql"
    )
    db_setup.initialize_database()