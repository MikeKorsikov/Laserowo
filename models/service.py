# P1_desktop_app/models/service.py
from sqlalchemy import Column, Integer, String, Text
# from config.database import Base # DELETE THIS LINE
from .base import Base # <--- ADD THIS LINE

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }