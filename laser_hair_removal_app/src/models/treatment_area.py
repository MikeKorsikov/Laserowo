from typing import Optional

class TreatmentArea:
    """Represents a treatment area with associated data and validation."""
    
    def __init__(self, area_id: int, area_name: str, default_price: float = 0.0, 
                 estimated_duration_minutes: int = 0):
        """Initialize a TreatmentArea instance with provided attributes."""
        self.area_id = self._validate_area_id(area_id)
        self.area_name = self._validate_name(area_name)
        self.default_price = self._validate_price(default_price)
        self.estimated_duration_minutes = self._validate_duration(estimated_duration_minutes)
    
    def _validate_area_id(self, area_id: int) -> int:
        """Validate area_id is a positive integer."""
        if not isinstance(area_id, int) or area_id <= 0:
            raise ValueError("Area ID must be a positive integer")
        return area_id
    
    def _validate_name(self, name: str) -> str:
        """Validate that the area name is non-empty."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Area name must not be empty")
        return name.strip()
    
    def _validate_price(self, price: float) -> float:
        """Validate default_price is a non-negative number."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Default price must be a non-negative number")
        return float(price)
    
    def _validate_duration(self, duration: int) -> int:
        """Validate estimated_duration_minutes is a non-negative integer."""
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("Estimated duration must be a non-negative integer")
        return duration
    
    def to_dict(self) -> dict:
        """Convert treatment area data to a dictionary for database storage or display."""
        return {
            'area_id': self.area_id,
            'area_name': self.area_name,
            'default_price': self.default_price,
            'estimated_duration_minutes': self.estimated_duration_minutes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TreatmentArea':
        """Create a TreatmentArea instance from a dictionary (e.g., database result)."""
        return cls(
            area_id=data.get('area_id'),
            area_name=data.get('area_name'),
            default_price=data.get('default_price', 0.0),
            estimated_duration_minutes=data.get('estimated_duration_minutes', 0)
        )

    def __str__(self) -> str:
        """Return a string representation of the treatment area."""
        return f"Treatment Area {self.area_name} (ID: {self.area_id})"

if __name__ == "__main__":
    try:
        treatment_area = TreatmentArea(
            area_id=1,
            area_name="Legs",
            default_price=100.00,
            estimated_duration_minutes=45
        )
        print(treatment_area)
        print(treatment_area.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")