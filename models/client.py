# --- models/client.py ---
from sqlalchemy import Column, Integer, String
from config.database import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)