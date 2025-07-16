# client.py

import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from database.database import execute_query, fetch_one, fetch_all

class Client:
    """Represents a client in the laser hair removal business application."""
    
    MIN_VISIT_SPACING_WEEKS = 6  # Minimum weeks between laser treatment appointments

    def __init__(self, client_id: Optional[int] = None, first_name: str = "", last_name: str = "", 
                 email: str = "", phone: str = "", notes: str = ""):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.notes = notes

    def validate(self) -> bool:
        """Validate client data before saving to the database."""
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required.")
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Valid email is required.")
        if not self.phone or not self.phone.strip():
            raise ValueError("Phone number is required.")
        return True

    def save(self) -> int:
        """Save or update the client in the database. Returns the client ID."""
        try:
            self.validate()
            if self.client_id is None:
                # Insert new client
                query = """
                    INSERT INTO clients (first_name, last_name, email, phone, notes)
                    VALUES (?, ?, ?, ?, ?)
                """
                params = (self.first_name, self.last_name, self.email, self.phone, self.notes)
                self.client_id = execute_query(query, params, return_id=True)
            else:
                # Update existing client
                query = """
                    UPDATE clients
                    SET first_name = ?, last_name = ?, email = ?, phone = ?, notes = ?
                    WHERE id = ?
                """
                params = (self.first_name, self.last_name, self.email, self.phone, self.notes, self.client_id)
                execute_query(query, params)
            return self.client_id
        except Exception as e:
            raise Exception(f"Failed to save client: {str(e)}")

    @staticmethod
    def get_by_id(client_id: int) -> Optional['Client']:
        """Retrieve a client by ID from the database."""
        try:
            query = "SELECT id, first_name, last_name, email, phone, notes FROM clients WHERE id = ?"
            result = fetch_one(query, (client_id,))
            if result:
                return Client(
                    client_id=result[0],
                    first_name=result[1],
                    last_name=result[2],
                    email=result[3],
                    phone=result[4],
                    notes=result[5]
                )
            return None
        except Exception as e:
            raise Exception(f"Failed to retrieve client: {str(e)}")

    @staticmethod
    def get_all() -> List['Client']:
        """Retrieve all clients from the database."""
        try:
            query = "SELECT id, first_name, last_name, email, phone, notes FROM clients"
            results = fetch_all(query)
            return [
                Client(
                    client_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    phone=row[4],
                    notes=row[5]
                ) for row in results
            ]
        except Exception as e:
            raise Exception(f"Failed to retrieve clients: {str(e)}")

    def delete(self) -> None:
        """Delete the client from the database."""
        try:
            if self.client_id is None:
                raise ValueError("Cannot delete client: No client ID specified.")
            query = "DELETE FROM clients WHERE id = ?"
            execute_query(query, (self.client_id,))
        except Exception as e:
            raise Exception(f"Failed to delete client: {str(e)}")

    def schedule_appointment(self, date: datetime, treatment_type: str) -> int:
        """Schedule an appointment for the client, enforcing visit spacing logic. Returns appointment ID."""
        try:
            if self.client_id is None:
                raise ValueError("Cannot schedule appointment: Client not saved.")
            
            # Check last appointment date to enforce minimum spacing
            query = "SELECT MAX(date) FROM appointments WHERE client_id = ? AND treatment_type = ?"
            last_appointment = fetch_one(query, (self.client_id, treatment_type))
            if last_appointment and last_appointment[0]:
                last_date = datetime.strptime(last_appointment[0], "%Y-%m-%d %H:%M:%S")
                min_next_date = last_date + timedelta(weeks=self.MIN_VISIT_SPACING_WEEKS)
                if date < min_next_date:
                    raise ValueError(
                        f"Appointments must be at least {self.MIN_VISIT_SPACING_WEEKS} weeks apart. "
                        f"Earliest possible date: {min_next_date.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

            # Insert appointment
            query = """
                INSERT INTO appointments (client_id, date, treatment_type)
                VALUES (?, ?, ?)
            """
            params = (self.client_id, date.strftime("%Y-%m-%d %H:%M:%S"), treatment_type)
            return execute_query(query, params, return_id=True)
        except Exception as e:
            raise Exception(f"Failed to schedule appointment: {str(e)}")

    def get_appointments(self) -> List[Dict]:
        """Retrieve all appointments for the client."""
        try:
            query = "SELECT id, date, treatment_type FROM appointments WHERE client_id = ? ORDER BY date"
            results = fetch_all(query, (self.client_id,))
            return [
                {
                    "id": row[0],
                    "date": datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"),
                    "treatment_type": row[2]
                } for row in results
            ]
        except Exception as e:
            raise Exception(f"Failed to retrieve appointments: {str(e)}")