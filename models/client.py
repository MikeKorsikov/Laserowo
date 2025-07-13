# models/client.py
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from models.base import Base # Assuming your Base is defined here
from datetime import date # Import date for type hinting

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    facebook_id = Column(String, nullable=True)
    instagram_handle = Column(String, nullable=True)
    booksy_used = Column(Boolean, default=False)
    date_of_birth = Column(Date, nullable=True)
    is_blacklisted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
    excel_id = Column(String, unique=True, nullable=True) # <--- ADD THIS LINE

    appointments = relationship("Appointment", back_populates="client")

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "facebook_id": self.facebook_id,
            "instagram_handle": self.instagram_handle,
            "booksy_used": self.booksy_used,
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "is_blacklisted": self.is_blacklisted,
            "is_active": self.is_active,
            "notes": self.notes,
            "excel_id": self.excel_id # <--- INCLUDE IN TO_DICT
        }

    def __repr__(self):
        return f"<Client(id={self.id}, full_name='{self.full_name}', phone_number='{self.phone_number}')>"

# updated