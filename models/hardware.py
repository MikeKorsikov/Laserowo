# models/hardware.py
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relationship
from models.base import Base # <--- IMPORTANT: Ensure this is your shared 'Base' object
from datetime import date # Import date for type hinting

class Hardware(Base): # <--- IMPORTANT: Inherit from 'Base' (NOT BaseModel)
    __tablename__ = 'hardware' # <--- This must be 'hardware' for the foreign key to match

    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(255), nullable=False) # <--- Use Column
    serial_number = Column(String(255), unique=True, nullable=True)
    purchase_date = Column(Date, nullable=True)
    last_maintenance_date = Column(Date, nullable=True)
    next_maintenance_date = Column(Date, nullable=True)
    last_insurance_date = Column(Date, nullable=True)
    next_insurance_date = Column(Date, nullable=True)
    current_impulse_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    # Ensure 'Appointment' and 'OwnerReminder' are also defined in 1.x syntax
    # If OwnerReminder is not defined yet or not needed for import, you can comment it out for now.
    appointments = relationship("Appointment", back_populates="hardware")
    owner_reminders = relationship("OwnerReminder", back_populates="hardware") # Keep if OwnerReminder is also defined in 1.x

    def to_dict(self):
        return {
            "id": self.id,
            "device_name": self.device_name,
            "serial_number": self.serial_number,
            "purchase_date": str(self.purchase_date) if self.purchase_date else None,
            "last_maintenance_date": str(self.last_maintenance_date) if self.last_maintenance_date else None,
            "next_maintenance_date": str(self.next_maintenance_date) if self.next_maintenance_date else None,
            "last_insurance_date": str(self.last_insurance_date) if self.last_insurance_date else None,
            "next_insurance_date": str(self.next_insurance_date) if self.next_insurance_date else None,
            "current_impulse_count": self.current_impulse_count,
            "notes": self.notes,
            "is_active": self.is_active
        }

    def __repr__(self):
        return (f"<Hardware(id={self.id}, name='{self.device_name}', "
                f"serial='{self.serial_number}', active={self.is_active})>")