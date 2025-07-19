-- Initial schema for the laser hair removal business application database
-- Creating tables based on the revised requirements for Phase 1 (Desktop, macOS)
-- Ensuring GDPR compliance with encrypted storage (handled by SQLCipher in db_setup.py)

-- Table: clients 
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT,
    dob DATE,
    is_blacklisted BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT
);

-- Table: appointments
CREATE TABLE appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    area_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    session_number_for_area INTEGER NOT NULL,
    power DECIMAL,
    appointment_status TEXT NOT NULL CHECK (appointment_status IN ('Scheduled', 'Completed', 'Cancelled', 'Rescheduled')),
    amount DECIMAL,
    payment_method_id INTEGER NOT NULL,
    next_suggested_appointment_date DATETIME,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (area_id) REFERENCES treatment_areas(area_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Table: services
CREATE TABLE services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT,
    price DECIMAL NOT NULL,
    duration_minutes INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Table: expenses
CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date DATE NOT NULL,
    amount DECIMAL NOT NULL CHECK (amount >= 0),
    description TEXT,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES expense_categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Table: expense_categories
CREATE TABLE expense_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    is_tax_deductible BOOLEAN DEFAULT FALSE
);

-- Table: promotions (Phase 2, included as placeholder)
CREATE TABLE promotions (
    promotion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    promotion_name TEXT NOT NULL,
    promotion_type TEXT,
    discount_value DECIMAL,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    target_categories TEXT
);

-- Table: operating_hours
CREATE TABLE operating_hours (
    day_of_week_id INTEGER PRIMARY KEY,
    day_of_week TEXT NOT NULL,
    start_time TIME,
    end_time TIME,
    is_closed BOOLEAN DEFAULT FALSE
);

-- Table: inventory
CREATE TABLE inventory (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    current_quantity DECIMAL NOT NULL CHECK (current_quantity >= 0),
    unit TEXT NOT NULL,
    low_stock_threshold DECIMAL DEFAULT 10
);

-- Table: users (Single admin user)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

-- Table: treatment_areas
CREATE TABLE treatment_areas (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT NOT NULL,
    default_price DECIMAL,
    estimated_duration_minutes INTEGER
);

-- Table: payment_methods
CREATE TABLE payment_methods (
    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name TEXT NOT NULL
);

-- Table: hardware
CREATE TABLE hardware (
    hardware_id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_name TEXT NOT NULL,
    purchase_date DATE,
    last_maintenance_date DATE,
    next_maintenance_due_date DATE,
    last_insurance_date DATE,
    next_insurance_due_date DATE,
    maximum_impulses_on_purchase INTEGER,
    total_impulses_recorded INTEGER CHECK (total_impulses_recorded <= maximum_impulses_on_purchase)
);

-- Table: digital_checklists
CREATE TABLE digital_checklists (
    checklist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    checklist_date DATE NOT NULL,
    questions TEXT, -- JSON field for dynamic questions
    is_completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Table: owner_reminders
CREATE TABLE owner_reminders (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reminder_type TEXT NOT NULL,
    related_id INTEGER,
    due_date DATE NOT NULL,
    reminder_date DATE NOT NULL,
    message TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    delivery_method TEXT NOT NULL CHECK (delivery_method IN ('Popup', 'SMS', 'Email'))
);

-- Indexes for frequently queried columns
CREATE INDEX idx_clients_full_name ON clients(full_name);
CREATE INDEX idx_appointments_client_id ON appointments(client_id);
CREATE INDEX idx_appointments_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_expenses_expense_date ON expenses(expense_date);