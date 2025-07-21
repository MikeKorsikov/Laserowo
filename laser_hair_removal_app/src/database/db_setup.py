# db_setup.py 

import os
import logging
from pysqlcipher3 import dbapi2 as sqlite3
from src.utils.config import Config
from src.utils.logger import Logger
from src.database.db_operations import DatabaseOperations

class DatabaseSetup:
    """Handles database initialization and migration management with SQLCipher encryption."""
    
    def __init__(self, config_path: str, secrets_path: str, db_path: str):
        """Initialize with configuration and database paths."""
        self.config = Config(config_path, secrets_path)
        self.db_path = db_path
        self.logger = Logger().get_logger(__name__)
        self.db_ops = DatabaseOperations(secrets_path, db_path)
        self.migration_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        self.migration_log = os.path.join(self.migration_dir, 'migrations.log')
        self.encryption_key = self.config.get('database.encryption_key', 'default_key')

    def initialize_database(self):
        """Initialize the database with encryption and apply migrations."""
        if not os.path.exists(self.db_path):
            self.logger.info("Creating new database at %s", self.db_path)
            conn = sqlite3.connect(self.db_path)
            conn.execute(f"PRAGMA key = '{self.encryption_key}'")
            conn.execute("PRAGMA cipher_use_hmac = OFF")  # Optional: Adjust based on security needs
            conn.close()
        else:
            self.logger.info("Database already exists at %s, applying migrations", self.db_path)

        self.apply_migrations()

    def apply_migrations(self):
        """Apply pending migrations in sequence."""
        if not os.path.exists(self.migration_dir):
            self.logger.error("Migrations directory not found at %s", self.migration_dir)
            raise FileNotFoundError("Migrations directory missing")

        applied_migrations = self.get_applied_migrations()
        migration_files = [f for f in os.listdir(self.migration_dir) if f.endswith('.sql') and f.isdigit() + f[3:].isdigit()]
        migration_files.sort()  # Sort by filename (e.g., 001_init_schema.sql)

        conn = self.db_ops.get_connection()
        cursor = conn.cursor()

        for migration_file in migration_files:
            migration_version = int(migration_file.split('_')[0])
            if migration_version not in applied_migrations:
                migration_path = os.path.join(self.migration_dir, migration_file)
                self.logger.info("Applying migration %s", migration_path)
                with open(migration_path, 'r') as f:
                    cursor.executescript(f.read())
                with open(self.migration_log, 'a') as f:
                    f.write(f"{migration_version}\n")
                self.logger.info("Migration %s applied successfully", migration_version)
            else:
                self.logger.info("Migration %s already applied, skipping", migration_version)

        conn.commit()
        conn.close()

    def get_applied_migrations(self):
        """Retrieve list of applied migration versions from log."""
        applied = set()
        if os.path.exists(self.migration_log):
            with open(self.migration_log, 'r') as f:
                applied = {int(line.strip()) for line in f if line.strip().isdigit()}
        return applied

    def rollback_migration(self, version: int):
        """Rollback to a specific migration version (simplified, assumes reversible migrations)."""
        applied_migrations = self.get_applied_migrations()
        if version not in applied_migrations:
            self.logger.error("Migration version %d not applied, cannot rollback", version)
            raise ValueError(f"Migration {version} not found in applied set")

        conn = self.db_ops.get_connection()
        cursor = conn.cursor()

        # Simplified rollback: Reverse apply all migrations after the target version
        migration_files = [f for f in os.listdir(self.migration_dir) if f.endswith('.sql') and f.isdigit() + f[3:].isdigit()]
        migration_files.sort(reverse=True)

        rollback_needed = [int(f.split('_')[0]) for f in migration_files if int(f.split('_')[0]) > version]
        if rollback_needed:
            for migration_version in sorted(rollback_needed, reverse=True):
                migration_file = next(f for f in migration_files if int(f.split('_')[0]) == migration_version)
                migration_path = os.path.join(self.migration_dir, migration_file)
                self.logger.info("Rolling back migration %s", migration_path)
                # Assume reverse SQL is provided or manually crafted (e.g., DROP TABLE)
                with open(migration_path.replace('.sql', '_rollback.sql'), 'r') as f:
                    cursor.executescript(f.read())  # Requires rollback scripts
                with open(self.migration_log, 'w') as f:
                    f.writelines(f"{v}\n" for v in applied_migrations if v <= version)
                self.logger.info("Rolled back to migration %d", version)
        else:
            self.logger.info("No rollbacks needed, already at or before version %d", version)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    setup = DatabaseSetup("config/app_config.yaml", "config/secrets.yaml", "data/database.db")
    setup.initialize_database()
    # Example rollback (uncomment to test)
    # setup.rollback_migration(1)