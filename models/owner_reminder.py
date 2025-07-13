# models/owner_reminder.py
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base # <--- IMPORTANT: Ensure this is your shared 'Base' object
from datetime import date # Import date for type hinting if you use it in methods

class OwnerReminder(Base): # <--- IMPORTANT: Inherit from 'Base' (NOT BaseModel)
    __tablename__ = 'owner_reminders'

    id = Column(Integer, primary_key=True, index=True)
    reminder_type = Column(String(100), nullable=False) # <--- Use Column
    due_date = Column(Date, nullable=False)
    hardware_id = Column(Integer, ForeignKey('hardware.id'), nullable=True) # Matches 'hardware' tablename and 'id' column
    message = Column(Text, nullable=False)
    is_dismissed = Column(Boolean, default=False)
    dismissed_date = Column(Date, nullable=True)

    # Relationship to Hardware
    hardware = relationship("Hardware", back_populates="owner_reminders") # Make sure back_populates matches relationship in Hardware

    def to_dict(self):
        return {
            "id": self.id,
            "reminder_type": self.reminder_type,
            "due_date": str(self.due_date) if self.due_date else None,
            "hardware_id": self.hardware_id,
            "message": self.message,
            "is_dismissed": self.is_dismissed,
            "dismissed_date": str(self.dismissed_date) if self.dismissed_date else None
        }

    def __repr__(self):
        return (f"<OwnerReminder(id={self.id}, type='{self.reminder_type}', "
                f"due_date={self.due_date}, dismissed={self.is_dismissed})>")
    