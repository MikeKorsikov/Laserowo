from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit)
from src.backend.hardware_manager import HardwareManager
import logging
from src.utils.config import Config
from datetime import datetime

class HardwareView(QWidget):
    """UI component for managing hardware data."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the hardware view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.hardware_manager = HardwareManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.hardware_id = 1  # Single laser ID
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.impulses_input = QLineEdit(self)
        self.last_maintenance_input = QDateEdit(self)
        self.next_maintenance_input = QDateEdit(self)
        self.last_insurance_input = QDateEdit(self)
        self.next_insurance_input = QDateEdit(self)
        
        # Set default dates to current date
        today = datetime.now()
        self.last_maintenance_input.setDate(today)
        self.next_maintenance_input.setDate(today)
        self.last_insurance_input.setDate(today)
        self.next_insurance_input.setDate(today)
        
        input_layout.addWidget(QLabel("Impulses Used:"))
        input_layout.addWidget(self.impulses_input)
        input_layout.addWidget(QLabel("Last Maintenance:"))
        input_layout.addWidget(self.last_maintenance_input)
        input_layout.addWidget(QLabel("Next Maintenance:"))
        input_layout.addWidget(self.next_maintenance_input)
        input_layout.addWidget(QLabel("Last Insurance:"))
        input_layout.addWidget(self.last_insurance_input)
        input_layout.addWidget(QLabel("Next Insurance:"))
        input_layout.addWidget(self.next_insurance_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.update_button = QPushButton("Update Status", self)
        self.refresh_button = QPushButton("Refresh", self)
        
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.refresh_button)
        
        # Table for hardware status
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Field", "Value"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.update_button.clicked.connect(self.update_hardware)
        self.refresh_button.clicked.connect(self.refresh_table)
        self.refresh_table()
    
    def update_hardware(self):
        """Update the hardware status based on input data."""
        try:
            self.hardware_manager.record_impulse(self.hardware_id, 
                                               int(self.impulses_input.text()) if self.impulses_input.text() else 0)
            self.hardware_manager.update_maintenance(self.hardware_id,
                                                   self.last_maintenance_input.date().toString("yyyy-MM-dd"),
                                                   self.next_maintenance_input.date().toString("yyyy-MM-dd"))
            self.hardware_manager.update_insurance(self.hardware_id,
                                                 self.last_insurance_input.date().toString("yyyy-MM-dd"),
                                                 self.next_insurance_input.date().toString("yyyy-MM-dd"))
            QMessageBox.information(self, "Success", "Hardware status updated")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error updating hardware: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error updating hardware: {e}")
            QMessageBox.critical(self, "Error", "Failed to update hardware status")
    
    def refresh_table(self):
        """Refresh the hardware table with current data."""
        try:
            hardware = self.hardware_manager.get_hardware(self.hardware_id)
            if hardware:
                self.table.setRowCount(5)
                self.table.setItem(0, 0, QTableWidgetItem("Impulses Recorded"))
                self.table.setItem(0, 1, QTableWidgetItem(str(hardware.total_impulses_recorded)))
                self.table.setItem(1, 0, QTableWidgetItem("Last Maintenance"))
                self.table.setItem(1, 1, QTableWidgetItem(hardware.last_maintenance_date or ""))
                self.table.setItem(2, 0, QTableWidgetItem("Next Maintenance"))
                self.table.setItem(2, 1, QTableWidgetItem(hardware.next_maintenance_due_date or ""))
                self.table.setItem(3, 0, QTableWidgetItem("Last Insurance"))
                self.table.setItem(3, 1, QTableWidgetItem(hardware.last_insurance_date or ""))
                self.table.setItem(4, 0, QTableWidgetItem("Next Insurance"))
                self.table.setItem(4, 1, QTableWidgetItem(hardware.next_insurance_date or ""))
                self.logger.info("Hardware table refreshed")
            else:
                self.logger.warning("No hardware found with ID 1")
                QMessageBox.warning(self, "Warning", "No hardware data available")
        except Exception as e:
            self.logger.error(f"Error refreshing hardware table: {e}")
            QMessageBox.critical(self, "Error", "Failed to refresh hardware status")
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.impulses_input.clear()
        self.last_maintenance_input.setDate(datetime.now())
        self.next_maintenance_input.setDate(datetime.now())
        self.last_insurance_input.setDate(datetime.now())
        self.next_insurance_input.setDate(datetime.now())

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = HardwareView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Hardware Management")
    window.show()
    sys.exit(app.exec_())