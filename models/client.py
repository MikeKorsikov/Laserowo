# models/client.py
from sqlalchemy import String, Boolean, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.base_model import BaseModel # Using BaseModel

class Client(BaseModel):
    __tablename__ = 'clients'

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    facebook_id: Mapped[str] = mapped_column(String(255), nullable=True)
    instagram_handle: Mapped[str] = mapped_column(String(255), nullable=True)
    booksy_indicator: Mapped[bool] = mapped_column(Boolean, default=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=True)
    is_blacklisted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="client")
    digital_checklists: Mapped[List["DigitalChecklist"]] = relationship(back_populates="client")

    def __repr__(self):
        return (f"<Client(id={self.id}, full_name='{self.full_name}', "
                f"phone='{self.phone_number}', email='{self.email}')>")