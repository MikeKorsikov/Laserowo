from src.database.db_operations import DatabaseOperations
from src.models.appointment import Appointment
from src.models.client import Client
from src.utils.calendar_sync import CalendarSync
from src.utils.email_sender import EmailSender
from src.utils.sms_sender import SMSSender
import logging
from datetime import datetime, timedelta
from typing import List, Optional

class AppointmentManager:
    """Manages appointment-related operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.calendar_sync = CalendarSync(config_path)
        self.email_sender = EmailSender(config_path)
        self.sms_sender = SMSSender(config_path)
    
    def schedule_appointment(self, client_id: int, service_id: int, area_id: int, 
                            appointment_date: str, session_number: int, power: float = None, 
                            amount: float = None, payment_method_id: int = None) -> int:
        """Schedule a new appointment and return the appointment_id."""
        try:
            client = self._get_client(client_id)
            if not client or not client.is_active:
                raise ValueError("Client is inactive or not found")
            
            # Validate visit spacing
            previous_appointment = self.get_previous_appointment(client_id, area_id)
            new_appointment = Appointment(0, client_id, service_id, area_id, appointment_date, session_number, power, amount=amount, payment_method_id=payment_method_id)
            if previous_appointment and not new_appointment.validate_visit_spacing(previous_appointment):
                raise ValueError("Insufficient waiting period since last appointment")
            
            # Insert appointment
            query = """
                INSERT INTO appointments (client_id, service_id, area_id, appointment_date, session_number_for_area, power, 
                appointment_status, amount, payment_method_id)
                VALUES (?, ?, ?, ?, ?, ?, 'Scheduled', ?, ?)
            """
            params = (client_id, service_id, area_id, appointment_date, session_number, power, amount, payment_method_id)
            self.db.execute_query(query, params)
            appointment_id = self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            
            # Sync to calendar and send reminder
            self._sync_and_notify(appointment_id, appointment_date, client)
            self.logger.info(f"Scheduled appointment {appointment_id} for client {client_id}")
            return appointment_id
        except ValueError as e:
            self.logger.error(f"Validation error scheduling appointment: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error scheduling appointment: {e}")
            raise
    
    def get_previous_appointment(self, client_id: int, area_id: int) -> Optional[Appointment]:
        """Retrieve the most recent completed appointment for the given client and area."""
        try:
            query = """
                SELECT * FROM appointments 
                WHERE client_id = ? AND area_id = ? AND appointment_status = 'Completed'
                ORDER BY appointment_date DESC LIMIT 1
            """
            results = self.db.execute_query(query, (client_id, area_id))
            return Appointment.from_dict(results[0]) if results else None
        except Exception as e:
            self.logger.error(f"Error retrieving previous appointment: {e}")
            raise
    
    def reschedule_appointment(self, appointment_id: int, new_date: str) -> bool:
        """Reschedule an existing appointment to a new date."""
        try:
            appointment = self._get_appointment(appointment_id)
            if not appointment or appointment.appointment_status not in ['Scheduled', 'Rescheduled']:
                raise ValueError("Appointment not available for rescheduling")
            
            query = "UPDATE appointments SET appointment_date = ?, appointment_status = 'Rescheduled' WHERE appointment_id = ?"
            self.db.execute_query(query, (new_date, appointment_id))
            self._sync_and_notify(appointment_id, new_date, self._get_client(appointment.client_id))
            self.logger.info(f"Rescheduled appointment {appointment_id} to {new_date}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error rescheduling appointment {appointment_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error rescheduling appointment {appointment_id}: {e}")
            raise
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an existing appointment."""
        try:
            appointment = self._get_appointment(appointment_id)
            if not appointment or appointment.appointment_status not in ['Scheduled', 'Rescheduled']:
                raise ValueError("Appointment not available for cancellation")
            
            query = "UPDATE appointments SET appointment_status = 'Cancelled' WHERE appointment_id = ?"
            self.db.execute_query(query, (appointment_id,))
            self.logger.info(f"Cancelled appointment {appointment_id}")
            return True
        except ValueError as e:
            self.logger.error(f"Validation error cancelling appointment {appointment_id}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error cancelling appointment {appointment_id}: {e}")
            raise
    
    def get_appointments_by_date(self, date: str) -> List[Appointment]:
        """Retrieve all appointments for a specific date."""
        try:
            query = "SELECT * FROM appointments WHERE appointment_date = ? AND appointment_status IN ('Scheduled', 'Rescheduled')"
            results = self.db.execute_query(query, (date,))
            return [Appointment.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving appointments for {date}: {e}")
            raise
    
    def _get_client(self, client_id: int) -> Optional[Client]:
        """Helper method to retrieve client."""
        with self.db as db:
            result = db.get_client(client_id)
            return Client.from_dict(result) if result else None
    
    def _get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """Helper method to retrieve appointment."""
        with self.db as db:
            query = "SELECT * FROM appointments WHERE appointment_id = ?"
            results = db.execute_query(query, (appointment_id,))
            return Appointment.from_dict(results[0]) if results else None
    
    def _sync_and_notify(self, appointment_id: int, appointment_date: str, client: Client) -> None:
        """Sync appointment to calendar and send reminder."""
        try:
            # Sync to calendar
            self.calendar_sync.add_event(appointment_id, appointment_date, client.full_name)
            
            # Send reminder (e.g., 24 hours before)
            reminder_date = (datetime.strptime(appointment_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            if datetime.now().date() <= datetime.strptime(reminder_date, '%Y-%m-%d').date():
                message = f"Reminder: Your appointment on {appointment_date} is tomorrow."
                self.email_sender.send_email(client.email, "Appointment Reminder", message)
                self.sms_sender.send_sms(client.phone_number, message)
                self.logger.info(f"Sent reminder for appointment {appointment_id}")
        except Exception as e:
            self.logger.error(f"Error syncing or notifying for appointment {appointment_id}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = AppointmentManager("config/secrets.yaml", "data/database.db")
    try:
        # Schedule an appointment
        client_id = 1
        appointment_id = manager.schedule_appointment(
            client_id=client_id,
            service_id=1,
            area_id=1,
            appointment_date="2025-07-18",
            session_number=1,
            power=50.0,
            amount=100.0,
            payment_method_id=1
        )
        print(f"Scheduled appointment ID: {appointment_id}")
        
        # Get appointments for a date
        appointments = manager.get_appointments_by_date("2025-07-18")
        print(f"Appointments on 2025-07-18: {[str(a) for a in appointments]}")
    except Exception as e:
        print(f"Error: {e}")