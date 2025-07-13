# models/treatment_area.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class TreatmentArea(Base):
    __tablename__ = 'treatment_areas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self):
        return f"<TreatmentArea(id={self.id}, name='{self.name}')>"

# updated