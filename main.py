# main.py
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import ttkbootstrap as tb # Using ttkbootstrap for styling

from config.database import init_db, get_db
from controllers.client_controller import ClientController
from controllers.appointment_controller import AppointmentController
from controllers.service_controller import ServiceController
from controllers.treatment_area_controller import TreatmentAreaController
from controllers.payment_method_controller import PaymentMethodController
# Import views
from views.main_window import MainWindow # Import the updated MainWindow
from views.client_view import ClientView
from views.appointment_view import AppointmentView
# Also import other empty controllers and views for completeness if you plan to use them
from controllers.finance_controller import FinanceController
from controllers.hardware_controller import HardwareController
from controllers.reporting_controller import ReportingController
from config.settings import settings

# Then, use settings.APP_NAME and settings.WINDOW_SIZE
# For example:
app_name = settings.APP_NAME
window_size = settings.WINDOW_SIZE

class App(ctk.CTk): # Changed to inherit from ctk.CTk
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        
        # Initialize database
        init_db()
        self.db_session = next(get_db()) # Get a database session

        # Initialize controllers
        self.client_controller = ClientController(self.db_session)
        self.appointment_controller = AppointmentController(self.db_session)
        self.service_controller = ServiceController(self.db_session)
        self.treatment_area_controller = TreatmentAreaController(self.db_session)
        self.payment_method_controller = PaymentMethodController(self.db_session)
        self.finance_controller = FinanceController(self.db_session) # Initialize empty controller
        self.hardware_controller = HardwareController(self.db_session) # Initialize empty controller
        self.reporting_controller = ReportingController(self.db_session) # Initialize empty controller

        # Store controllers in a dictionary for easy lookup by prefix
        self.controllers = {
            "client": self.client_controller,
            "appointment": self.appointment_controller,
            "service": self.service_controller,
            "treatment_area": self.treatment_area_controller,
            "payment_method": self.payment_method_controller,
            "finance": self.finance_controller,
            "hardware": self.hardware_controller,
            "reporting": self.reporting_controller
        }

        self.create_main_layout()

        # Handle app closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def dispatch_controller_action(self, action_string: str, **kwargs: Any) -> Any:
        """
        Dispatches an action to the appropriate controller method.
        action_string examples: "client_get_all_clients", "appointment_create_appointment"
        """
        try:
            parts = action_string.split('_', 1) # Split only on the first underscore
            if len(parts) < 2:
                raise ValueError(f"Invalid action string format: {action_string}. Expected 'controller_method'.")
            
            controller_prefix, method_name = parts
            
            controller = self.controllers.get(controller_prefix)
            if not controller:
                raise ValueError(f"No controller found for prefix: {controller_prefix}")

            method = getattr(controller, method_name, None)
            if not method:
                raise AttributeError(f"Controller '{controller_prefix}' has no method: {method_name}")

            result = method(**kwargs)
            
            # Convert SQLAlchemy ORM objects to dictionaries before returning to view
            if hasattr(result, 'to_dict'):
                return result.to_dict()
            elif isinstance(result, list) and all(hasattr(item, 'to_dict') for item in result):
                return [item.to_dict() for item in result]
            else:
                return result

        except Exception as e:
            print(f"Error dispatching action '{action_string}': {e}")
            import traceback
            traceback.print_exc()
            return None # Return None or raise an exception to signal failure

    def create_main_layout(self):
        # Using MainWindow to manage the main window layout
        self.main_window = MainWindow(self, self.dispatch_controller_action)
        # MainWindow already packs itself into the root, no need to pack here
        
        # Access tabs from MainWindow and pass them to the respective views
        # Note: self.main_window.clients_tab and self.main_window.appointments_tab
        # are created within the MainWindow class.
        
        # Pass the specific tab frames from MainWindow to your views
        self.client_view = ClientView(self.main_window.clients_tab, self.dispatch_controller_action)
        self.client_view.pack(expand=True, fill="both")

        self.appointment_view = AppointmentView(self.main_window.appointments_tab, self.dispatch_controller_action)
        self.appointment_view.pack(expand=True, fill="both")

        # Set up other views similarly as they are implemented

    def on_closing(self):
        """Closes the database session when the application is closed."""
        if self.db_session:
            self.db_session.close()
            print("Database session closed.")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

# updated