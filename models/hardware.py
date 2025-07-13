# models/hardware.py
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base_model import BaseModel

class Hardware(BaseModel):
    __tablename__ = 'hardware'

    equipment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    purchase_date: Mapped[Date] = mapped_column(Date, nullable=True)
    last_maintenance_date: Mapped[Date] = mapped_column(Date, nullable=True)
    next_maintenance_due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    last_insurance_date: Mapped[Date] = mapped_column(Date, nullable=True)
    next_insurance_due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    total_impulses_recorded: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="hardware")
    owner_reminders: Mapped[List["OwnerReminder"]] = relationship(back_populates="hardware")