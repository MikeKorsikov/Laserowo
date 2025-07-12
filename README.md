# 💡 Laser Business Desktop App

A desktop application built for managing a laser salon business. It supports appointment scheduling, client management, service tracking, and expense monitoring with a clean UI and modular architecture.

---

## 🛠 Tech Stack

- **GUI**: Tkinter with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for modern styling
- **Database**: SQLite (local storage)
- **ORM**: SQLAlchemy
- **Excel Integration**: pandas (planned in later phase)
- **AI Integration**: OpenAI API (GPT-4 for chatbot features)
- **Task Scheduling**: APScheduler (background jobs)
- **Architecture**: Modular MVC pattern (Models, Views, Controllers)

---

## 🚀 Features (Phase 1)

- 📋 Client management
- 🗓 Appointment tracking
- 💼 Service and expense modeling
- 🧱 Scalable folder structure for future phases
- 💬 AI integration module (placeholder)
- 📅 Background scheduler setup (placeholder)

---

## 📂 Project Structure

```plaintext
laser_business_app/
├── main.py                 # Application entry point
│
├── config/
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy DB engine setup
│   └── settings.py         # App-wide constants & config
│
├── models/
│   ├── __init__.py
│   ├── client.py           # Client table definition
│   ├── appointment.py      # Appointment table
│   ├── service.py          # Services offered
│   └── expense.py          # Business expenses
│
├── controllers/
│   ├── __init__.py
│   └── client_controller.py# Business logic for clients
│
├── views/
│   ├── __init__.py
│   └── main_window.py      # Base GUI setup (ttkbootstrap)
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py       # GPT-4 chatbot integration (stub)
│   └── scheduler.py        # APScheduler tasks (stub)
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # Reusable utility functions
│   └── constants.py        # App constants (e.g., status, labels)
│
├── data/
│   ├── database.db         # SQLite local DB file
│   └── imports/            # Excel files (future)
│
├── assets/
│   ├── icons/              # App icons
│   └── styles/             # ttkbootstrap styles/themes
│
├── requirements.txt        # List of Python dependencies
└── README.md               # Project documentation
