import os
from flask import Flask
from .database.db import init_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "jet-hr-secret-prototype-key-2026"),
        DATABASE_PATH=os.environ.get("DATABASE_PATH", os.path.join(app.root_path, "database", "parameters.db")),
    )

    if test_config is not None:
        app.config.update(test_config)

    # Inizializza il database se non esiste
    with app.app_context():
        init_db(app.config["DATABASE_PATH"])

    # Registra i filtri Jinja personalizzati per la formattazione italiana (punto migliaia, virgola decimali)
    from .core.formatters import format_number_it, format_currency_it, format_percent_it
    app.jinja_env.filters["number_it"] = format_number_it
    app.jinja_env.filters["currency"] = format_currency_it
    app.jinja_env.filters["percent_it"] = format_percent_it

    # Registra i Blueprint
    from .routes import main_bp, admin_bp, api_bp, deploy_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(deploy_bp)

    return app
