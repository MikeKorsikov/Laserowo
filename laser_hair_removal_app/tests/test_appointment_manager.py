import unittest
from src.backend.appointment_manager import AppointmentManager
from src.backend.client_manager import ClientManager
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os
import shutil
from datetime import datetime

class TestAppointmentManager(unittest.TestCase):
    """Test cases for the AppointmentManager class."""
    
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
        self.manager = AppointmentManager(self.config_path, self.db_path)
        
        # Add a test client
        self.client_id = self.client_manager.add_client("Test Client", "1234567890", "test@example.com", "1990-01-01")
    
    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_schedule_appointment(self):
        """Test scheduling a new appointment."""
        appointment_id = self.manager.schedule_appointment(
            self.client_id, 1, 1, "2025-07-21", 1, 10.5, 50.0
        )
        self.assertGreater(appointment_id, 0)
        appointment = self.manager.get_appointment(appointment_id)
        self.assertEqual(appointment.client_id, self.client_id)
        self.assertEqual(appointment.appointment_date, "2025-07-21")
        self.assertEqual(appointment.session_number, 1)
        self.assertEqual(appointment.power, 10.5)
        self.assertEqual(appointment.amount, 50.0)
        self.assertEqual(appointment.appointment_status, "Scheduled")
    
    def test_reschedule_appointment(self):
        """Test rescheduling an existing appointment."""
        appointment_id = self.manager.schedule_appointment(
            self.client_id, 1, 1, "2025-07-21", 1, 10.5, 50.0
        )
        self.manager.reschedule_appointment(appointment_id, "2025-07-22")
        updated_appointment = self.manager.get_appointment(appointment_id)
        self.assertEqual(updated_appointment.appointment_date, "2025-07-22")
    
    def test_cancel_appointment(self):
        """Test cancelling an appointment."""
        appointment_id = self.manager.schedule_appointment(
            self.client_id, 1, 1, "2025-07-21", 1, 10.5, 50.0
        )
        self.manager.cancel_appointment(appointment_id)
        cancelled_appointment = self.manager.get_appointment(appointment_id)
        self.assertEqual(cancelled_appointment.appointment_status, "Cancelled")
    
    def test_get_appointments_by_date(self):
        """Test retrieving appointments by date."""
        self.manager.schedule_appointment(self.client_id, 1, 1, "2025-07-21", 1, 10.5, 50.0)
        appointments = self.manager.get_appointments_by_date("2025-07-21")
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0].appointment_date, "2025-07-21")

if __name__ == "__main__":
    unittest.main()