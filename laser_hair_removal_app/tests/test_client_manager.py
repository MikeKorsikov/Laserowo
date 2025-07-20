import unittest
from src.backend.client_manager import ClientManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil

class TestClientManager(unittest.TestCase):
    """Test cases for the ClientManager class."""
    
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
        self.manager = ClientManager(self.config_path, self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_add_client(self):
        """Test adding a new client."""
        client_id = self.manager.add_client("John Doe", "1234567890", "john@example.com", "1990-01-01")
        self.assertGreater(client_id, 0)
        client = self.manager.get_client(client_id)
        self.assertEqual(client.full_name, "John Doe")
        self.assertEqual(client.phone_number, "1234567890")
        self.assertEqual(client.email, "john@example.com")
        self.assertEqual(client.dob, "1990-01-01")
    
    def test_update_client(self):
        """Test updating an existing client."""
        client_id = self.manager.add_client("Jane Doe", "0987654321", "jane@example.com", "1995-02-02")
        self.manager.update_client(client_id, "Jane Smith", "1112223333", "jane.smith@example.com", "1995-02-03")
        updated_client = self.manager.get_client(client_id)
        self.assertEqual(updated_client.full_name, "Jane Smith")
        self.assertEqual(updated_client.phone_number, "1112223333")
        self.assertEqual(updated_client.email, "jane.smith@example.com")
        self.assertEqual(updated_client.dob, "1995-02-03")
    
    def test_search_clients(self):
        """Test searching for clients."""
        self.manager.add_client("Alice Brown", "5555555555", "alice@example.com", "1985-03-03")
        self.manager.add_client("Bob Green", "6666666666", "bob@example.com", "1986-04-04")
        results = self.manager.search_clients("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Alice Brown")
    
    def test_delete_client(self):
        """Test deleting a client."""
        client_id = self.manager.add_client("Charlie Black", "7777777777", "charlie@example.com", "1987-05-05")
        self.manager.delete_client(client_id)
        client = self.manager.get_client(client_id)
        self.assertIsNone(client)

if __name__ == "__main__":
    unittest.main()