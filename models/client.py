# models/client.py
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import date # Import date for type hinting

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False) # Removed unique=True if names might duplicate
    email = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(50), unique=True, nullable=True) # Usually unique
    gender = Column(String(10), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    
    # New fields based on Excel import mapping
    facebook_id = Column(String(255), nullable=True)
    instagram_handle = Column(String(255), nullable=True)
    booksy_used = Column(Boolean, default=False, nullable=False)
    is_blacklisted = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    excel_id = Column(String(255), unique=True, nullable=True) # Store original Excel ID

    def __repr__(self):
        return f"<Client(id={self.id}, full_name='{self.full_name}')>"

    def to_dict(self):
        """Converts the Client object to a dictionary for easy serialization."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'notes': self.notes,
            'facebook_id': self.facebook_id,
            'instagram_handle': self.instagram_handle,
            'booksy_used': self.booksy_used,
            'is_blacklisted': self.is_blacklisted,
            'is_active': self.is_active,
            'excel_id': self.excel_id
        }

#reviewed