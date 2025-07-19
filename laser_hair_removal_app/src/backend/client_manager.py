from src.database.db_operations import DatabaseOperations
from src.models.client import Client
from src.utils.csv_importer import CSVImporter
import logging
from typing import List, Optional
import os
from pathlib import Path

class ClientManager:
    """Manages client-related operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
    
    def add_client(self, full_name: str, phone_number: str, email: str = None, dob: str = None, 
                   notes: str = None) -> int:
        """Add a new client and return the client_id."""
        try:
            client = Client(0, full_name, phone_number, email, dob, notes=notes)
            client_id = self.db.add_client(
                client.full_name, client.phone_number, client.email, client.dob, client.notes
            )
            self.logger.info(f"Added client {full_name} with ID {client_id}")
            return client_id
        except ValueError as e:
            self.logger.error(f"Validation error adding client: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error adding client: {e}")
            raise
    
    def get_client(self, client_id: int) -> Optional[Client]:
        """Retrieve a client by client_id."""
        try:
            result = self.db.get_client(client_id)
            return Client.from_dict(result) if result else None
        except Exception as e:
            self.logger.error(f"Error retrieving client {client_id}: {e}")
            raise
    
    def update_client(self, client_id: int, full_name: str = None, phone_number: str = None, 
                      email: str = None, dob: str = None, is_blacklisted: bool = None, 
                      is_active: bool = None, notes: str = None) -> bool:
        """Update client details and return success status."""
        try:
            current_client = self.get_client(client_id)
            if not current_client:
                self.logger.warning(f"Client {client_id} not found for update")
                return False
            
            # Use existing values if not provided
            full_name = full_name or current_client.full_name
            phone_number = phone_number or current_client.phone_number
            email = email or current_client.email
            dob = dob or current_client.dob
            is_blacklisted = is_blacklisted if is_blacklisted is not None else current_client.is_blacklisted
            is_active = is_active if is_active is not None else current_client.is_active
            notes = notes or current_client.notes
            
            client = Client(client_id, full_name, phone_number, email, dob, is_blacklisted, is_active, notes)
            success = self.db.update_client(
                client_id, client.full_name, client.phone_number, client.email, client.dob,
                client.is_blacklisted, client.is_active, client.notes
            )
            if success:
                self.logger.info(f"Updated client {client_id}")
            return success
        except ValueError as e:
            self.logger.error(f"Validation error updating client {client_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating client {client_id}: {e}")
            raise
    
    def deactivate_client(self, client_id: int) -> bool:
        """Deactivate a client by setting is_active to False."""
        try:
            current_client = self.get_client(client_id)
            if not current_client:
                self.logger.warning(f"Client {client_id} not found for deactivation")
                return False
            success = self.db.delete_client(client_id)
            if success:
                self.logger.info(f"Deactivated client {client_id}")
            return success
        except Exception as e:
            self.logger.error(f"Error deactivating client {client_id}: {e}")
            raise
    
    def search_clients(self, search_term: str) -> List[Client]:
        """Search clients by name and return a list of matching clients."""
        try:
            with self.db as db:
                query = "SELECT * FROM clients WHERE full_name LIKE ? AND is_active = TRUE"
                results = db.execute_query(query, ('%' + search_term + '%',))
                return [Client.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error searching clients: {e}")
            raise
    
    def import_clients_from_csv(self, csv_path: str) -> int:
        """Import clients from a CSV file and return the number of imported clients."""
        try:
            importer = CSVImporter(self.db)
            imported_count = importer.import_clients(csv_path)
            self.logger.info(f"Imported {imported_count} clients from {csv_path}")
            return imported_count
        except Exception as e:
            self.logger.error(f"Error importing clients from {csv_path}: {e}")
            raise
    
    def get_digital_checklist(self, client_id: int) -> Optional[dict]:
        """Retrieve the digital checklist for a client (placeholder for future implementation)."""
        try:
            with self.db as db:
                query = "SELECT * FROM digital_checklists WHERE client_id = ? AND is_completed = FALSE"
                results = db.execute_query(query, (client_id,))
                return results[0] if results else None
        except Exception as e:
            self.logger.error(f"Error retrieving checklist for client {client_id}: {e}")
            raise
    
    def update_digital_checklist(self, client_id: int, questions: str) -> bool:
        """Update or create a digital checklist for a client (placeholder for future implementation)."""
        try:
            with self.db as db:
                query = "INSERT OR REPLACE INTO digital_checklists (client_id, checklist_date, questions, is_completed) VALUES (?, ?, ?, ?)"
                params = (client_id, datetime.now().strftime('%Y-%m-%d'), questions, False)
                db.execute_query(query, params)
                self.logger.info(f"Updated checklist for client {client_id}")
                return True
        except Exception as e:
            self.logger.error(f"Error updating checklist for client {client_id}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = ClientManager("config/secrets.yaml", "data/database.db")
    try:
        # Add a client
        client_id = manager.add_client("Maria Nowak", "+48 987 654 321", "maria@example.com", "1992-06-20")
        print(f"Added client ID: {client_id}")
        
        # Retrieve client
        client = manager.get_client(client_id)
        print(f"Retrieved client: {client}")
        
        # Update client
        manager.update_client(client_id, notes="First visit completed")
        updated_client = manager.get_client(client_id)
        print(f"Updated client: {updated_client}")
        
        # Search clients
        search_results = manager.search_clients("Maria")
        print(f"Search results: {[str(c) for c in search_results]}")
    except Exception as e:
        print(f"Error: {e}")