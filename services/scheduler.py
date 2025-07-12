# --- services/scheduler.py ---
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Add job examples here
    scheduler.start()