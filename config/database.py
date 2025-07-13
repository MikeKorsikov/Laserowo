# P1_desktop_app/config/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base # Corrected import

# Import all your model modules to ensure their table definitions are registered with Base.metadata
from models import client, appointment, service, treatment_area, payment_method

# --- Database Configuration ---
# Construct path relative to the project root
# Assumes config/database.py is in P1_desktop_app/config/
# And database.db should go into P1_desktop_app/data/

# Get the directory of the current script (database.py)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to P1_desktop_app, then into 'data'
data_dir = os.path.join(os.path.dirname(current_script_dir), 'data')
# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Define the full path to the database file
DB_FILE_PATH = os.path.join(data_dir, 'database.db')
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_FILE_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (or already exist).")

if __name__ == '__main__':
    init_db()

# reviewed