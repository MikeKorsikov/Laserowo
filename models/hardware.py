# models/hardware.py
from sqlalchemy import String, Date, Text, Integer, Boolean, DECIMAL # Ensure all types are imported
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from typing import List, Optional

class Hardware(BaseModel):
    __tablename__ = 'hardware'

    device_name: Mapped[str] = mapped_column(String(255), nullable=False)
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    purchase_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    last_maintenance_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    next_maintenance_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    last_insurance_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    next_insurance_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    current_impulse_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="hardware")
    # Reference the class name as a string for forward references
    owner_reminders: Mapped[List["OwnerReminder"]] = relationship("OwnerReminder", back_populates="hardware")

    def __repr__(self):
        return (f"<Hardware(id={self.id}, name='{self.device_name}', "
                f"serial='{self.serial_number}', active={self.is_active})>")

# reviewed