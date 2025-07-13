# models/payment_method.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationship (if appointments reference payment methods)
    appointments = relationship("Appointment", back_populates="payment_method")

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }