# controllers/appointment_controller.py
from sqlalchemy.orm import Session
from models.appointment import Appointment
from models.client import Client # Import Client model for potential joins/lookups
from models.service import Service # Import Service model for potential joins/lookups
from models.treatment_area import TreatmentArea # Import TreatmentArea model for potential joins/lookups
from models.payment_method import PaymentMethod # Import PaymentMethod model for potential joins/lookups
from datetime import date, time, datetime
from typing import Optional, List, Dict, Any

class AppointmentController:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self,
                           client_id: int,
                           appointment_date: date,
                           start_time: time,
                           # All parameters below must have default values if they are optional
                           service_id: Optional[int] = None,
                           area_id: Optional[int] = None,
                           end_time: Optional[time] = None,
                           session_number_for_area: Optional[int] = None,
                           power_j_cm3: Optional[str] = None,
                           appointment_status: Optional[str] = 'Completed',
                           amount: float = 0.0,
                           payment_method_id: Optional[int] = None,
                           promotion_id: Optional[int] = None,
                           hardware_id: Optional[int] = None,
                           notes: Optional[str] = None,
                           next_suggested_appointment_date: Optional[date] = None
                           ) -> Optional[Appointment]:
        """
        Creates a new appointment record in the database.

        Args:
            client_id (int): The ID of the client for this appointment.
            appointment_date (date): The date of the appointment.
            start_time (time): The start time of the appointment.
            service_id (Optional[int]): The ID of the service provided.
            area_id (Optional[int]): The ID of the treatment area.
            end_time (Optional[time]): The end time of the appointment.
            session_number_for_area (Optional[int]): The session number for the specific area.
            power_j_cm3 (Optional[str]): Power setting in J/cm³.
            appointment_status (Optional[str]): The status of the appointment (e.g., 'Completed', 'Scheduled', 'Cancelled').
            amount (float): The monetary amount for the appointment.
            payment_method_id (Optional[int]): The ID of the payment method used.
            promotion_id (Optional[int]): The ID of any promotion applied.
            hardware_id (Optional[int]): The ID of the hardware used.
            notes (Optional[str]): Any additional notes for the appointment.
            next_suggested_appointment_date (Optional[date]): The suggested date for the next appointment.

        Returns:
            Optional[Appointment]: The newly created Appointment object, or None if creation fails.
        """
        if not client_id or not appointment_date or not start_time:
            print("Error: client_id, appointment_date, and start_time are required for appointment creation.")
            return None

        # Basic validation for end_time: ensure it's not before start_time if both are provided
        if start_time and end_time and end_time < start_time:
            print(f"Warning: end_time ({end_time}) is before start_time ({start_time}). Adjusting end_time to be 1 hour after start_time.")
            # This requires converting to datetime for timedelta operations
            dummy_datetime = datetime.combine(appointment_date, start_time)
            end_time = (dummy_datetime + pd.Timedelta(hours=1)).time()


        new_appointment = Appointment(
            client_id=client_id,
            service_id=service_id,
            area_id=area_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            session_number_for_area=session_number_for_area,
            power_j_cm3=power_j_cm3,
            appointment_status=appointment_status,
            amount=amount,
            payment_method_id=payment_method_id,
            promotion_id=promotion_id,
            hardware_id=hardware_id,
            notes=notes,
            next_suggested_appointment_date=next_suggested_appointment_date
        )
        try:
            self.db.add(new_appointment)
            self.db.commit()
            self.db.refresh(new_appointment)
            print(f"Appointment created: ID {new_appointment.id} for Client {new_appointment.client_id} on {new_appointment.appointment_date}")
            return new_appointment
        except Exception as e:
            self.db.rollback()
            print(f"Error creating appointment for client {client_id} on {appointment_date}: {e}")
            return None

    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Retrieves an appointment by its ID."""
        return self.db.query(Appointment).get(appointment_id)

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        """
        Retrieves all appointments, ordered by date descending.
        Eagerly loads related client, service, area, and payment method data.
        """
        appointments = self.db.query(Appointment).options(
            # Use joinedload to fetch relationships in one query
            # This prevents N+1 query problem when accessing appt.client.full_name etc.
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.area),
            joinedload(Appointment.payment_method)
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]

    def get_appointments_by_client_id(self, client_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves appointments for a specific client, ordered by date descending.
        Eagerly loads related service, area, and payment method data.
        """
        appointments = self.db.query(Appointment).filter(Appointment.client_id == client_id).options(
            joinedload(Appointment.service),
            joinedload(Appointment.area),
            joinedload(Appointment.payment_method)
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]

    def update_appointment(self, appointment_id: int, updates: Dict[str, Any]) -> Optional[Appointment]:
        """
        Updates an existing appointment record.

        Args:
            appointment_id (int): The ID of the appointment to update.
            updates (Dict[str, Any]): A dictionary of fields to update and their new values.

        Returns:
            Optional[Appointment]: The updated Appointment object, or None if update fails or not found.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            print(f"Appointment with ID {appointment_id} not found for update.")
            return None

        # Handle specific type conversions if updates might come as strings (e.g., from a UI form)
        if 'appointment_date' in updates and isinstance(updates['appointment_date'], str):
            updates['appointment_date'] = datetime.strptime(updates['appointment_date'], '%Y-%m-%d').date()
        if 'start_time' in updates and isinstance(updates['start_time'], str):
            updates['start_time'] = datetime.strptime(updates['start_time'], '%H:%M:%S').time() # Or '%H:%M'
        if 'end_time' in updates and isinstance(updates['end_time'], str):
            updates['end_time'] = datetime.strptime(updates['end_time'], '%H:%M:%S').time() # Or '%H:%M'
        if 'next_suggested_appointment_date' in updates and isinstance(updates['next_suggested_appointment_date'], str):
            updates['next_suggested_appointment_date'] = datetime.strptime(updates['next_suggested_appointment_date'], '%Y-%m-%d').date()
        if 'amount' in updates:
            try:
                updates['amount'] = float(updates['amount'])
            except (ValueError, TypeError):
                print(f"Warning: Invalid amount value '{updates['amount']}' for appointment {appointment_id}. Skipping update for amount.")
                updates.pop('amount')


        for key, value in updates.items():
            if hasattr(appointment, key): # Only set attributes that exist on the model
                setattr(appointment, key, value)
            else:
                print(f"Warning: Attempted to set non-existent field '{key}' on Appointment model for ID {appointment_id}.")

        try:
            self.db.commit()
            self.db.refresh(appointment)
            return appointment
        except Exception as e:
            self.db.rollback()
            print(f"Error updating appointment {appointment_id}: {e}")
            return None

    def delete_appointment(self, appointment_id: int) -> bool:
        """
        Deletes an appointment record from the database.

        Args:
            appointment_id (int): The ID of the appointment to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            print(f"Appointment with ID {appointment_id} not found for deletion.")
            return False
        try:
            self.db.delete(appointment)
            self.db.commit()
            print(f"Appointment {appointment_id} deleted successfully.")
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting appointment {appointment_id}: {e}")
            return False

    def _to_dict_with_relations(self, appt: Appointment) -> Dict[str, Any]:
        """
        Helper to convert an Appointment object to a dictionary, including related entity names.
        This assumes relationships are already loaded (e.g., via joinedload).
        """
        appt_dict = appt.to_dict()
        # Add names of related objects if they exist
        if appt.client:
            appt_dict['client_name'] = appt.client.full_name
        if appt.service:
            appt_dict['service_name'] = appt.service.name
        if appt.area:
            appt_dict['area_name'] = appt.area.name
        if appt.payment_method:
            appt_dict['payment_method_name'] = appt.payment_method.name
        return appt_dict

    def search_appointments(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for appointments by client name, service name, or area name.
        """
        search_pattern = f"%{query.lower()}%"
        appointments = self.db.query(Appointment).options(
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.area)
        ).join(Client, Appointment.client_id == Client.id).outerjoin(Service, Appointment.service_id == Service.id).outerjoin(TreatmentArea, Appointment.area_id == TreatmentArea.id).filter(
            or_(
                Client.full_name.ilike(search_pattern),
                Service.name.ilike(search_pattern),
                TreatmentArea.name.ilike(search_pattern),
                Appointment.appointment_status.ilike(search_pattern) # Also search by status
            )
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]