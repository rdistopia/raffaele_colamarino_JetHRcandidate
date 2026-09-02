#!/bin/bash
# ==============================================================================
# Script di aggiornamento rapido e reload per PythonAnywhere
# Uso: bash scripts/update_pythonanywhere.sh
# ==============================================================================

set -e

echo "=== 1. Pulling latest code from GitHub ==="
git pull origin main

echo "=== 2. Ensuring dependencies are installed ==="
pip install -r requirements.txt --quiet

echo "=== 3. Inizializzazione Database SQLite se necessario ==="
python3 scripts/init_db.py

echo "=== 4. Reload Web App (touch wsgi file) ==="
# Sostituisci con il percorso del tuo file wsgi su PythonAnywhere, es:
# touch /var/www/<username>_pythonanywhere_com_wsgi.py
if [ -n "$WSGI_FILE_PATH" ]; then
    touch "$WSGI_FILE_PATH"
    echo "Reload eseguito con successo su: $WSGI_FILE_PATH"
else
    touch wsgi.py
    echo "Reload eseguito su wsgi.py locale"
fi

echo "=== Deploy completato con successo! ==="
