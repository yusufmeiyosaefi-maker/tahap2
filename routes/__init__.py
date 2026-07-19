# routes/__init__.py
from .main_routes import bp as main_bp
from .admin_routes import bp as admin_bp
from .api_routes import bp as api_bp

__all__ = ['main_bp', 'admin_bp', 'api_bp']