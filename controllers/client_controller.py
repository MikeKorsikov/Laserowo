# controllers/client_controller.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
from models.client import Client
from models.appointment import Appointment # For checking blacklisted status against appointments
from models.digital_checklist import DigitalChecklist # For linking digital checklist
from config.database import get_db # To get a session
from typing import List, Optional

class ClientController:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_client(self,
                      full_name: str,
                      phone_number: Optional[str] = None,
                      email: Optional[str] = None,
                      facebook_id: Optional[str] = None,
                      instagram_handle: Optional[str] = None,
                      booksy_indicator: bool = False,
                      date_of_birth: Optional[date] = None) -> Optional[Client]:
        """
        Creates a new client record.
        Returns the created Client object or None if creation fails.
        """
        try:
            # Basic validation
            if not full_name:
                raise ValueError("Full name cannot be empty.")
            if phone_number and self.db.query(Client).filter_by(phone_number=phone_number).first():
                raise ValueError(f"Client with phone number {phone_number} already exists.")
            if email and self.db.query(Client).filter_by(email=email).first():
                raise ValueError(f"Client with email {email} already exists.")

            new_client = Client(
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                facebook_id=facebook_id,
                instagram_handle=instagram_handle,
                booksy_indicator=booksy_indicator,
                date_of_birth=date_of_birth,
                is_active=True,
                is_blacklisted=False # New clients are not blacklisted by default
            )
            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            return new_client
        except ValueError as e:
            print(f"Error creating client: {e}")
            self.db.rollback()
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.db.rollback()
            return None

    def get_client(self, client_id: int) -> Optional[Client]:
        """Retrieves a client by their ID."""
        return self.db.query(Client).get(client_id)

    def get_all_clients(self, include_inactive: bool = False) -> List[Client]:
        """Retrieves all active clients, optionally including inactive ones."""
        query = self.db.query(Client)
        if not include_inactive:
            query = query.filter(Client.is_active == True)
        return query.order_by(Client.full_name).all()

    def search_clients(self, query_string: str) -> List[Client]:
        """
        Searches clients by full name, phone number, or email.
        """
        search_pattern = f"%{query_string}%"
        return self.db.query(Client).filter(
            or_(
                Client.full_name.ilike(search_pattern),
                Client.phone_number.ilike(search_pattern),
                Client.email.ilike(search_pattern)
            )
        ).all()

    def update_client(self, client_id: int, **kwargs) -> Optional[Client]:
        """
        Updates an existing client's details.
        Kwargs can include: full_name, phone_number, email, facebook_id, instagram_handle,
                          booksy_indicator, date_of_birth, is_blacklisted, is_active.
        """
        client = self.get_client(client_id)
        if not client:
            print(f"Client with ID {client_id} not found.")
            return None

        try:
            for key, value in kwargs.items():
                if hasattr(client, key):
                    setattr(client, key, value)
                else:
                    print(f"Warning: Attempted to update non-existent field '{key}' for client.")

            # Specific validation for unique fields during update
            if 'phone_number' in kwargs and kwargs['phone_number'] is not None:
                existing_client = self.db.query(Client).filter(Client.phone_number == kwargs['phone_number'], Client.id != client_id).first()
                if existing_client:
                    raise ValueError(f"Phone number {kwargs['phone_number']} is already in use by another client.")
            if 'email' in kwargs and kwargs['email'] is not None:
                existing_client = self.db.query(Client).filter(Client.email == kwargs['email'], Client.id != client_id).first()
                if existing_client:
                    raise ValueError(f"Email {kwargs['email']} is already in use by another client.")

            self.db.commit()
            self.db.refresh(client)
            return client
        except ValueError as e:
            print(f"Error updating client: {e}")
            self.db.rollback()
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.db.rollback()
            return None

    def deactivate_client(self, client_id: int) -> bool:
        """
        Deactivates a client, retaining their history.
        Prevents new appointments but keeps historical data.
        """
        client = self.get_client(client_id)
        if client:
            try:
                client.is_active = False
                self.db.commit()
                return True
            except Exception as e:
                print(f"Error deactivating client {client_id}: {e}")
                self.db.rollback()
                return False
        return False

    def blacklist_client(self, client_id: int, blacklist: bool = True) -> bool:
        """
        Sets or unsets the 'blacklist' flag for a client.
        """
        client = self.get_client(client_id)
        if client:
            try:
                client.is_blacklisted = blacklist
                self.db.commit()
                return True
            except Exception as e:
                print(f"Error blacklisting client {client_id}: {e}")
                self.db.rollback()
                return False
        return False

    def get_client_history(self, client_id: int) -> List[Appointment]:
        """
        Retrieves all appointments for a given client, ordered by date.
        """
        client = self.get_client(client_id)
        if not client:
            return []
        return self.db.query(Appointment).filter(Appointment.client_id == client_id).order_by(Appointment.appointment_date, Appointment.start_time).all()

    def add_digital_checklist(self, client_id: int, allergies: Optional[str] = None,
                              health_issues: Optional[str] = None, medications: Optional[str] = None,
                              other_notes: Optional[str] = None) -> Optional[DigitalChecklist]:
        """
        Adds a digital checklist entry for a client.
        """
        client = self.get_client(client_id)
        if not client:
            print(f"Client with ID {client_id} not found for checklist.")
            return None
        try:
            new_checklist = DigitalChecklist(
                client_id=client_id,
                checklist_date=date.today(),
                allergies=allergies,
                health_issues=health_issues,
                medications=medications,
                other_notes=other_notes,
                is_completed=True
            )
            self.db.add(new_checklist)
            self.db.commit()
            self.db.refresh(new_checklist)
            return new_checklist
        except Exception as e:
            print(f"Error adding digital checklist for client {client_id}: {e}")
            self.db.rollback()
            return None

    def get_digital_checklist(self, client_id: int) -> Optional[DigitalChecklist]:
        """
        Retrieves the most recent digital checklist for a client.
        Assuming one-off, so just get the latest if multiple somehow exist.
        """
        return self.db.query(DigitalChecklist).filter(DigitalChecklist.client_id == client_id).order_by(DigitalChecklist.checklist_date.desc()).first()