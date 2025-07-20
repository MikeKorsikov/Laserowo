import unittest
from src.backend.finance_manager import FinanceManager
from src.backend.appointment_manager import AppointmentManager
from src.backend.client_manager import ClientManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil
from datetime import datetime

class TestFinanceManager(unittest.TestCase):
    """Test cases for the FinanceManager class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Use a temporary directory for testing
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_path = f"{self.test_dir}/app_config.yaml"
        self.secrets_path = f"{self.test_dir}/secrets.yaml"
        self.db_path = f"{self.test_dir}/test_database.db"
        
        # Create minimal config and secrets files
        with open(self.config_path, 'w') as f:
            f.write("database:\n  db_path: test_database.db\n")
        with open(self.secrets_path, 'w') as f:
            f.write("database:\n  encryption_key: testkey12345678901234567890123456789012\n")
        
        # Initialize database
        self.db = DatabaseOperations(self.secrets_path, self.db_path)
        self.db.initialize_database()
        self.client_manager = ClientManager(self.config_path, self.db_path)
        self.appointment_manager = AppointmentManager(self.config_path, self.db_path)
        self.manager = FinanceManager(self.config_path, self.db_path)
        
        # Add a test client and appointment
        self.client_id = self.client_manager.add_client("Test Client", "1234567890", "test@example.com", "1990-01-01")
        self.appointment_id = self.appointment_manager.schedule_appointment(
            self.client_id, 1, 1, "2025-07-20", 1, 10.5, 100.0
        )
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_revenue_by_date(self):
        """Test retrieving revenue for a specific date."""
        revenue = self.manager.get_revenue_by_date("2025-07-20", "2025-07-20")
        self.assertEqual(revenue, 100.0)
    
    def test_get_expenses_by_date(self):
        """Test retrieving expenses for a specific date (placeholder as no expenses added)."""
        expenses = self.manager.get_expenses_by_date("2025-07-20", "2025-07-20")
        self.assertEqual(len(expenses), 0)  # No expenses added yet
        # Simulate adding an expense (assuming add_expense method exists)
        self.manager.add_expense("Supplies", 20.0, "2025-07-20")
        expenses = self.manager.get_expenses_by_date("2025-07-20", "2025-07-20")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].amount, 20.0)
    
    def test_get_profit_by_date(self):
        """Test calculating profit for a specific date."""
        self.manager.add_expense("Supplies", 20.0, "2025-07-20")
        profit = self.manager.get_profit_by_date("2025-07-20", "2025-07-20")
        self.assertEqual(profit, 80.0)  # 100.0 revenue - 20.0 expense
    
    def test_get_client_activity_report(self):
        """Test generating a client activity report."""
        self.appointment_manager.schedule_appointment(
            self.client_id, 1, 1, "2025-07-20", 2, 10.5, 100.0
        )
        report = self.manager.get_client_activity_report("2025-07-20", "2025-07-20")
        self.assertEqual(len(report['clients']), 1)
        self.assertEqual(report['clients'][0]['full_name'], "Test Client")
        self.assertEqual(report['clients'][0]['appointment_count'], 2)

if __name__ == "__main__":
    unittest.main()