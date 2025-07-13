# 💼 Laserowo — Laser Business Desktop App

A desktop application built for managing a laser salon business. It supports appointment scheduling, client management, service tracking, and expense monitoring — all with a clean UI and modular architecture.

🔗 **Repository**: [github.com/MikeKorsikov/Laserowo](https://github.com/MikeKorsikov/Laserowo)

---

## 💻 Tech Stack

- **👩‍🎨 GUI**: Tkinter with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)  
- **🗃️ Database**: SQLite  
- **🧩 ORM**: SQLAlchemy  
- **📊 Excel Integration**: `pandas` *(planned)*  
- **🤖 AI**: OpenAI GPT-4 (chatbot integration planned)  
- **⏱️ Task Scheduling**: APScheduler  
- **🏗️ Architecture**: Modular MVC pattern  

---

## ✨ Features (Phase 1)

- 🧑‍💼 Client management  
- 📅 Appointment tracking  
- 💰 Service and expense modeling  
- 🧱 Scalable modular architecture  
- 🤖 AI integration *(placeholder)*  
- ⏳ Background scheduler setup *(placeholder)*  

---

## 📂 Project Structure

```plaintext
P1_DESKTOP_APP/
├── assets/
│   ├── icons/                 # Application icons
│   └── styles/                # UI styling configurations
├── config/
│   ├── __init__.py
│   ├── database.py            # SQLAlchemy engine, session, Base setup
│   └── settings.py            # Application-wide settings (e.g., hours, rates)
├── controllers/
│   ├── __init__.py
│   ├── appointment_controller.py # Logic for appointment management
│   ├── client_controller.py   # Logic for client management
│   ├── finance_controller.py  # Logic for financial operations
│   ├── hardware_controller.py # Logic for hardware tracking
│   ├── reporting_controller.py# Logic for generating reports
│   └── service_controller.py  # Logic for services and inventory
├── data/
│   └── database.db            # SQLite local database file
├── imports/
│   └── excel_importer.py      # Script for importing Excel data
├── models/                    # SQLAlchemy ORM models (DB schema definitions)
│   ├── __init__.py
│   ├── appointment.py
│   ├── client.py
│   ├── digital_checklist.py
│   ├── expense.py
│   ├── expense_category.py
│   ├── hardware.py
│   ├── inventory.py
│   ├── operating_hour.py
│   ├── owner_reminder.py
│   ├── payment_method.py
│   ├── promotion.py
│   ├── service.py
│   ├── treatment_area.py
│   └── user.py
├── services/                  # Business logic services (e.g., AI/Chatbot)
│   ├── __init__.py
│   ├── ai_service.py          # AI/Chatbot integration
│   └── scheduler.py           # Background scheduler tasks (e.g., for reminders)
├── tests/
│   ├── __init__.py
│   ├── test_controllers.py
│   ├── test_models.py
│   └── test_services.py
├── utils/                     # Utility functions and helpers
│   ├── __init__.py
│   ├── constants.py           # Global constants
│   ├── date_helpers.py        # Date calculation helpers (e.g., visit spacing)
│   ├── message_helpers.py     # Message formatting for reminders (popups)
│   └── validation_helpers.py  # Input validation functions
├── views/                     # CustomTkinter UI components
│   ├── __init__.py
│   ├── components/            # Reusable UI widgets
│   │   ├── date_picker.py
│   │   └── table_widget.py
│   ├── appointment_view.py
│   ├── client_view.py
│   ├── finance_view.py
│   ├── hardware_view.py
│   ├── main_window.py         # Main application window structure
│   ├── reports_view.py
│   ├── service_view.py
│   └── settings_view.py       # View for application settings
├── LICENSE
├── README.md                  # This file
├── main.py                    # Application entry point
└── requirements.txt           # Python dependencies

```
---

## 🔧 Installation

1. **Clone the repository**

```bash
git clone https://github.com/MikeKorsikov/Laserowo.git
cd Laserowo
```

2. **Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```
---
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to propose.

---
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.