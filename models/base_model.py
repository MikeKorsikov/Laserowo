# models/base_model.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer
from config.database import Base

class BaseModel(Base):
    __abstract__ = True # This tells SQLAlchemy not to create a table for BaseModel

    # Every model will have an auto-incrementing integer ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        # Generic representation for easy debugging
        attrs = ', '.join(f"{c.name}={getattr(self, c.name)!r}" for c in self.__table__.columns if c.name != 'id')
        return f"<{self.__class__.__name__}(id={self.id!r}, {attrs})>"

    def to_dict(self):
        """Converts the model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}