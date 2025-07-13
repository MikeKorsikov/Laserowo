# models/treatment_area.py
from sqlalchemy import String, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base_model import BaseModel

class TreatmentArea(BaseModel):
    __tablename__ = 'treatment_areas'

    area_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    default_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=True)
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="treatment_area")