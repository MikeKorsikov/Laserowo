# models/appointment.py
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, DECIMAL, Text, Time # <--- ADD Time HERE
from sqlalchemy.orm import relationship
from models.base import Base # Assuming your Base is defined here
from datetime import datetime # Import datetime for DateTime type hinting, date for Date

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True) # Now 'Time' is defined
    end_time = Column(Time, nullable=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    treatment_area_id = Column(Integer, ForeignKey('treatment_areas.id'), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)
    is_paid = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    promotion_id = Column(Integer, ForeignKey('promotions.id'), nullable=True)
    hardware_id = Column(Integer, ForeignKey('hardware.id'), nullable=True)
    # New fields
    appointment_type = Column(String(50), nullable=True) # e.g., 'Regular', 'Consultation', 'Follow-up'
    status = Column(String(50), default='Scheduled', nullable=False) # e.g., 'Scheduled', 'Completed', 'Cancelled', 'No-show'
    staff_member = Column(String(100), nullable=True) # Name of the staff member
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    duration_minutes = Column(Integer, nullable=True) # Duration of the appointment in minutes
    is_rescheduled = Column(Boolean, default=False)
    original_appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=True) # For rescheduled appointments

    # Relationships
    client = relationship("Client", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    treatment_area = relationship("TreatmentArea", back_populates="appointments")
    payment_method = relationship("PaymentMethod", back_populates="appointments")
    promotion = relationship("Promotion", back_populates="appointments")
    hardware = relationship("Hardware", back_populates="appointments")
    # For rescheduled appointments
    original_appointment = relationship("Appointment", remote_side=[id], backref="rescheduled_appointments")


    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "appointment_date": str(self.appointment_date) if self.appointment_date else None,
            "start_time": str(self.start_time) if self.start_time else None,
            "end_time": str(self.end_time) if self.end_time else None,
            "service_id": self.service_id,
            "treatment_area_id": self.treatment_area_id,
            "price": float(self.price) if self.price else None,
            "payment_method_id": self.payment_method_id,
            "is_paid": self.is_paid,
            "notes": self.notes,
            "promotion_id": self.promotion_id,
            "hardware_id": self.hardware_id,
            "appointment_type": self.appointment_type,
            "status": self.status,
            "staff_member": self.staff_member,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "duration_minutes": self.duration_minutes,
            "is_rescheduled": self.is_rescheduled,
            "original_appointment_id": self.original_appointment_id,
        }

    def __repr__(self):
        return f"<Appointment(id={self.id}, client_id={self.client_id}, date={self.appointment_date})>"