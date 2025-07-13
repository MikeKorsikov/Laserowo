# main.py
import customtkinter as ctk
from config.database import init_db, get_db
from config.settings import settings
from controllers.client_controller import ClientController
from controllers.appointment_controller import AppointmentController
from views.client_view import ClientView
from views.appointment_view import AppointmentView # Assuming you will create this

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(settings.APP_NAME)
        self.geometry(settings.WINDOW_SIZE)

        init_db()
        self.db_session = next(get_db())

        self.client_controller = ClientController(self.db_session)
        self.appointment_controller = AppointmentController(self.db_session)
        # Add other controllers here
        self.controllers = {
            "client": self.client_controller,
            "appointment": self.appointment_controller,
            # Add other controllers here by their prefixes (e.g., "service": self.service_controller)
        }

        self.create_main_layout()

    def create_main_layout(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Clients Tab
        self.clients_tab = self.tabview.add("Clients")
        # --- FIX FOR AttributeError: 'ClientView' object has no attribute 'pack' ---
        # Create the ClientView instance
        self.client_view = ClientView(self.clients_tab, self.dispatch_controller_action)
        # Then pack the instance *itself* into its parent tab
        self.client_view.pack(fill="both", expand=True, padx=5, pady=5)
        # --- END FIX ---

        # Appointments Tab
        self.appointments_tab = self.tabview.add("Appointments")
        # Similarly for AppointmentView when it's ready:
        self.appointment_view = AppointmentView(self.appointments_tab, self.dispatch_controller_action)
        self.appointment_view.pack(fill="both", expand=True, padx=5, pady=5)
        # ctk.CTkLabel(self.appointments_tab, text="Appointment Management will go here").pack(padx=20, pady=20)


        # Finance Tab (Placeholder)
        self.finance_tab = self.tabview.add("Finance")
        ctk.CTkLabel(self.finance_tab, text="Finance Management will go here").pack(padx=20, pady=20)

        # Hardware Tab (Placeholder)
        self.hardware_tab = self.tabview.add("Hardware")
        ctk.CTkLabel(self.hardware_tab, text="Hardware Tracking will go here").pack(padx=20, pady=20)

        # Reports Tab (Placeholder)
        self.reports_tab = self.tabview.add("Reports")
        ctk.CTkLabel(self.reports_tab, text="Reporting Functionality will go here").pack(padx=20, pady=20)

    def dispatch_controller_action(self, action_name: str, *args, **kwargs):
        """
        A central dispatcher for views to interact with controllers.
        This helps decouple views from direct controller instances.
        The `action_name` should be prefixed with the controller type (e.g., "client_get_all_clients").
        """
        parts = action_name.split('_', 1)
        if len(parts) < 2:
            print(f"Error: Invalid action_name format: {action_name}. Expected 'controller_prefix_method_name'.")
            return None

        controller_prefix = parts[0]
        method_name = parts[1]

        controller = self.controllers.get(controller_prefix)

        if not controller:
            print(f"Error: Controller '{controller_prefix}' not found for action '{action_name}'.")
            return None

        method = getattr(controller, method_name, None)

        if not method:
            print(f"Error: Method '{method_name}' not found in {controller_prefix} controller.")
            return None

        try:
            result = method(*args, **kwargs)

            if method_name.startswith("get_") or method_name.startswith("search_"):
                return result
            else:
                if hasattr(result, 'to_dict'):
                    return result.to_dict()
                return result

        except Exception as e:
            print(f"An error occurred during dispatching action '{action_name}': {e}")
            raise # Re-raise for debugging or UI error handling
            # return None # Or return None if you prefer silent failure or specific error object


    def on_closing(self):
        """Clean up database session on application close."""
        if self.db_session:
            self.db_session.close()
            print("Database session closed.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

# reviewed