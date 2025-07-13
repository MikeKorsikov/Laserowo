# 💼 Laser Business Desktop App

A desktop application built for managing a laser salon business. It supports appointment scheduling, client management, service tracking, and expense monitoring with a clean UI and modular architecture.

---

## 💻 Tech Stack

- **👩‍🎨 GUI**: Tkinter with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for modern styling  
- **🗃️ Database**: SQLite (local storage)  
- **🧩 ORM**: SQLAlchemy  
- **📊 Excel Integration**: pandas *(planned in later phase)*  
- **🤖 AI Integration**: OpenAI API (GPT-4 for chatbot features)  
- **⏱️ Task Scheduling**: APScheduler (background jobs)  
- **🏗️ Architecture**: Modular MVC pattern (Models, Views, Controllers)

---

## ✨ Features (Phase 1)

- 🧑‍💼 Client management  
- 📅 Appointment tracking  
- 💰 Service and expense modeling  
- 🧱 Scalable folder structure for future phases  
- 🧠 AI integration module *(placeholder)*  
- ⏳ Background scheduler setup *(placeholder)*

---

## 📂 Project Structure

```plaintext
laser_business_app/
├── main.py                 # Application entry point
├── config/
│   ├── __init__.py
│   ├── database.py         # SQLAlchemy DB engine setup
│   └── settings.py         # App-wide constants & config
├── models/
│   ├── __init__.py
│   ├── client.py           # Client table definition
│   ├── appointment.py      # Appointment table
│   ├── service.py          # Services offered
│   └── expense.py          # Business expenses
├── controllers/
│   ├── __init__.py
│   ├── client_controller.py
│   ├── appointment_controller.py
│   ├── finance_controller.py
│   └── service_controller.py
├── views/
│   ├── __init__.py
│   ├── main_window.py      # Base GUI setup (ttkbootstrap)
│   ├── client_view.py
│   ├── appointment_view.py
│   ├── finance_view.py
│   └── service_view.py
├── services/
│   ├── __init__.py
│   ├── ai_service.py       # GPT-4 chatbot integration (stub)
│   └── scheduler.py        # APScheduler tasks (stub)
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # Reusable utility functions
│   └── constants.py        # App constants (e.g., status, labels)
├── data/
│   ├── database.db         # SQLite local DB file
│   └── imports/            # Excel files (future)
├── assets/
│   ├── icons/              # App icons
│   └── styles/             # ttkbootstrap styles/themes
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_services.py
├── requirements.txt        # List of Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Git exclusions

---

## 🔧 Installation

1. **Clone the repository**

```bash
git clone https://github.com/MikeKorsikov/Laserowo.git
cd Laserowo


2. **Create and activate a virtual environment**
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


3. **Install dependencies**
pip install -r requirements.txt


4. **Run the application**
python main.py
