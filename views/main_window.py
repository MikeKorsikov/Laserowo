# views/main_window.py
import customtkinter as ctk # Use customtkinter
from tkinter import ttk # Keep ttk for Notebook as ctk doesn't have native tab widget
import ttkbootstrap as tb
from config.settings import settings

# Then, use settings.APP_NAME and settings.WINDOW_SIZE
# For example, within your MainWindow class or function:
# self.setWindowTitle(settings.APP_NAME)
# self.setGeometry(100, 100, int(settings.WINDOW_SIZE.split('x')[0]), int(settings.WINDOW_SIZE.split('x')[1]))
class MainWindow:
    # Accept dispatch_action_callback to pass it down to child views
    def __init__(self, root: ctk.CTk, dispatch_action_callback):
        self.root = root
        self.dispatch_action_callback = dispatch_action_callback # Store callback
        # Root title and geometry are set in App.__init__ now, can remove here if desired, or keep as fallback
        # self.root.title(APP_NAME)
        # self.root.geometry(WINDOW_SIZE)
        self.style = tb.Style("flatly") # Apply ttkbootstrap style
        
        self.notebook = None # Initialize notebook attribute
        self.clients_tab = None # Initialize tab attributes
        self.appointments_tab = None
        # Add other tabs as needed:
        # self.finance_tab = None
        # self.hardware_tab = None
        # self.report_tab = None
        # self.service_tab = None
        # self.settings_tab = None

        self.create_widgets()

    def create_widgets(self):
        # Remove the welcome label and placeholder buttons
        # label = ttk.Label(self.root, text="Welcome to Laser Salon Manager", font=("Helvetica", 18))
        # label.pack(pady=20)
        # btn_client = ttk.Button(self.root, text="Clients", command=self.open_clients)
        # btn_client.pack(pady=10)

        # Create the main notebook (tabbed interface)
        # Use ttk.Notebook as customtkinter doesn't have a direct equivalent for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create individual tabs using CTkFrame for consistency with other CustomTkinter views
        self.clients_tab = ctk.CTkFrame(self.notebook)
        self.appointments_tab = ctk.CTkFrame(self.notebook)
        # self.finance_tab = ctk.CTkFrame(self.notebook)
        # self.hardware_tab = ctk.CTkFrame(self.notebook)
        # self.report_tab = ctk.CTkFrame(self.notebook)
        # self.service_tab = ctk.CTkFrame(self.notebook)
        # self.settings_tab = ctk.CTkFrame(self.notebook)

        # Pack each tab frame inside itself before adding to notebook
        self.clients_tab.pack(expand=True, fill="both")
        self.appointments_tab.pack(expand=True, fill="both")
        # Pack other tabs here too

        # Add tabs to the notebook
        self.notebook.add(self.clients_tab, text="Clients")
        self.notebook.add(self.appointments_tab, text="Appointments")
        # self.notebook.add(self.finance_tab, text="Finance")
        # self.notebook.add(self.hardware_tab, text="Hardware")
        # self.notebook.add(self.report_tab, text="Reports")
        # self.notebook.add(self.service_tab, text="Services")
        # self.notebook.add(self.settings_tab, text="Settings")

    # The open_clients method is no longer needed with a tabbed interface
    # def open_clients(self):
    #     print("Client section to be implemented")

# updated