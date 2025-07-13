# models/appointment.py
from sqlalchemy import Column, Integer, String, Date, Time, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base # Assuming Base is defined here
from datetime import date, time # Import date and time for type hinting

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    area_id = Column(Integer, ForeignKey('treatment_areas.id'), nullable=True)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    session_number_for_area = Column(Integer, nullable=True)
    power_j_cm3 = Column(String, nullable=True) # Storing as string to handle "NA" or ranges
    appointment_status = Column(String, default="Scheduled") # e.g., "Scheduled", "Completed", "Cancelled"
    amount = Column(Float, nullable=True) # Payment amount for the service
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)
    promotion_id = Column(Integer, ForeignKey('promotions.id'), nullable=True) # Assuming a promotions table
    hardware_id = Column(Integer, ForeignKey('hardware.id'), nullable=True) # Assuming a hardware table
    notes = Column(String, nullable=True)
    next_suggested_appointment_date = Column(Date, nullable=True) # <--- ADD THIS LINE

    # Relationships
    client = relationship("Client", back_populates="appointments")
    service = relationship("Service")
    treatment_area = relationship("TreatmentArea")
    payment_method = relationship("PaymentMethod")
    # promotion = relationship("Promotion") # Uncomment if Promotion model is defined
    # hardware = relationship("Hardware") # Uncomment if Hardware model is defined

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "service_id": self.service_id,
            "area_id": self.area_id,
            "appointment_date": str(self.appointment_date) if self.appointment_date else None,
            "start_time": str(self.start_time) if self.start_time else None,
            "end_time": str(self.end_time) if self.end_time else None,
            "session_number_for_area": self.session_number_for_area,
            "power_j_cm3": self.power_j_cm3,
            "appointment_status": self.appointment_status,
            "amount": self.amount,
            "payment_method_id": self.payment_method_id,
            "promotion_id": self.promotion_id,
            "hardware_id": self.hardware_id,
            "notes": self.notes,
            "next_suggested_appointment_date": str(self.next_suggested_appointment_date) if self.next_suggested_appointment_date else None, # <--- INCLUDE IN TO_DICT
            # Include related object names for display in UI if available
            "client_name": self.client.full_name if self.client else "N/A",
            "service_name": self.service.name if self.service else "N/A",
            "area_name": self.treatment_area.name if self.treatment_area else "N/A",
            "payment_method_name": self.payment_method.name if self.payment_method else "N/A",
            # "promotion_name": self.promotion.name if self.promotion else "N/A",
            # "hardware_name": self.hardware.name if self.hardware else "N/A",
        }

    def __repr__(self):
        return f"<Appointment(id={self.id}, client_id={self.client_id}, date={self.appointment_date})>"

# updated