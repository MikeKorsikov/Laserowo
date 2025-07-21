-- Initial schema migration for laser hair removal application
-- Version: 001
-- Date: 2025-07-21

CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    dob TEXT CHECK (length(dob) = 10), -- YYYY-MM-DD format
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    duration INTEGER NOT NULL CHECK (duration > 0)
);

CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    appointment_date TEXT NOT NULL CHECK (length(appointment_date) = 10), -- YYYY-MM-DD
    session_number INTEGER NOT NULL CHECK (session_number > 0),
    power REAL,
    amount REAL NOT NULL CHECK (amount >= 0),
    appointment_status TEXT NOT NULL DEFAULT 'Scheduled' CHECK (appointment_status IN ('Scheduled', 'Completed', 'Cancelled')),
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE RESTRICT
);

CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    date TEXT NOT NULL CHECK (length(date) = 10), -- YYYY-MM-DD
    tax_deductible INTEGER NOT NULL CHECK (tax_deductible IN (0, 1)) DEFAULT 0
);

CREATE TABLE inventory (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL UNIQUE,
    current_quantity REAL NOT NULL CHECK (current_quantity >= 0),
    unit TEXT NOT NULL,
    low_stock_threshold REAL NOT NULL CHECK (low_stock_threshold >= 0)
);

CREATE TABLE hardware (
    hardware_id INTEGER PRIMARY KEY,
    total_impulses_recorded INTEGER NOT NULL CHECK (total_impulses_recorded >= 0) DEFAULT 0,
    last_maintenance_date TEXT CHECK (length(last_maintenance_date) = 10), -- YYYY-MM-DD
    next_maintenance_due_date TEXT CHECK (length(next_maintenance_due_date) = 10), -- YYYY-MM-DD
    last_insurance_date TEXT CHECK (length(last_insurance_date) = 10), -- YYYY-MM-DD
    next_insurance_date TEXT CHECK (length(next_insurance_date) = 10) -- YYYY-MM-DD
);

CREATE TABLE reminders (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL CHECK (entity_type IN ('maintenance', 'inventory', 'expense')),
    entity_id INTEGER NOT NULL,
    due_date TEXT NOT NULL CHECK (length(due_date) = 10), -- YYYY-MM-DD
    is_active INTEGER NOT NULL CHECK (is_active IN (0, 1)) DEFAULT 1,
    FOREIGN KEY (entity_id) REFERENCES hardware(hardware_id) ON DELETE CASCADE
    -- Additional foreign keys can be added for inventory/expense as needed
);

-- Indexes for performance
CREATE INDEX idx_appointments_client_id ON appointments(client_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_expenses_date ON expenses(date);
CREATE INDEX idx_inventory_name ON inventory(item_name);
CREATE INDEX idx_reminders_due_date ON reminders(due_date);

-- Initial data (optional, can be moved to a seed script)
INSERT INTO services (name, price, duration) VALUES
    ('Full Legs', 150.0, 60),
    ('Bikini Line', 80.0, 30);