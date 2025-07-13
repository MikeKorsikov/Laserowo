# controllers/client_controller.py
from sqlalchemy.orm import Session
from models.client import Client 
from typing import Optional, List, Dict, Any, Union
from datetime import date 

class ClientController:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self,
                      full_name: str,
                      phone_number: Optional[str] = None,
                      email: Optional[str] = None,
                      facebook_id: Optional[str] = None,
                      instagram_handle: Optional[str] = None,
                      booksy_used: bool = False,
                      date_of_birth: Optional[date] = None,
                      is_blacklisted: bool = False,
                      is_active: bool = True,
                      notes: Optional[str] = None,
                      excel_id: Optional[str] = None # Added excel_id
                      ) -> Optional[Client]:
        """
        Creates a new client in the database.
        Checks for existing clients by phone, email, or excel_id to prevent duplicates.
        """
        if not full_name:
            print("Error: Client full name cannot be empty.")
            return None

        # Check for existing client by unique identifiers
        # Prioritize excel_id, then phone, then email
        existing_client = None
        if excel_id:
            existing_client = self.get_client_by_excel_id(excel_id)
        if not existing_client and phone_number:
            existing_client = self.get_client_by_phone_number(phone_number)
        if not existing_client and email:
            existing_client = self.get_client_by_email(email)

        if existing_client:
            print(f"Warning: Client with similar details (excel_id: {excel_id}, phone: {phone_number}, email: {email}) already exists (ID: {existing_client.id}, Name: {existing_client.full_name}). Skipping creation.")
            return existing_client # Return existing client if found

        new_client = Client(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            facebook_id=facebook_id,
            instagram_handle=instagram_handle,
            booksy_used=booksy_used,
            date_of_birth=date_of_birth,
            is_blacklisted=is_blacklisted,
            is_active=is_active,
            notes=notes,
            excel_id=excel_id # Assign excel_id
        )
        try:
            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            print(f"Client created: {new_client.full_name} (ID: {new_client.id})")
            return new_client
        except Exception as e:
            self.db.rollback()
            print(f"Error creating client '{full_name}': {e}")
            return None

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Retrieves a client by their ID."""
        return self.db.query(Client).get(client_id)

    def get_client_by_phone_number(self, phone_number: str) -> Optional[Client]:
        """Retrieves a client by their phone number."""
        if not phone_number: return None
        return self.db.query(Client).filter(Client.phone_number == phone_number).first()

    def get_client_by_email(self, email: str) -> Optional[Client]:
        """Retrieves a client by their email address."""
        if not email: return None
        return self.db.query(Client).filter(Client.email == email).first()

    def get_client_by_excel_id(self, excel_id: str) -> Optional[Client]:
        """Retrieves a client by their Excel import ID."""
        if not excel_id: return None
        return self.db.query(Client).filter(Client.excel_id == excel_id).first()

    def get_client_by_name(self, full_name: str) -> Optional[Client]:
        """Retrieves a client by their full name (case-insensitive search)."""
        if not full_name: return None
        return self.db.query(Client).filter(Client.full_name.ilike(full_name)).first() # ilike for case-insensitive

    def get_client_by_phone_or_email_or_name(self,
                                              phone_number: Optional[str] = None,
                                              email: Optional[str] = None,
                                              full_name: Optional[str] = None) -> Optional[Client]:
        """
        Retrieves a client by phone number, email, or full name.
        Prioritizes phone, then email, then name.
        """
        if phone_number:
            client = self.get_client_by_phone_number(phone_number)
            if client: return client
        if email:
            client = self.get_client_by_email(email)
            if client: return client
        if full_name:
            # Use a more exact match for name if possible, or case-insensitive contains
            client = self.db.query(Client).filter(Client.full_name.ilike(full_name)).first()
            if client: return client
        return None

    def search_clients(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches clients by full name, phone number, or email.
        Returns a list of client dictionaries.
        """
        search_query = f"%{query.lower()}%"
        clients = self.db.query(Client).filter(
            (Client.full_name.ilike(search_query)) |
            (Client.phone_number.ilike(search_query)) |
            (Client.email.ilike(search_query))
        ).order_by(Client.full_name).all()
        return [client.to_dict() for client in clients]

    def update_client(self, client_id: int, updates: Dict[str, Any]) -> Optional[Client]:
        """
        Updates an existing client's information.
        Args:
            client_id (int): The ID of the client to update.
            updates (Dict[str, Any]): A dictionary of fields to update and their new values.
        Returns:
            Optional[Client]: The updated client object, or None if not found or update fails.
        """
        client = self.db.query(Client).get(client_id)
        if not client:
            print(f"Error: Client with ID {client_id} not found for update.")
            return None

        # Clean up updates dictionary: remove None values for optional fields if they are not explicitly set
        # And ensure date_of_birth is converted to date object if it's a string
        cleaned_updates = {}
        for key, value in updates.items():
            if key == 'date_of_birth' and isinstance(value, str):
                try:
                    cleaned_updates[key] = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    print(f"Warning: Invalid date format for date_of_birth: {value}. Skipping update for this field.")
                    continue
            elif value == "": # Convert empty strings to None for nullable fields
                cleaned_updates[key] = None
            else:
                cleaned_updates[key] = value

        try:
            for key, value in cleaned_updates.items():
                if hasattr(client, key):
                    setattr(client, key, value)
            self.db.commit()
            self.db.refresh(client)
            print(f"Client '{client.full_name}' (ID: {client.id}) updated successfully.")
            return client
        except Exception as e:
            self.db.rollback()
            print(f"Error updating client {client_id}: {e}")
            return None

    def delete_client(self, client_id: int) -> bool:
        """
        Deletes a client from the database.
        Args:
            client_id (int): The ID of the client to delete.
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        client = self.db.query(Client).get(client_id)
        if not client:
            print(f"Error: Client with ID {client_id} not found for deletion.")
            return False
        try:
            self.db.delete(client)
            self.db.commit()
            print(f"Client '{client.full_name}' (ID: {client.id}) deleted successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting client {client_id}: {e}")
            return False

    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Retrieves all clients, ordered by full name, as a list of dictionaries."""
        clients = self.db.query(Client).order_by(Client.full_name).all()
        return [client.to_dict() for client in clients]

# updated