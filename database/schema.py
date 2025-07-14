# schema.py

"""
Database schema definitions for the Laser Hair Removal Management Application
"""

# SQL table creation statements
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'regular')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CLIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT,
    date_of_birth DATE,
    is_blacklisted BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SERVICES_TABLE = """
CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT,
    base_price DECIMAL(10, 2),
    estimated_duration_minutes INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TREATMENT_AREAS_TABLE = """
CREATE TABLE IF NOT EXISTS treatment_areas (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_APPOINTMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    area_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients (client_id),
    FOREIGN KEY (service_id) REFERENCES services (service_id),
    FOREIGN KEY (area_id) REFERENCES treatment_areas (area_id)
);
"""

# List of all table creation statements
ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_CLIENTS_TABLE,
    CREATE_SERVICES_TABLE,
    CREATE_TREATMENT_AREAS_TABLE,
    CREATE_APPOINTMENTS_TABLE
]

# Sample data for initial setup
SAMPLE_SERVICES = [
    ("Laser Hair Removal - Face", "Facial hair removal treatment", 150.00, 30),
    ("Laser Hair Removal - Legs", "Full leg hair removal treatment", 300.00, 60),
    ("Laser Hair Removal - Arms", "Full arm hair removal treatment", 200.00, 45),
    ("Laser Hair Removal - Underarms", "Underarm hair removal treatment", 100.00, 15),
    ("Laser Hair Removal - Bikini", "Bikini area hair removal treatment", 180.00, 30)
]

SAMPLE_TREATMENT_AREAS = [
    ("Face",),
    ("Legs",),
    ("Arms",),
    ("Underarms",),
    ("Bikini",),
    ("Back",),
    ("Chest",)
]