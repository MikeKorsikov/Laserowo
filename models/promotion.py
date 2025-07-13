# models/promotion.py
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, Float
from sqlalchemy.orm import relationship
from models.base import Base # Assuming your shared Base is here
from datetime import date # For type hinting

class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False) # E.g., "Summer Sale", "First Visit Discount"
    description = Column(Text, nullable=True)
    discount_percentage = Column(Float, nullable=True) # E.g., 0.10 for 10%
    fixed_discount_amount = Column(Float, nullable=True) # E.g., 10.00 for $10 off
    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date, nullable=True) # Can be ongoing if None
    is_active = Column(Boolean, default=True)

    # Relationships:
    # Add this relationship to link back to Appointments
    # This means a Promotion can have multiple Appointments associated with it.
    appointments = relationship("Appointment", back_populates="promotion")


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "discount_percentage": self.discount_percentage,
            "fixed_discount_amount": self.fixed_discount_amount,
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<Promotion(id={self.id}, name='{self.name}', active={self.is_active})>"