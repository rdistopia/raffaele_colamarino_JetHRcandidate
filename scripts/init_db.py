#!/usr/bin/env python3
"""
Script standalone per inizializzare o resettare il database SQLite dei parametri.
Uso:
    python scripts/init_db.py
    python scripts/init_db.py --reset
"""

import sys
import os

# Aggiunge la root del repository al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.db import init_db, reset_db_to_seed, get_db_path

def main():
    db_path = get_db_path()
    if "--reset" in sys.argv:
        print(f"Ripristino database ai valori predefiniti seed in: {db_path}...")
        reset_db_to_seed(db_path)
        print("Database ripristinato con successo.")
    else:
        print(f"Inizializzazione database in: {db_path}...")
        init_db(db_path)
        print("Database inizializzato con successo.")

if __name__ == "__main__":
    main()
