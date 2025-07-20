from src.ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import logging
from src.utils.logger import Logger
from src.utils.config import Config
from src.database.db_operations import DatabaseOperations
import os

def main():
    """Main entry point for the laser hair removal application."""
    # Initialize logging
    logger = Logger().get_logger()
    
    # Load configuration
    config_path = "config/app_config.yaml"
    secrets_path = "config/secrets.yaml"
    config = Config(config_path, secrets_path)
    
    # Ensure data directory exists
    data_dir = config.get('paths.data_dir', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Initialize database
    db_path = f"{data_dir}/database.db"
    db = DatabaseOperations(secrets_path, db_path)
    db.initialize_database()
    
    # Set up application
    app = QApplication(sys.argv)
    window = MainWindow(config_path, db_path)
    window.show()
    
    logger.info("Application started successfully at 06:56 PM CEST, July 20, 2025")
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.getLogger(__name__).error(f"Application crashed: {e}")
        sys.exit(1)