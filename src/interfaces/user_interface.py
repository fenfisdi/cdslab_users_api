from typing import Optional

from src.models import User


class UserInterface:

    @staticmethod
    def find_one(
        email: str,
        is_enabled: bool = True,
        is_valid: bool = True
    ) -> Optional[User]:
        filters = dict(
            email=email,
            is_enabled=is_enabled,
            is_valid=is_valid,
            is_deleted=False
        )
        return User.objects(**filters).first()

    @classmethod
    def find_all(cls, is_enabled: bool = True, is_valid: bool = True):
        filters = dict(
            is_enabled=is_enabled,
            is_valid=is_valid,
            is_deleted=False
        )
        return User.objects(**filters).all()
