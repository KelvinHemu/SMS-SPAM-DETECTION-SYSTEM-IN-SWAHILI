"""
API Endpoints Package
FastAPI routers for different endpoint groups
"""

from . import analysis, health, admin

__all__ = ["analysis", "health", "admin"] 