# config/settings.py

class AppSettings:
    APP_NAME = "Laserowo Business Management" # This is APP_TITLE equivalent
    # You didn't explicitly define WINDOW_SIZE, so we'll add it
    WINDOW_SIZE = "1200x800" # Example default window size

    DEFAULT_OPERATING_HOURS = {
        "Monday": {"start": "10:00", "end": "19:00"},
        "Tuesday": {"start": "10:00", "end": "19:00"},
        "Wednesday": {"start": "10:00", "end": "19:00"},
        "Thursday": {"start": "10:00", "end": "19:00"},
        "Friday": {"start": "10:00", "end": "19:00"},
        "Saturday": {"start": "10:00", "end": "14:00"},
        "Sunday": {"start": "00:00", "end": "00:00", "is_closed": True},
    }
    # Example tax rate for statutory income statement
    POLISH_SOLE_PROPRIETORSHIP_TAX_RATE = 0.19 # Example, adjust as needed

    # Appointment spacing rules (in weeks)
    SESSION_SPACING_WEEKS = {
        1: 0,
        2: 4,
        3: 6,
        4: 8,
        5: 10,
        6: 12,
        7: 14,
        8: 16,
        9: 18,
        10: 20
    }

    # Low stock threshold for inventory alerts
    DEFAULT_LOW_STOCK_THRESHOLD = 5

    # Reminder intervals for hardware maintenance/insurance (in days before due date)
    HARDWARE_REMINDER_DAYS = [30, 14]

    # Placeholder for communication methods (Phase 2 & 3)
    COMMUNICATION_METHODS = ["SMS", "Email", "Instagram", "Facebook"]

    # Excel import settings
    EXCEL_CLIENTS_TAB_NAME = "KLIENCI"
    EXCEL_VISITS_TAB_NAME = "WIZYTY"

# Instantiate settings for easy import
settings = AppSettings()

# reviewed