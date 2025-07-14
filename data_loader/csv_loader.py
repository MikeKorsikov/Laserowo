"""
CSV data loader for initial database population
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Any
from app.config import CSV_DATA_DIR, CSV_FILES
from app.database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class CSVLoader:
    """Handles loading CSV data into the database"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.csv_dir = Path(CSV_DATA_DIR)
    
    def load_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load a CSV file and return list of dictionaries"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
                logger.info(f"Loaded {len(data)} records from {file_path}")
                return data
        except FileNotFoundError:
            logger.warning(f"CSV file not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            return []
    
    def load_clients_csv(self):
        """Load clients from CSV file"""
        csv_path = self.csv_dir / CSV_FILES['clients']
        if not csv_path.exists():
            logger.info("No clients.csv file found, skipping client import")
            return
        
        # Check if clients table already has data
        if self.db_manager.get_table_count('clients') > 0:
            logger.info("Clients table already has data, skipping import")
            return
        
        clients_data = self.load_csv_file(csv_path)
        if not clients_data:
            return
        
        try:
            for client in clients_data:
                # Convert boolean strings to actual booleans
                is_blacklisted = client.get('is_blacklisted', '0').lower() in ('1', 'true', 'yes')
                is_active = client.get('is_active', '1').lower() in ('1', 'true', 'yes')
                
                self.db_manager.execute_query(
                    """INSERT INTO clients (full_name, phone_number, email, date_of_birth, 
                       is_blacklisted, is_active) VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        client.get('full_name', ''),
                        client.get('phone_number', ''),
                        client.get('email', ''),
                        client.get('date_of_birth', ''),
                        is_blacklisted,
                        is_active
                    )
                )
            logger.info(f"Imported {len(clients_data)} clients")
        except Exception as e:
            logger.error(f"Error importing clients: {e}")
    
    def load_services_csv(self):
        """Load services from CSV file"""
        csv_path = self.csv_dir / CSV_FILES['services']
        if not csv_path.exists():
            logger.info("No services.csv file found, skipping service import")
            return
        
        # Check if services table already has data (beyond sample data)
        if self.db_manager.get_table_count('services') > 5:  # More than sample data
            logger.info("Services table already has data, skipping import")
            return
        
        services_data = self.load_csv_file(csv_path)
        if not services_data:
            return
        
        try:
            for service in services_data:
                # Convert string values to appropriate types
                base_price = float(service.get('base_price', 0.0))
                duration = int(service.get('estimated_duration_minutes', 0))
                is_active = service.get('is_active', '1').lower() in ('1', 'true', 'yes')
                
                self.db_manager.execute_query(
                    """INSERT INTO services (service_name, description, base_price, 
                       estimated_duration_minutes, is_active) VALUES (?, ?, ?, ?, ?)""",
                    (
                        service.get('service_name', ''),
                        service.get('description', ''),
                        base_price,
                        duration,
                        is_active
                    )
                )
            logger.info(f"Imported {len(services_data)} services")
        except Exception as e:
            logger.error(f"Error importing services: {e}")
    
    def load_treatment_areas_csv(self):
        """Load treatment areas from CSV file"""
        csv_path = self.csv_dir / CSV_FILES['treatment_areas']
        if not csv_path.exists():
            logger.info("No treatment_areas.csv file found, skipping area import")
            return
        
        # Check if treatment_areas table already has data (beyond sample data)
        if self.db_manager.get_table_count('treatment_areas') > 7:  # More than sample data
            logger.info("Treatment areas table already has data, skipping import")
            return
        
        areas_data = self.load_csv_file(csv_path)
        if not areas_data:
            return
        
        try:
            for area in areas_data:
                is_active = area.get('is_active', '1').lower() in ('1', 'true', 'yes')
                
                self.db_manager.execute_query(
                    "INSERT INTO treatment_areas (area_name, is_active) VALUES (?, ?)",
                    (area.get('area_name', ''), is_active)
                )
            logger.info(f"Imported {len(areas_data)} treatment areas")
        except Exception as e:
            logger.error(f"Error importing treatment areas: {e}")
    
    def load_appointments_csv(self):
        """Load appointments from CSV file"""
        csv_path = self.csv_dir / CSV_FILES['appointments']
        if not csv_path.exists():
            logger.info("No appointments.csv file found, skipping appointment import")
            return
        
        # Check if appointments table already has data
        if self.db_manager.get_table_count('appointments') > 0:
            logger.info("Appointments table already has data, skipping import")
            return
        
        appointments_data = self.load_csv_file(csv_path)
        if not appointments_data:
            return
        
        try:
            for appointment in appointments_data:
                # Convert string IDs to integers
                client_id = int(appointment.get('client_id', 0))
                service_id = int(appointment.get('service_id', 0))
                area_id = int(appointment.get('area_id', 0))
                
                self.db_manager.execute_query(
                    """INSERT INTO appointments (client_id, service_id, area_id, 
                       appointment_date, start_time, end_time, status, notes) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        client_id,
                        service_id,
                        area_id,
                        appointment.get('appointment_date', ''),
                        appointment.get('start_time', ''),
                        appointment.get('end_time', ''),
                        appointment.get('status', 'scheduled'),
                        appointment.get('notes', '')
                    )
                )
            logger.info(f"Imported {len(appointments_data)} appointments")
        except Exception as e:
            logger.error(f"Error importing appointments: {e}")
    
    def load_initial_data(self):
        """Load all initial data from CSV files"""
        logger.info("Starting CSV data import process")
        
        # Load in order due to foreign key dependencies
        self.load_clients_csv()
        self.load_services_csv()
        self.load_treatment_areas_csv()
        self.load_appointments_csv()
        
        logger.info("CSV data import process completed")

def load_initial_data(db_manager: DatabaseManager):
    """Convenience function to load initial data"""
    loader = CSVLoader(db_manager)
    loader.load_initial_data()