# main.py
import customtkinter as ctk
from config.database import init_db, get_db
from config.settings import settings
from controllers.client_controller import ClientController
# Import other controllers as they are created
from views.main_window import MainWindow # Placeholder for your main window
from views.client_view import ClientView # Your new client view

# Set custom tkinter appearance
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(settings.APP_NAME)
        self.geometry("1200x800") # Adjust as needed

        # Initialize database
        init_db()
        self.db_session = next(get_db()) # Get a single session for the app lifetime for now (simple approach)

        # Initialize controllers
        self.client_controller = ClientController(self.db_session)
        # self.appointment_controller = AppointmentController(self.db_session)
        # ... other controllers

        self.create_main_layout()

    def create_main_layout(self):
        # Create a tabview for different sections of the app
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Clients Tab
        self.clients_tab = self.tabview.add("Clients")
        self.client_view = ClientView(self.clients_tab, self.dispatch_controller_action)
        self.client_view.pack(fill="both", expand=True, padx=5, pady=5)

        # Appointments Tab (Placeholder)
        self.appointments_tab = self.tabview.add("Appointments")
        ctk.CTkLabel(self.appointments_tab, text="Appointment Management will go here").pack(padx=20, pady=20)

        # Finance Tab (Placeholder)
        self.finance_tab = self.tabview.add("Finance")
        ctk.CTkLabel(self.finance_tab, text="Finance Management will go here").pack(padx=20, pady=20)

        # Hardware Tab (Placeholder)
        self.hardware_tab = self.tabview.add("Hardware")
        ctk.CTkLabel(self.hardware_tab, text="Hardware Tracking will go here").pack(padx=20, pady=20)

        # Reports Tab (Placeholder)
        self.reports_tab = self.tabview.add("Reports")
        ctk.CTkLabel(self.reports_tab, text="Reporting Functionality will go here").pack(padx=20, pady=20)


    def dispatch_controller_action(self, controller_method_name: str, **kwargs):
        """
        A central dispatcher for view to interact with controllers.
        This helps decouple views from direct controller instances.
        """
        if controller_method_name.startswith("get_") or controller_method_name.startswith("search_"):
            # For read operations, return data
            method = getattr(self.client_controller, controller_method_name, None)
            if method:
                result = method(**kwargs)
                # Convert SQLAlchemy model instances to dictionaries for easier view handling
                if isinstance(result, list):
                    return [item.to_dict() for item in result]
                elif result:
                    return result.to_dict()
                return result
            else:
                print(f"Error: Method '{controller_method_name}' not found in ClientController.")
                return None
        else:
            # For write operations (create, update, delete, blacklist, deactivate), just execute
            method = getattr(self.client_controller, controller_method_name, None)
            if method:
                return method(**kwargs)
            else:
                print(f"Error: Method '{controller_method_name}' not found in ClientController.")
                return None


    def on_closing(self):
        """Clean up database session on application close."""
        if self.db_session:
            self.db_session.close()
            print("Database session closed.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing) # Handle window close event
    app.mainloop()