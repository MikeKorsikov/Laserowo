# config.py
"""
Configuration file for Laser Hair Removal Business Management Application
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent
DATABASE_DIR = BASE_DIR / "database"
CSV_DATA_DIR = BASE_DIR / "data_loader" / "csv_files"

# Database configuration
DATABASE_FILE_PATH = DATABASE_DIR / "app.db"

# Default admin user for first run
DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123",  # Should be changed after first login
    "role": "admin"
}

# Application settings
APP_NAME = "Laser Hair Removal Management"
APP_VERSION = "1.0.0"

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# CSV file names (expected in csv_files directory)
CSV_FILES = {
    "clients": "clients.csv",
    "services": "services.csv",
    "treatment_areas": "treatment_areas.csv",
    "appointments": "appointments.csv"
}

# Ensure directories exist
DATABASE_DIR.mkdir(exist_ok=True)
CSV_DATA_DIR.mkdir(exist_ok=True)