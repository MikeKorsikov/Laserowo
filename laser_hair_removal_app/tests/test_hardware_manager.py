import unittest
from src.backend.hardware_manager import HardwareManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil
from datetime import datetime

class TestHardwareManager(unittest.TestCase):
    """Test cases for the HardwareManager class."""
    
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
        self.manager = HardwareManager(self.config_path, self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialize_hardware(self):
        """Test initializing hardware record."""
        hardware_id = self.manager.initialize_hardware(0, "2025-07-01", "2025-12-01", "2025-07-01", "2025-12-01")
        self.assertEqual(hardware_id, 1)  # Assuming single hardware ID
        hardware = self.manager.get_hardware_status()
        self.assertEqual(hardware[1], 0)  # total_impulses_recorded
    
    def test_update_impulses(self):
        """Test updating total impulses recorded."""
        self.manager.initialize_hardware(0, "2025-07-01", "2025-12-01", "2025-07-01", "2025-12-01")
        self.manager.update_impulses(100)
        hardware = self.manager.get_hardware_status()
        self.assertEqual(hardware[1], 100)  # total_impulses_recorded
    
    def test_check_maintenance_due(self):
        """Test checking if maintenance is due."""
        self.manager.initialize_hardware(0, "2025-07-01", "2025-07-22", "2025-07-01", "2025-12-01")
        due = self.manager.is_maintenance_due()
        self.assertTrue(due)  # Due date is tomorrow

if __name__ == "__main__":
    unittest.main()