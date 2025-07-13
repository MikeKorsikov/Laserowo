# imports/excel_importer.py
import os
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, date, time, timedelta # Import timedelta
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid # For generating unique IDs for placeholder clients if needed
import traceback # For detailed error logging

# --- Path Configuration ---
# Get the directory of the current script (excel_importer.py)
current_script_dir = Path(__file__).resolve().parent

# The project root is two levels up from excel_importer.py:
# P1_desktop_app/data/imports/excel_importer.py
# ^           ^      ^
# project_root data   imports
project_root = current_script_dir.parent.parent

# Add project root to sys.path to allow imports like 'controllers.client_controller'
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import your controllers and models
from controllers.client_controller import ClientController
from controllers.appointment_controller import AppointmentController
from controllers.service_controller import ServiceController
from controllers.treatment_area_controller import TreatmentAreaController
from controllers.payment_method_controller import PaymentMethodController
from models.client import Client # Needed for direct client queries in importer
# Assuming your controllers have a get_or_create_X method for convenience
# e.g., service_controller.get_or_create_service(name)

# --- Configuration for your Excel File ---
# IMPORTANT: Adjust this path if your Excel file is not directly in 'data/imports'
EXCEL_FILE_PATH = project_root / "data" / "imports" / "KLIENTS 2024.xls" # NEW

CLIENTS_SHEET_NAME = "KLIENCI"
VISITS_SHEET_NAME = "WIZYTY"

# Mapping of Excel column names to your model field names for Clients
# Ensure these match the EXACT column headers in your "KLIENCI" sheet.
CLIENT_COLUMN_MAPPING = {
    'ID Klienta': 'excel_client_id',
    'Imie Nazwisko': 'full_name',
    'Telefon kontaktowy': 'phone_number',
    'e-mail.': 'email',
    'Facebook': 'facebook_id',
    'Instagram': 'instagram_handle',
    'Booksy': 'booksy_used_excel', # Map to a temporary name to process boolean/string
    'Data Urodzenia': 'date_of_birth',
    'Blacklista': 'is_blacklisted_excel',
    'Aktywny': 'is_active_excel',
}

# Mapping of Excel column names to your model field names for Visits/Appointments
# Ensure these match the EXACT column headers in your "WIZYTY" sheet.
VISIT_COLUMN_MAPPING = {
    'ID Wizyty': 'excel_appointment_id',
    'ID Klienta': 'excel_client_id_for_appt',
    'Imię Nazwisko': 'client_full_name',
    'Data': 'appointment_date',
    'Godzina Rozpoczęcia': 'start_time',
    'Godzina Zakończenia': 'end_time',
    'Numer wizyty': 'session_number_for_area',
    'Obszar': 'area_name',
    'Moc , J/cm3': 'power_j_cm3',
    'Następna wizyta': 'next_suggested_appointment_date',
    'Kwota': 'amount',
    'Usługa': 'service_name',
    'Metoda Płatności': 'payment_method_name',
    'Status wizyty': 'appointment_status',
    'Status następnej wizyty': 'status_next_appointment', # Keep for logging, as it's not directly mapped
}

# --- Helper Functions for Data Cleaning and Parsing ---
def clean_string(value: Any) -> Optional[str]:
    """Converts a value to a string and strips whitespace, or returns None if NaN."""
    if pd.isna(value):
        return None
    s_val = str(value).strip()
    return s_val if s_val else None # Return None for empty strings too

def parse_excel_date(excel_date_value: Any, row_identifier: str, field_name: str, default: Optional[date] = None) -> Optional[date]:
    """
    Parses various Excel date formats (datetime objects, floats, strings) to a date object.
    Returns default if parsing fails.
    """
    if pd.isna(excel_date_value) or excel_date_value is None:
        return default

    if isinstance(excel_date_value, datetime):
        return excel_date_value.date()
    if isinstance(excel_date_value, date):
        return excel_date_value
    
    # Handle Excel's numeric date format (float representing days since 1899-12-30)
    if isinstance(excel_date_value, (int, float)):
        try:
            return pd.to_datetime(excel_date_value, unit='D', origin='1899-12-30').date()
        except Exception as e:
            print(f"Warning: Could not parse numeric date '{excel_date_value}' for {field_name} in {row_identifier} as Excel date: {e}. Attempting string parse.")
            # Fall through to string parsing if numeric conversion fails unexpectedly

    if isinstance(excel_date_value, str):
        # Common formats, including Polish specific ones. Be careful with ambiguous ones (e.g., 01.02.2023 could be Feb 1 or Jan 2)
        # Prioritize YYYY-MM-DD or unambiguous formats first.
        formats = [
            '%Y-%m-%d',        # 2023-01-25
            '%d.%m.%Y',        # 25.01.2023 (Polish format)
            '%d/%m/%Y',        # 25/01/2023
            '%Y/%m/%d',        # 2023/01/25
            '%Y-%m-%dT%H:%M:%S', # For datetime strings
            '%m/%d/%Y',        # 01/25/2023
            '%b %d, %Y',       # Jan 25, 2023
            '%B %d, %Y',       # January 25, 2023
        ]
        for fmt in formats:
            try:
                return datetime.strptime(excel_date_value, fmt).date()
            except ValueError:
                pass # Try next format
        print(f"Warning: Could not parse string date '{excel_date_value}' for {field_name} in {row_identifier}. Using default: {default}.")
    else:
        print(f"Warning: Unexpected date format type '{type(excel_date_value).__name__}' ({excel_date_value}) for {field_name} in {row_identifier}. Using default: {default}.")
    return default

def parse_excel_time(excel_time_value: Any, row_identifier: str, field_name: str, default: Optional[time] = None) -> Optional[time]:
    """
    Parses various Excel time formats (datetime objects, floats, strings) to a time object.
    Returns default if parsing fails.
    """
    if pd.isna(excel_time_value) or excel_time_value is None:
        return default

    if isinstance(excel_time_value, datetime):
        return excel_time_value.time()
    if isinstance(excel_time_value, time):
        return excel_time_value
    
    # Handle Excel's numeric time format (float representing fraction of a day)
    if isinstance(excel_time_value, (int, float)):
        try:
            # Excel stores time as a fraction of a day (e.g., 0.5 is 12:00 PM)
            # Use timedelta for robust conversion
            total_seconds = excel_time_value * 24 * 3600
            td = timedelta(seconds=total_seconds)
            # Create a dummy datetime object to extract time
            dummy_dt = datetime.min + td
            return dummy_dt.time()
        except Exception as e:
            print(f"Warning: Could not parse numeric time '{excel_time_value}' for {field_name} in {row_identifier} as Excel time: {e}. Attempting string parse.")
            # Fall through to string parsing if numeric conversion fails unexpectedly

    if isinstance(excel_time_value, str):
        formats = [
            '%H:%M:%S',       # 14:30:00
            '%H:%M',          # 14:30
            '%I:%M:%S %p',    # 02:30:00 PM
            '%I:%M %p',       # 02:30 PM
        ]
        for fmt in formats:
            try:
                return datetime.strptime(excel_time_value, fmt).time()
            except ValueError:
                pass
        print(f"Warning: Could not parse string time '{excel_time_value}' for {field_name} in {row_identifier}. Using default: {default}.")
    else:
        print(f"Warning: Unexpected time format type '{type(excel_time_value).__name__}' ({excel_time_value}) for {field_name} in {row_identifier}. Using default: {default}.")
    return default

# --- Main Import Function ---
def import_data_from_excel(file_path: str, db_session: Session):
    """
    Imports client and appointment data from an Excel file into the database.
    Args:
        file_path (str): The path to the Excel file.
        db_session (Session): The SQLAlchemy database session.
    """
    client_controller = ClientController(db_session)
    appointment_controller = AppointmentController(db_session)
    service_controller = ServiceController(db_session)
    treatment_area_controller = TreatmentAreaController(db_session)
    payment_method_controller = PaymentMethodController(db_session)

    print(f"\n--- Starting data import from: {file_path} ---")

    # --- Step 1: Import Clients ---
    print(f"\n--- Importing clients from '{CLIENTS_SHEET_NAME}' tab ---")
    try:
        clients_df = pd.read_excel(file_path, sheet_name=CLIENTS_SHEET_NAME)
        # Rename columns *after* reading, so the original Excel names are used
        clients_df.rename(columns=CLIENT_COLUMN_MAPPING, inplace=True)
        print(f"Loaded {len(clients_df)} rows from clients sheet.")
    except FileNotFoundError:
        print(f"Error: Excel file not found at '{file_path}'. Please check the path.")
        return
    except Exception as e:
        print(f"Error reading clients sheet '{CLIENTS_SHEET_NAME}': {e}")
        traceback.print_exc() # Print full traceback
        return

    # Store mapping from Excel identifiers to database client IDs
    # Keys will be a combination of excel_client_id (if available) or normalized full_name-phone_number
    # This helps in linking appointments to correct clients.
    excel_identifier_to_db_id: Dict[str, int] = {}
    imported_clients_count = 0
    failed_clients_count = 0

    for index, row in clients_df.iterrows():
        row_num = index + 2 # Excel rows are 1-indexed, and header is row 1
        
        try:
            # Get raw values first
            raw_excel_client_id = row.get('excel_client_id')
            raw_full_name = row.get('full_name')
            raw_phone_number = row.get('phone_number')
            raw_email = row.get('email')

            # Clean and process values
            full_name = clean_string(raw_full_name)
            excel_client_id = clean_string(raw_excel_client_id)
            phone_number = clean_string(raw_phone_number)
            email = clean_string(raw_email)
            
            client_identifier_log = f"Row {row_num} (Name: {full_name or 'N/A'}, Phone: {phone_number or 'N/A'}, Email: {email or 'N/A'}, Excel ID: {excel_client_id or 'N/A'})"

            if not full_name and not phone_number and not email:
                print(f"Skipping client {client_identifier_log}: No identifying information (Name, Phone, Email).")
                failed_clients_count += 1
                continue

            # If full_name is missing, generate a placeholder
            if not full_name:
                full_name = f"Unknown Client {uuid.uuid4().hex[:8]}"
                print(f"Warning: Client {client_identifier_log}: Full Name is missing. Assigning placeholder '{full_name}'.")

            # Attempt to find an existing client
            existing_client = None
            if excel_client_id:
                existing_client = client_controller.get_client_by_excel_id(excel_client_id) # Assuming this method exists
            
            if not existing_client:
                existing_client = client_controller.get_client_by_phone_or_email_or_name(
                    phone_number=phone_number, email=email, full_name=full_name
                )

            db_client = None
            if existing_client:
                db_client = existing_client
                print(f"Client '{full_name}' (ID: {db_client.id}) already exists, skipping creation for {client_identifier_log}.")
            else:
                # Process 'Booksy' (booksy_used_excel)
                booksy_used_val = clean_string(row.get('booksy_used_excel'))
                booksy_used = (booksy_used_val == '+') if booksy_used_val else False

                # Process 'Blacklista' (is_blacklisted_excel)
                is_blacklisted_val = clean_string(row.get('is_blacklisted_excel'))
                is_blacklisted = (is_blacklisted_val == '+') if is_blacklisted_val else False

                # Process 'Aktywny' (is_active_excel)
                is_active_val = clean_string(row.get('is_active_excel'))
                is_active = (is_active_val == '+') if is_active_val else True # Default to True

                # Process 'Data Urodzenia' (date_of_birth)
                date_of_birth = parse_excel_date(row.get('date_of_birth'), client_identifier_log, 'date_of_birth')

                client_data = {
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'email': email,
                    'facebook_id': clean_string(row.get('facebook_id')),
                    'instagram_handle': clean_string(row.get('instagram_handle')),
                    'booksy_used': booksy_used,
                    'date_of_birth': date_of_birth,
                    'is_blacklisted': is_blacklisted,
                    'is_active': is_active,
                    'excel_id': excel_client_id # Store the Excel ID in the DB if your model supports it
                }
                db_client = client_controller.create_client(**client_data)

            if db_client:
                imported_clients_count += 1
                # Store mapping: prioritize Excel ID, then a unique name-phone combination
                if db_client.excel_id: # Use the ID from the created/found client
                    excel_identifier_to_db_id[db_client.excel_id] = db_client.id
                if db_client.full_name:
                    excel_identifier_to_db_id[db_client.full_name.lower()] = db_client.id 
                if db_client.phone_number: # Store by phone number as well
                    excel_identifier_to_db_id[db_client.phone_number] = db_client.id

            else:
                print(f"CRITICAL ERROR: Failed to create or find client for {client_identifier_log}. Skipping this client record.")
                failed_clients_count += 1

        except Exception as e:
            print(f"ERROR: Exception while processing client from {client_identifier_log}: {e}")
            traceback.print_exc()
            failed_clients_count += 1
            continue # Continue to next row even if one fails

    print(f"--- Finished client import. Imported: {imported_clients_count} clients. Failed: {failed_clients_count} ---")

    # --- Step 2: Import Appointments ---
    print(f"\n--- Importing appointments from '{VISITS_SHEET_NAME}' tab ---")
    try:
        visits_df = pd.read_excel(file_path, sheet_name=VISITS_SHEET_NAME)
        visits_df.rename(columns=VISIT_COLUMN_MAPPING, inplace=True)
        print(f"Loaded {len(visits_df)} rows from appointments sheet.")
    except Exception as e:
        print(f"Error reading visits sheet '{VISITS_SHEET_NAME}': {e}")
        traceback.print_exc()
        return

    imported_appointments_count = 0
    failed_appointments_count = 0

    for index, row in visits_df.iterrows():
        row_num = index + 2 # Excel rows are 1-indexed, and header is row 1
        
        try:
            # Get raw values
            raw_excel_client_id_for_appt = row.get('excel_client_id_for_appt')
            raw_client_full_name = row.get('client_full_name')

            # Clean and process values
            excel_client_id_for_appt = clean_string(raw_excel_client_id_for_appt)
            client_full_name = clean_string(raw_client_full_name)

            appt_identifier = f"Row {row_num} (Client: {client_full_name or 'N/A'}, Excel Client ID: {excel_client_id_for_appt or 'N/A'}, Date: {row.get('appointment_date') or 'N/A'})"

            client_id = None
            # Try to find client in our mapping, prioritizing Excel ID then cleaned full name
            if excel_client_id_for_appt and excel_client_id_for_appt in excel_identifier_to_db_id:
                client_id = excel_identifier_to_db_id[excel_client_id_for_appt]
                # print(f"Debug: Client '{client_full_name}' for {appt_identifier} matched by Excel ID from cached clients.")
            elif client_full_name and client_full_name.lower() in excel_identifier_to_db_id:
                client_id = excel_identifier_to_db_id[client_full_name.lower()]
                # print(f"Debug: Client '{client_full_name}' for {appt_identifier} matched by name from cached clients.")
            
            # If not found in cache, query DB directly (should ideally be rare if client import ran first)
            if not client_id:
                found_client_db = None
                if excel_client_id_for_appt:
                    found_client_db = client_controller.get_client_by_excel_id(excel_client_id_for_appt)
                if not found_client_db and client_full_name:
                    found_client_db = client_controller.get_client_by_name(client_full_name) # Assuming this method exists

                if found_client_db:
                    client_id = found_client_db.id
                    # Add to map for faster future lookups within the same import run
                    if found_client_db.excel_id:
                        excel_identifier_to_db_id[found_client_db.excel_id] = client_id
                    if found_client_db.full_name:
                        excel_identifier_to_db_id[found_client_db.full_name.lower()] = client_id
                    if found_client_db.phone_number:
                        excel_identifier_to_db_id[found_client_db.phone_number] = client_id
                    print(f"Info: Client '{client_full_name}' for {appt_identifier} found by direct DB query (ID: {client_id}).")
            
            if not client_id:
                # If client still not found, create a placeholder client for the appointment
                placeholder_name = client_full_name if client_full_name else f"Unknown Client for Appt {row_num}"
                # Check for existing placeholder (either from previous import or this run)
                existing_placeholder_client = client_controller.get_client_by_name(placeholder_name)
                
                if existing_placeholder_client:
                    client_db_obj = existing_placeholder_client
                    client_id = client_db_obj.id
                    print(f"Warning: Re-using existing placeholder client '{placeholder_name}' with ID: {client_id} for {appt_identifier}.")
                else:
                    print(f"Warning: Client '{placeholder_name}' (Excel ID: {excel_client_id_for_appt}) not found for appointment {appt_identifier}. Creating a new placeholder client.")
                    placeholder_client_data = {
                        'full_name': placeholder_name,
                        'email': f"placeholder_{uuid.uuid4().hex[:8]}@example.com", # Generate unique email
                        'phone_number': None,
                        'is_active': False, # Mark placeholder clients as inactive by default
                        'notes': f"Auto-created placeholder for client from Excel Appointment Row {row_num}.",
                        'excel_id': excel_client_id_for_appt # Store original excel ID if available
                    }
                    client_db_obj = client_controller.create_client(**placeholder_client_data)
                    if client_db_obj:
                        client_id = client_db_obj.id
                        print(f"New placeholder client created with ID: {client_id}.")
                        # Add to map in case this unknown client has more appointments later in the sheet
                        if client_db_obj.excel_id:
                            excel_identifier_to_db_id[client_db_obj.excel_id] = client_id
                        if client_db_obj.full_name:
                            excel_identifier_to_db_id[client_db_obj.full_name.lower()] = client_id
                    else:
                        print(f"CRITICAL ERROR: Could not create placeholder client for appointment {appt_identifier}. Skipping appointment.")
                        failed_appointments_count += 1
                        continue # Skip this appointment if client cannot be linked/created

            # Parse appointment date and times. Set sensible defaults if missing.
            appointment_date = parse_excel_date(row.get('appointment_date'), appt_identifier, 'appointment_date', default=date.today())
            if not appointment_date: # If date couldn't be parsed even with default
                print(f"Skipping appointment {appt_identifier} due to unparsable appointment date.")
                failed_appointments_count += 1
                continue

            start_time_obj = parse_excel_time(row.get('start_time'), appt_identifier, 'start_time', default=time(9, 0))
            end_time_obj = parse_excel_time(row.get('end_time'), appt_identifier, 'end_time', default=time(10, 0))

            # Ensure start_time is always before end_time, or set default end_time
            if start_time_obj and end_time_obj and start_time_obj >= end_time_obj:
                print(f"Warning: Start time ({start_time_obj}) is not before end time ({end_time_obj}) for {appt_identifier}. Adjusting end time to 1 hour after start.")
                # Combine with a dummy date to use timedelta for time arithmetic
                temp_dt_start = datetime.combine(date.min, start_time_obj)
                end_time_obj = (temp_dt_start + timedelta(hours=1)).time()
                # If adding 1 hour pushes to next day, cap at 23:59:59
                if end_time_obj < start_time_obj: # Means it wrapped around to next day
                    end_time_obj = time(23, 59, 59)


            # Look up or create Service, Treatment Area, Payment Method
            service_id = None
            service_name = clean_string(row.get('service_name'))
            if service_name:
                service = service_controller.get_or_create_service(service_name)
                if service: service_id = service.id
                else: print(f"Warning: Service '{service_name}' could not be created/found for {appt_identifier}. Linking as None.")

            area_id = None
            area_name = clean_string(row.get('area_name'))
            if area_name:
                area = treatment_area_controller.get_or_create_area(area_name)
                if area: area_id = area.id
                else: print(f"Warning: Treatment Area '{area_name}' could not be created/found for {appt_identifier}. Linking as None.")

            payment_method_id = None
            payment_method_name = clean_string(row.get('payment_method_name'))
            if payment_method_name:
                payment_method = payment_method_controller.get_or_create_method(payment_method_name)
                if payment_method: payment_method_id = payment_method.id
                else: print(f"Warning: Payment Method '{payment_method_name}' could not be created/found for {appt_identifier}. Linking as None.")

            # Prepare other appointment data
            amount = row.get('amount')
            amount = float(amount) if pd.notna(amount) else 0.0

            session_number = row.get('session_number_for_area')
            # Use pd.to_numeric for robust conversion, then convert to int if not NaN
            session_number_for_area = pd.to_numeric(session_number, errors='coerce')
            session_number_for_area = int(session_number_for_area) if pd.notna(session_number_for_area) else None

            power_j_cm3 = clean_string(row.get('power_j_cm3'))

            next_suggested_appointment_date = parse_excel_date(row.get('next_suggested_appointment_date'), appt_identifier, 'next_suggested_appointment_date')

            appointment_status_excel = clean_string(row.get('appointment_status'))
            appointment_status = appointment_status_excel if appointment_status_excel else 'Completed' # Default status

            # Log and ignore 'Status następnej wizyty' if it's not mapped to a model field
            status_next_appointment_log = clean_string(row.get('status_next_appointment'))
            if status_next_appointment_log:
                print(f"Note: 'Status następnej wizyty' ('{status_next_appointment_log}') for {appt_identifier} is not mapped to an Appointment model field. Ignoring for import.")

            # Promotion ID and Hardware ID - ensure they are integers or None
            # Need to get raw values first, as .get might return NaN if column is empty
            raw_promotion_id = row.get('promotion_id')
            promotion_id = pd.to_numeric(raw_promotion_id, errors='coerce')
            promotion_id = int(promotion_id) if pd.notna(promotion_id) else None
            
            raw_hardware_id = row.get('hardware_id')
            hardware_id = pd.to_numeric(raw_hardware_id, errors='coerce')
            hardware_id = int(hardware_id) if pd.notna(hardware_id) else None

            appointment_data = {
                'client_id': client_id,
                'service_id': service_id,
                'area_id': area_id,
                'appointment_date': appointment_date,
                'start_time': start_time_obj,
                'end_time': end_time_obj,
                'session_number_for_area': session_number_for_area,
                'power_j_cm3': power_j_cm3,
                'appointment_status': appointment_status,
                'amount': amount,
                'payment_method_id': payment_method_id,
                'promotion_id': promotion_id,
                'hardware_id': hardware_id,
                'notes': None, # Add notes field if you have it in Excel
                'next_suggested_appointment_date': next_suggested_appointment_date
            }

            created_appointment = appointment_controller.create_appointment(**appointment_data)
            if created_appointment:
                imported_appointments_count += 1
            else:
                print(f"CRITICAL ERROR: Failed to create appointment for {appt_identifier}. Check appointment_controller.create_appointment return value.")
                failed_appointments_count += 1

        except Exception as e:
            print(f"ERROR: Exception while creating appointment for {appt_identifier}: {e}")
            traceback.print_exc() # Print full traceback for more detailed debugging
            failed_appointments_count += 1
            continue # Continue to next row even if one fails

    print(f"--- Finished appointment import. Imported: {imported_appointments_count} appointments. Failed: {failed_appointments_count} ---")
    print(f"\n--- Total import process completed. Clients: {imported_clients_count}. Appointments: {imported_appointments_count}. ---")

if __name__ == "__main__":
    # Ensure this part is only run when the script is executed directly
    from config.database import get_db, init_db
    
    print("Initializing database (if not already done)...")
    init_db() # This will create tables if they don't exist

    db_session = next(get_db()) # Get a session
    try:
        import_data_from_excel(EXCEL_FILE_PATH, db_session)
    finally:
        db_session.close() # Always close the session