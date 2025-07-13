# models/payment_method.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from typing import List

class PaymentMethod(BaseModel):
    __tablename__ = 'payment_methods'

    method_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="payment_method")
    # Add the relationship to expenses
    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="payment_method")

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, name='{self.method_name}')>"