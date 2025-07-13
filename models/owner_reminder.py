# models/owner_reminder.py
from sqlalchemy import String, Date, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from typing import Optional

class OwnerReminder(BaseModel):
    __tablename__ = 'owner_reminders'

    # Reminder types could be 'Hardware Maintenance', 'Hardware Insurance', 'Accountant Visit', 'Inventory Check'
    reminder_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # The date the reminder is due
    due_date: Mapped[Date] = mapped_column(Date, nullable=False)
    # Optional foreign key if the reminder is related to a specific hardware item
    hardware_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('hardware.id'), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_dismissed: Mapped[bool] = mapped_column(Boolean, default=False)
    dismissed_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)

    # Relationship to Hardware (if applicable)
    hardware: Mapped["Hardware"] = relationship("Hardware", back_populates="owner_reminders")

    def __repr__(self):
        return (f"<OwnerReminder(id={self.id}, type='{self.reminder_type}', "
                f"due_date={self.due_date}, dismissed={self.is_dismissed})>")

# reviewed