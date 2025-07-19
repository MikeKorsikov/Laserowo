from typing import Optional
import re
from datetime import datetime

class Client:
    """Represents a client with associated data and validation."""
    
    def __init__(self, client_id: int, full_name: str, phone_number: str, email: str = None, 
                 dob: str = None, is_blacklisted: bool = False, is_active: bool = True, 
                 notes: str = None):
        """Initialize a Client instance with provided attributes."""
        self.client_id = client_id
        self.full_name = self._validate_name(full_name)
        self.phone_number = self._validate_phone(phone_number)
        self.email = self._validate_email(email) if email else None
        self.dob = self._validate_date(dob) if dob else None
        self.is_blacklisted = bool(is_blacklisted)
        self.is_active = bool(is_active)
        self.notes = notes
    
    def _validate_name(self, name: str) -> str:
        """Validate that the name is non-empty and contains only letters and spaces."""
        if not name or not isinstance(name, str) or not re.match(r'^[a-zA-Z\s]+$', name.strip()):
            raise ValueError("Full name must contain only letters and spaces")
        return name.strip()
    
    def _validate_phone(self, phone: str) -> str:
        """Validate phone number format (e.g., +48 123 456 789 or 123-456-789)."""
        if not phone or not isinstance(phone, str):
            raise ValueError("Phone number is required")
        # Simple validation for Polish format (+48) or basic digits
        if not re.match(r'^\+?\d{9,15}$', phone.replace(' ', '').replace('-', '')):
            raise ValueError("Invalid phone number format")
        return phone.strip()
    
    def _validate_email(self, email: str) -> str:
        """Validate email format."""
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email.strip()):
            raise ValueError("Invalid email format")
        return email.strip() if email else None
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return None
    
    def to_dict(self) -> dict:
        """Convert client data to a dictionary for database storage or display."""
        return {
            'client_id': self.client_id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'dob': self.dob,
            'is_blacklisted': self.is_blacklisted,
            'is_active': self.is_active,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Client':
        """Create a Client instance from a dictionary (e.g., database result)."""
        return cls(
            client_id=data.get('client_id'),
            full_name=data.get('full_name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            dob=data.get('dob'),
            is_blacklisted=data.get('is_blacklisted', False),
            is_active=data.get('is_active', True),
            notes=data.get('notes')
        )

    def __str__(self) -> str:
        """Return a string representation of the client."""
        return f"Client {self.full_name} (ID: {self.client_id})"

if __name__ == "__main__":
    # Example usage
    try:
        client = Client(
            client_id=1,
            full_name="Anna Kowalska",
            phone_number="+48 123 456 789",
            email="anna@example.com",
            dob="1995-03-10",
            notes="First visit notes"
        )
        print(client)
        print(client.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")