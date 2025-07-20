from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, QComboBox, 
                            QMessageBox, QDateEdit)
from src.backend.appointment_manager import AppointmentManager
from src.backend.client_manager import ClientManager
from src.models.treatment_area import TreatmentArea
import logging
from src.utils.config import Config
from datetime import datetime

class AppointmentView(QWidget):
    """UI component for managing appointment data."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the appointment view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.appointment_manager = AppointmentManager(config_path, db_path)
        self.client_manager = ClientManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.areas = [TreatmentArea(1, "Legs"), TreatmentArea(2, "Bikini"), TreatmentArea(3, "Armpits")]  # Sample areas
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.client_id_input = QComboBox(self)
        self.date_input = QDateEdit(self)
        self.date_input.setDate(datetime.now())
        self.session_input = QLineEdit(self)
        self.power_input = QLineEdit(self)
        self.amount_input = QLineEdit(self)
        self.area_input = QComboBox(self)
        
        # Populate client dropdown
        clients = self.client_manager.search_clients("")
        self.client_id_input.addItem("Select Client", "")
        for client in clients:
            self.client_id_input.addItem(f"{client.full_name} (ID: {client.client_id})", client.client_id)
        
        # Populate area dropdown
        self.area_input.addItem("Select Area", 0)
        for area in self.areas:
            self.area_input.addItem(area.area_name, area.area_id)
        
        input_layout.addWidget(QLabel("Client:"))
        input_layout.addWidget(self.client_id_input)
        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(QLabel("Session #:"))
        input_layout.addWidget(self.session_input)
        input_layout.addWidget(QLabel("Power:"))
        input_layout.addWidget(self.power_input)
        input_layout.addWidget(QLabel("Amount:"))
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(QLabel("Area:"))
        input_layout.addWidget(self.area_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.schedule_button = QPushButton("Schedule", self)
        self.reschedule_button = QPushButton("Reschedule", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.refresh_button = QPushButton("Refresh", self)
        
        button_layout.addWidget(self.schedule_button)
        button_layout.addWidget(self.reschedule_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.refresh_button)
        
        # Table for appointment list
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Client", "Date", "Session #", "Power", "Amount", "Area", "Status"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.schedule_button.clicked.connect(self.schedule_appointment)
        self.reschedule_button.clicked.connect(self.reschedule_appointment)
        self.cancel_button.clicked.connect(self.cancel_appointment)
        self.refresh_button.clicked.connect(self.refresh_table)
        self.refresh_table()
    
    def schedule_appointment(self):
        """Schedule a new appointment based on input data."""
        try:
            client_id = self.client_id_input.currentData()
            area_id = self.area_input.currentData()
            if not client_id or not area_id:
                raise ValueError("Select a client and area")
            appointment_id = self.appointment_manager.schedule_appointment(
                client_id,
                1,  # Placeholder service_id
                area_id,
                self.date_input.date().toString("yyyy-MM-dd"),
                int(self.session_input.text() or 1),
                float(self.power_input.text()) if self.power_input.text() else None,
                float(self.amount_input.text()) if self.amount_input.text() else None
            )
            QMessageBox.information(self, "Success", f"Appointment scheduled with ID {appointment_id}")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error scheduling appointment: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error scheduling appointment: {e}")
            QMessageBox.critical(self, "Error", "Failed to schedule appointment")
    
    def reschedule_appointment(self):
        """Reschedule the selected appointment to a new date."""
        try:
            selected = self.table.currentRow()
            if selected < 0:
                raise ValueError("Select an appointment to reschedule")
            appointment_id = int(self.table.item(selected, 0).text())
            self.appointment_manager.reschedule_appointment(
                appointment_id,
                self.date_input.date().toString("yyyy-MM-dd")
            )
            QMessageBox.information(self, "Success", f"Appointment {appointment_id} rescheduled")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error rescheduling appointment: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error rescheduling appointment: {e}")
            QMessageBox.critical(self, "Error", "Failed to reschedule appointment")
    
    def cancel_appointment(self):
        """Cancel the selected appointment."""
        try:
            selected = self.table.currentRow()
            if selected < 0:
                raise ValueError("Select an appointment to cancel")
            appointment_id = int(self.table.item(selected, 0).text())
            self.appointment_manager.cancel_appointment(appointment_id)
            QMessageBox.information(self, "Success", f"Appointment {appointment_id} cancelled")
            self.refresh_table()
        except ValueError as e:
            self.logger.error(f"Validation error cancelling appointment: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error cancelling appointment: {e}")
            QMessageBox.critical(self, "Error", "Failed to cancel appointment")
    
    def refresh_table(self):
        """Refresh the appointment table with current data."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            appointments = self.appointment_manager.get_appointments_by_date(today)
            self.table.setRowCount(len(appointments))
            for row, appointment in enumerate(appointments):
                self.table.setItem(row, 0, QTableWidgetItem(str(appointment.appointment_id)))
                client = self.client_manager.get_client(appointment.client_id)
                self.table.setItem(row, 1, QTableWidgetItem(client.full_name if client else "Unknown"))
                self.table.setItem(row, 2, QTableWidgetItem(appointment.appointment_date))
                self.table.setItem(row, 3, QTableWidgetItem(str(appointment.session_number)))
                self.table.setItem(row, 4, QTableWidgetItem(str(appointment.power) if appointment.power else ""))
                self.table.setItem(row, 5, QTableWidgetItem(str(appointment.amount) if appointment.amount else ""))
                # Map area_id to area_name (simplified mapping based on self.areas)
                area_name = next((area.area_name for area in self.areas if area.area_id == appointment.area_id), "Unknown")
                self.table.setItem(row, 6, QTableWidgetItem(area_name))
                self.table.setItem(row, 7, QTableWidgetItem(appointment.appointment_status))
            self.logger.info("Appointment table refreshed")
        except Exception as e:
            self.logger.error(f"Error refreshing appointment table: {e}")
            QMessageBox.critical(self, "Error", "Failed to refresh appointment list")
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.client_id_input.setCurrentIndex(0)
        self.date_input.setDate(datetime.now())
        self.session_input.clear()
        self.power_input.clear()
        self.amount_input.clear()
        self.area_input.setCurrentIndex(0)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = AppointmentView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Appointment Management")
    window.show()
    sys.exit(app.exec_())