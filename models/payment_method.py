# models/payment_method.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base_model import BaseModel

class PaymentMethod(BaseModel):
    __tablename__ = 'payment_methods'

    method_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="payment_method")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="payment_method")