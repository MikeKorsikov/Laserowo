# --- models/expense.py ---
from sqlalchemy import Column, Integer, String, Float, DateTime
from config.database import Base
import datetime

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.datetime.utcnow)