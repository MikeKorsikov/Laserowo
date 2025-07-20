from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QAction, QFileDialog, QMessageBox)
from src.ui.client_view import ClientView
from src.ui.appointment_view import AppointmentView
from src.ui.finance_view import FinanceView
from src.ui.inventory_view import InventoryView
from src.ui.hardware_view import HardwareView
from src.ui.report_view import ReportView
import logging
from src.utils.config import Config
from datetime import datetime

class MainWindow(QMainWindow):
    """Main application window integrating all views."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize the main window with configuration and database paths."""
        super().__init__()
        self.config = Config(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Set up the main window layout and components."""
        # Set window properties
        self.setWindowTitle(self.config.get('ui.window_title', 'Laser Hair Removal Manager'))
        self.setGeometry(100, 100, 900, 700)
        
        # Create tab widget
        self.tabs = QTabWidget(self)
        
        # Initialize views
        self.client_view = ClientView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                    self.config.get('paths.data_dir') + '/database.db', self)
        self.appointment_view = AppointmentView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                              self.config.get('paths.data_dir') + '/database.db', self)
        self.finance_view = FinanceView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                      self.config.get('paths.data_dir') + '/database.db', self)
        self.inventory_view = InventoryView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                          self.config.get('paths.data_dir') + '/database.db', self)
        self.hardware_view = HardwareView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                        self.config.get('paths.data_dir') + '/database.db', self)
        self.report_view = ReportView(self.config.get('paths.config_dir') + '/app_config.yaml', 
                                    self.config.get('paths.data_dir') + '/database.db', self)
        
        # Add tabs
        self.tabs.addTab(self.client_view, "Clients")
        self.tabs.addTab(self.appointment_view, "Appointments")
        self.tabs.addTab(self.finance_view, "Finance")
        self.tabs.addTab(self.inventory_view, "Inventory")
        self.tabs.addTab(self.hardware_view, "Hardware")
        self.tabs.addTab(self.report_view, "Reports")
        
        # Set central widget
        self.setCentralWidget(self.tabs)
        
        # Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        # Backup action
        backup_action = QAction('Backup Database', self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        self.logger.info("Main window initialized at %s", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    def backup_database(self):
        """Create a backup of the database file."""
        try:
            db_path = self.config.get('paths.data_dir') + '/database.db'
            backup_path, _ = QFileDialog.getSaveFileName(self, "Save Database Backup", 
                                                       f"data/backup_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                                                       "Database Files (*.db)")
            if backup_path:
                with open(db_path, 'rb') as source, open(backup_path, 'wb') as target:
                    target.write(source.read())
                QMessageBox.information(self, "Success", f"Database backed up to {backup_path}")
                self.logger.info(f"Database backed up to {backup_path}")
        except Exception as e:
            self.logger.error(f"Error backing up database: {e}")
            QMessageBox.critical(self, "Error", "Failed to backup database")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow("config/app_config.yaml", "data/database.db")
    window.show()
    sys.exit(app.exec_())