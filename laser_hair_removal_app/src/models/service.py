from typing import Optional

class Service:
    """Represents a service with associated data and validation."""
    
    def __init__(self, service_id: int, service_name: str, description: str = None, 
                 price: float = 0.0, duration_minutes: int = 0, is_active: bool = True):
        """Initialize a Service instance with provided attributes."""
        self.service_id = self._validate_service_id(service_id)
        self.service_name = self._validate_name(service_name)
        self.description = description
        self.price = self._validate_price(price)
        self.duration_minutes = self._validate_duration(duration_minutes)
        self.is_active = bool(is_active)
    
    def _validate_service_id(self, service_id: int) -> int:
        """Validate service_id is a positive integer."""
        if not isinstance(service_id, int) or service_id <= 0:
            raise ValueError("Service ID must be a positive integer")
        return service_id
    
    def _validate_name(self, name: str) -> str:
        """Validate that the service name is non-empty."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Service name must not be empty")
        return name.strip()
    
    def _validate_price(self, price: float) -> float:
        """Validate price is a non-negative number."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        return float(price)
    
    def _validate_duration(self, duration: int) -> int:
        """Validate duration is a non-negative integer."""
        if not isinstance(duration, int) or duration < 0:
            raise ValueError("Duration must be a non-negative integer")
        return duration
    
    def to_dict(self) -> dict:
        """Convert service data to a dictionary for database storage or display."""
        return {
            'service_id': self.service_id,
            'service_name': self.service_name,
            'description': self.description,
            'price': self.price,
            'duration_minutes': self.duration_minutes,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Service':
        """Create a Service instance from a dictionary (e.g., database result)."""
        return cls(
            service_id=data.get('service_id'),
            service_name=data.get('service_name'),
            description=data.get('description'),
            price=data.get('price', 0.0),
            duration_minutes=data.get('duration_minutes', 0),
            is_active=data.get('is_active', True)
        )

    def __str__(self) -> str:
        """Return a string representation of the service."""
        return f"Service {self.service_name} (ID: {self.service_id})"

if __name__ == "__main__":
    try:
        service = Service(
            service_id=1,
            service_name="Laser Hair Removal",
            description="Full body treatment",
            price=150.00,
            duration_minutes=60
        )
        print(service)
        print(service.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")