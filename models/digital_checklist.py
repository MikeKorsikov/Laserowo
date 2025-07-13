# D:\PYTHON\Laserowo\P1_desktop_app\models\digital_checklist.py

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class DigitalChecklist(Base):
    __tablename__ = 'digital_checklists'

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False) # Foreign key to clients table
    date_filled = Column(Date, default=datetime.now().date(), nullable=False)
    consent_given = Column(Boolean, default=False)
    skin_type_assessed = Column(Boolean, default=False)
    contraindications_checked = Column(Boolean, default=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # This is the singular relationship that `Client.digital_checklists` back-populates
    client = relationship("Client", back_populates="digital_checklists") # <-- THIS IS CORRECT (singular 'client')

    def __repr__(self):
        return f"<DigitalChecklist(id={self.id}, client_id={self.client_id}, date={self.date_filled})>"
    

#reviewed 