# config/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'data', 'database.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy Engine
# The echo=True argument will log all SQL statements, useful for debugging.
engine = create_engine(DATABASE_URL, echo=False)

# Base class for declarative models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database by creating all tables defined in Base.
    This should be called once when the application starts.
    """
    # Ensure the 'data' directory exists
    data_dir = os.path.join(os.path.dirname(BASE_DIR), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Import all models here so that Base knows about them before creating tables
    # This is important for SQLAlchemy to discover all models
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

    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DATABASE_PATH}")

def get_db():
    """
    Dependency to get a database session.
    Use this in your controllers to get a session, ensuring it's closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # This block allows you to run `python config/database.py`
    # to initialize the database directly for testing purposes.
    init_db()