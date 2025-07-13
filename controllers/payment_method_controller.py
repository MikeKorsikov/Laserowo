# controllers/payment_method_controller.py
from sqlalchemy.orm import Session
from models.payment_method import PaymentMethod # Make sure your PaymentMethod model is defined
from typing import Optional, List, Dict, Any

class PaymentMethodController:
    def __init__(self, db: Session):
        self.db = db

    def create_method(self, name: str) -> Optional[PaymentMethod]:
        """Creates a new payment method."""
        if not name:
            print("Error: Payment method name cannot be empty.")
            return None
        new_method = PaymentMethod(name=name)
        try:
            self.db.add(new_method)
            self.db.commit()
            self.db.refresh(new_method)
            print(f"Payment Method created: {new_method.name}")
            return new_method
        except Exception as e:
            self.db.rollback()
            print(f"Error creating payment method '{name}': {e}")
            return None

    def get_method_by_id(self, method_id: int) -> Optional[PaymentMethod]:
        """Retrieves a payment method by ID."""
        return self.db.query(PaymentMethod).get(method_id)

    def get_method_by_name(self, name: str) -> Optional[PaymentMethod]:
        """Retrieves a payment method by name."""
        return self.db.query(PaymentMethod).filter(PaymentMethod.name == name).first()

    def get_or_create_method(self, name: str) -> Optional[PaymentMethod]:
        """Retrieves a payment method by name, or creates it if it doesn't exist."""
        method = self.get_method_by_name(name)
        if not method:
            method = self.create_method(name)
        return method

    def get_all_methods(self) -> List[Dict[str, Any]]:
        """Retrieves all payment methods."""
        methods = self.db.query(PaymentMethod).order_by(PaymentMethod.name).all()
        return [method.to_dict() for method in methods]

# reviewed