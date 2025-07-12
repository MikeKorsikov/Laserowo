# --- models/appointment.py ---
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from config.database import Base

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    date_time = Column(DateTime)