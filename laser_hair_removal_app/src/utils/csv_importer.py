import csv
from src.database.db_operations import DatabaseOperations
from src.models.client import Client
from src.models.appointment import Appointment
import logging
from pathlib import Path
from typing import Dict, List, Optional

class CSVImporter:
    """Handles importing data from CSV files into the database."""
    
    def __init__(self, db: DatabaseOperations):
        """Initialize with a database operations instance."""
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def _validate_client_data(self, row: Dict) -> Dict:
        """Validate and clean client data from CSV row."""
        required = {'Client_ID', 'Name', 'Phone'}
        if not all(field in row for field in required):
            raise ValueError("Missing required client fields")
        return {
            'client_id': int(row['Client_ID']) if row['Client_ID'] else 0,
            'full_name': str(row['Name']).strip(),
            'phone_number': str(row['Phone']).strip(),
            'email': str(row['Email']).strip() if row['Email'] else None,
            'dob': str(row['DOB']).strip() if row['DOB'] else None,
            'notes': f"Social: FB={row['Facebook'] or ''}, IG={row['Instagram'] or ''}, Booksy={row['Booksy'] or ''}"
        }
    
    def _validate_visit_data(self, row: Dict) -> Dict:
        """Validate and clean visit data from CSV row."""
        required = {'Visit_ID', 'Client_ID', 'Name', 'Date', 'Visit_number', 'Area'}
        if not all(field in row for field in required):
            raise ValueError("Missing required visit fields")
        return {
            'appointment_id': int(row['Visit_ID']) if row['Visit_ID'] else 0,
            'client_id': int(row['Client_ID']),
            'service_id': 1,  # Placeholder, assumes a default service
            'area_id': int(row['Area']) if row['Area'].isdigit() else 1,  # Placeholder mapping
            'appointment_date': str(row['Date']).strip(),
            'session_number': int(row['Visit_number']),
            'power': float(row['Power']) if row['Power'] else None,
            'next_suggested_appointment_date': str(row['Next_visit_calculated']).strip() if row['Next_visit_calculated'] else None,
            'appointment_status': 'Completed' if row['Visit_confirmed'] == 'Yes' else 'Scheduled',
            'amount': float(row['Amount']) if row['Amount'] else None
        }
    
    def import_clients(self, csv_path: str) -> int:
        """Import clients from a CSV file and return the number of imported clients."""
        try:
            csv_path = Path(csv_path)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != ['Client_ID', 'Name', 'Phone', 'Email', 'Facebook', 'Instagram', 'Booksy', 'DOB']:
                    raise ValueError("Invalid CSV column headers for clients")
                
                count = 0
                for row in reader:
                    try:
                        data = self._validate_client_data(row)
                        client = Client(data['client_id'], data['full_name'], data['phone_number'], 
                                      data['email'], data['dob'], notes=data['notes'])
                        if data['client_id'] == 0:
                            self.db.add_client(client.full_name, client.phone_number, client.email, 
                                             client.dob, client.notes)
                        else:
                            self.db.update_client(data['client_id'], client.full_name, client.phone_number, 
                                                client.email, client.dob, notes=client.notes)
                        count += 1
                    except ValueError as e:
                        self.logger.warning(f"Skipping invalid client row: {e}")
                    except Exception as e:
                        self.logger.error(f"Error importing client from row: {e}")
                self.logger.info(f"Imported {count} clients from {csv_path}")
                return count
        except Exception as e:
            self.logger.error(f"Error importing clients from {csv_path}: {e}")
            raise
    
    def import_visits(self, csv_path: str) -> int:
        """Import visits from a CSV file and return the number of imported visits."""
        try:
            csv_path = Path(csv_path)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != ['Visit_ID', 'Client_ID', 'Name', 'Date', 'Visit_number', 'Area', 
                                        'Power', 'Next_visit_calculated', 'Visit_confirmed', 'Amount']:
                    raise ValueError("Invalid CSV column headers for visits")
                
                count = 0
                for row in reader:
                    try:
                        data = self._validate_visit_data(row)
                        appointment = Appointment(data['appointment_id'], data['client_id'], data['service_id'], 
                                                data['area_id'], data['appointment_date'], data['session_number'], 
                                                data['power'], data['appointment_status'], data['amount'], 
                                                next_suggested_appointment_date=data['next_suggested_appointment_date'])
                        if data['appointment_id'] == 0:
                            query = """
                                INSERT INTO appointments (client_id, service_id, area_id, appointment_date, 
                                session_number_for_area, power, appointment_status, amount, 
                                next_suggested_appointment_date)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """
                            params = (appointment.client_id, appointment.service_id, appointment.area_id, 
                                    appointment.appointment_date, appointment.session_number, appointment.power, 
                                    appointment.appointment_status, appointment.amount, 
                                    appointment.next_suggested_appointment_date)
                            self.db.execute_query(query, params)
                        else:
                            query = """
                                UPDATE appointments SET client_id = ?, service_id = ?, area_id = ?, 
                                appointment_date = ?, session_number_for_area = ?, power = ?, 
                                appointment_status = ?, amount = ?, next_suggested_appointment_date = ?
                                WHERE appointment_id = ?
                            """
                            params = (appointment.client_id, appointment.service_id, appointment.area_id, 
                                    appointment.appointment_date, appointment.session_number, appointment.power, 
                                    appointment.appointment_status, appointment.amount, 
                                    appointment.next_suggested_appointment_date, data['appointment_id'])
                            self.db.execute_query(query, params)
                        count += 1
                    except ValueError as e:
                        self.logger.warning(f"Skipping invalid visit row: {e}")
                    except Exception as e:
                        self.logger.error(f"Error importing visit from row: {e}")
                self.logger.info(f"Imported {count} visits from {csv_path}")
                return count
        except Exception as e:
            self.logger.error(f"Error importing visits from {csv_path}: {e}")
            raise

if __name__ == "__main__":
    from src.database.db_operations import DatabaseOperations
    logging.basicConfig(level=logging.INFO)
    db = DatabaseOperations("config/secrets.yaml", "data/database.db")
    importer = CSVImporter(db)
    try:
        client_count = importer.import_clients("data/clients.csv")
        visit_count = importer.import_visits("data/visits.csv")
        print(f"Imported {client_count} clients and {visit_count} visits")
    except Exception as e:
        print(f"Error: {e}")