# P1_desktop_app/models/promotion.py

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import relationship
from models.base import Base # Assuming you have a base.py in models

class Promotion(Base):
    __tablename__ = 'promotions' # The name of the table in your database

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))
    discount_percentage = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    active = Column(Boolean, default=True)

    # Optional: Define relationships if Promotions can be linked to Appointments
    # appointments = relationship("Appointment", back_populates="promotion")

    def __repr__(self):
        return f"<Promotion(id={self.id}, name='{self.name}', discount={self.discount_percentage}%)>"

# You could also add constants or very simple utility functions related to promotions here
# For example:
# DEFAULT_PROMOTION_DURATION_DAYS = 30
#
# def calculate_discounted_price(original_price: float, discount_percentage: float) -> float:
#     return original_price * (1 - discount_percentage / 100.0)