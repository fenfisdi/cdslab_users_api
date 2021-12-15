from .credentials import credential_routes
from .root import root_routes
from .user import user_routes

__all__ = [
    'user_routes',
    'credential_routes',
    'root_routes'
]
