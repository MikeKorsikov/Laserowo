# models/expense.py
from sqlalchemy import String, DECIMAL, Date, Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel
from typing import Optional

class Expense(BaseModel):
    __tablename__ = 'expenses'

    expense_name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    expense_date: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_tax_deductible: Mapped[bool] = mapped_column(Boolean, default=False)

    payment_method_id: Mapped[int] = mapped_column(Integer, ForeignKey('payment_methods.id'), nullable=False)
    # This foreign key
    expense_category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('expense_categories.id'), nullable=True)

    # Relationships
    payment_method: Mapped["PaymentMethod"] = relationship("PaymentMethod", back_populates="expenses")
    # This relationship, explicitly referencing the class name as a string
    expense_category: Mapped[Optional["ExpenseCategory"]] = relationship("ExpenseCategory", back_populates="expenses")


    def __repr__(self):
        return (f"<Expense(id={self.id}, name='{self.expense_name}', "
                f"amount={self.amount}, date={self.expense_date})>")