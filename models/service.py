# --- models/service.py ---
from sqlalchemy import Column, Integer, String, Float
from config.database import Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)