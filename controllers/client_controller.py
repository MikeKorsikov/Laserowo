# controllers/client_controller.py
from datetime import date, datetime # <--- ADD datetime here
from sqlalchemy.orm import Session
from models.client import Client
from sqlalchemy import or_
from typing import Optional, List, Dict, Any

class ClientController:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self,
                      full_name: str,
                      email: Optional[str] = None,
                      phone_number: Optional[str] = None,
                      gender: Optional[str] = None,
                      date_of_birth: Optional[date] = None,
                      notes: Optional[str] = None,
                      facebook_id: Optional[str] = None,
                      instagram_handle: Optional[str] = None,
                      booksy_used: bool = False,
                      is_blacklisted: bool = False,
                      is_active: bool = True,
                      excel_id: Optional[str] = None
                     ) -> Optional[Client]:
        """Creates a new client."""
        if not full_name:
            print("Error: Client full name is required.")
            return None
        
        # Check for existing client to prevent duplicates (using phone/email/excel_id as primary unique fields)
        existing_client = self.db.query(Client).filter(
            or_(
                Client.excel_id == excel_id if excel_id else False,
                Client.phone_number == phone_number if phone_number else False,
                Client.email == email if email else False
            )
        ).first()

        if existing_client:
            print(f"Warning: Client '{full_name}' (Email: {email}, Phone: {phone_number}) already exists with ID {existing_client.id}. Skipping creation.")
            return existing_client

        new_client = Client(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            gender=gender,
            date_of_birth=date_of_birth,
            notes=notes,
            facebook_id=facebook_id,
            instagram_handle=instagram_handle,
            booksy_used=booksy_used,
            is_blacklisted=is_blacklisted,
            is_active=is_active,
            excel_id=excel_id
        )
        try:
            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            print(f"Client created: ID {new_client.id}, Name: {new_client.full_name}")
            return new_client
        except Exception as e:
            self.db.rollback()
            print(f"Error creating client '{full_name}': {e}")
            return None

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Retrieves a client by their ID."""
        return self.db.query(Client).get(client_id)

    def get_client_by_name(self, full_name: str) -> Optional[Client]:
        """Retrieves a client by their full name (case-insensitive match)."""
        return self.db.query(Client).filter(Client.full_name.ilike(full_name)).first()

    def get_client_by_excel_id(self, excel_id: str) -> Optional[Client]:
        """Retrieves a client by their external Excel ID."""
        return self.db.query(Client).filter(Client.excel_id == excel_id).first()

    def get_client_by_phone_or_email_or_name(self, phone_number: Optional[str] = None, 
                                              email: Optional[str] = None, 
                                              full_name: Optional[str] = None) -> Optional[Client]:
        """
        Retrieves a client by phone number, email, or full name. 
        Prioritizes phone, then email, then name.
        """
        query = self.db.query(Client)
        filters = []
        if phone_number:
            filters.append(Client.phone_number == phone_number)
        if email:
            filters.append(Client.email == email)
        if full_name:
            filters.append(Client.full_name.ilike(full_name))

        if filters:
            return query.filter(or_(*filters)).first()
        return None
    
    def search_clients(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for clients by full name, email, or phone number (case-insensitive).
        Returns clients as dictionaries.
        """
        search_pattern = f"%{search_term}%" # For LIKE queries

        clients = self.db.query(Client).filter(
            or_(
                Client.full_name.ilike(search_pattern),
                Client.email.ilike(search_pattern),
                Client.phone_number.ilike(search_pattern)
            )
        ).all()
        return [client.to_dict() for client in clients]


    def get_all_clients_raw(self) -> List[Client]:
        """Retrieves all client ORM objects directly."""
        return self.db.query(Client).all()

    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Retrieves all clients as dictionaries."""
        clients = self.db.query(Client).all()
        return [client.to_dict() for client in clients]

    def update_client(self, client_id: int, updates: Dict[str, Any]) -> Optional[Client]:
        """Updates an existing client."""
        client = self.get_client_by_id(client_id)
        if not client:
            print(f"Client with ID {client_id} not found.")
            return None
        
        # Handle date_of_birth string to date conversion if present in updates
        if 'date_of_birth' in updates:
            dob_value = updates['date_of_birth']
            if isinstance(dob_value, str):
                try:
                    updates['date_of_birth'] = datetime.strptime(dob_value, '%Y-%m-%d').date()
                except ValueError:
                    print(f"Warning: Could not parse date_of_birth '{dob_value}'. Skipping update for this field.")
                    updates.pop('date_of_birth')

        for key, value in updates.items():
            if hasattr(client, key):
                setattr(client, key, value)
            else:
                print(f"Warning: Attempted to set non-existent field '{key}' on Client model for ID {client_id}.")
        try:
            self.db.commit()
            self.db.refresh(client)
            print(f"Client {client_id} updated.")
            return client
        except Exception as e:
            self.db.rollback()
            print(f"Error updating client {client_id}: {e}")
            return None

    def delete_client(self, client_id: int) -> bool:
        """Deletes a client by ID."""
        client = self.get_client_by_id(client_id)
        if not client:
            print(f"Client with ID {client_id} not found for deletion.")
            return False
        try:
            self.db.delete(client)
            self.db.commit()
            print(f"Client {client_id} deleted successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting client {client_id}: {e}")
            return False