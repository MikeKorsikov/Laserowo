from src.database.db_operations import DatabaseOperations
from src.models.expense import Expense
import logging
from datetime import datetime
from typing import List, Optional

class FinanceManager:
    """Manages financial operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
    
    def record_sale(self, appointment_id: int, amount: float, payment_method_id: int) -> bool:
        """Record a sale linked to an appointment."""
        try:
            query = """
                UPDATE appointments SET amount = ?, payment_method_id = ? 
                WHERE appointment_id = ? AND appointment_status = 'Completed'
            """
            params = (amount, payment_method_id, appointment_id)
            result = self.db.execute_query(query, params)
            if result:
                self.logger.info(f"Recorded sale {amount} for appointment {appointment_id}")
                return True
            self.logger.warning(f"No sale recorded for appointment {appointment_id}")
            return False
        except Exception as e:
            self.logger.error(f"Error recording sale for appointment {appointment_id}: {e}")
            raise
    
    def add_expense(self, expense_date: str, amount: float, description: str = None, 
                    category_id: int = None) -> int:
        """Add a new expense and return the expense_id."""
        try:
            expense = Expense(0, expense_date, amount, description, category_id)
            query = """
                INSERT INTO expenses (expense_date, amount, description, category_id)
                VALUES (?, ?, ?, ?)
            """
            params = (expense.expense_date, expense.amount, expense.description, expense.category_id)
            self.db.execute_query(query, params)
            expense_id = self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self.logger.info(f"Added expense {amount} with ID {expense_id}")
            return expense_id
        except ValueError as e:
            self.logger.error(f"Validation error adding expense: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error adding expense: {e}")
            raise
    
    def get_expenses_by_date(self, start_date: str, end_date: str) -> List[Expense]:
        """Retrieve all expenses between start_date and end_date."""
        try:
            query = """
                SELECT * FROM expenses 
                WHERE expense_date BETWEEN ? AND ? 
                ORDER BY expense_date ASC
            """
            results = self.db.execute_query(query, (start_date, end_date))
            return [Expense.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving expenses between {start_date} and {end_date}: {e}")
            raise
    
    def get_revenue_by_date(self, start_date: str, end_date: str) -> float:
        """Calculate total revenue from completed appointments between dates."""
        try:
            query = """
                SELECT SUM(amount) as total_revenue 
                FROM appointments 
                WHERE appointment_date BETWEEN ? AND ? AND appointment_status = 'Completed'
            """
            results = self.db.execute_query(query, (start_date, end_date))
            return float(results[0].get('total_revenue', 0.0)) if results else 0.0
        except Exception as e:
            self.logger.error(f"Error calculating revenue between {start_date} and {end_date}: {e}")
            raise
    
    def get_profit_by_date(self, start_date: str, end_date: str) -> float:
        """Calculate profit as revenue minus expenses between dates."""
        try:
            revenue = self.get_revenue_by_date(start_date, end_date)
            expenses = sum(exp.amount for exp in self.get_expenses_by_date(start_date, end_date))
            profit = revenue - expenses
            self.logger.info(f"Calculated profit {profit} between {start_date} and {end_date}")
            return profit
        except Exception as e:
            self.logger.error(f"Error calculating profit between {start_date} and {end_date}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = FinanceManager("config/secrets.yaml", "data/database.db")
    try:
        # Record a sale
        success = manager.record_sale(1, 100.0, 1)
        print(f"Sale recorded: {success}")
        
        # Add an expense
        expense_id = manager.add_expense("2025-07-16", 50.0, "Supplies", 1)
        print(f"Added expense ID: {expense_id}")
        
        # Get revenue and profit for today
        today = datetime.now().strftime('%Y-%m-%d')
        revenue = manager.get_revenue_by_date(today, today)
        profit = manager.get_profit_by_date(today, today)
        print(f"Revenue today: {revenue}, Profit today: {profit}")
    except Exception as e:
        print(f"Error: {e}")