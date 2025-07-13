# controllers/client_controller.py
from sqlalchemy.orm import Session
from sqlalchemy import or_ # Import or_ for combining filters
from models.client import Client
from typing import Optional, List, Dict, Any, Union
from datetime import date, datetime # Import datetime for date parsing

import traceback # For detailed error logging

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
                      excel_id: Optional[str] = None
                      ) -> Optional[Client]:
        """
        Creates a new client in the database.
        This method is typically called by get_or_create_client if no existing client is found.
        It does NOT perform duplicate checks itself to avoid redundant lookups.
        """
        if not full_name:
            print("Error: Client full name cannot be empty for creation.")
            return None

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
            excel_id=excel_id
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
            traceback.print_exc() # Print full traceback for detailed debugging
            return None

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """Retrieves a client by their ID."""
        return self.db.query(Client).get(client_id)

    def get_client_by_phone_number(self, phone_number: str) -> Optional[Client]:
        """Retrieves a client by their phone number."""
        if not phone_number:
            return None
        return self.db.query(Client).filter(Client.phone_number == phone_number).first()

    def get_client_by_email(self, email: str) -> Optional[Client]:
        """Retrieves a client by their email address."""
        if not email:
            return None
        return self.db.query(Client).filter(Client.email == email).first()

    def get_client_by_excel_id(self, excel_id: str) -> Optional[Client]:
        """Retrieves a client by their Excel import ID."""
        if not excel_id:
            return None
        return self.db.query(Client).filter(Client.excel_id == excel_id).first()

    def get_client_by_name(self, full_name: str) -> Optional[Client]:
        """Retrieves a client by their full name (case-insensitive search)."""
        if not full_name:
            return None
        # Using .ilike() for case-insensitive contains, assuming full_name might not be exact
        return self.db.query(Client).filter(Client.full_name.ilike(full_name)).first()

    def get_or_create_client(self, **client_data: Any) -> Optional[Client]:
        """
        Retrieves a client by available identifying data (excel_id, phone, email, full_name)
        or creates a new client if no match is found.
        Prioritizes excel_id, then phone_number, then email, then attempts to create using full_name.
        """
        excel_id = client_data.get('excel_id')
        phone_number = client_data.get('phone_number')
        email = client_data.get('email')
        full_name = client_data.get('full_name') # full_name is required for creation if no match

        client = None

        # 1. Try to find by Excel ID (most reliable for imports)
        if excel_id:
            client = self.get_client_by_excel_id(excel_id)
            if client:
                print(f"Found client by Excel ID '{excel_id}': {client.full_name}")
                return client

        # 2. Try to find by phone number
        if phone_number:
            client = self.get_client_by_phone_number(phone_number)
            if client:
                print(f"Found client by phone number '{phone_number}': {client.full_name}")
                # If found by phone, but had an excel_id that didn't match an existing client,
                # you might want to update the existing client's excel_id here.
                # For now, we'll just return it.
                if excel_id and not client.excel_id: # If existing client has no excel_id, assign it
                    print(f"Updating client {client.id} with excel_id: {excel_id}")
                    self.update_client(client.id, {'excel_id': excel_id})
                    return client
                return client

        # 3. Try to find by email
        if email:
            client = self.get_client_by_email(email)
            if client:
                print(f"Found client by email '{email}': {client.full_name}")
                # Same logic as above for excel_id update
                if excel_id and not client.excel_id:
                    print(f"Updating client {client.id} with excel_id: {excel_id}")
                    self.update_client(client.id, {'excel_id': excel_id})
                    return client
                return client

        # 4. Try to find by full_name (least reliable for uniqueness)
        if full_name:
            client = self.get_client_by_name(full_name) # Uses ilike for case-insensitivity
            if client:
                print(f"Found client by name '{full_name}': {client.full_name}. Consider combining/merging if this isn't the same client.")
                # Same logic as above for excel_id update
                if excel_id and not client.excel_id:
                    print(f"Updating client {client.id} with excel_id: {excel_id}")
                    self.update_client(client.id, {'excel_id': excel_id})
                    return client
                return client

        # 5. If still no client found, create a new one using the provided data
        if full_name: # full_name is mandatory for new client creation
            print(f"Client with provided details not found. Creating new client: '{full_name}'.")
            # Filter out keys that are specifically handled or not directly mapped to Client model constructor
            filtered_client_data = {
                k: v for k, v in client_data.items()
                if k in ['full_name', 'phone_number', 'email', 'facebook_id', 'instagram_handle',
                         'booksy_used', 'date_of_birth', 'is_blacklisted', 'is_active', 'notes', 'excel_id']
            }
            # Ensure date_of_birth is a date object if provided as a string
            if 'date_of_birth' in filtered_client_data and isinstance(filtered_client_data['date_of_birth'], str):
                try:
                    filtered_client_data['date_of_birth'] = datetime.strptime(filtered_client_data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    print(f"Warning: Invalid date_of_birth format '{filtered_client_data['date_of_birth']}'. Skipping date_of_birth for new client.")
                    filtered_client_data['date_of_birth'] = None

            return self.create_client(**filtered_client_data)
        else:
            print("Error: Cannot create client. 'full_name' is required when no existing client is found by other identifiers.")
            return None


    def search_clients(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches clients by full name, phone number, email, or excel_id (case-insensitive).
        Returns a list of client dictionaries.
        """
        search_pattern = f"%{query.lower()}%"
        clients = self.db.query(Client).filter(
            or_(
                Client.full_name.ilike(search_pattern),
                Client.phone_number.ilike(search_pattern),
                Client.email.ilike(search_pattern),
                Client.excel_id.ilike(search_pattern) # Added excel_id to search
            )
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

        cleaned_updates = {}
        for key, value in updates.items():
            if key == 'date_of_birth':
                if isinstance(value, str):
                    try:
                        cleaned_updates[key] = datetime.strptime(value, '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Warning: Invalid date format for date_of_birth: {value}. Skipping update for this field.")
                        continue
                elif value is None: # Allow setting to None
                    cleaned_updates[key] = None
                elif isinstance(value, date): # Allow passing date objects directly
                    cleaned_updates[key] = value
                else:
                    print(f"Warning: Unexpected type for date_of_birth: {type(value)}. Skipping update for this field.")
                    continue
            elif value == "": # Convert empty strings to None for nullable fields
                cleaned_updates[key] = None
            else:
                cleaned_updates[key] = value

        try:
            for key, value in cleaned_updates.items():
                if hasattr(client, key):
                    setattr(client, key, value)
                else:
                    print(f"Warning: Attempted to set non-existent field '{key}' on Client model for ID {client_id}.")
            self.db.commit()
            self.db.refresh(client)
            print(f"Client '{client.full_name}' (ID: {client.id}) updated successfully.")
            return client
        except Exception as e:
            self.db.rollback()
            print(f"Error updating client {client_id}: {e}")
            traceback.print_exc()
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
            # You might want to add logic here to handle related appointments (e.g., cascade delete, set null, or prevent deletion)
            self.db.delete(client)
            self.db.commit()
            print(f"Client '{client.full_name}' (ID: {client.id}) deleted successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting client {client_id}: {e}")
            traceback.print_exc()
            return False

    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Retrieves all clients, ordered by full name, as a list of dictionaries."""
        clients = self.db.query(Client).order_by(Client.full_name).all()
        return [client.to_dict() for client in clients]