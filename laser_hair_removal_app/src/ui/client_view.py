from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from src.backend.client_manager import ClientManager
import logging
from src.utils.config import Config

class ClientView(QWidget):
    """UI component for managing client data."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the client view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.client_manager = ClientManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.dob_input = QLineEdit(self)
        
        input_layout.addWidget(QLabel("Name:"))
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(QLabel("Phone:"))
        input_layout.addWidget(self.phone_input)
        input_layout.addWidget(QLabel("Email:"))
        input_layout.addWidget(self.email_input)
        input_layout.addWidget(QLabel("DOB (YYYY-MM-DD):"))
        input_layout.addWidget(self.dob_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Client", self)
        self.update_button = QPushButton("Update Client", self)
        self.refresh_button = QPushButton("Refresh", self)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.refresh_button)
        
        # Table for client list
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "DOB"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.add_button.clicked.connect(self.add_client)
        self.update_button.clicked.connect(self.update_client)
        self.refresh_button.clicked.connect(self.refresh_table)
        self.refresh_table()
    
    def add_client(self):
        """Add a new client based on input data."""
        try:
            client_id = self.client_manager.add_client(
                self.name_input.text(),
                self.phone_input.text(),
                self.email_input.text(),
                self.dob_input.text()
            )
            QMessageBox.information(self, "Success", f"Client added with ID {client_id}")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error adding client: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error adding client: {e}")
            QMessageBox.critical(self, "Error", "Failed to add client")
    
    def update_client(self):
        """Update the selected client's data."""
        try:
            selected = self.table.currentRow()
            if selected < 0:
                raise ValueError("Select a client to update")
            client_id = int(self.table.item(selected, 0).text())
            self.client_manager.update_client(
                client_id,
                self.name_input.text() or None,
                self.phone_input.text() or None,
                self.email_input.text() or None,
                self.dob_input.text() or None
            )
            QMessageBox.information(self, "Success", f"Client {client_id} updated")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error updating client: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error updating client: {e}")
            QMessageBox.critical(self, "Error", "Failed to update client")
    
    def refresh_table(self):
        """Refresh the client table with current data."""
        try:
            clients = self.client_manager.search_clients("")
            self.table.setRowCount(len(clients))
            for row, client in enumerate(clients):
                self.table.setItem(row, 0, QTableWidgetItem(str(client.client_id)))
                self.table.setItem(row, 1, QTableWidgetItem(client.full_name))
                self.table.setItem(row, 2, QTableWidgetItem(client.phone_number))
                self.table.setItem(row, 3, QTableWidgetItem(client.email or ""))
                self.table.setItem(row, 4, QTableWidgetItem(client.dob or ""))
            self.logger.info("Client table refreshed")
        except Exception as e:
            self.logger.error(f"Error refreshing client table: {e}")
            QMessageBox.critical(self, "Error", "Failed to refresh client list")
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.dob_input.clear()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = ClientView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Client Management")
    window.show()
    sys.exit(app.exec_())