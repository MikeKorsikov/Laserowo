import sys
import os
import logging
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox, QApplication)
from src.ui.client_view import ClientView
from src.ui.appointment_view import AppointmentView
from src.ui.finance_view import FinanceView
from src.ui.inventory_view import InventoryView
from src.ui.hardware_view import HardwareView
from src.ui.report_view import ReportView
from src.utils.config import Config
from src.utils.logger import Logger
from src.database.db_operations import DatabaseOperations
from src.backend.reporting import Reporting

class MainWindow(QMainWindow):
    """Main application window with tabbed navigation."""
    
    def __init__(self, config_path: str, secrets_path: str, db_path: str):
        """Initialize the main window with configuration and database paths."""
        super().__init__()
        self.config = Config(config_path, secrets_path)
        self.logger = Logger().get_logger(__name__)
        self.db = DatabaseOperations(secrets_path, db_path)
        self.reporting = Reporting(config_path, secrets_path, db_path)
        self.init_ui()

    def init_ui(self):
        """Set up the user interface."""
        self.setWindowTitle(self.config.get('ui.window_title', 'Laser Hair Removal App'))
        self.setGeometry(100, 100, 800, 600)

        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize views
        self.client_view = ClientView(self.config, self.db)
        self.appointment_view = AppointmentView(self.config, self.db)
        self.finance_view = FinanceView(self.config, self.db)
        self.inventory_view = InventoryView(self.config, self.db)
        self.hardware_view = HardwareView(self.config, self.db)
        self.report_view = ReportView(self.config, self.reporting)

        # Add tabs
        self.tabs.addTab(self.client_view, "Clients")
        self.tabs.addTab(self.appointment_view, "Appointments")
        self.tabs.addTab(self.finance_view, "Finance")
        self.tabs.addTab(self.inventory_view, "Inventory")
        self.tabs.addTab(self.hardware_view, "Hardware")
        self.tabs.addTab(self.report_view, "Reports")

        # Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # Backup action
        backup_action = QAction('Backup Database', self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

        # Export Reports action
        export_action = QAction('Export Reports', self)
        export_action.triggered.connect(self.export_reports)
        file_menu.addAction(export_action)

        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.logger.info("Main window initialized")
        self.show()

    def backup_database(self):
        """Create a backup of the database."""
        backup_path, _ = QFileDialog.getSaveFileName(self, "Save Database Backup", "", "SQLite Database (*.db)")
        if backup_path:
            try:
                with open(backup_path, 'wb') as backup_file:
                    with open(self.db.db_path, 'rb') as db_file:
                        backup_file.write(db_file.read())
                QMessageBox.information(self, "Success", f"Database backed up to {backup_path}")
                self.logger.info("Database backed up to %s", backup_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to backup database: {str(e)}")
                self.logger.error("Backup failed: %s", str(e))

    def export_reports(self):
        """Export all reports to a directory."""
        export_dir = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if export_dir:
            try:
                current_date = datetime.now().strftime('%Y-%m-%d')
                reports = {
                    "revenue": self.reporting.get_revenue_report("2025-07-01", current_date),
                    "expense": self.reporting.get_expense_report("2025-07-01", current_date),
                    "inventory": self.reporting.get_inventory_report(),
                    "hardware": self.reporting.get_hardware_report(),
                    "reminders": self.reporting.get_reminder_report(current_date)
                }
                for report_type, report_data in reports.items():
                    file_path = os.path.join(export_dir, f"{report_type}_report_{current_date}.txt")
                    with open(file_path, 'w') as f:
                        f.write(str(report_data))
                    self.logger.info("Exported %s report to %s", report_type, file_path)
                QMessageBox.information(self, "Success", f"Reports exported to {export_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export reports: {str(e)}")
                self.logger.error("Export failed: %s", str(e))

    def closeEvent(self, event):
        """Handle window close event."""
        self.db.close_connection()
        self.logger.info("Application closed")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("config/app_config.yaml", "config/secrets.yaml", "data/database.db")
    sys.exit(app.exec_())