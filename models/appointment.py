# P1_desktop_app/models/appointment.py
from sqlalchemy import Column, Integer, String, Date, Time, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base # Assuming Base is defined here or imported

# If Base is in a separate file (e.g., models/base.py), import it:
# from .base import Base

Base = declarative_base() # Or wherever your Base is initialized

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Client relationship
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False) # <--- CHECK THIS LINE
    client = relationship("Client", backref="appointments")

    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    service = relationship("Service", backref="appointments")

    area_id = Column(Integer, ForeignKey('treatment_areas.id'), nullable=True)
    area = relationship("TreatmentArea", backref="appointments")

    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True) # End time can be optional

    session_number_for_area = Column(Integer, nullable=True)
    power_j_cm3 = Column(String(50), nullable=True) # Assuming this is string or float
    
    # Status and Payment
    appointment_status = Column(String(50), default="Scheduled", nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)
    payment_method = relationship("PaymentMethod", backref="appointments")

    # Optional fields
    promotion_id = Column(Integer, ForeignKey('promotions.id'), nullable=True) # Assuming a promotions table
    promotion = relationship("Promotion", backref="appointments")

    hardware_id = Column(Integer, ForeignKey('hardwares.id'), nullable=True) # Assuming a hardwares table
    hardware = relationship("Hardware", backref="appointments")

    notes = Column(Text, nullable=True)
    next_suggested_appointment_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Appointment(id={self.id}, client_id={self.client_id}, date={self.appointment_date})>"

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'service_id': self.service_id,
            'area_id': self.area_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'session_number_for_area': self.session_number_for_area,
            'power_j_cm3': self.power_j_cm3,
            'appointment_status': self.appointment_status,
            'amount': self.amount,
            'payment_method_id': self.payment_method_id,
            'promotion_id': self.promotion_id,
            'hardware_id': self.hardware_id,
            'notes': self.notes,
            'next_suggested_appointment_date': self.next_suggested_appointment_date.isoformat() if self.next_suggested_appointment_date else None,
            'client_full_name': self.client.full_name if self.client else None # Example for client's name
        }

# reviewed