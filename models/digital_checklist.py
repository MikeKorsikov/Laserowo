# models/digital_checklist.py
from sqlalchemy import String, Boolean, Date, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from datetime import date

class DigitalChecklist(BaseModel):
    __tablename__ = 'digital_checklists'

    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    checklist_date: Mapped[Date] = mapped_column(Date, nullable=False, default=date.today)
    allergies: Mapped[str] = mapped_column(Text, nullable=True)
    health_issues: Mapped[str] = mapped_column(Text, nullable=True)
    medications: Mapped[str] = mapped_column(Text, nullable=True)
    other_notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False) # Or True, if it's considered complete on creation

    # Relationship
    client: Mapped["Client"] = relationship(back_populates="digital_checklists")

    def __repr__(self):
        return (f"<DigitalChecklist(id={self.id}, client_id={self.client_id}, "
                f"date={self.checklist_date}, completed={self.is_completed})>")