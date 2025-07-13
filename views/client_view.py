# views/client_view.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from typing import Callable, Any # Import Callable and Any for type hinting

class ClientView(ctk.CTkFrame):
    # Rename client_controller to dispatch_action_callback
    def __init__(self, parent: ctk.CTkFrame, dispatch_action_callback: Callable[[str, Any], Any]):
        super().__init__(parent)
        self.dispatch_action_callback = dispatch_action_callback # Store the callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row for client list

        self.create_widgets()
        self.load_clients()
        self.selected_client_data = None # To store the currently selected client's data

    def create_widgets(self):
        # Current Clients Section
        self.current_clients_frame = ctk.CTkFrame(self)
        self.current_clients_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.current_clients_frame.grid_columnconfigure(0, weight=1)
        self.current_clients_frame.grid_rowconfigure(2, weight=1) # Row for scrollable frame

        self.search_entry = ctk.CTkEntry(self.current_clients_frame, placeholder_text="Search clients...")
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.search_button = ctk.CTkButton(self.current_clients_frame, text="Search", command=self.search_clients)
        self.search_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.client_list_scroll_frame = ctk.CTkScrollableFrame(self.current_clients_frame)
        self.client_list_scroll_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.client_list_scroll_frame.grid_columnconfigure(0, weight=1)

        # Client Details Section
        self.client_details_frame = ctk.CTkFrame(self)
        self.client_details_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(1, weight=2) # Make details section wider

        self.details_label = ctk.CTkLabel(self.client_details_frame, text="Client Details", font=ctk.CTkFont(size=16, weight="bold"))
        self.details_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Using a dictionary to manage entries for easier access and iteration
        self.entries = {}
        fields = [
            ("Full Name:", "full_name"),
            ("Phone:", "phone_number"),
            ("Email:", "email"),
            ("Facebook ID:", "facebook_id"),
            ("Instagram Handle:", "instagram_handle"),
            ("Date of Birth (YYYY-MM-DD):", "date_of_birth"),
            ("Excel ID:", "excel_id") # Add Excel ID field
        ]

        for i, (label_text, key) in enumerate(fields):
            label = ctk.CTkLabel(self.client_details_frame, text=label_text)
            label.grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
            entry = ctk.CTkEntry(self.client_details_frame)
            entry.grid(row=i+1, column=1, padx=5, pady=2, sticky="ew")
            self.entries[key] = entry # Store entry widgets in the dictionary

        # Checkboxes
        self.booksy_used_checkbox = ctk.CTkCheckBox(self.client_details_frame, text="Booksy Used")
        self.booksy_used_checkbox.grid(row=len(fields)+1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.blacklisted_checkbox = ctk.CTkCheckBox(self.client_details_frame, text="Blacklisted")
        self.blacklisted_checkbox.grid(row=len(fields)+2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.active_client_checkbox = ctk.CTkCheckBox(self.client_details_frame, text="Active Client")
        self.active_client_checkbox.grid(row=len(fields)+3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.active_client_checkbox.select() # Default to active

        # Buttons
        self.add_button = ctk.CTkButton(self.client_details_frame, text="Add Client", command=self.add_client)
        self.add_button.grid(row=len(fields)+4, column=0, padx=5, pady=10, sticky="ew")
        self.update_button = ctk.CTkButton(self.client_details_frame, text="Update Client", command=self.update_client)
        self.update_button.grid(row=len(fields)+4, column=1, padx=5, pady=10, sticky="ew")
        self.delete_button = ctk.CTkButton(self.client_details_frame, text="Delete Client", command=self.delete_client, fg_color="red", hover_color="darkred")
        self.delete_button.grid(row=len(fields)+5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Selected Client History Section
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.history_label = ctk.CTkLabel(self.history_frame, text="Selected Client History", font=ctk.CTkFont(size=14, weight="bold"))
        self.history_label.pack(padx=10, pady=10)
        self.history_text = ctk.CTkLabel(self.history_frame, text="Select a client to view their history.") # Placeholder
        self.history_text.pack(padx=10, pady=10)


    def load_clients(self):
        # Clear existing buttons
        for widget in self.client_list_scroll_frame.winfo_children():
            widget.destroy()

        # Use dispatch_action_callback to get clients
        clients = self.dispatch_action_callback("client_get_all_clients")
        for i, client_data in enumerate(clients):
            # Using client_data (dictionary) directly in lambda
            client_button = ctk.CTkButton(
                self.client_list_scroll_frame,
                text=client_data.get('full_name', 'Unknown Client'),
                command=lambda c=client_data: self.display_client(c)
            )
            client_button.grid(row=i, column=0, padx=5, pady=2, sticky="ew")

    def display_client(self, client_data: Dict[str, Any]): # Add type hint
        """Displays the selected client's data in the details section."""
        self.selected_client_data = client_data # Store the full client data

        # Clear existing entries
        for key in self.entries:
            self.entries[key].delete(0, ctk.END) # Use ctk.END

        # Populate entries
        for key, entry_widget in self.entries.items():
            value = client_data.get(key)
            if value is not None: # Only insert if value is not None
                # Dates are already strings from to_dict(), so direct insert is fine
                entry_widget.insert(0, str(value))
            
        # Set checkboxes
        self.booksy_used_checkbox.select() if client_data.get('booksy_used') else self.booksy_used_checkbox.deselect()
        self.blacklisted_checkbox.select() if client_data.get('is_blacklisted') else self.blacklisted_checkbox.deselect()
        self.active_client_checkbox.select() if client_data.get('is_active') else self.active_client_checkbox.deselect()

        # Update history label - TODO: Load actual appointment history here.
        client_id = client_data.get('id', 'N/A')
        client_name = client_data.get('full_name', 'Unknown')
        
        # Fetch appointments for the selected client
        appointments = self.dispatch_action_callback("appointment_get_appointments_by_client_id", client_id=client_id)
        
        history_text_content = f"History for {client_name} (ID: {client_id})\n\n"
        if appointments:
            for appt in appointments:
                appt_date = appt.get('appointment_date', 'N/A')
                service_name = appt.get('service_name', 'N/A')
                history_text_content += f" - Date: {appt_date}, Service: {service_name}\n"
        else:
            history_text_content += "No appointment history found."
        self.history_text.configure(text=history_text_content)


    def search_clients(self):
        search_term = self.search_entry.get()
        if search_term:
            # Use dispatch_action_callback for search
            filtered_clients = self.dispatch_action_callback("client_search_clients", query=search_term)
        else:
            filtered_clients = self.dispatch_action_callback("client_get_all_clients")

        # Clear existing buttons
        for widget in self.client_list_scroll_frame.winfo_children():
            widget.destroy()

        for i, client_data in enumerate(filtered_clients):
            client_button = ctk.CTkButton(
                self.client_list_scroll_frame,
                text=client_data.get('full_name', 'Unknown Client'),
                command=lambda c=client_data: self.display_client(c)
            )
            client_button.grid(row=i, column=0, padx=5, pady=2, sticky="ew")


    def add_client(self):
        full_name = self.entries['full_name'].get()
        if not full_name:
            messagebox.showerror("Error", "Full Name is required.")
            return

        client_data = {
            'full_name': full_name,
            'phone_number': self.entries['phone_number'].get() or None,
            'email': self.entries['email'].get() or None,
            'facebook_id': self.entries['facebook_id'].get() or None,
            'instagram_handle': self.entries['instagram_handle'].get() or None,
            'booksy_used': self.booksy_used_checkbox.get() == 1,
            'is_blacklisted': self.blacklisted_checkbox.get() == 1,
            'is_active': self.active_client_checkbox.get() == 1,
            'excel_id': self.entries['excel_id'].get() or None # Get excel_id from entry
        }
        
        dob_str = self.entries['date_of_birth'].get()
        if dob_str:
            try:
                client_data['date_of_birth'] = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
                return
        else:
            client_data['date_of_birth'] = None

        # Use dispatch_action_callback to add client
        new_client_dict = self.dispatch_action_callback("client_create_client", **client_data)
        if new_client_dict: # Controller returns Client ORM object, which gets .to_dict() in main.py
            messagebox.showinfo("Success", f"Client '{new_client_dict.get('full_name')}' added.")
            self.load_clients() # Refresh the list
            self.clear_fields() # Clear the entry fields
        else:
            messagebox.showerror("Error", "Failed to add client. Check logs for details.")

    def update_client(self):
        if not self.selected_client_data:
            messagebox.showwarning("Warning", "No client selected to update.")
            return

        client_id = self.selected_client_data.get('id')
        updates = {}

        # Collect updates from entries
        for key, entry_widget in self.entries.items():
            current_value = entry_widget.get() or None
            # Only add to updates if the value has changed or it's a field that needs explicit update
            # Note: For simplicity, we are sending all current form values for update.
            # The controller can handle determining if an actual change occurred.
            updates[key] = current_value

        # Handle date_of_birth separately for conversion
        dob_str = self.entries['date_of_birth'].get()
        if dob_str:
            try:
                updates['date_of_birth'] = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Error", "Invalid Date of Birth format. Use YYYY-MM-DD.")
                return
        else:
            updates['date_of_birth'] = None # Allow setting to None

        # Collect updates from checkboxes
        updates['booksy_used'] = self.booksy_used_checkbox.get() == 1
        updates['is_blacklisted'] = self.blacklisted_checkbox.get() == 1
        updates['is_active'] = self.active_client_checkbox.get() == 1

        # Use dispatch_action_callback to update client
        updated_client_dict = self.dispatch_action_callback("client_update_client", client_id=client_id, updates=updates)
        if updated_client_dict: # Controller returns Client ORM object, which gets .to_dict() in main.py
            messagebox.showinfo("Success", f"Client '{updated_client_dict.get('full_name')}' updated.")
            self.load_clients() # Refresh the list
            # Re-display the updated client data to reflect changes
            self.display_client(updated_client_dict) # Pass the dictionary directly
        else:
            messagebox.showerror("Error", "Failed to update client. Check logs for details.")

    def delete_client(self):
        if not self.selected_client_data:
            messagebox.showwarning("Warning", "No client selected to delete.")
            return

        client_id = self.selected_client_data.get('id')
        client_name = self.selected_client_data.get('full_name')

        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete client '{client_name}' (ID: {client_id})?"):
            # Use dispatch_action_callback to delete client
            if self.dispatch_action_callback("client_delete_client", client_id=client_id):
                messagebox.showinfo("Success", f"Client '{client_name}' deleted.")
                self.load_clients() # Refresh the list
                self.clear_fields() # Clear the form
            else:
                messagebox.showerror("Error", "Failed to delete client. Check logs for details.")

    def clear_fields(self):
        """Clears all entry fields and resets checkboxes."""
        for key in self.entries:
            self.entries[key].delete(0, ctk.END)
        
        self.booksy_used_checkbox.deselect()
        self.blacklisted_checkbox.deselect()
        self.active_client_checkbox.select() # Default to active
        self.selected_client_data = None # Clear selected client

        self.history_text.configure(text="Select a client to view their history.")
    
    # updated