from .credentials import credential_routes
from .roles import role_routes
from .user import user_routes

__all__ = [
    'user_routes',
    'credential_routes',
    'role_routes'
]
