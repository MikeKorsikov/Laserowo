from typing import Optional

class Inventory:
    """Represents an inventory item with associated data and validation."""
    
    def __init__(self, item_id: int, item_name: str, current_quantity: float, unit: str, 
                 low_stock_threshold: float = 10.0):
        """Initialize an Inventory instance with provided attributes."""
        self.item_id = self._validate_item_id(item_id)
        self.item_name = self._validate_name(item_name)
        self.current_quantity = self._validate_quantity(current_quantity)
        self.unit = self._validate_unit(unit)
        self.low_stock_threshold = self._validate_threshold(low_stock_threshold)
    
    def _validate_item_id(self, item_id: int) -> int:
        """Validate item_id is a positive integer."""
        if not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("Item ID must be a positive integer")
        return item_id
    
    def _validate_name(self, name: str) -> str:
        """Validate that the item name is non-empty."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Item name must not be empty")
        return name.strip()
    
    def _validate_quantity(self, quantity: float) -> float:
        """Validate quantity is a non-negative number."""
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError("Quantity must be a non-negative number")
        return float(quantity)
    
    def _validate_unit(self, unit: str) -> str:
        """Validate that the unit is non-empty."""
        if not unit or not isinstance(unit, str) or not unit.strip():
            raise ValueError("Unit must not be empty")
        return unit.strip()
    
    def _validate_threshold(self, threshold: float) -> float:
        """Validate low_stock_threshold is a non-negative number."""
        if not isinstance(threshold, (int, float)) or threshold < 0:
            raise ValueError("Low stock threshold must be a non-negative number")
        return float(threshold)
    
    def is_low_stock(self) -> bool:
        """Check if the current quantity is below the low stock threshold."""
        return self.current_quantity < self.low_stock_threshold
    
    def to_dict(self) -> dict:
        """Convert inventory data to a dictionary for database storage or display."""
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'current_quantity': self.current_quantity,
            'unit': self.unit,
            'low_stock_threshold': self.low_stock_threshold
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Inventory':
        """Create an Inventory instance from a dictionary (e.g., database result)."""
        return cls(
            item_id=data.get('item_id'),
            item_name=data.get('item_name'),
            current_quantity=data.get('current_quantity', 0.0),
            unit=data.get('unit'),
            low_stock_threshold=data.get('low_stock_threshold', 10.0)
        )

    def __str__(self) -> str:
        """Return a string representation of the inventory item."""
        return f"Inventory {self.item_name} (ID: {self.item_id}, Quantity: {self.current_quantity} {self.unit})"

if __name__ == "__main__":
    try:
        inventory = Inventory(
            item_id=1,
            item_name="Laser Gel",
            current_quantity=15.0,
            unit="ml",
            low_stock_threshold=10.0
        )
        print(inventory)
        print(f"Low stock: {inventory.is_low_stock()}")
        print(inventory.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")