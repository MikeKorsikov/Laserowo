# models/treatment_area.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class TreatmentArea(Base):
    __tablename__ = 'treatment_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relationship (if appointments reference areas)
    appointments = relationship("Appointment", back_populates="area")

    def __repr__(self):
        return f"<TreatmentArea(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

#reviewed