# models/base_model.py
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer

# Define Base ONCE here
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for BaseModel itself
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def to_dict(self):
        """Converts a model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
# reviewed