# main_window.py

"""
Main application window with login and navigation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from services import UserService
from ui.placeholders import (
    create_placeholder_frame, create_finance_frame, create_reports_frame,
    create_hardware_frame, create_settings_frame, ClientsFrame, AppointmentsFrame, AIChatbotFrame
)

logger = logging.getLogger(__name__)

class LoginWindow:
    """Login window for user authentication"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.resizable(True, True)

