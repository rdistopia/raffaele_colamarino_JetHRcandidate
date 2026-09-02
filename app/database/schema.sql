-- Schema SQLite per il database dei parametri Jet HR

CREATE TABLE IF NOT EXISTS global_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    inps_employee_rate REAL NOT NULL DEFAULT 0.0919,
    default_months INTEGER NOT NULL DEFAULT 13,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS irpef_brackets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bracket_order INTEGER NOT NULL,
    min_income REAL NOT NULL,
    max_income REAL,
    rate REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS regional_tax_brackets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL,
    bracket_order INTEGER NOT NULL,
    min_income REAL NOT NULL,
    max_income REAL,
    rate REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS municipal_tax_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    municipality_name TEXT UNIQUE NOT NULL,
    exemption_threshold REAL NOT NULL DEFAULT 23000.0,
    rate REAL NOT NULL DEFAULT 0.008
);

CREATE TABLE IF NOT EXISTS deductions_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    category TEXT NOT NULL DEFAULT 'lavoro_dipendente',
    base_max_deduction REAL NOT NULL DEFAULT 1955.0,
    tier1_limit REAL NOT NULL DEFAULT 15000.0,
    tier2_limit REAL NOT NULL DEFAULT 28000.0,
    tier3_limit REAL NOT NULL DEFAULT 50000.0,
    tier2_base REAL NOT NULL DEFAULT 1910.0,
    tier2_factor REAL NOT NULL DEFAULT 1190.0,
    bonus_25_35k REAL NOT NULL DEFAULT 65.0
);
