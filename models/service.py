# models/service.py
from sqlalchemy import String, Boolean, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base_model import BaseModel

class Service(BaseModel):
    __tablename__ = 'services'

    service_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    default_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=True)
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="service")
    # treatment_protocols: Mapped[List["TreatmentProtocol"]] = relationship(back_populates="service") # If you implement protocols per service