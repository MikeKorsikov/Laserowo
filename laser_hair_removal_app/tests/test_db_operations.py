import unittest
from src.database.db_operations import DatabaseOperations
import os
import shutil

class TestDatabaseOperations(unittest.TestCase):
    """Test cases for the DatabaseOperations class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Use a temporary directory for testing
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.secrets_path = f"{self.test_dir}/secrets.yaml"
        self.db_path = f"{self.test_dir}/test_database.db"
        
        # Create minimal secrets file
        with open(self.secrets_path, 'w') as f:
            f.write("database:\n  encryption_key: testkey12345678901234567890123456789012\n")
        
        # Initialize database
        self.db = DatabaseOperations(self.secrets_path, self.db_path)
        self.db.initialize_database()
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_initialize_database(self):
        """Test database initialization."""
        # Check if database file exists
        self.assertTrue(os.path.exists(self.db_path))
        # Verify basic tables are created (assuming schema includes clients table)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients';")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()
    
    def test_add_client(self):
        """Test adding a client to the database."""
        client_id = self.db.add_client("Test Client", "1234567890", "test@example.com", "1990-01-01")
        self.assertGreater(client_id, 0)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, phone_number, email, dob FROM clients WHERE client_id = ?", (client_id,))
        client = cursor.fetchone()
        self.assertEqual(client, ("Test Client", "1234567890", "test@example.com", "1990-01-01"))
        conn.close()
    
    def test_update_client(self):
        """Test updating a client in the database."""
        client_id = self.db.add_client("Old Name", "0987654321", "old@example.com", "1990-01-01")
        self.db.update_client(client_id, "New Name", "1112223333", "new@example.com", "1990-01-02")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, phone_number, email, dob FROM clients WHERE client_id = ?", (client_id,))
        client = cursor.fetchone()
        self.assertEqual(client, ("New Name", "1112223333", "new@example.com", "1990-01-02"))
        conn.close()
    
    def test_delete_client(self):
        """Test deleting a client from the database."""
        client_id = self.db.add_client("Delete Me", "5555555555", "delete@example.com", "1990-01-01")
        self.db.delete_client(client_id)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clients WHERE client_id = ?", (client_id,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)
        conn.close()

if __name__ == "__main__":
    unittest.main()