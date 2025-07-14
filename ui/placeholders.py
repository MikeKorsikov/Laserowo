# placeholders.py
"""
Placeholder UI components for main application modules
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Callable, Optional
from services import ClientService, AppointmentService
from services.ai_service import ChatbotService

class PlaceholderFrame(ttk.Frame):
    """Base placeholder frame"""
    
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        self.create_widgets(title, message)
    
    def create_widgets(self, title: str, message: str):
        # Title
        title_label = ttk.Label(self, text=title, font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Message
        message_label = ttk.Label(self, text=message, font=('Arial', 12))
        message_label.pack(pady=10)

class ClientsFrame(ttk.Frame):
    """Basic clients management frame"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_clients()
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Clients Management", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Client", command=self.add_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.load_clients).pack(side=tk.LEFT, padx=5)
        
        # Clients listbox with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.clients_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.clients_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.clients_listbox.yview)
        
        # Bind double-click to view client details
        self.clients_listbox.bind('<Double-1>', self.view_client_details)
    
    def load_clients(self):
        """Load and display clients"""
        self.clients_listbox.delete(0, tk.END)
        clients = ClientService.get_all_clients()
        
        for client in clients:
            display_text = f"{client['full_name']} - {client['phone_number'] or 'No phone'}"
            if client['is_blacklisted']:
                display_text += " [BLACKLISTED]"
            self.clients_listbox.insert(tk.END, display_text)
    
    def add_client(self):
        """Add a new client"""
        dialog = ClientDialog(self)
        if dialog.result:
            self.load_clients()
    
    def view_client_details(self, event):
        """View client details on double-click"""
        selection = self.clients_listbox.curselection()
        if selection:
            index = selection[0]
            clients = ClientService.get_all_clients()
            if index < len(clients):
                client = clients[index]
                details = f"""Client Details:
                
Name: {client['full_name']}
Phone: {client['phone_number'] or 'Not provided'}
Email: {client['email'] or 'Not provided'}
Date of Birth: {client['date_of_birth'] or 'Not provided'}
Status: {'Active' if client['is_active'] else 'Inactive'}
Blacklisted: {'Yes' if client['is_blacklisted'] else 'No'}"""
                messagebox.showinfo("Client Details", details)

class AppointmentsFrame(ttk.Frame):
    """Basic appointments management frame"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_appointments()
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Appointments Management", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Add Appointment", command=self.add_appointment).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.load_appointments).pack(side=tk.LEFT, padx=5)
        
        # Appointments listbox with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.appointments_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.appointments_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.appointments_listbox.yview)
        
        # Bind double-click to view appointment details
        self.appointments_listbox.bind('<Double-1>', self.view_appointment_details)
    
    def load_appointments(self):
        """Load and display appointments"""
        self.appointments_listbox.delete(0, tk.END)
        appointments = AppointmentService.get_all_appointments(limit=50)
        
        for appointment in appointments:
            display_text = f"{appointment['appointment_date']} {appointment['start_time']} - {appointment['client_name']} - {appointment['service_name']}"
            self.appointments_listbox.insert(tk.END, display_text)
    
    def add_appointment(self):
        """Add a new appointment"""
        messagebox.showinfo("Add Appointment", "Advanced appointment booking coming soon!\nFor now, use CSV import for initial data.")
    
    def view_appointment_details(self, event):
        """View appointment details on double-click"""
        selection = self.appointments_listbox.curselection()
        if selection:
            index = selection[0]
            appointments = AppointmentService.get_all_appointments(limit=50)
            if index < len(appointments):
                appointment = appointments[index]
                details = f"""Appointment Details:
                
Date: {appointment['appointment_date']}
Time: {appointment['start_time']} - {appointment['end_time']}
Client: {appointment['client_name']}
Service: {appointment['service_name']}
Area: {appointment['area_name']}
Status: {appointment['status']}
Price: ${appointment['base_price']}
Duration: {appointment['estimated_duration_minutes']} minutes"""
                messagebox.showinfo("Appointment Details", details)

class AIChatbotFrame(ttk.Frame):
    """Basic AI chatbot interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.chatbot = ChatbotService()
        self.create_widgets()
        self.display_welcome_message()
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="AI Business Assistant", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Chat display area
        chat_frame = ttk.Frame(self)
        chat_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Scrollable text widget for chat history
        chat_scrollbar = ttk.Scrollbar(chat_frame)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(chat_frame, yscrollcommand=chat_scrollbar.set, 
                                   height=20, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        chat_scrollbar.config(command=self.chat_display.yview)
        
        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(input_frame, text="Ask me anything:").pack(anchor=tk.W)
        
        # Input entry and send button
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.input_entry = ttk.Entry(entry_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(entry_frame, text="Send", command=self.send_message).pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.input_entry.bind('<Return>', lambda event: self.send_message())
    
    def display_welcome_message(self):
        """Display welcome message"""
        welcome_msg = self.chatbot.interact("hello")
        self.display_message("Bot", welcome_msg)
    
    def send_message(self):
        """Send user message to chatbot"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        # Display user message
        self.display_message("You", user_input)
        
        # Get bot response
        bot_response = self.chatbot.interact(user_input)
        self.display_message("Bot", bot_response)
        
        # Clear input
        self.input_entry.delete(0, tk.END)
    
    def display_message(self, sender: str, message: str):
        """Display a message in the chat area"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        
        # Format message
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

class ClientDialog:
    """Simple dialog for adding clients"""
    
    def __init__(self, parent):
        self.result = None
        self.create_dialog(parent)
    
    def create_dialog(self, parent):
        # Get client information
        name = simpledialog.askstring("Add Client", "Enter client full name:")
        if not name:
            return
        
        phone = simpledialog.askstring("Add Client", "Enter phone number (optional):")
        email = simpledialog.askstring("Add Client", "Enter email (optional):")
        
        # Add client
        client_id = ClientService.add_client(
            full_name=name,
            phone_number=phone if phone else None,
            email=email if email else None
        )
        
        if client_id:
            messagebox.showinfo("Success", f"Client '{name}' added successfully!")
            self.result = True
        else:
            messagebox.showerror("Error", "Failed to add client. Please try again.")

def create_placeholder_frame(parent, module_name: str) -> ttk.Frame:
    """Create appropriate frame based on module name"""
    if module_name == "Clients":
        return ClientsFrame(parent)
    elif module_name == "Appointments":
        return AppointmentsFrame(parent)
    elif module_name == "AI Chatbot":
        return AIChatter(parent)
    else:
        return PlaceholderFrame(parent, 
                              f"{module_name} Module", 
                              f"{module_name} functionality coming soon!\nThis is a placeholder for the {module_name.lower()} module.")

# Define frame classes for different modules
def create_finance_frame(parent):
    return PlaceholderFrame(parent, "Finance Module", "Financial reporting and analytics coming soon!")

def create_reports_frame(parent):
    return PlaceholderFrame(parent, "Reports Module", "Business reports and analytics coming soon!")

def create_hardware_frame(parent):
    return PlaceholderFrame(parent, "Hardware Module", "Hardware management and settings coming soon!")

def create_settings_frame(parent):
    return PlaceholderFrame(parent, "Settings Module", "Application settings and preferences coming soon!")

# Alias for chatbot frame
def create_chatbot_frame(parent):
    return AIChatter(parent)

# Shorter alias for the chatbot frame
AIChatter = AIChatbotFrame