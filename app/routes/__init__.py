"""
Flask Blueprint routes package.
"""

from .main_routes import main_bp
from .admin_routes import admin_bp
from .api_routes import api_bp
from .deploy_webhook import deploy_bp

__all__ = ["main_bp", "admin_bp", "api_bp", "deploy_bp"]
