# controllers/appointment_controller.py
from sqlalchemy.orm import Session, joinedload # Import joinedload for eager loading
from sqlalchemy import or_ # Import or_ for search queries
from models.appointment import Appointment
from models.client import Client
from models.service import Service
from models.treatment_area import TreatmentArea
from models.payment_method import PaymentMethod
# Import other models if their controllers will be used to resolve IDs
from models.promotion import Promotion
from models.hardware import Hardware

from datetime import date, time, datetime, timedelta # Import timedelta for time calculations
from typing import Optional, List, Dict, Any

# You'll need to import other controllers if they exist and are used to get/create entities by name
# Example:
from .client_controller import ClientController # Assuming these exist in the same 'controllers' package
from .service_controller import ServiceController
from .treatment_area_controller import TreatmentAreaController
from .payment_method_controller import PaymentMethodController
from .promotion_controller import PromotionController
from .hardware_controller import HardwareController


class AppointmentController:
    def __init__(self, db: Session):
        self.db = db
        # Initialize other controllers here, as they'll be used by create_appointment
        self.client_controller = ClientController(db)
        self.service_controller = ServiceController(db)
        self.treatment_area_controller = TreatmentAreaController(db)
        self.payment_method_controller = PaymentMethodController(db)
        self.promotion_controller = PromotionController(db)
        self.hardware_controller = HardwareController(db)

    def create_appointment(self,
                           client_data: Dict[str, Any], # Changed to accept client_data (name, phone, etc.)
                           appointment_date: date,
                           start_time: time,
                           # Parameters below are now names, as importer likely provides names
                           service_name: Optional[str] = None,
                           treatment_area_name: Optional[str] = None, # Changed from area_id to treatment_area_name
                           payment_method_name: Optional[str] = None,
                           promotion_name: Optional[str] = None,
                           hardware_name: Optional[str] = None,
                           # Other existing optional parameters
                           end_time: Optional[time] = None,
                           session_number_for_area: Optional[int] = None,
                           power_j_cm3: Optional[str] = None,
                           appointment_status: Optional[str] = 'Scheduled', # Default to Scheduled, not Completed
                           price: Optional[float] = None, # Changed from 'amount' to 'price' to match model
                           notes: Optional[str] = None,
                           next_suggested_appointment_date: Optional[date] = None,
                           # New fields from your Appointment model
                           appointment_type: Optional[str] = None,
                           status: Optional[str] = 'Scheduled', # Using 'status' to match model, removed appointment_status
                           staff_member: Optional[str] = None,
                           duration_minutes: Optional[int] = None,
                           is_rescheduled: Optional[bool] = False,
                           original_appointment_id: Optional[int] = None # Not for direct use from excel import usually
                           ) -> Optional[Appointment]:
        """
        Creates a new appointment record in the database.
        It handles getting or creating related entities by name (service, area, payment method, promotion, hardware).

        Args:
            client_data (Dict[str, Any]): Dictionary containing client identifying info (e.g., 'full_name', 'phone_number').
            appointment_date (date): The date of the appointment.
            start_time (time): The start time of the appointment.
            service_name (Optional[str]): The name of the service provided.
            treatment_area_name (Optional[str]): The name of the treatment area.
            payment_method_name (Optional[str]): The name of the payment method used.
            promotion_name (Optional[str]): The name of any promotion applied.
            hardware_name (Optional[str]): The name of the hardware used.
            # ... other args ...

        Returns:
            Optional[Appointment]: The newly created Appointment object, or None if creation fails.
        """
        # --- Resolve Client ID ---
        # Assuming your excel_importer now provides client_data
        client = self.client_controller.get_or_create_client(
            full_name=client_data.get('full_name'),
            phone_number=client_data.get('phone_number'),
            email=client_data.get('email'),
            excel_id=client_data.get('excel_id') # Ensure Excel ID is passed
        )
        if not client:
            print("Error: Client could not be found or created for appointment.")
            return None
        client_id = client.id

        # --- Resolve Service ID ---
        service_id = None
        if service_name:
            service = self.service_controller.get_or_create_service(service_name)
            if service:
                service_id = service.id

        # --- Resolve Treatment Area ID ---
        treatment_area_id = None # Corrected variable name to match model
        if treatment_area_name:
            # Assuming get_or_create_area method exists in TreatmentAreaController
            area = self.treatment_area_controller.get_or_create_area(treatment_area_name)
            if area:
                treatment_area_id = area.id

        # --- Resolve Payment Method ID ---
        payment_method_id = None
        if payment_method_name:
            method = self.payment_method_controller.get_or_create_method(payment_method_name)
            if method:
                payment_method_id = method.id

        # --- Resolve Promotion ID ---
        promotion_id = None
        if promotion_name:
            promotion = self.promotion_controller.get_or_create_promotion(promotion_name)
            if promotion:
                promotion_id = promotion.id

        # --- Resolve Hardware ID ---
        hardware_id = None
        if hardware_name:
            hardware = self.hardware_controller.get_or_create_hardware(hardware_name)
            if hardware:
                hardware_id = hardware.id

        # --- Basic validation for required fields ---
        if not client_id or not appointment_date or not start_time:
            print("Error: client_id, appointment_date, and start_time are required for appointment creation.")
            return None

        # --- Handle end_time calculation if not provided or invalid ---
        if not end_time and duration_minutes:
            # Calculate end_time based on start_time and duration
            dummy_datetime = datetime.combine(appointment_date, start_time)
            end_time = (dummy_datetime + timedelta(minutes=duration_minutes)).time()
        elif end_time and start_time and end_time < start_time:
            print(f"Warning: end_time ({end_time}) is before start_time ({start_time}). Adjusting end_time based on 1 hour duration.")
            dummy_datetime = datetime.combine(appointment_date, start_time)
            end_time = (dummy_datetime + timedelta(hours=1)).time()
        # If no end_time and no duration, leave end_time as None

        try:
            new_appointment = Appointment(
                client_id=client_id,
                appointment_date=appointment_date,
                start_time=start_time,
                end_time=end_time,
                service_id=service_id,
                treatment_area_id=treatment_area_id, # <--- Corrected to treatment_area_id
                price=price, # Corrected to 'price'
                payment_method_id=payment_method_id,
                promotion_id=promotion_id,
                hardware_id=hardware_id,
                notes=notes,
                next_suggested_appointment_date=next_suggested_appointment_date,
                # New fields from your Appointment model (ensure these match column names)
                appointment_type=appointment_type,
                status=status, # Using 'status' as defined in model
                staff_member=staff_member,
                # created_at and updated_at handled by model default/onupdate
                duration_minutes=duration_minutes,
                is_rescheduled=is_rescheduled,
                original_appointment_id=original_appointment_id,
                # Specific fields from older definitions, mapping to new if needed
                session_number_for_area=session_number_for_area,
                power_j_cm3=power_j_cm3,
            )
            self.db.add(new_appointment)
            self.db.commit()
            self.db.refresh(new_appointment)
            print(f"Appointment created: ID {new_appointment.id} for Client {new_appointment.client.full_name} on {new_appointment.appointment_date}")
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
        Eagerly loads related client, service, area, payment method, promotion, and hardware data.
        """
        appointments = self.db.query(Appointment).options(
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.treatment_area), # Corrected relationship name
            joinedload(Appointment.payment_method),
            joinedload(Appointment.promotion), # Added
            joinedload(Appointment.hardware) # Added
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]

    def get_appointments_by_client_id(self, client_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves appointments for a specific client, ordered by date descending.
        Eagerly loads related service, area, payment method, promotion, and hardware data.
        """
        appointments = self.db.query(Appointment).filter(Appointment.client_id == client_id).options(
            joinedload(Appointment.service),
            joinedload(Appointment.treatment_area), # Corrected relationship name
            joinedload(Appointment.payment_method),
            joinedload(Appointment.promotion), # Added
            joinedload(Appointment.hardware) # Added
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
        if 'price' in updates: # Changed from 'amount' to 'price'
            try:
                updates['price'] = float(updates['price'])
            except (ValueError, TypeError):
                print(f"Warning: Invalid price value '{updates['price']}' for appointment {appointment_id}. Skipping update for price.")
                updates.pop('price')


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
        if appt.treatment_area: # Corrected relationship name
            appt_dict['treatment_area_name'] = appt.treatment_area.name # Corrected key name
        if appt.payment_method:
            appt_dict['payment_method_name'] = appt.payment_method.name
        if appt.promotion: # Added
            appt_dict['promotion_name'] = appt.promotion.promotion_name # Assuming 'promotion_name' is the field in Promotion model
        if appt.hardware: # Added
            appt_dict['hardware_name'] = appt.hardware.device_name # Assuming 'device_name' is the field in Hardware model
        return appt_dict

    def search_appointments(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for appointments by client name, service name, or area name.
        """
        search_pattern = f"%{query.lower()}%"
        appointments = self.db.query(Appointment).options(
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.treatment_area) # Corrected relationship name
        ).join(Client, Appointment.client_id == Client.id)\
         .outerjoin(Service, Appointment.service_id == Service.id)\
         .outerjoin(TreatmentArea, Appointment.treatment_area_id == TreatmentArea.id)\
         .filter( # Corrected join for treatment_area
            or_(
                Client.full_name.ilike(search_pattern),
                Service.name.ilike(search_pattern),
                TreatmentArea.name.ilike(search_pattern),
                Appointment.status.ilike(search_pattern) # Using 'status' now
            )
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]