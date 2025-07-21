import logging
from pysqlcipher3 import dbapi2 as sqlite3
from src.utils.config import Config
from src.utils.logger import Logger
import os

class DatabaseOperations:
    """Handles CRUD operations for the encrypted SQLite database."""
    
    def __init__(self, secrets_path: str, db_path: str):
        """Initialize with secrets and database paths."""
        self.config = Config("config/app_config.yaml", secrets_path)
        self.db_path = db_path
        self.logger = Logger().get_logger(__name__)
        self.encryption_key = self.config.get('database.encryption_key', 'default_key')
        self._ensure_connection()

    def _ensure_connection(self):
        """Ensure a valid database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute(f"PRAGMA key = '{self.encryption_key}'")
            self.logger.info("Database connection established at %s", self.db_path)
        except sqlite3.Error as e:
            self.logger.error("Failed to connect to database: %s", str(e))
            raise

    def get_connection(self):
        """Return the database connection."""
        if not hasattr(self, 'conn') or self.conn is None:
            self._ensure_connection()
        return self.conn

    def close_connection(self):
        """Close the database connection."""
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()
            self.logger.info("Database connection closed")
            self.conn = None

    # Client CRUD Operations
    def add_client(self, full_name: str, phone_number: str, email: str, dob: str) -> int:
        """Add a new client and return the client_id."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "INSERT INTO clients (full_name, phone_number, email, dob) VALUES (?, ?, ?, ?)",
                (full_name, phone_number, email, dob)
            )
            self.conn.commit()
            client_id = cursor.lastrowid
            self.logger.info("Added client %s with ID %d", full_name, client_id)
            return client_id
        except sqlite3.Error as e:
            self.logger.error("Error adding client: %s", str(e))
            raise

    def get_client(self, client_id: int):
        """Retrieve a client by ID."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error("Error retrieving client %d: %s", client_id, str(e))
            raise

    def update_client(self, client_id: int, full_name: str, phone_number: str, email: str, dob: str):
        """Update client details."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "UPDATE clients SET full_name = ?, phone_number = ?, email = ?, dob = ? WHERE client_id = ?",
                (full_name, phone_number, email, dob, client_id)
            )
            self.conn.commit()
            self.logger.info("Updated client %d", client_id)
        except sqlite3.Error as e:
            self.logger.error("Error updating client %d: %s", client_id, str(e))
            raise

    def delete_client(self, client_id: int):
        """Delete a client by ID."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
            self.conn.commit()
            self.logger.info("Deleted client %d", client_id)
        except sqlite3.Error as e:
            self.logger.error("Error deleting client %d: %s", client_id, str(e))
            raise

    # Appointment CRUD Operations (similar pattern for other tables)
    def add_appointment(self, client_id: int, service_id: int, appointment_date: str, session_number: int, power: float, amount: float) -> int:
        """Add a new appointment and return the appointment_id."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "INSERT INTO appointments (client_id, service_id, appointment_date, session_number, power, amount) VALUES (?, ?, ?, ?, ?, ?)",
                (client_id, service_id, appointment_date, session_number, power, amount)
            )
            self.conn.commit()
            appointment_id = cursor.lastrowid
            self.logger.info("Added appointment for client %d with ID %d", client_id, appointment_id)
            return appointment_id
        except sqlite3.Error as e:
            self.logger.error("Error adding appointment: %s", str(e))
            raise

    def get_appointment(self, appointment_id: int):
        """Retrieve an appointment by ID."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("SELECT * FROM appointments WHERE appointment_id = ?", (appointment_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error("Error retrieving appointment %d: %s", appointment_id, str(e))
            raise

    def update_appointment(self, appointment_id: int, client_id: int, service_id: int, appointment_date: str, session_number: int, power: float, amount: float, status: str):
        """Update appointment details."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "UPDATE appointments SET client_id = ?, service_id = ?, appointment_date = ?, session_number = ?, power = ?, amount = ?, appointment_status = ? WHERE appointment_id = ?",
                (client_id, service_id, appointment_date, session_number, power, amount, status, appointment_id)
            )
            self.conn.commit()
            self.logger.info("Updated appointment %d", appointment_id)
        except sqlite3.Error as e:
            self.logger.error("Error updating appointment %d: %s", appointment_id, str(e))
            raise

    def delete_appointment(self, appointment_id: int):
        """Delete an appointment by ID."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
            self.conn.commit()
            self.logger.info("Deleted appointment %d", appointment_id)
        except sqlite3.Error as e:
            self.logger.error("Error deleting appointment %d: %s", appointment_id, str(e))
            raise

    # Similar CRUD methods for services, expenses, inventory, hardware, reminders can be added here
    # Example for inventory
    def add_inventory_item(self, item_name: str, current_quantity: float, unit: str, low_stock_threshold: float) -> int:
        """Add a new inventory item and return the item_id."""
        try:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "INSERT INTO inventory (item_name, current_quantity, unit, low_stock_threshold) VALUES (?, ?, ?, ?)",
                (item_name, current_quantity, unit, low_stock_threshold)
            )
            self.conn.commit()
            item_id = cursor.lastrowid
            self.logger.info("Added inventory item %s with ID %d", item_name, item_id)
            return item_id
        except sqlite3.Error as e:
            self.logger.error("Error adding inventory item: %s", str(e))
            raise

    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close_connection()

if __name__ == "__main__":
    db = DatabaseOperations("config/secrets.yaml", "data/database.db")
    # Example usage
    client_id = db.add_client("Test User", "1234567890", "test@example.com", "1990-01-01")
    print(f"Added client with ID: {client_id}")
    db.close_connection()