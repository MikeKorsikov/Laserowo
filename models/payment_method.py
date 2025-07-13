# models/payment_method.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True) # e.g., "Cash", "Card", "Bank Transfer"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, name='{self.name}')>"

# updated