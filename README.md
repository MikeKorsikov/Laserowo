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

├── P1_DESKTOP_APP/
│   ├── config.py             # Global application configurations and settings.
│   ├── main.py               # The main application entry point.
│   ├── database/             # Database management (SQLite initially).
│   │   ├── db_manager.py     # Handles database operations.
│   │   └── schema.py         # Defines the database table schemas (in English).
│   ├── ui/                   # User Interface components.
│   │   ├── main_window.py    # Defines the main application window and its layout.
│   │   └── placeholders.py   # Simple placeholder views for modules under development.
│   ├── services/             # Business logic and application services.
│   │   ├── __init__.py       # Makes 'services' a Python package.
│   │   └── client_service.py # Example: Service layer for client-related operations.
│   ├── data_loader/          # Handles initial data load from CSV files into the DB.
│   │   └── csv_loader.py     # Script to parse and load CSV data.
│   │   └── csv_files/        # Directory for initial CSV data files.
│   └── models/               # Python classes representing database entities.
│       └── __init__.py       # Makes 'models' a Python package.
└── README.md                 # This documentation file.
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