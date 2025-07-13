# config/settings.py

class AppSettings:
    APP_NAME = "Laserowo Business Management"
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
    POLISH_SOLE_PROPRIETORSHIP_TAX_RATE = 0.19 # Enteractual rate

    # Appointment spacing rules (in weeks)
    SESSION_SPACING_WEEKS = {
        1: 0,  # Session 1 is initial
        2: 4,  # Session 2: Minimum 4 weeks after Session 1.
        3: 6,  # Session 3: Minimum 6 weeks after Session 2.
        4: 8,  # Session 4: Minimum 8 weeks after Session 3.
        5: 10, # Session 5: Minimum 10 weeks after Session 4.
        6: 12, # Session 6: Minimum 12 weeks after Session 5.
        7: 14, # Session 7: Minimum 14 weeks after Session 6.
        8: 16, # Session 8: Minimum 16 weeks after Session 7.
        9: 18, # Session 9: Minimum 18 weeks after Session 8.
        10: 20 # Session 10: Minimum 20 weeks after Session 9.
    }

    # Low stock threshold for inventory alerts
    DEFAULT_LOW_STOCK_THRESHOLD = 5

    # Reminder intervals for hardware maintenance/insurance (in days before due date)
    HARDWARE_REMINDER_DAYS = [30, 14] # 1 month and 2 weeks

    # Placeholder for communication methods (Phase 2 & 3)
    COMMUNICATION_METHODS = ["SMS", "Email", "Instagram", "Facebook"]

    # Excel import settings
    EXCEL_CLIENTS_TAB_NAME = "KLIENCI"
    EXCEL_VISITS_TAB_NAME = "WIZYTY"

# Instantiate settings for easy import
settings = AppSettings()