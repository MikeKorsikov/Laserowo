# appointment.py

import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from src.database.db_manager import DBManager
from src.utils.helpers import validate_date, log_error

class Appointment:
    def __init__(self, client_id: str, appointment_date: str, appointment_time: str, 
                 body_part: str, price: float, status: str = "scheduled", 
                 appointment_id: Optional[str] = None):
        """Initialize an Appointment object.

        Args:
            client_id (str): UUID of the client.
            appointment_date (str): Date of the appointment (YYYY-MM-DD).
            appointment_time (str): Time of the appointment (HH:MM).
            body_part (str): Body part for laser hair removal (e.g., 'legs').
            price (float): Price of the appointment.
            status (str): Appointment status (e.g., 'scheduled', 'completed', 'canceled').
            appointment_id (Optional[str]): UUID of the appointment, generated if None.
        """
        self.appointment_id = appointment_id or str(uuid.uuid4())
        self.client_id = client_id
        self.appointment_date = validate_date(appointment_date)
        self.appointment_time = appointment_time
        self.body_part = body_part
        self.price = float(price)
        self.status = status
        self.db_manager = DBManager()

    def save(self) -> bool:
        """Save the appointment to the database after validating visit spacing.

        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            # Check for visit spacing (minimum 4 weeks for same client and body part)
            if not self._validate_visit_spacing():
                log_error(f"Appointment for client {self.client_id} on {self.body_part} violates 4-week spacing rule.")
                return False

            query = """
                INSERT INTO appointments (appointment_id, client_id, appointment_date, 
                                         appointment_time, body_part, price, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.appointment_id, self.client_id, self.appointment_date, 
                      self.appointment_time, self.body_part, self.price, self.status)
            self.db_manager.execute_query(query, params)
            return True
        except Exception as e:
            log_error(f"Failed to save appointment: {str(e)}")
            return False

    def _validate_visit_spacing(self) -> bool:
        """Check if the appointment adheres to the 4-week spacing rule.

        Returns:
            bool: True if valid, False if another appointment exists within 4 weeks.
        """
        try:
            four_weeks_ago = (datetime.strptime(self.appointment_date, "%Y-%m-%d") - 
                             timedelta(weeks=4)).strftime("%Y-%m-%d")
            query = """
                SELECT appointment_date FROM appointments 
                WHERE client_id = ? AND body_part = ? AND status = 'scheduled'
                AND appointment_date >= ? AND appointment_date <= ?
            """
            params = (self.client_id, self.body_part, four_weeks_ago, self.appointment_date)
            result = self.db_manager.fetch_all(query, params)
            return len(result) == 0
        except Exception as e:
            log_error(f"Error validating visit spacing: {str(e)}")
            return False

    @staticmethod
    def get_by_id(appointment_id: str) -> Optional['Appointment']:
        """Retrieve an appointment by its ID.

        Args:
            appointment_id (str): UUID of the appointment.

        Returns:
            Optional[Appointment]: Appointment object if found, None otherwise.
        """
        try:
            query = """
                SELECT client_id, appointment_date, appointment_time, body_part, price, status
                FROM appointments WHERE appointment_id = ?
            """
            result = DBManager().fetch_one(query, (appointment_id,))
            if result:
                return Appointment(
                    client_id=result[0],
                    appointment_date=result[1],
                    appointment_time=result[2],
                    body_part=result[3],
                    price=result[4],
                    status=result[5],
                    appointment_id=appointment_id
                )
            return None
        except Exception as e:
            log_error(f"Error retrieving appointment {appointment_id}: {str(e)}")
            return None

    @staticmethod
    def get_all_by_client(client_id: str) -> List['Appointment']:
        """Retrieve all appointments for a client.

        Args:
            client_id (str): UUID of the client.

        Returns:
            List[Appointment]: List of Appointment objects.
        """
        try:
            query = """
                SELECT appointment_id, client_id, appointment_date, appointment_time, 
                       body_part, price, status
                FROM appointments WHERE client_id = ?
            """
            results = DBManager().fetch_all(query, (client_id,))
            return [
                Appointment(
                    client_id=r[1],
                    appointment_date=r[2],
                    appointment_time=r[3],
                    body_part=r[4],
                    price=r[5],
                    status=r[6],
                    appointment_id=r[0]
                ) for r in results
            ]
        except Exception as e:
            log_error(f"Error retrieving appointments for client {client_id}: {str(e)}")
            return []

    def update(self, **kwargs) -> bool:
        """Update appointment attributes in the database.

        Args:
            **kwargs: Fields to update (e.g., appointment_date, status).

        Returns:
            bool: True if updated successfully, False otherwise.
        """
        try:
            # Update object attributes if provided
            if "appointment_date" in kwargs:
                self.appointment_date = validate_date(kwargs["appointment_date"])
            if "appointment_time" in kwargs:
                self.appointment_time = kwargs["appointment_time"]
            if "body_part" in kwargs:
                self.body_part = kwargs["body_part"]
            if "price" in kwargs:
                self.price = float(kwargs["price"])
            if "status" in kwargs:
                self.status = kwargs["status"]

            # Validate visit spacing if date or body part is updated
            if "appointment_date" in kwargs or "body_part" in kwargs:
                if not self._validate_visit_spacing():
                    log_error(f"Updated appointment violates 4-week spacing rule.")
                    return False

            query = """
                UPDATE appointments 
                SET appointment_date = ?, appointment_time = ?, body_part = ?, 
                    price = ?, status = ?
                WHERE appointment_id = ?
            """
            params = (self.appointment_date, self.appointment_time, self.body_part, 
                      self.price, self.status, self.appointment_id)
            self.db_manager.execute_query(query, params)
            return True
        except Exception as e:
            log_error(f"Error updating appointment {self.appointment_id}: {str(e)}")
            return False

    def delete(self) -> bool:
        """Delete the appointment from the database.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        try:
            query = "DELETE FROM appointments WHERE appointment_id = ?"
            self.db_manager.execute_query(query, (self.appointment_id,))
            return True
        except Exception as e:
            log_error(f"Error deleting appointment {self.appointment_id}: {str(e)}")
            return False