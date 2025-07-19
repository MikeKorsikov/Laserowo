from typing import Optional
import re
from datetime import datetime, timedelta
from src.models.client import Client  # For potential future reference

class Appointment:
    """Represents an appointment with associated data and validation."""
    
    # Minimum waiting periods (in weeks) between sessions for the same treatment area
    MIN_WAITING_PERIODS = {
        1: 0,  # Initial session
        2: 4,  # 4 weeks after Session 1
        3: 6,  # 6 weeks after Session 2
        4: 8,  # 8 weeks after Session 3
        5: 10, # 10 weeks after Session 4
        6: 12, # 12 weeks after Session 5
        7: 14, # 14 weeks after Session 6
        8: 16, # 16 weeks after Session 7
        9: 18, # 18 weeks after Session 8
        10: 20 # 20 weeks after Session 9
    }
    
    def __init__(self, appointment_id: int, client_id: int, service_id: int, area_id: int, 
                 appointment_date: str, session_number: int, power: float = None, 
                 appointment_status: str = 'Scheduled', amount: float = None, 
                 payment_method_id: int = None, next_suggested_appointment_date: str = None):
        """Initialize an Appointment instance with provided attributes."""
        self.appointment_id = appointment_id
        self.client_id = self._validate_client_id(client_id)
        self.service_id = self._validate_service_id(service_id)
        self.area_id = self._validate_area_id(area_id)
        self.appointment_date = self._validate_date(appointment_date)
        self.session_number = self._validate_session_number(session_number)
        self.power = power
        self.appointment_status = self._validate_status(appointment_status)
        self.amount = amount
        self.payment_method_id = payment_method_id
        self.next_suggested_appointment_date = self._validate_date(next_suggested_appointment_date) if next_suggested_appointment_date else None
    
    def _validate_client_id(self, client_id: int) -> int:
        """Validate client_id is a positive integer."""
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("Client ID must be a positive integer")
        return client_id
    
    def _validate_service_id(self, service_id: int) -> int:
        """Validate service_id is a positive integer."""
        if not isinstance(service_id, int) or service_id <= 0:
            raise ValueError("Service ID must be a positive integer")
        return service_id
    
    def _validate_area_id(self, area_id: int) -> int:
        """Validate area_id is a positive integer."""
        if not isinstance(area_id, int) or area_id <= 0:
            raise ValueError("Area ID must be a positive integer")
        return area_id
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return None
    
    def _validate_session_number(self, session_number: int) -> int:
        """Validate session number is a positive integer up to 10."""
        if not isinstance(session_number, int) or session_number < 1 or session_number > 10:
            raise ValueError("Session number must be between 1 and 10")
        return session_number
    
    def _validate_status(self, status: str) -> str:
        """Validate appointment status is one of the allowed values."""
        valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'Rescheduled']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return status
    
    def validate_visit_spacing(self, previous_appointment: 'Appointment') -> bool:
        """Validate the minimum waiting period between this and the previous appointment for the same area."""
        if not previous_appointment or previous_appointment.area_id != self.area_id:
            return True  # No previous appointment or different area, assume valid
        
        prev_date = datetime.strptime(previous_appointment.appointment_date, '%Y-%m-%d')
        curr_date = datetime.strptime(self.appointment_date, '%Y-%m-%d')
        min_weeks = self.MIN_WAITING_PERIODS.get(previous_appointment.session_number, 20)
        min_date = prev_date + timedelta(weeks=min_weeks)
        
        return curr_date >= min_date
    
    def to_dict(self) -> dict:
        """Convert appointment data to a dictionary for database storage or display."""
        return {
            'appointment_id': self.appointment_id,
            'client_id': self.client_id,
            'service_id': self.service_id,
            'area_id': self.area_id,
            'appointment_date': self.appointment_date,
            'session_number_for_area': self.session_number,
            'power': self.power,
            'appointment_status': self.appointment_status,
            'amount': self.amount,
            'payment_method_id': self.payment_method_id,
            'next_suggested_appointment_date': self.next_suggested_appointment_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Appointment':
        """Create an Appointment instance from a dictionary (e.g., database result)."""
        return cls(
            appointment_id=data.get('appointment_id'),
            client_id=data.get('client_id'),
            service_id=data.get('service_id'),
            area_id=data.get('area_id'),
            appointment_date=data.get('appointment_date'),
            session_number=data.get('session_number_for_area'),
            power=data.get('power'),
            appointment_status=data.get('appointment_status', 'Scheduled'),
            amount=data.get('amount'),
            payment_method_id=data.get('payment_method_id'),
            next_suggested_appointment_date=data.get('next_suggested_appointment_date')
        )

    def __str__(self) -> str:
        """Return a string representation of the appointment."""
        return f"Appointment {self.appointment_id} for Client {self.client_id} on {self.appointment_date}"

if __name__ == "__main__":
    # Example usage
    try:
        # Sample previous appointment for validation
        prev_appointment = Appointment(
            appointment_id=1,
            client_id=1,
            service_id=1,
            area_id=1,
            appointment_date="2025-07-01",
            session_number=1,
            appointment_status="Completed"
        )
        
        # New appointment to validate spacing
        new_appointment = Appointment(
            appointment_id=2,
            client_id=1,
            service_id=1,
            area_id=1,
            appointment_date="2025-08-01",
            session_number=2,
            appointment_status="Scheduled"
        )
        
        is_valid = new_appointment.validate_visit_spacing(prev_appointment)
        print(f"Appointment spacing valid: {is_valid}")
        print(new_appointment)
        print(new_appointment.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")