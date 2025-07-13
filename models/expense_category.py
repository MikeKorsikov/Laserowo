# models/expense_category.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from typing import List

class ExpenseCategory(BaseModel):
    __tablename__ = 'expense_categories' # Ensure this matches the foreign key reference

    category_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="expense_category")

    def __repr__(self):
        return f"<ExpenseCategory(id={self.id}, name='{self.category_name}')>"