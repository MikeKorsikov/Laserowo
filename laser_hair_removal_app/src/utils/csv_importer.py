import csv
import os
import logging
from src.utils.config import Config
from src.utils.logger import Logger
from src.backend.client_manager import ClientManager

class CSVImporter:
    """Handles importing client data from CSV files."""
    
    def __init__(self, config_path: str, secrets_path: str, db_path: str):
        """Initialize with configuration and database paths."""
        self.config = Config(config_path, secrets_path)
        self.logger = Logger().get_logger(__name__)
        self.client_manager = ClientManager(config_path, db_path)
        self.import_dir = self.config.get('paths.imports_dir', 'data/imports')
        self.default_file = os.path.join(self.import_dir, 'clients.csv')

    def import_clients(self, file_path: str = None):
        """Import client data from a CSV file."""
        file_path = file_path or self.default_file
        if not os.path.exists(file_path):
            self.logger.error("CSV file not found at %s", file_path)
            raise FileNotFoundError(f"CSV file not found at {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_fields = {'full_name', 'phone_number', 'email', 'dob'}
                if not all(field in reader.fieldnames for field in required_fields):
                    self.logger.error("CSV file %s missing required fields: %s", file_path, required_fields)
                    raise ValueError(f"Missing required fields: {required_fields}")

                for row in reader:
                    try:
                        # Validate and clean data
                        full_name = row['full_name'].strip()
                        phone_number = row['phone_number'].strip()
                        email = row['email'].strip() if row['email'] else None
                        dob = row['dob'].strip() if row['dob'] else None

                        if not full_name or not phone_number:
                            self.logger.warning("Skipping row with missing name or phone: %s", row)
                            continue
                        if dob and len(dob) != 10:  # Expect YYYY-MM-DD
                            self.logger.warning("Invalid DOB format in row %s, skipping", row)
                            continue

                        # Add client to database
                        client_id = self.client_manager.add_client(full_name, phone_number, email, dob)
                        self.logger.info("Imported client %s with ID %d", full_name, client_id)
                    except Exception as e:
                        self.logger.error("Error processing row %s: %s", row, str(e))
                        continue

            self.logger.info("Successfully imported clients from %s", file_path)
            return True
        except Exception as e:
            self.logger.error("Failed to import CSV file %s: %s", file_path, str(e))
            raise

if __name__ == "__main__":
    importer = CSVImporter("config/app_config.yaml", "config/secrets.yaml", "data/database.db")
    try:
        importer.import_clients()
    except Exception as e:
        print(f"Import failed: {e}")