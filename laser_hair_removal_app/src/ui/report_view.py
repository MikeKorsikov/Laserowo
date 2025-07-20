from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit, 
                            QComboBox)
from src.backend.reporting import Reporting
import logging
from src.utils.config import Config
from datetime import datetime

class ReportView(QWidget):
    """UI component for generating and viewing detailed reports."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the report view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.reporting = Reporting(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Date range and report type selection
        control_layout = QHBoxLayout()
        self.start_date_input = QDateEdit(self)
        self.end_date_input = QDateEdit(self)
        self.report_type_input = QComboBox(self)
        
        self.start_date_input.setDate(datetime(2025, 7, 13))  # Start of month
        self.end_date_input.setDate(datetime.now())
        
        self.report_type_input.addItems(["Financial", "Client Activity", "Inventory"])
        
        control_layout.addWidget(QLabel("Start Date:"))
        control_layout.addWidget(self.start_date_input)
        control_layout.addWidget(QLabel("End Date:"))
        control_layout.addWidget(self.end_date_input)
        control_layout.addWidget(QLabel("Report Type:"))
        control_layout.addWidget(self.report_type_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate Report", self)
        self.export_button = QPushButton("Export Report", self)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.export_button)
        
        # Table for report data
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Detail", "Value 1", "Value 2", "Value 3"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(control_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.generate_button.clicked.connect(self.generate_report)
        self.export_button.clicked.connect(self.export_report)
        self.generate_report()
    
    def generate_report(self):
        """Generate and display the selected report type."""
        try:
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            report_type = self.report_type_input.currentText()
            
            if report_type == "Financial":
                report = self.reporting.generate_daily_report() if start_date == end_date else \
                         self.reporting.generate_weekly_report() if (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days <= 7 else \
                         {"period": f"{start_date} to {end_date}", "revenue": 0.0, "expenses": 0.0, "profit": 0.0, "appointments": 0}
                self.update_table([
                    ("Period", report.get('date', report.get('period', '')), "", ""),
                    ("Revenue", f"${report.get('revenue', 0.0):.2f}", "", ""),
                    ("Expenses", f"${report.get('expenses', 0.0):.2f}", "", ""),
                    ("Profit", f"${report.get('profit', 0.0):.2f}", "", ""),
                    ("Appointments", str(report.get('appointments', 0)), "", "")
                ])
            elif report_type == "Client Activity":
                report = self.reporting.generate_client_activity_report(start_date, end_date)
                self.update_table([(f"{row['full_name']}", str(row['appointment_count']), "", "") 
                                 for row in report['clients']])
            elif report_type == "Inventory":
                # Placeholder for inventory report (assume low stock items)
                items = [("Item Name", "Quantity", "Threshold", "")]  # To be implemented in InventoryManager
                self.update_table(items)
            
            self.logger.info(f"Generated {report_type.lower()} report for {start_date} to {end_date}")
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            QMessageBox.critical(self, "Error", "Failed to generate report")
    
    def update_table(self, data: list):
        """Update the table with the provided report data."""
        self.table.setRowCount(len(data))
        for row, (detail, value1, value2, value3) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(detail)))
            self.table.setItem(row, 1, QTableWidgetItem(str(value1)))
            self.table.setItem(row, 2, QTableWidgetItem(str(value2)))
            self.table.setItem(row, 3, QTableWidgetItem(str(value3)))
    
    def export_report(self):
        """Export the current table data to a text file."""
        try:
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            report_type = self.report_type_input.currentText()
            file_path = f"data/{report_type.lower().replace(' ', '_')}_report_{start_date}_to_{end_date}.txt"
            with open(file_path, 'w') as f:
                f.write(f"{report_type} Report: {start_date} to {end_date}\n")
                for row in range(self.table.rowCount()):
                    items = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                    f.write(f"{' | '.join(items)}\n")
            QMessageBox.information(self, "Success", f"Report exported to {file_path}")
            self.logger.info(f"Exported {report_type.lower()} report to {file_path}")
        except Exception as e:
            self.logger.error(f"Error exporting report: {e}")
            QMessageBox.critical(self, "Error", "Failed to export report")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = ReportView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Report Management")
    window.show()
    sys.exit(app.exec_())