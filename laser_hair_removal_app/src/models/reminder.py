from typing import Optional
from datetime import datetime

class Reminder:
    """Represents a reminder with associated data and validation."""
    
    def __init__(self, reminder_id: int, reminder_type: str, related_id: int = None, 
                 due_date: str, reminder_date: str, message: str, is_active: bool = True, 
                 delivery_method: str = 'Popup'):
        """Initialize a Reminder instance with provided attributes."""
        self.reminder_id = self._validate_reminder_id(reminder_id)
        self.reminder_type = self._validate_type(reminder_type)
        self.related_id = self._validate_related_id(related_id) if related_id else None
        self.due_date = self._validate_date(due_date)
        self.reminder_date = self._validate_date(reminder_date)
        self.message = self._validate_message(message)
        self.is_active = bool(is_active)
        self.delivery_method = self._validate_delivery_method(delivery_method)
    
    def _validate_reminder_id(self, reminder_id: int) -> int:
        """Validate reminder_id is a positive integer."""
        if not isinstance(reminder_id, int) or reminder_id <= 0:
            raise ValueError("Reminder ID must be a positive integer")
        return reminder_id
    
    def _validate_type(self, reminder_type: str) -> str:
        """Validate reminder_type is non-empty."""
        if not reminder_type or not isinstance(reminder_type, str) or not reminder_type.strip():
            raise ValueError("Reminder type must not be empty")
        return reminder_type.strip()
    
    def _validate_related_id(self, related_id: int) -> int:
        """Validate related_id is a positive integer."""
        if related_id is not None and (not isinstance(related_id, int) or related_id <= 0):
            raise ValueError("Related ID must be a positive integer")
        return related_id
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if not date_str or not isinstance(date_str, str):
            raise ValueError("Date is required")
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    def _validate_message(self, message: str) -> str:
        """Validate message is non-empty."""
        if not message or not isinstance(message, str) or not message.strip():
            raise ValueError("Message must not be empty")
        return message.strip()
    
    def _validate_delivery_method(self, method: str) -> str:
        """Validate delivery_method is one of the allowed values."""
        valid_methods = ['Popup', 'SMS', 'Email']
        if method not in valid_methods:
            raise ValueError(f"Delivery method must be one of {valid_methods}")
        return method
    
    def is_due(self) -> bool:
        """Check if the reminder is due based on current date."""
        current_date = datetime.now().date()
        reminder_date = datetime.strptime(self.reminder_date, '%Y-%m-%d').date()
        return current_date >= reminder_date
    
    def to_dict(self) -> dict:
        """Convert reminder data to a dictionary for database storage or display."""
        return {
            'reminder_id': self.reminder_id,
            'reminder_type': self.reminder_type,
            'related_id': self.related_id,
            'due_date': self.due_date,
            'reminder_date': self.reminder_date,
            'message': self.message,
            'is_active': self.is_active,
            'delivery_method': self.delivery_method
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reminder':
        """Create a Reminder instance from a dictionary (e.g., database result)."""
        return cls(
            reminder_id=data.get('reminder_id'),
            reminder_type=data.get('reminder_type'),
            related_id=data.get('related_id'),
            due_date=data.get('due_date'),
            reminder_date=data.get('reminder_date'),
            message=data.get('message'),
            is_active=data.get('is_active', True),
            delivery_method=data.get('delivery_method', 'Popup')
        )

    def __str__(self) -> str:
        """Return a string representation of the reminder."""
        return f"Reminder {self.reminder_id} for {self.reminder_type} on {self.reminder_date}"

if __name__ == "__main__":
    try:
        reminder = Reminder(
            reminder_id=1,
            reminder_type="Maintenance",
            related_id=1,
            due_date="2025-07-31",
            reminder_date="2025-07-16",
            message="Perform laser machine maintenance",
            delivery_method="Popup"
        )
        print(reminder)
        print(f"Reminder due: {reminder.is_due()}")
        print(reminder.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")