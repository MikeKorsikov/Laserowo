# --- config/database.py ---
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/database.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from models import client, appointment, service, expense
    Base.metadata.create_all(bind=engine)