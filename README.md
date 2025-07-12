# --- README.md ---
# Laser Salon Manager
A modular desktop app for managing a laser salon's clients, appointments, services, and finances.

## Project Structure
laser_business_app/
├── main.py
├── config/
│   ├── __init__.py
│   ├── database.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── client.py
│   ├── appointment.py
│   ├── service.py
│   ├── expense.py
│   └── user.py               # For access control or audit
├── controllers/
│   ├── __init__.py
│   ├── client_controller.py
│   ├── appointment_controller.py
│   ├── finance_controller.py
│   └── service_controller.py
├── views/
│   ├── __init__.py
│   ├── main_window.py
│   ├── client_view.py
│   ├── appointment_view.py
│   ├── finance_view.py
│   └── service_view.py
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── data_import.py
│   ├── scheduler.py          # Setup and job definitions
│   └── validation.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── constants.py
├── data/
│   ├── database.db
│   └── imports/
├── assets/
│   ├── icons/
│   └── styles/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_services.py
├── requirements.txt
└── README.md

## Stack
- Python + Tkinter + ttkbootstrap
- SQLite + SQLAlchemy
- APScheduler
- OpenAI GPT integration (planned)

## Run
```bash
python main.py
```