# models/payment_method.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship # <--- Make sure relationship is imported
from models.base import Base

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Add the appointments relationship
    appointments = relationship("Appointment", back_populates="payment_method") # <--- ADD THIS LINE

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, name='{self.name}')>"