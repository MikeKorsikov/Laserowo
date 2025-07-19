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

├laser_hair_removal_app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── client_manager.py
│   │   ├── appointment_manager.py
│   │   ├── finance_manager.py
│   │   ├── inventory_manager.py
│   │   ├── hardware_manager.py
│   │   ├── reminder_manager.py
│   │   └── reporting.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_setup.py
│   │   ├── db_operations.py
│   │   └── migrations/
│   │       └── init_schema.sql
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── client_view.py
│   │   ├── appointment_view.py
│   │   ├── finance_view.py
│   │   ├── inventory_view.py
│   │   ├── hardware_view.py
│   │   └── report_view.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── csv_importer.py
│   │   ├── email_sender.py
│   │   ├── sms_sender.py
│   │   └── calendar_sync.py
│   └── models/
│       ├── __init__.py
│       ├── client.py
│       ├── appointment.py
│       ├── service.py
│       ├── expense.py
│       ├── inventory.py
│       ├── hardware.py
│       ├── reminder.py
│       └── treatment_area.py
├── data/
│   ├── database.db
│   └── imports/
│       └── clients.csv
├── config/
│   ├── app_config.yaml
│   └── secrets.yaml
├── tests/
│   ├── __init__.py
│   ├── test_client_manager.py
│   ├── test_appointment_manager.py
│   ├── test_finance_manager.py
│   └── test_db_operations.py
├── requirements.txt
├── README.md
└── setup.py
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