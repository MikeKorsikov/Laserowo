# models/appointment.py
from sqlalchemy import Integer, String, Date, Time, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class Appointment(BaseModel):
    __tablename__ = 'appointments'

    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey('services.id'), nullable=True)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey('treatment_areas.id'), nullable=True)
    appointment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    session_number_for_area: Mapped[int] = mapped_column(Integer, nullable=True)
    power_j_cm3: Mapped[str] = mapped_column(String(50), nullable=True) # Storing as string for flexibility (e.g., "10J/cm3")
    appointment_status: Mapped[str] = mapped_column(String(50), default='Scheduled') # e.g., 'Scheduled', 'Completed', 'Cancelled', 'Rescheduled'
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=True)
    payment_method_id: Mapped[int] = mapped_column(Integer, ForeignKey('payment_methods.id'), nullable=True)
    next_suggested_appointment_date: Mapped[Date] = mapped_column(Date, nullable=True)
    promotion_id: Mapped[int] = mapped_column(Integer, ForeignKey('promotions.id'), nullable=True)
    hardware_id: Mapped[int] = mapped_column(Integer, ForeignKey('hardware.id'), nullable=True) # Link to hardware used

    # Relationships
    client: Mapped["Client"] = relationship(back_populates="appointments")
    service: Mapped["Service"] = relationship(back_populates="appointments")
    treatment_area: Mapped["TreatmentArea"] = relationship(back_populates="appointments")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="appointments")
    promotion: Mapped["Promotion"] = relationship(back_populates="appointments")
    hardware: Mapped["Hardware"] = relationship(back_populates="appointments")

    def __repr__(self):
        return (f"<Appointment(id={self.id}, client_id={self.client_id}, "
                f"date={self.appointment_date}, time={self.start_time}-{self.end_time}, "
                f"status='{self.appointment_status}')>")