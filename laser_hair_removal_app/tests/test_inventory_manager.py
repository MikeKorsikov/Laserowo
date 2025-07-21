import unittest
from src.backend.inventory_manager import InventoryManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil

class TestInventoryManager(unittest.TestCase):
    """Test cases for the InventoryManager class."""
    
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
        self.manager = InventoryManager(self.config_path, self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_add_inventory_item(self):
        """Test adding a new inventory item."""
        item_id = self.manager.add_inventory_item("Laser Gel", 50.0, "liters", 10.0)
        self.assertGreater(item_id, 0)
        item = self.manager.get_inventory_item(item_id)
        self.assertEqual(item[1], "Laser Gel")  # item_name
        self.assertEqual(item[2], 50.0)  # current_quantity
    
    def test_check_low_stock(self):
        """Test checking low stock status."""
        self.manager.add_inventory_item("Razors", 5.0, "units", 10.0)
        low_stock_items = self.manager.get_low_stock_items()
        self.assertEqual(len(low_stock_items), 1)
        self.assertEqual(low_stock_items[0][1], "Razors")  # item_name
    
    def test_update_inventory_quantity(self):
        """Test updating inventory quantity."""
        item_id = self.manager.add_inventory_item("Wipes", 20.0, "packs", 5.0)
        self.manager.update_inventory_quantity(item_id, 15.0)
        item = self.manager.get_inventory_item(item_id)
        self.assertEqual(item[2], 15.0)  # current_quantity

if __name__ == "__main__":
    unittest.main()