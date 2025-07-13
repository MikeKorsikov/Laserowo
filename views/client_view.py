# views/client_view.py
import customtkinter as ctk
from datetime import date, datetime
from typing import Callable, List, Optional, Dict, Any # Add List, Optional, Dict, Any here


class ClientView(ctk.CTkFrame):
    def __init__(self, master, controller_callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.controller_callback = controller_callback # This will be a method in the main controller

        self.create_widgets()
        self.load_clients() # Load clients when the view is initialized

    def create_widgets(self):
        # Client List Section
        self.client_list_frame = ctk.CTkFrame(self)
        self.client_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.client_list_frame.grid_columnconfigure(0, weight=1)

        self.client_list_label = ctk.CTkLabel(self.client_list_frame, text="Current Clients", font=ctk.CTkFont(size=16, weight="bold"))
        self.client_list_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.client_search_entry = ctk.CTkEntry(self.client_list_frame, placeholder_text="Search clients...")
        self.client_search_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.client_search_entry.bind("<Return>", self.search_clients) # Bind Enter key
        self.search_button = ctk.CTkButton(self.client_list_frame, text="Search", command=self.search_clients)
        self.search_button.grid(row=1, column=1, padx=10, pady=5)


        self.client_listbox = ctk.CTkScrollableFrame(self.client_list_frame, height=200)
        self.client_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Client Details/Form Section
        self.client_form_frame = ctk.CTkFrame(self)
        self.client_form_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.client_form_frame.grid_columnconfigure((0,1), weight=1)

        self.form_label = ctk.CTkLabel(self.client_form_frame, text="Client Details", font=ctk.CTkFont(size=16, weight="bold"))
        self.form_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        labels = ["Full Name:", "Phone:", "Email:", "Facebook ID:", "Instagram Handle:", "Date of Birth (YYYY-MM-DD):"]
        self.entries = {}
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.client_form_frame, text=text).grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.client_form_frame)
            entry.grid(row=i+1, column=1, padx=5, pady=2, sticky="ew")
            self.entries[text.replace(":", "").replace(" ", "_").lower()] = entry # Store references to entries

        self.blacklist_checkbox = ctk.CTkCheckBox(self.client_form_frame, text="Blacklisted")
        self.blacklist_checkbox.grid(row=len(labels)+1, column=0, padx=5, pady=5, sticky="w")

        self.active_checkbox = ctk.CTkCheckBox(self.client_form_frame, text="Active Client")
        self.active_checkbox.grid(row=len(labels)+1, column=1, padx=5, pady=5, sticky="w")
        self.active_checkbox.select() # Default to active

        self.add_button = ctk.CTkButton(self.client_form_frame, text="Add Client", command=self.add_client)
        self.add_button.grid(row=len(labels)+2, column=0, padx=10, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(self.client_form_frame, text="Update Client", command=self.update_client)
        self.update_button.grid(row=len(labels)+2, column=1, padx=10, pady=10, sticky="ew")
        self.update_button.configure(state="disabled") # Disable until a client is selected

        # Client details display area (for history)
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)

        self.details_label = ctk.CTkLabel(self.details_frame, text="Selected Client History", font=ctk.CTkFont(size=14, weight="bold"))
        self.details_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.history_textbox = ctk.CTkTextbox(self.details_frame, wrap="word", height=150)
        self.history_textbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.history_textbox.insert("end", "Select a client to view their history.")
        self.history_textbox.configure(state="disabled")

        self.selected_client_id = None

    def load_clients(self, clients: Optional[List[Dict]] = None):
        """Loads or reloads the client list in the UI."""
        for widget in self.client_listbox.winfo_children():
            widget.destroy() # Clear existing client buttons

        if clients is None:
            clients = self.controller_callback("get_all_clients")

        if not clients:
            ctk.CTkLabel(self.client_listbox, text="No clients found.").pack(pady=5)
            return

        for client in clients:
            client_button = ctk.CTkButton(self.client_listbox,
                                         text=client['full_name'],
                                         command=lambda c=client: self.display_client(c))
            client_button.pack(fill="x", padx=5, pady=2)

    def search_clients(self, event=None):
        query = self.client_search_entry.get()
        if query:
            results = self.controller_callback("search_clients", query_string=query)
            self.load_clients(results)
        else:
            self.load_clients() # Reload all if search is empty

    def display_client(self, client_data: Dict[str, Any]):
        """Displays selected client's data in the form and history."""
        self.selected_client_id = client_data['id']
        self.entries['full_name'].delete(0, "end")
        self.entries['full_name'].insert(0, client_data.get('full_name', ''))
        self.entries['phone_number'].delete(0, "end")
        self.entries['phone_number'].insert(0, client_data.get('phone_number', ''))
        self.entries['email'].delete(0, "end")
        self.entries['email'].insert(0, client_data.get('email', ''))
        self.entries['facebook_id'].delete(0, "end")
        self.entries['facebook_id'].insert(0, client_data.get('facebook_id', ''))
        self.entries['instagram_handle'].delete(0, "end")
        self.entries['instagram_handle'].insert(0, client_data.get('instagram_handle', ''))
        dob = client_data.get('date_of_birth')
        self.entries['date_of_birth_(yyyy-mm-dd)'].delete(0, "end")
        if dob:
            self.entries['date_of_birth_(yyyy-mm-dd)'].insert(0, dob.strftime("%Y-%m-%d") if isinstance(dob, date) else str(dob))

        if client_data.get('is_blacklisted'):
            self.blacklist_checkbox.select()
        else:
            self.blacklist_checkbox.deselect()

        if client_data.get('is_active'):
            self.active_checkbox.select()
        else:
            self.active_checkbox.deselect()

        self.update_button.configure(state="normal")
        self.add_button.configure(state="disabled") # Cannot add if one is selected for editing

        # Load and display client history
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        history = self.controller_callback("get_client_history", client_id=self.selected_client_id)
        if history:
            self.history_textbox.insert("end", "Appointments History:\n")
            for appt in history:
                service_name = appt.service.service_name if appt.service else "N/A"
                area_name = appt.treatment_area.area_name if appt.treatment_area else "N/A"
                self.history_textbox.insert("end", f"- {appt.appointment_date} {appt.start_time}: {service_name} ({area_name}), Session {appt.session_number_for_area}, Status: {appt.appointment_status}\n")
        else:
            self.history_textbox.insert("end", "No appointment history found for this client.")
        self.history_textbox.configure(state="disabled")


    def add_client(self):
        full_name = self.entries['full_name'].get()
        phone = self.entries['phone_number'].get()
        email = self.entries['email'].get()
        facebook_id = self.entries['facebook_id'].get()
        instagram_handle = self.entries['instagram_handle'].get()
        dob_str = self.entries['date_of_birth_(yyyy-mm-dd)'].get()
        is_blacklisted = self.blacklist_checkbox.get() == 1
        is_active = self.active_checkbox.get() == 1

        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                ctk.CTkMessagebox.showerror("Input Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
                return

        client_data = {
            "full_name": full_name,
            "phone_number": phone if phone else None,
            "email": email if email else None,
            "facebook_id": facebook_id if facebook_id else None,
            "instagram_handle": instagram_handle if instagram_handle else None,
            "booksy_indicator": False, # Assuming manual add doesn't set this via Booksy
            "date_of_birth": dob,
            "is_blacklisted": is_blacklisted,
            "is_active": is_active
        }

        created_client = self.controller_callback("create_client", **client_data)
        if created_client:
            ctk.CTkMessagebox.showinfo("Success", f"Client '{created_client.full_name}' added.")
            self.clear_form()
            self.load_clients()
        else:
            ctk.CTkMessagebox.showerror("Error", "Failed to add client. Check inputs.")


    def update_client(self):
        if not self.selected_client_id:
            ctk.CTkMessagebox.show_warning("No Client Selected", "Please select a client to update.")
            return

        updates = {}
        updates['full_name'] = self.entries['full_name'].get()
        updates['phone_number'] = self.entries['phone_number'].get() or None
        updates['email'] = self.entries['email'].get() or None
        updates['facebook_id'] = self.entries['facebook_id'].get() or None
        updates['instagram_handle'] = self.entries['instagram_handle'].get() or None
        dob_str = self.entries['date_of_birth_(yyyy-mm-dd)'].get()
        if dob_str:
            try:
                updates['date_of_birth'] = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                ctk.CTkMessagebox.showerror("Input Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
                return
        else:
            updates['date_of_birth'] = None

        updates['is_blacklisted'] = self.blacklist_checkbox.get() == 1
        updates['is_active'] = self.active_checkbox.get() == 1

        updated_client = self.controller_callback("update_client", client_id=self.selected_client_id, **updates)
        if updated_client:
            ctk.CTkMessagebox.showinfo("Success", f"Client '{updated_client.full_name}' updated.")
            self.clear_form()
            self.load_clients()
        else:
            ctk.CTkMessagebox.showerror("Error", "Failed to update client. Check inputs.")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.blacklist_checkbox.deselect()
        self.active_checkbox.select()
        self.selected_client_id = None
        self.update_button.configure(state="disabled")
        self.add_button.configure(state="normal")
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        self.history_textbox.insert("end", "Select a client to view their history.")
        self.history_textbox.configure(state="disabled")