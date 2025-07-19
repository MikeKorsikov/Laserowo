from src.database.db_operations import DatabaseOperations
from src.models.reminder import Reminder
from src.utils.email_sender import EmailSender
from src.utils.sms_sender import SMSSender
import logging
from datetime import datetime, timedelta
from typing import Optional

class ReminderManager:
    """Manages reminder-related operations for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.email_sender = EmailSender(config_path)
        self.sms_sender = SMSSender(config_path)
    
    def schedule_reminder(self, reminder_type: str, related_id: int, due_date: str, 
                         message: str, delivery_method: str = 'Popup', reminder_date: str = None) -> int:
        """Schedule a new reminder and return the reminder_id."""
        try:
            if not reminder_date:
                # Default to 1 day before due date
                due = datetime.strptime(due_date, '%Y-%m-%d')
                reminder_date = (due - timedelta(days=1)).strftime('%Y-%m-%d')
            
            reminder = Reminder(0, reminder_type, related_id, due_date, reminder_date, message, delivery_method=delivery_method)
            query = """
                INSERT INTO owner_reminders (reminder_type, related_id, due_date, reminder_date, message, delivery_method)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (reminder.reminder_type, reminder.related_id, reminder.due_date, reminder.reminder_date, 
                      reminder.message, reminder.delivery_method)
            self.db.execute_query(query, params)
            reminder_id = self.db.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self.logger.info(f"Scheduled reminder {reminder_id} for {reminder_type}")
            return reminder_id
        except ValueError as e:
            self.logger.error(f"Validation error scheduling reminder for {reminder_type}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error scheduling reminder for {reminder_type}: {e}")
            raise
    
    def get_due_reminders(self) -> List[Reminder]:
        """Retrieve all active reminders that are due."""
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            query = """
                SELECT * FROM owner_reminders 
                WHERE reminder_date <= ? AND is_active = TRUE
            """
            results = self.db.execute_query(query, (current_date,))
            return [Reminder.from_dict(result) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving due reminders: {e}")
            raise
    
    def send_reminders(self) -> int:
        """Send notifications for due reminders and return the number sent."""
        try:
            due_reminders = self.get_due_reminders()
            count = 0
            for reminder in due_reminders:
                try:
                    if reminder.delivery_method == 'Email' and reminder.related_id:
                        client = self._get_client(reminder.related_id)  # Assume client retrieval
                        if client and client.email:
                            self.email_sender.send_email(client.email, "Reminder", reminder.message)
                            count += 1
                    elif reminder.delivery_method == 'SMS' and reminder.related_id:
                        client = self._get_client(reminder.related_id)
                        if client and client.phone_number:
                            self.sms_sender.send_sms(client.phone_number, reminder.message)
                            count += 1
                    elif reminder.delivery_method == 'Popup':
                        # Placeholder for UI popup (to be implemented in UI layer)
                        self.logger.info(f"Popup reminder: {reminder.message}")
                        count += 1
                    self._mark_as_sent(reminder.reminder_id)
                except Exception as e:
                    self.logger.error(f"Error sending reminder {reminder.reminder_id}: {e}")
            self.logger.info(f"Sent {count} reminders")
            return count
        except Exception as e:
            self.logger.error(f"Error processing reminders: {e}")
            raise
    
    def _get_client(self, client_id: int) -> Optional[dict]:
        """Helper method to retrieve client data (placeholder)."""
        try:
            query = "SELECT * FROM clients WHERE client_id = ?"
            results = self.db.execute_query(query, (client_id,))
            return results[0] if results else None
        except Exception as e:
            self.logger.error(f"Error retrieving client {client_id}: {e}")
            raise
    
    def _mark_as_sent(self, reminder_id: int) -> None:
        """Mark a reminder as inactive after sending."""
        try:
            query = "UPDATE owner_reminders SET is_active = FALSE WHERE reminder_id = ?"
            self.db.execute_query(query, (reminder_id,))
            self.logger.info(f"Marked reminder {reminder_id} as sent")
        except Exception as e:
            self.logger.error(f"Error marking reminder {reminder_id} as sent: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = ReminderManager("config/secrets.yaml", "data/database.db")
    try:
        # Schedule a reminder
        reminder_id = manager.schedule_reminder(
            "Maintenance", 1, "2025-07-26", "Maintenance due for laser machine"
        )
        print(f"Scheduled reminder ID: {reminder_id}")
        
        # Send due reminders
        sent_count = manager.send_reminders()
        print(f"Sent {sent_count} reminders")
    except Exception as e:
        print(f"Error: {e}")