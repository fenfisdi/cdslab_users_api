from typing import Union

from src.models import User


class UserInterface:

    @staticmethod
    def find_one(email: str) -> Union[None, User]:
        filters = dict(
            email=email,
        )
        return User.objects(**filters).first()

    @staticmethod
    def find_one_active(email: str) -> Union[None, User]:
        filters = dict(
            email=email,
            is_active=True,
            is_deleted=False,
        )
        return User.objects(**filters).first()

    @staticmethod
    def find_one_inactive(email: str) -> Union[None, User]:
        filters = dict(
            email=email,
            is_active=False,
            is_deleted=False,
        )
        return User.objects(**filters).first()
