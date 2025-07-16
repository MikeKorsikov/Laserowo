# config.py
# P1_DESKTOP_APP/config.py
import os

# Define basic application settings
# Adjust paths to be relative to the P1_DESKTOP_APP root
DATABASE_FILE_PATH = os.path.join('database', 'app.db')
CSV_DATA_DIR = os.path.join('data_loader', 'csv_files')

# Default admin username/password for first run
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin_password'