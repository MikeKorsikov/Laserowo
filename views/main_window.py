# --- views/main_window.py ---
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from config.settings import APP_TITLE, WINDOW_SIZE

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.style = tb.Style("flatly")
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.root, text="Welcome to Laser Salon Manager", font=("Helvetica", 18))
        label.pack(pady=20)

        # Placeholder navigation buttons
        btn_client = ttk.Button(self.root, text="Clients", command=self.open_clients)
        btn_client.pack(pady=10)

    def open_clients(self):
        print("Client section to be implemented")