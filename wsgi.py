"""
WSGI Entrypoint per il deployment su PythonAnywhere o server WSGI (Gunicorn/uWSGI).
"""

import sys
import os

# Aggiunge la directory corrente al path per garantire la corretta risoluzione dei moduli
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import create_app

# PythonAnywhere si aspetta la variabile 'application'
application = create_app()

if __name__ == "__main__":
    application.run()
