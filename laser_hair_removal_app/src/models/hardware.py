from typing import Optional
from datetime import datetime

class Hardware:
    """Represents hardware equipment with associated data and validation."""
    
    def __init__(self, hardware_id: int, equipment_name: str, purchase_date: str = None, 
                 last_maintenance_date: str = None, next_maintenance_due_date: str = None, 
                 last_insurance_date: str = None, next_insurance_due_date: str = None, 
                 maximum_impulses_on_purchase: int = 0, total_impulses_recorded: int = 0):
        """Initialize a Hardware instance with provided attributes."""
        self.hardware_id = self._validate_hardware_id(hardware_id)
        self.equipment_name = self._validate_name(equipment_name)
        self.purchase_date = self._validate_date(purchase_date) if purchase_date else None
        self.last_maintenance_date = self._validate_date(last_maintenance_date) if last_maintenance_date else None
        self.next_maintenance_due_date = self._validate_date(next_maintenance_due_date) if next_maintenance_due_date else None
        self.last_insurance_date = self._validate_date(last_insurance_date) if last_insurance_date else None
        self.next_insurance_date = self._validate_date(next_insurance_due_date) if next_insurance_due_date else None
        self.maximum_impulses_on_purchase = self._validate_max_impulses(maximum_impulses_on_purchase)
        self.total_impulses_recorded = self._validate_total_impulses(total_impulses_recorded)
        self._validate_impulse_constraint()
    
    def _validate_hardware_id(self, hardware_id: int) -> int:
        """Validate hardware_id is a positive integer."""
        if not isinstance(hardware_id, int) or hardware_id <= 0:
            raise ValueError("Hardware ID must be a positive integer")
        return hardware_id
    
    def _validate_name(self, name: str) -> str:
        """Validate that the equipment name is non-empty."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Equipment name must not be empty")
        return name.strip()
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if date_str:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return None
    
    def _validate_max_impulses(self, max_impulses: int) -> int:
        """Validate maximum_impulses_on_purchase is a non-negative integer."""
        if not isinstance(max_impulses, int) or max_impulses < 0:
            raise ValueError("Maximum impulses must be a non-negative integer")
        return max_impulses
    
    def _validate_total_impulses(self, total_impulses: int) -> int:
        """Validate total_impulses_recorded is a non-negative integer."""
        if not isinstance(total_impulses, int) or total_impulses < 0:
            raise ValueError("Total impulses recorded must be a non-negative integer")
        return total_impulses
    
    def _validate_impulse_constraint(self) -> None:
        """Validate that total_impulses_recorded does not exceed maximum_impulses_on_purchase."""
        if self.total_impulses_recorded > self.maximum_impulses_on_purchase:
            raise ValueError("Total impulses recorded cannot exceed maximum impulses on purchase")
    
    def is_maintenance_due(self) -> bool:
        """Check if maintenance is due based on current date."""
        if not self.next_maintenance_due_date:
            return False
        current_date = datetime.now().date()
        due_date = datetime.strptime(self.next_maintenance_due_date, '%Y-%m-%d').date()
        return current_date >= due_date
    
    def is_insurance_due(self) -> bool:
        """Check if insurance is due based on current date."""
        if not self.next_insurance_date:
            return False
        current_date = datetime.now().date()
        due_date = datetime.strptime(self.next_insurance_date, '%Y-%m-%d').date()
        return current_date >= due_date
    
    def to_dict(self) -> dict:
        """Convert hardware data to a dictionary for database storage or display."""
        return {
            'hardware_id': self.hardware_id,
            'equipment_name': self.equipment_name,
            'purchase_date': self.purchase_date,
            'last_maintenance_date': self.last_maintenance_date,
            'next_maintenance_due_date': self.next_maintenance_due_date,
            'last_insurance_date': self.last_insurance_date,
            'next_insurance_due_date': self.next_insurance_date,
            'maximum_impulses_on_purchase': self.maximum_impulses_on_purchase,
            'total_impulses_recorded': self.total_impulses_recorded
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Hardware':
        """Create a Hardware instance from a dictionary (e.g., database result)."""
        return cls(
            hardware_id=data.get('hardware_id'),
            equipment_name=data.get('equipment_name'),
            purchase_date=data.get('purchase_date'),
            last_maintenance_date=data.get('last_maintenance_date'),
            next_maintenance_due_date=data.get('next_maintenance_due_date'),
            last_insurance_date=data.get('last_insurance_date'),
            next_insurance_due_date=data.get('next_insurance_due_date'),
            maximum_impulses_on_purchase=data.get('maximum_impulses_on_purchase', 0),
            total_impulses_recorded=data.get('total_impulses_recorded', 0)
        )

    def __str__(self) -> str:
        """Return a string representation of the hardware."""
        return f"Hardware {self.equipment_name} (ID: {self.hardware_id})"

if __name__ == "__main__":
    try:
        hardware = Hardware(
            hardware_id=1,
            equipment_name="Laser Machine",
            purchase_date="2024-01-15",
            last_maintenance_date="2025-01-01",
            next_maintenance_due_date="2025-07-31",
            last_insurance_date="2025-01-01",
            next_insurance_due_date="2025-12-31",
            maximum_impulses_on_purchase=1000000,
            total_impulses_recorded=500000
        )
        print(hardware)
        print(f"Maintenance due: {hardware.is_maintenance_due()}")
        print(f"Insurance due: {hardware.is_insurance_due()}")
        print(hardware.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")