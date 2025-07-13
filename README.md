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
Laserowo/
├── main.py                 # Application entry point
├── config/
│   ├── database.py         # SQLAlchemy DB engine setup
│   └── settings.py         # App-wide constants & config
├── models/
│   ├── client.py           # Client table definition
│   ├── appointment.py      # Appointment table
│   ├── service.py          # Services offered
│   └── expense.py          # Business expenses
├── controllers/
│   ├── client_controller.py
│   ├── appointment_controller.py
│   ├── finance_controller.py
│   └── service_controller.py
├── views/
│   ├── main_window.py      # Base GUI setup
│   ├── client_view.py
│   ├── appointment_view.py
│   ├── finance_view.py
│   └── service_view.py
├── services/
│   ├── ai_service.py       # GPT-4 chatbot integration (stub)
│   └── scheduler.py        # APScheduler background tasks
├── utils/
│   ├── helpers.py          # Reusable utility functions
│   └── constants.py        # App constants
├── data/
│   ├── database.db         # SQLite local DB file
│   └── imports/            # Excel files (future)
├── assets/
│   ├── icons/              # App icons
│   └── styles/             # ttkbootstrap themes
├── tests/
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_services.py
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Git exclusions

```
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
```
---
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to propose.

---
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.