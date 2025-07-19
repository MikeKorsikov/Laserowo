from typing import Optional

class Expense:
    """Represents an expense with associated data and validation."""
    
    def __init__(self, expense_id: int, expense_date: str, amount: float, description: str = None, 
                 category_id: int = None):
        """Initialize an Expense instance with provided attributes."""
        self.expense_id = self._validate_expense_id(expense_id)
        self.expense_date = self._validate_date(expense_date)
        self.amount = self._validate_amount(amount)
        self.description = description
        self.category_id = self._validate_category_id(category_id) if category_id else None
    
    def _validate_expense_id(self, expense_id: int) -> int:
        """Validate expense_id is a positive integer."""
        if not isinstance(expense_id, int) or expense_id <= 0:
            raise ValueError("Expense ID must be a positive integer")
        return expense_id
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if not date_str or not isinstance(date_str, str):
            raise ValueError("Expense date is required")
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    def _validate_amount(self, amount: float) -> float:
        """Validate amount is a non-negative number."""
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a non-negative number")
        return float(amount)
    
    def _validate_category_id(self, category_id: int) -> int:
        """Validate category_id is a positive integer."""
        if not isinstance(category_id, int) or category_id <= 0:
            raise ValueError("Category ID must be a positive integer")
        return category_id
    
    def to_dict(self) -> dict:
        """Convert expense data to a dictionary for database storage or display."""
        return {
            'expense_id': self.expense_id,
            'expense_date': self.expense_date,
            'amount': self.amount,
            'description': self.description,
            'category_id': self.category_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create an Expense instance from a dictionary (e.g., database result)."""
        return cls(
            expense_id=data.get('expense_id'),
            expense_date=data.get('expense_date'),
            amount=data.get('amount', 0.0),
            description=data.get('description'),
            category_id=data.get('category_id')
        )

    def __str__(self) -> str:
        """Return a string representation of the expense."""
        return f"Expense {self.expense_id} on {self.expense_date} for {self.amount}"

if __name__ == "__main__":
    try:
        expense = Expense(
            expense_id=1,
            expense_date="2025-07-16",
            amount=50.00,
            description="Supplies purchase",
            category_id=1
        )
        print(expense)
        print(expense.to_dict())
    except ValueError as e:
        print(f"Validation error: {e}")