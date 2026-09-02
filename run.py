#!/usr/bin/env python3
"""
Entrypoint per avviare l'applicazione in ambiente di sviluppo locale.
Uso:
    python run.py
"""

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    print(f"Avvio del server di sviluppo Jet HR su http://127.0.0.1:{port} (debug={debug})")
    app.run(host="127.0.0.1", port=port, debug=debug)
