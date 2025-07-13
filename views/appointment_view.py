# D:\PYTHON\Laserowo\P1_desktop_app\views\appointment_view.py

import customtkinter as ctk
from typing import Callable, Any

class AppointmentView(ctk.CTkFrame): # It's good practice for views to inherit from CTkFrame
    def __init__(self, master_tab: ctk.CTkFrame, controller_callback: Callable[[str, Any], Any]):
        super().__init__(master_tab)
        self.master_tab = master_tab
        self.controller_callback = controller_callback
        self.create_widgets()

    def create_widgets(self):
        # Placeholder content for now
        label = ctk.CTkLabel(self, text="Appointment Management Content Goes Here")
        label.pack(padx=20, pady=20)

        # Example of how you might add a button to interact with the controller
        # fetch_appointments_button = ctk.CTkButton(self, text="Fetch Appointments",
        #                                          command=lambda: self.controller_callback("appointment_get_all_appointments"))
        # fetch_appointments_button.pack(pady=10)
        