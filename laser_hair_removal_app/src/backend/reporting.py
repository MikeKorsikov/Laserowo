from src.database.db_operations import DatabaseOperations
from src.backend.finance_manager import FinanceManager
from src.backend.appointment_manager import AppointmentManager
import logging
from datetime import datetime, timedelta
from typing import Dict, List

class Reporting:
    """Manages report generation for the laser hair removal application."""
    
    def __init__(self, config_path: str, db_path: str):
        """Initialize with database configuration and path."""
        self.db = DatabaseOperations(config_path, db_path)
        self.finance_manager = FinanceManager(config_path, db_path)
        self.appointment_manager = AppointmentManager(config_path, db_path)
        self.logger = logging.getLogger(__name__)
    
    def generate_daily_report(self) -> Dict:
        """Generate a daily financial and appointment report for today."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            report = {
                'date': today,
                'revenue': self.finance_manager.get_revenue_by_date(today, today),
                'expenses': sum(exp.amount for exp in self.finance_manager.get_expenses_by_date(today, today)),
                'profit': self.finance_manager.get_profit_by_date(today, today),
                'appointments': len(self.appointment_manager.get_appointments_by_date(today))
            }
            self.logger.info(f"Generated daily report for {today}")
            return report
        except Exception as e:
            self.logger.error(f"Error generating daily report for {today}: {e}")
            raise
    
    def generate_weekly_report(self) -> Dict:
        """Generate a weekly financial and appointment report (last 7 days)."""
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            report = {
                'period': f"{start_date} to {end_date}",
                'revenue': self.finance_manager.get_revenue_by_date(start_date, end_date),
                'expenses': sum(exp.amount for exp in self.finance_manager.get_expenses_by_date(start_date, end_date)),
                'profit': self.finance_manager.get_profit_by_date(start_date, end_date),
                'appointments': sum(len(self.appointment_manager.get_appointments_by_date(
                    (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'))) for i in range(7))
            }
            self.logger.info(f"Generated weekly report for {start_date} to {end_date}")
            return report
        except Exception as e:
            self.logger.error(f"Error generating weekly report: {e}")
            raise
    
    def generate_client_activity_report(self, start_date: str, end_date: str) -> Dict:
        """Generate a report of client activity (appointments) between dates."""
        try:
            query = """
                SELECT c.full_name, COUNT(a.appointment_id) as appointment_count
                FROM clients c
                LEFT JOIN appointments a ON c.client_id = a.client_id
                WHERE a.appointment_date BETWEEN ? AND ? AND a.appointment_status = 'Completed'
                GROUP BY c.client_id, c.full_name
            """
            results = self.db.execute_query(query, (start_date, end_date))
            report = {'period': f"{start_date} to {end_date}", 'clients': results}
            self.logger.info(f"Generated client activity report for {start_date} to {end_date}")
            return report
        except Exception as e:
            self.logger.error(f"Error generating client activity report: {e}")
            raise
    
    def export_report_to_file(self, report: Dict, file_path: str) -> bool:
        """Export a report to a text file (simplified format)."""
        try:
            with open(file_path, 'w') as f:
                f.write(f"Report Date: {report.get('date', report.get('period', 'N/A'))}\n")
                f.write(f"Revenue: {report.get('revenue', 0.0)}\n")
                f.write(f"Expenses: {report.get('expenses', 0.0)}\n")
                f.write(f"Profit: {report.get('profit', 0.0)}\n")
                f.write(f"Appointments: {report.get('appointments', 0)}\n")
                if 'clients' in report:
                    f.write("Client Activity:\n")
                    for client in report['clients']:
                        f.write(f"- {client['full_name']}: {client['appointment_count']} appointments\n")
            self.logger.info(f"Exported report to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting report to {file_path}: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reporter = Reporting("config/secrets.yaml", "data/database.db")
    try:
        # Generate and export daily report
        daily_report = reporter.generate_daily_report()
        reporter.export_report_to_file(daily_report, "data/daily_report.txt")
        print(f"Daily report: {daily_report}")
        
        # Generate and export weekly report
        weekly_report = reporter.generate_weekly_report()
        reporter.export_report_to_file(weekly_report, "data/weekly_report.txt")
        print(f"Weekly report: {weekly_report}")
    except Exception as e:
        print(f"Error: {e}")