# models/promotion.py
from sqlalchemy import String, DECIMAL, Date, Boolean, JSON, Integer # Add Integer here
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from models.base_model import BaseModel

class Promotion(BaseModel):
    __tablename__ = 'promotions'

    promotion_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    promotion_type: Mapped[str] = mapped_column(String(50)) # e.g., 'Loyalty', 'Referral', 'Bulk Purchase'
    discount_value: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 4)) # e.g., 0.10 for 10%
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # target_categories: Mapped[Optional[str]] = mapped_column(JSON, nullable=True) # Or Text, or a separate join table
    partnership_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # Integer will now be recognized

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="promotion")

    def __repr__(self):
        return (f"<Promotion(id={self.id}, name='{self.promotion_name}', "
                f"type='{self.promotion_type}', active={self.is_active})>")