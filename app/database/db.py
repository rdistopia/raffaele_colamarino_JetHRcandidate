import os
import json
import sqlite3
from typing import Dict, Any, List, Optional

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(DB_DIR, "parameters.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")
SEED_PATH = os.path.join(DB_DIR, "seed_data.json")

def get_db_path() -> str:
    return os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)

def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path: Optional[str] = None) -> None:
    path = db_path or get_db_path()
    conn = get_db_connection(path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()

    # Se le tabelle sono vuote, popola con i dati seed
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM global_settings")
    if cur.fetchone()[0] == 0:
        populate_from_seed(conn)
    conn.close()

def populate_from_seed(conn: sqlite3.Connection) -> None:
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. global_settings
    g = data["global_settings"]
    conn.execute(
        "INSERT OR REPLACE INTO global_settings (id, inps_employee_rate, default_months) VALUES (1, ?, ?)",
        (g["inps_employee_rate"], g["default_months"])
    )

    # 2. irpef_brackets
    conn.execute("DELETE FROM irpef_brackets")
    for b in data["irpef_brackets"]:
        conn.execute(
            "INSERT INTO irpef_brackets (bracket_order, min_income, max_income, rate) VALUES (?, ?, ?, ?)",
            (b["bracket_order"], b["min_income"], b["max_income"], b["rate"])
        )

    # 3. regional_tax_brackets
    conn.execute("DELETE FROM regional_tax_brackets")
    for r in data["regional_tax_brackets"]:
        conn.execute(
            "INSERT INTO regional_tax_brackets (region_name, bracket_order, min_income, max_income, rate) VALUES (?, ?, ?, ?, ?)",
            (r["region_name"], r["bracket_order"], r["min_income"], r["max_income"], r["rate"])
        )

    # 4. municipal_tax_settings
    conn.execute("DELETE FROM municipal_tax_settings")
    for m in data["municipal_tax_settings"]:
        conn.execute(
            "INSERT INTO municipal_tax_settings (municipality_name, exemption_threshold, rate) VALUES (?, ?, ?)",
            (m["municipality_name"], m["exemption_threshold"], m["rate"])
        )

    # 5. deductions_settings
    d = data["deductions_settings"]
    conn.execute(
        """INSERT OR REPLACE INTO deductions_settings 
           (id, category, base_max_deduction, tier1_limit, tier2_limit, tier3_limit, tier2_base, tier2_factor, bonus_25_35k) 
           VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (d["category"], d["base_max_deduction"], d["tier1_limit"], d["tier2_limit"], d["tier3_limit"],
         d["tier2_base"], d["tier2_factor"], d["bonus_25_35k"])
    )
    conn.commit()

def reset_db_to_seed(db_path: Optional[str] = None) -> None:
    path = db_path or get_db_path()
    conn = get_db_connection(path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    populate_from_seed(conn)
    conn.close()

def get_calculation_parameters(
    region: str = "Lombardia",
    municipality: str = "Milano",
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    path = db_path or get_db_path()
    if not os.path.exists(path):
        init_db(path)

    conn = get_db_connection(path)
    cur = conn.cursor()

    # global
    cur.execute("SELECT inps_employee_rate, default_months FROM global_settings WHERE id = 1")
    g_row = cur.fetchone()
    inps_rate = g_row["inps_employee_rate"] if g_row else 0.0919
    default_months = g_row["default_months"] if g_row else 13

    # irpef
    cur.execute("SELECT id, bracket_order, min_income, max_income, rate FROM irpef_brackets ORDER BY bracket_order ASC")
    irpef = [dict(row) for row in cur.fetchall()]

    # regional
    cur.execute(
        "SELECT id, region_name, bracket_order, min_income, max_income, rate FROM regional_tax_brackets WHERE region_name = ? ORDER BY bracket_order ASC",
        (region,)
    )
    regional = [dict(row) for row in cur.fetchall()]

    # municipal
    cur.execute(
        "SELECT exemption_threshold, rate FROM municipal_tax_settings WHERE municipality_name = ?",
        (municipality,)
    )
    m_row = cur.fetchone()
    municipal_settings = {
        "threshold": m_row["exemption_threshold"] if m_row else 23000.0,
        "rate": m_row["rate"] if m_row else 0.008
    }

    # deductions
    cur.execute("SELECT * FROM deductions_settings WHERE id = 1")
    d_row = cur.fetchone()
    deductions = dict(d_row) if d_row else {
        "base_max_deduction": 1955.0,
        "tier1_limit": 15000.0,
        "tier2_limit": 28000.0,
        "tier3_limit": 50000.0,
        "tier2_base": 1910.0,
        "tier2_factor": 1190.0,
        "bonus_25_35k": 65.0
    }

    conn.close()

    return {
        "inps_employee_rate": inps_rate,
        "default_months": default_months,
        "irpef_brackets": irpef,
        "regional_brackets": regional,
        "municipal_settings": municipal_settings,
        "deductions_settings": deductions
    }

def update_calculation_parameters(data: Dict[str, Any], db_path: Optional[str] = None) -> None:
    path = db_path or get_db_path()
    conn = get_db_connection(path)

    if "inps_employee_rate" in data:
        rate = float(data["inps_employee_rate"])
        months = int(data.get("default_months", 13))
        conn.execute(
            "UPDATE global_settings SET inps_employee_rate = ?, default_months = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1",
            (rate, months)
        )

    if "municipal_rate" in data or "municipal_threshold" in data:
        cur = conn.cursor()
        cur.execute("SELECT exemption_threshold, rate FROM municipal_tax_settings WHERE municipality_name = 'Milano'")
        curr_m = cur.fetchone()
        t = float(data.get("municipal_threshold", curr_m["exemption_threshold"] if curr_m else 23000.0))
        r = float(data.get("municipal_rate", curr_m["rate"] if curr_m else 0.008))
        conn.execute(
            "UPDATE municipal_tax_settings SET exemption_threshold = ?, rate = ? WHERE municipality_name = 'Milano'",
            (t, r)
        )

    if "irpef_brackets" in data:
        for b in data["irpef_brackets"]:
            conn.execute(
                "UPDATE irpef_brackets SET min_income = ?, max_income = ?, rate = ? WHERE id = ?",
                (b["min_income"], b["max_income"], b["rate"], b["id"])
            )

    if "regional_brackets" in data:
        for r in data["regional_brackets"]:
            conn.execute(
                "UPDATE regional_tax_brackets SET min_income = ?, max_income = ?, rate = ? WHERE id = ?",
                (r["min_income"], r["max_income"], r["rate"], r["id"])
            )

    conn.commit()
    conn.close()
