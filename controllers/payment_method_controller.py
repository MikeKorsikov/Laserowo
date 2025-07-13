# controllers/payment_method_controller.py
from sqlalchemy.orm import Session
from models.payment_method import PaymentMethod # Make sure this import is correct
from typing import Optional, List, Dict, Any

class PaymentMethodController:
    def __init__(self, db: Session):
        self.db = db

    def get_method_by_name(self, name: str) -> Optional[PaymentMethod]:
        """Retrieves a payment method by its name (case-insensitive)."""
        if not name: return None
        return self.db.query(PaymentMethod).filter(PaymentMethod.name.ilike(name)).first()

    def create_method(self, name: str, description: Optional[str] = None) -> Optional[PaymentMethod]:
        """Creates a new payment method."""
        if not name:
            print("Error: Payment method name cannot be empty.")
            return None
        existing_method = self.get_method_by_name(name)
        if existing_method:
            print(f"Warning: Payment method '{name}' already exists (ID: {existing_method.id}). Skipping creation.")
            return existing_method

        new_method = PaymentMethod(name=name, description=description)
        try:
            self.db.add(new_method)
            self.db.commit()
            self.db.refresh(new_method)
            print(f"Payment Method created: {new_method.name} (ID: {new_method.id})")
            return new_method
        except Exception as e:
            self.db.rollback()
            print(f"Error creating payment method '{name}': {e}")
            return None

    def get_or_create_method(self, name: str, description: Optional[str] = None) -> Optional[PaymentMethod]:
        """Gets a payment method by name, or creates it if it doesn't exist."""
        method = self.get_method_by_name(name)
        if method:
            return method
        return self.create_method(name, description)
    
    def get_all_methods(self) -> List[Dict[str, Any]]:
        """Retrieves all payment methods as a list of dictionaries."""
        methods = self.db.query(PaymentMethod).order_by(PaymentMethod.name).all()
        return [method.to_dict() for method in methods]

# updated