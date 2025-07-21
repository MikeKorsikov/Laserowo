import logging
from src.database.db_operations import DatabaseOperations
from src.utils.config import Config
from src.utils.logger import Logger
from src.backend.client_manager import ClientManager
from src.backend.appointment_manager import AppointmentManager
from src.backend.finance_manager import FinanceManager
from src.backend.inventory_manager import InventoryManager
from src.backend.hardware_manager import HardwareManager
from src.backend.reminder_manager import ReminderManager
from datetime import datetime

class Reporting:
    """Generates various reports for the laser hair removal application."""
    
    def __init__(self, config_path: str, secrets_path: str, db_path: str):
        """Initialize with configuration and database paths."""
        self.config = Config(config_path, secrets_path)
        self.logger = Logger().get_logger(__name__)
        self.db = DatabaseOperations(secrets_path, db_path)
        self.client_manager = ClientManager(config_path, db_path)
        self.appointment_manager = AppointmentManager(config_path, db_path)
        self.finance_manager = FinanceManager(config_path, db_path)
        self.inventory_manager = InventoryManager(config_path, db_path)
        self.hardware_manager = HardwareManager(config_path, db_path)
        self.reminder_manager = ReminderManager(config_path, db_path)

    def get_revenue_report(self, start_date: str, end_date: str):
        """Generate a revenue report for a date range."""
        try:
            revenue = self.finance_manager.get_revenue_by_date(start_date, end_date)
            self.logger.info("Generated revenue report for %s to %s: $%.2f", start_date, end_date, revenue)
            return {"type": "revenue", "start_date": start_date, "end_date": end_date, "total": revenue}
        except Exception as e:
            self.logger.error("Error generating revenue report: %s", str(e))
            raise

    def get_expense_report(self, start_date: str, end_date: str):
        """Generate an expense report for a date range."""
        try:
            expenses = self.finance_manager.get_expenses_by_date(start_date, end_date)
            total_expenses = sum(exp.amount for exp in expenses) if expenses else 0.0
            self.logger.info("Generated expense report for %s to %s: $%.2f", start_date, end_date, total_expenses)
            return {"type": "expense", "start_date": start_date, "end_date": end_date, "total": total_expenses, "details": expenses}
        except Exception as e:
            self.logger.error("Error generating expense report: %s", str(e))
            raise

    def get_client_progress_report(self, client_id: int):
        """Generate a client progress report."""
        try:
            client = self.client_manager.get_client(client_id)
            if not client:
                raise ValueError(f"Client {client_id} not found")
            appointments = self.appointment_manager.get_appointments_by_client(client_id)
            sessions_completed = sum(1 for appt in appointments if appt[7] == 'Completed')  # appointment_status index
            self.logger.info("Generated client progress report for client %d: %d sessions", client_id, sessions_completed)
            return {"type": "client_progress", "client_id": client_id, "full_name": client[1], "sessions_completed": sessions_completed, "appointments": appointments}
        except Exception as e:
            self.logger.error("Error generating client progress report: %s", str(e))
            raise

    def get_inventory_report(self):
        """Generate an inventory report with low-stock alerts."""
        try:
            inventory_items = self.inventory_manager.get_all_inventory()
            low_stock_items = [item for item in inventory_items if item[2] <= item[4]]  # current_quantity vs low_stock_threshold
            self.logger.info("Generated inventory report with %d low-stock items", len(low_stock_items))
            return {"type": "inventory", "total_items": len(inventory_items), "low_stock_items": low_stock_items}
        except Exception as e:
            self.logger.error("Error generating inventory report: %s", str(e))
            raise

    def get_hardware_report(self):
        """Generate a hardware maintenance and insurance report."""
        try:
            hardware = self.hardware_manager.get_hardware_status()
            current_date = datetime.now().strftime('%Y-%m-%d')
            maintenance_due = hardware[3] <= current_date if hardware[3] else False  # next_maintenance_due_date
            insurance_due = hardware[5] <= current_date if hardware[5] else False  # next_insurance_date
            self.logger.info("Generated hardware report: maintenance due=%s, insurance due=%s", maintenance_due, insurance_due)
            return {"type": "hardware", "total_impulses": hardware[1], "maintenance_due": maintenance_due, "insurance_due": insurance_due}
        except Exception as e:
            self.logger.error("Error generating hardware report: %s", str(e))
            raise

    def get_reminder_report(self, due_date: str = None):
        """Generate a report of active reminders."""
        try:
            reminders = self.reminder_manager.get_active_reminders(due_date)
            self.logger.info("Generated reminder report for %s with %d reminders", due_date or "all", len(reminders))
            return {"type": "reminders", "due_date": due_date, "reminders": reminders}
        except Exception as e:
            self.logger.error("Error generating reminder report: %s", str(e))
            raise

if __name__ == "__main__":
    reporter = Reporting("config/app_config.yaml", "config/secrets.yaml", "data/database.db")
    try:
        print(reporter.get_revenue_report("2025-07-01", "2025-07-21"))
        print(reporter.get_inventory_report())
        print(reporter.get_hardware_report())
    except Exception as e:
        print(f"Report generation failed: {e}")