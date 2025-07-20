from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, QComboBox, 
                            QMessageBox)
from src.backend.inventory_manager import InventoryManager
import logging
from src.utils.config import Config

class InventoryView(QWidget):
    """UI component for managing inventory data."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the inventory view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.inventory_manager = InventoryManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Input fields
        input_layout = QHBoxLayout()
        self.item_name_input = QLineEdit(self)
        self.quantity_input = QLineEdit(self)
        self.unit_input = QComboBox(self)
        self.threshold_input = QLineEdit(self)
        
        # Populate unit dropdown with common units
        self.unit_input.addItems(["ml", "g", "units"])
        
        input_layout.addWidget(QLabel("Item Name:"))
        input_layout.addWidget(self.item_name_input)
        input_layout.addWidget(QLabel("Quantity:"))
        input_layout.addWidget(self.quantity_input)
        input_layout.addWidget(QLabel("Unit:"))
        input_layout.addWidget(self.unit_input)
        input_layout.addWidget(QLabel("Low Stock Threshold:"))
        input_layout.addWidget(self.threshold_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item", self)
        self.update_button = QPushButton("Update Quantity", self)
        self.refresh_button = QPushButton("Refresh", self)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.refresh_button)
        
        # Table for inventory list
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Item Name", "Quantity", "Unit", "Threshold"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.add_button.clicked.connect(self.add_item)
        self.update_button.clicked.connect(self.update_quantity)
        self.refresh_button.clicked.connect(self.refresh_table)
        self.refresh_table()
    
    def add_item(self):
        """Add a new inventory item based on input data."""
        try:
            item_id = self.inventory_manager.add_item(
                self.item_name_input.text(),
                float(self.quantity_input.text()) if self.quantity_input.text() else 0.0,
                self.unit_input.currentText(),
                float(self.threshold_input.text()) if self.threshold_input.text() else 10.0
            )
            QMessageBox.information(self, "Success", f"Item added with ID {item_id}")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error adding item: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error adding item: {e}")
            QMessageBox.critical(self, "Error", "Failed to add item")
    
    def update_quantity(self):
        """Update the quantity of the selected inventory item."""
        try:
            selected = self.table.currentRow()
            if selected < 0:
                raise ValueError("Select an item to update")
            item_id = int(self.table.item(selected, 0).text())
            self.inventory_manager.update_quantity(
                item_id,
                float(self.quantity_input.text()) if self.quantity_input.text() else 0.0
            )
            QMessageBox.information(self, "Success", f"Quantity updated for item {item_id}")
            self.refresh_table()
            self.clear_inputs()
        except ValueError as e:
            self.logger.error(f"Validation error updating quantity: {e}")
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.logger.error(f"Error updating quantity: {e}")
            QMessageBox.critical(self, "Error", "Failed to update quantity")
    
    def refresh_table(self):
        """Refresh the inventory table with current data."""
        try:
            items = self.inventory_manager.get_all_inventory()
            self.table.setRowCount(len(items))
            for row, item in enumerate(items):
                self.table.setItem(row, 0, QTableWidgetItem(str(item.item_id)))
                self.table.setItem(row, 1, QTableWidgetItem(item.item_name))
                self.table.setItem(row, 2, QTableWidgetItem(f"{item.current_quantity:.2f}"))
                self.table.setItem(row, 3, QTableWidgetItem(item.unit))
                self.table.setItem(row, 4, QTableWidgetItem(f"{item.low_stock_threshold:.2f}"))
            self.logger.info("Inventory table refreshed")
        except Exception as e:
            self.logger.error(f"Error refreshing inventory table: {e}")
            QMessageBox.critical(self, "Error", "Failed to refresh inventory list")
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.item_name_input.clear()
        self.quantity_input.clear()
        self.unit_input.setCurrentIndex(0)
        self.threshold_input.clear()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = InventoryView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Inventory Management")
    window.show()
    sys.exit(app.exec_())