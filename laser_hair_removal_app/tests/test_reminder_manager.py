import unittest
from src.backend.reminder_manager import ReminderManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil

class TestReminderManager(unittest.TestCase):
    """Test cases for the ReminderManager class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.config_path = f"{self.test_dir}/app_config.yaml"
        self.secrets_path = f"{self.test_dir}/secrets.yaml"
        self.db_path = f"{self.test_dir}/test_database.db"
        
        with open(self.config_path, 'w') as f:
            f.write("database:\n  db_path: test_database.db\n")
        with open(self.secrets_path, 'w') as f:
            f.write("database:\n  encryption_key: testkey12345678901234567890123456789012\n")
        
        self.db = DatabaseOperations(self.secrets_path, self.db_path)
        self.db.initialize_database()
        self.manager = ReminderManager(self.config_path, self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_add_reminder(self):
        """Test adding a new reminder."""
        reminder_id = self.manager.add_reminder("maintenance", 1, "2025-07-22")
        self.assertGreater(reminder_id, 0)
        reminder = self.manager.get_reminder(reminder_id)
        self.assertEqual(reminder[2], "maintenance")  # entity_type
        self.assertEqual(reminder[4], "2025-07-22")  # due_date
    
    def test_get_active_reminders(self):
        """Test retrieving active reminders."""
        self.manager.add_reminder("inventory", 1, "2025-07-22")
        reminders = self.manager.get_active_reminders("2025-07-22")
        self.assertEqual(len(reminders), 1)
        self.assertEqual(reminders[0][4], "2025-07-22")  # due_date
    
    def test_deactivate_reminder(self):
        """Test deactivating a reminder."""
        reminder_id = self.manager.add_reminder("expense", 1, "2025-07-22")
        self.manager.deactivate_reminder(reminder_id)
        reminder = self.manager.get_reminder(reminder_id)
        self.assertEqual(reminder[5], 0)  # is_active

if __name__ == "__main__":
    unittest.main()