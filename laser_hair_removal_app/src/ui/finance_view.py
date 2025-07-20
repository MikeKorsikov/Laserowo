from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QMessageBox, QDateEdit)
from src.backend.finance_manager import FinanceManager
import logging
from src.utils.config import Config
from datetime import datetime

class FinanceView(QWidget):
    """UI component for managing financial data."""
    
    def __init__(self, config_path: str, db_path: str, parent=None):
        """Initialize the finance view with configuration and database paths."""
        super().__init__(parent)
        self.config = Config(config_path, db_path)
        self.finance_manager = FinanceManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI layout and components."""
        # Main layout
        layout = QVBoxLayout()
        
        # Date range for reports
        date_layout = QHBoxLayout()
        self.start_date_input = QDateEdit(self)
        self.end_date_input = QDateEdit(self)
        self.start_date_input.setDate(datetime.now())
        self.end_date_input.setDate(datetime.now())
        
        date_layout.addWidget(QLabel("Start Date:"))
        date_layout.addWidget(self.start_date_input)
        date_layout.addWidget(QLabel("End Date:"))
        date_layout.addWidget(self.end_date_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.daily_button = QPushButton("Daily Report", self)
        self.weekly_button = QPushButton("Weekly Report", self)
        self.client_button = QPushButton("Client Activity", self)
        self.export_button = QPushButton("Export Report", self)
        
        button_layout.addWidget(self.daily_button)
        button_layout.addWidget(self.weekly_button)
        button_layout.addWidget(self.client_button)
        button_layout.addWidget(self.export_button)
        
        # Financial summary labels
        summary_layout = QHBoxLayout()
        self.revenue_label = QLabel("Revenue: $0.00")
        self.expenses_label = QLabel("Expenses: $0.00")
        self.profit_label = QLabel("Profit: $0.00")
        self.appointments_label = QLabel("Appointments: 0")
        
        summary_layout.addWidget(self.revenue_label)
        summary_layout.addWidget(self.expenses_label)
        summary_layout.addWidget(self.profit_label)
        summary_layout.addWidget(self.appointments_label)
        
        # Table for detailed report
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Revenue", "Expenses", "Profit"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Add layouts
        layout.addLayout(date_layout)
        layout.addLayout(button_layout)
        layout.addLayout(summary_layout)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Connect buttons
        self.daily_button.clicked.connect(self.show_daily_report)
        self.weekly_button.clicked.connect(self.show_weekly_report)
        self.client_button.clicked.connect(self.show_client_activity)
        self.export_button.clicked.connect(self.export_report)
        self.show_daily_report()
    
    def show_daily_report(self):
        """Display the daily financial report."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            report = self.finance_manager.get_revenue_by_date(today, today), \
                     sum(exp.amount for exp in self.finance_manager.get_expenses_by_date(today, today)), \
                     self.finance_manager.get_profit_by_date(today, today), \
                     len(self.finance_manager.get_expenses_by_date(today, today))  # Placeholder for appointments
            self.update_summary(*report)
            self.update_table([(today, *report[:3])])
            self.logger.info(f"Displayed daily report for {today}")
        except Exception as e:
            self.logger.error(f"Error displaying daily report: {e}")
            QMessageBox.critical(self, "Error", "Failed to display daily report")
    
    def show_weekly_report(self):
        """Display the weekly financial report."""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            report = self.finance_manager.get_revenue_by_date(start_date, end_date), \
                     sum(exp.amount for exp in self.finance_manager.get_expenses_by_date(start_date, end_date)), \
                     self.finance_manager.get_profit_by_date(start_date, end_date), \
                     sum(len(self.finance_manager.get_expenses_by_date(start_date, end_date)))  # Placeholder
            self.update_summary(*report)
            self.update_table([(f"{start_date} to {end_date}", *report[:3])])
            self.logger.info(f"Displayed weekly report for {start_date} to {end_date}")
        except Exception as e:
            self.logger.error(f"Error displaying weekly report: {e}")
            QMessageBox.critical(self, "Error", "Failed to display weekly report")
    
    def show_client_activity(self):
        """Display the client activity report for the selected date range."""
        try:
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            report = self.finance_manager.get_client_activity_report(start_date, end_date)
            self.update_table([(f"{row['full_name']}: {row['appointment_count']}", "", "", "") 
                             for row in report['clients']])
            self.logger.info(f"Displayed client activity report for {start_date} to {end_date}")
        except Exception as e:
            self.logger.error(f"Error displaying client activity report: {e}")
            QMessageBox.critical(self, "Error", "Failed to display client activity report")
    
    def update_summary(self, revenue: float, expenses: float, profit: float, appointments: int):
        """Update the financial summary labels."""
        self.revenue_label.setText(f"Revenue: ${revenue:.2f}")
        self.expenses_label.setText(f"Expenses: ${expenses:.2f}")
        self.profit_label.setText(f"Profit: ${profit:.2f}")
        self.appointments_label.setText(f"Appointments: {appointments}")
    
    def update_table(self, data: list):
        """Update the table with the provided data."""
        self.table.setRowCount(len(data))
        for row, (date, revenue, expenses, profit) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(date)))
            self.table.setItem(row, 1, QTableWidgetItem(f"${revenue:.2f}" if revenue else ""))
            self.table.setItem(row, 2, QTableWidgetItem(f"${expenses:.2f}" if expenses else ""))
            self.table.setItem(row, 3, QTableWidgetItem(f"${profit:.2f}" if profit else ""))
    
    def export_report(self):
        """Export the current table data to a text file."""
        try:
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            file_path = f"data/finance_report_{start_date}_to_{end_date}.txt"
            with open(file_path, 'w') as f:
                f.write(f"Finance Report: {start_date} to {end_date}\n")
                f.write(f"Revenue: ${self.revenue_label.text().split('$')[1]}\n")
                f.write(f"Expenses: ${self.expenses_label.text().split('$')[1]}\n")
                f.write(f"Profit: ${self.profit_label.text().split('$')[1]}\n")
                f.write("Details:\n")
                for row in range(self.table.rowCount()):
                    items = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                    f.write(f"{' | '.join(items)}\n")
            QMessageBox.information(self, "Success", f"Report exported to {file_path}")
            self.logger.info(f"Exported report to {file_path}")
        except Exception as e:
            self.logger.error(f"Error exporting report: {e}")
            QMessageBox.critical(self, "Error", "Failed to export report")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = FinanceView("config/app_config.yaml", "data/database.db")
    window.setWindowTitle("Finance Management")
    window.show()
    sys.exit(app.exec_())