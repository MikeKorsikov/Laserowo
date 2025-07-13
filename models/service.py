# models/service.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship # <--- Make sure relationship is imported
from models.base import Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Add the appointments relationship
    appointments = relationship("Appointment", back_populates="service") # <--- ADD THIS LINE

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}')>"