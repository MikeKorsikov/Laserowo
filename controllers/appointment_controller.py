# controllers/appointment_controller.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import traceback

# Import models
from models.appointment import Appointment
from models.client import Client
from models.service import Service
from models.treatment_area import TreatmentArea
from models.payment_method import PaymentMethod
from models.promotion import Promotion
from models.hardware import Hardware

from datetime import date, time, datetime, timedelta
from typing import Optional, List, Dict, Any

# Import other controllers needed to resolve IDs from names
# Using relative imports ('.') is good practice when within a package
from .client_controller import ClientController
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
                           client_data: Dict[str, Any],
                           appointment_date: date,
                           start_time: time,
                           service_name: Optional[str] = None,
                           treatment_area_name: Optional[str] = None,
                           payment_method_name: Optional[str] = None,
                           promotion_name: Optional[str] = None,
                           hardware_name: Optional[str] = None,
                           end_time: Optional[time] = None,
                           session_number_for_area: Optional[int] = None,
                           power_j_cm3: Optional[str] = None,
                           price: Optional[float] = None,
                           notes: Optional[str] = None,
                           next_suggested_appointment_date: Optional[date] = None,
                           appointment_type: Optional[str] = None,
                           status: Optional[str] = 'Scheduled',
                           staff_member: Optional[str] = None,
                           duration_minutes: Optional[int] = None,
                           is_rescheduled: Optional[bool] = False,
                           original_appointment_id: Optional[int] = None
                           ) -> Optional[Appointment]:
        """
        Creates a new appointment record in the database.
        It handles getting or creating related entities by name (service, area, payment method, promotion, hardware).

        Args:
            client_data (Dict[str, Any]): Dictionary containing client identifying info (e.g., 'full_name', 'phone_number', 'email', 'excel_id').
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
        try:
            # --- Resolve Client ID ---
            # Use get_or_create_client with all relevant client_data fields
            client = self.client_controller.get_or_create_client(
                full_name=client_data.get('full_name'),
                phone_number=client_data.get('phone_number'),
                email=client_data.get('email'),
                excel_id=client_data.get('excel_id'), # Crucial for linking clients from Excel
                # Pass any other client-specific fields from client_data that get_or_create_client accepts
                # e.g., is_active=client_data.get('is_active'), notes=client_data.get('notes')
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
                else:
                    print(f"Warning: Could not get or create service '{service_name}'. Service will not be linked.")

            # --- Resolve Treatment Area ID ---
            treatment_area_id = None
            if treatment_area_name:
                # Ensure the method name matches your TreatmentAreaController (e.g., get_or_create_treatment_area)
                area = self.treatment_area_controller.get_or_create_treatment_area(treatment_area_name)
                if area:
                    treatment_area_id = area.id
                else:
                    print(f"Warning: Could not get or create treatment area '{treatment_area_name}'. Area will not be linked.")

            # --- Resolve Payment Method ID ---
            payment_method_id = None
            if payment_method_name:
                # Ensure the method name matches your PaymentMethodController (e.g., get_or_create_payment_method)
                method = self.payment_method_controller.get_or_create_payment_method(payment_method_name)
                if method:
                    payment_method_id = method.id
                else:
                    print(f"Warning: Could not get or create payment method '{payment_method_name}'. Method will not be linked.")

            # --- Resolve Promotion ID ---
            promotion_id = None
            if promotion_name:
                # Assuming get_or_create_promotion takes 'name' as its first arg
                promotion = self.promotion_controller.get_or_create_promotion(promotion_name)
                if promotion:
                    promotion_id = promotion.id
                else:
                    print(f"Warning: Could not get or create promotion '{promotion_name}'. Promotion will not be linked.")

            # --- Resolve Hardware ID ---
            hardware_id = None
            if hardware_name:
                # Assuming get_or_create_hardware takes 'device_name' as its first arg
                hardware = self.hardware_controller.get_or_create_hardware(device_name=hardware_name)
                if hardware:
                    hardware_id = hardware.id
                else:
                    print(f"Warning: Could not get or create hardware '{hardware_name}'. Hardware will not be linked.")

            # --- Basic validation for required fields ---
            if not client_id or not appointment_date or not start_time:
                print("Error: client_id, appointment_date, and start_time are required for appointment creation.")
                return None

            # --- Handle end_time calculation if not provided or invalid ---
            # Combine appointment_date and start_time to perform timedelta arithmetic
            combined_start_datetime = datetime.combine(appointment_date, start_time)

            if duration_minutes is not None: # Use duration if provided
                end_time = (combined_start_datetime + timedelta(minutes=duration_minutes)).time()
            elif end_time is None: # If no duration and no end_time, set a default duration
                 print(f"Warning: No end_time or duration_minutes provided. Defaulting to 60 minutes for appointment on {appointment_date} at {start_time}.")
                 end_time = (combined_start_datetime + timedelta(minutes=60)).time()
            elif end_time < start_time: # If end_time is provided but illogical
                print(f"Warning: Provided end_time ({end_time}) is before start_time ({start_time}). Recalculating based on 60 minutes duration.")
                end_time = (combined_start_datetime + timedelta(minutes=60)).time()


            new_appointment = Appointment(
                client_id=client_id,
                appointment_date=appointment_date,
                start_time=start_time,
                end_time=end_time,
                service_id=service_id,
                treatment_area_id=treatment_area_id,
                price=price,
                payment_method_id=payment_method_id,
                promotion_id=promotion_id,
                hardware_id=hardware_id,
                notes=notes,
                next_suggested_appointment_date=next_suggested_appointment_date,
                appointment_type=appointment_type,
                status=status,
                staff_member=staff_member,
                duration_minutes=duration_minutes, # Keep this even if end_time is derived from it
                is_rescheduled=is_rescheduled,
                original_appointment_id=original_appointment_id,
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
            # More specific logging for easier debugging
            client_name_for_log = client_data.get('full_name', 'N/A')
            print(f"Error creating appointment for client '{client_name_for_log}' on {appointment_date} at {start_time}: {e}")
            traceback.print_exc()
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
            joinedload(Appointment.treatment_area),
            joinedload(Appointment.payment_method),
            joinedload(Appointment.promotion),
            joinedload(Appointment.hardware)
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]

    def get_appointments_by_client_id(self, client_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves appointments for a specific client, ordered by date descending.
        Eagerly loads related service, area, payment method, promotion, and hardware data.
        """
        appointments = self.db.query(Appointment).filter(Appointment.client_id == client_id).options(
            joinedload(Appointment.service),
            joinedload(Appointment.treatment_area),
            joinedload(Appointment.payment_method),
            joinedload(Appointment.promotion),
            joinedload(Appointment.hardware)
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

        # Resolve IDs for related entities if names are provided in updates
        if 'service_name' in updates:
            service = self.service_controller.get_or_create_service(updates.pop('service_name'))
            if service:
                updates['service_id'] = service.id
            else:
                print(f"Warning: Service '{updates.get('service_name_original')}' not found/created for update.")
                # You might want to explicitly set service_id to None if the name couldn't be resolved
                updates['service_id'] = None # Added for clarity

        if 'treatment_area_name' in updates:
            area = self.treatment_area_controller.get_or_create_treatment_area(updates.pop('treatment_area_name'))
            if area:
                updates['treatment_area_id'] = area.id
            else:
                print(f"Warning: Treatment Area '{updates.get('treatment_area_name_original')}' not found/created for update.")
                updates['treatment_area_id'] = None

        if 'payment_method_name' in updates:
            method = self.payment_method_controller.get_or_create_payment_method(updates.pop('payment_method_name'))
            if method:
                updates['payment_method_id'] = method.id
            else:
                print(f"Warning: Payment Method '{updates.get('payment_method_name_original')}' not found/created for update.")
                updates['payment_method_id'] = None

        if 'promotion_name' in updates:
            promotion = self.promotion_controller.get_or_create_promotion(updates.pop('promotion_name'))
            if promotion:
                updates['promotion_id'] = promotion.id
            else:
                print(f"Warning: Promotion '{updates.get('promotion_name_original')}' not found/created for update.")
                updates['promotion_id'] = None

        if 'hardware_name' in updates:
            hardware = self.hardware_controller.get_or_create_hardware(device_name=updates.pop('hardware_name'))
            if hardware:
                updates['hardware_id'] = hardware.id
            else:
                print(f"Warning: Hardware '{updates.get('hardware_name_original')}' not found/created for update.")
                updates['hardware_id'] = None

        # Handle specific type conversions if updates might come as strings (e.g., from a UI form)
        # Using a more robust date/time parsing approach for flexibility
        if 'appointment_date' in updates and isinstance(updates['appointment_date'], str):
            try:
                updates['appointment_date'] = datetime.strptime(updates['appointment_date'], '%Y-%m-%d').date()
            except ValueError:
                print(f"Warning: Could not parse appointment_date '{updates['appointment_date']}'. Skipping update for this field.")
                updates.pop('appointment_date')

        if 'start_time' in updates and isinstance(updates['start_time'], str):
            try:
                updates['start_time'] = datetime.strptime(updates['start_time'], '%H:%M:%S').time()
            except ValueError: # Try another common format
                try:
                    updates['start_time'] = datetime.strptime(updates['start_time'], '%H:%M').time()
                except ValueError:
                    print(f"Warning: Could not parse start_time '{updates['start_time']}'. Skipping update for this field.")
                    updates.pop('start_time')

        if 'end_time' in updates and isinstance(updates['end_time'], str):
            try:
                updates['end_time'] = datetime.strptime(updates['end_time'], '%H:%M:%S').time()
            except ValueError:
                try:
                    updates['end_time'] = datetime.strptime(updates['end_time'], '%H:%M').time()
                except ValueError:
                    print(f"Warning: Could not parse end_time '{updates['end_time']}'. Skipping update for this field.")
                    updates.pop('end_time')

        if 'next_suggested_appointment_date' in updates and isinstance(updates['next_suggested_appointment_date'], str):
            try:
                updates['next_suggested_appointment_date'] = datetime.strptime(updates['next_suggested_appointment_date'], '%Y-%m-%d').date()
            except ValueError:
                print(f"Warning: Could not parse next_suggested_appointment_date '{updates['next_suggested_appointment_date']}'. Skipping update for this field.")
                updates.pop('next_suggested_appointment_date')

        if 'price' in updates:
            try:
                updates['price'] = float(updates['price'])
            except (ValueError, TypeError):
                print(f"Warning: Invalid price value '{updates['price']}' for appointment {appointment_id}. Skipping update for price.")
                updates.pop('price')
        
        if 'duration_minutes' in updates:
            try:
                updates['duration_minutes'] = int(updates['duration_minutes'])
            except (ValueError, TypeError):
                print(f"Warning: Invalid duration_minutes value '{updates['duration_minutes']}' for appointment {appointment_id}. Skipping update for duration_minutes.")
                updates.pop('duration_minutes')


        for key, value in updates.items():
            if hasattr(appointment, key):
                setattr(appointment, key, value)
            else:
                print(f"Warning: Attempted to set non-existent field '{key}' on Appointment model for ID {appointment_id}. Ignoring.")

        try:
            self.db.commit()
            self.db.refresh(appointment)
            return appointment
        except Exception as e:
            self.db.rollback()
            print(f"Error updating appointment {appointment_id}: {e}")
            traceback.print_exc()
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
            traceback.print_exc()
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
        if appt.treatment_area:
            appt_dict['treatment_area_name'] = appt.treatment_area.name
        if appt.payment_method:
            appt_dict['payment_method_name'] = appt.payment_method.name
        if appt.promotion:
            appt_dict['promotion_name'] = appt.promotion.name
        if appt.hardware:
            appt_dict['hardware_name'] = appt.hardware.device_name
        return appt_dict

    def search_appointments(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for appointments by client name, service name, area name, or status.
        """
        search_pattern = f"%{query.lower()}%"
        appointments = self.db.query(Appointment).options(
            joinedload(Appointment.client),
            joinedload(Appointment.service),
            joinedload(Appointment.treatment_area),
            joinedload(Appointment.payment_method), # Add for more comprehensive search if needed
            joinedload(Appointment.promotion),      # Add for more comprehensive search if needed
            joinedload(Appointment.hardware)        # Add for more comprehensive search if needed
        ).join(Client, Appointment.client_id == Client.id)\
         .outerjoin(Service, Appointment.service_id == Service.id)\
         .outerjoin(TreatmentArea, Appointment.treatment_area_id == TreatmentArea.id)\
         .outerjoin(PaymentMethod, Appointment.payment_method_id == PaymentMethod.id)\
         .outerjoin(Promotion, Appointment.promotion_id == Promotion.id)\
         .outerjoin(Hardware, Appointment.hardware_id == Hardware.id)\
         .filter(
            or_(
                Client.full_name.ilike(search_pattern),
                Service.name.ilike(search_pattern),
                TreatmentArea.name.ilike(search_pattern),
                PaymentMethod.name.ilike(search_pattern), # Assuming PaymentMethod has a 'name' field
                Promotion.name.ilike(search_pattern), # Assuming Promotion has a 'name' field
                Hardware.device_name.ilike(search_pattern), # Assuming Hardware has a 'device_name' field
                Appointment.status.ilike(search_pattern),
                Appointment.notes.ilike(search_pattern) # Search notes as well
            )
        ).order_by(Appointment.appointment_date.desc()).all()
        return [self._to_dict_with_relations(appt) for appt in appointments]