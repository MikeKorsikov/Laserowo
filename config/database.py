# config/database.py
import os
import sys

# Add the parent directory (P1_DESKTOP_APP) to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import Base from base_model
from models.base_model import Base # <--- CHANGE THIS LINE: Import Base from base_model

# Import all your models here so Base.metadata knows about them
import models.appointment
import models.client
import models.digital_checklist
import models.expense
import models.expense_category
import models.hardware
import models.inventory
import models.operating_hour
import models.owner_reminder
import models.payment_method
import models.promotion
import models.service
import models.treatment_area
import models.user

DATABASE_URL = "sqlite:///./data/database.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    print(f"Database initialized at: {DATABASE_URL.replace('sqlite:///', '')}")
    Base.metadata.create_all(bind=engine) # Base is now from models.base_model

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()