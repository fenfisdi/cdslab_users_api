from typing import Union

from src.models import User


class UserInterface:

    @staticmethod
    def find_one(email: str) -> Union[None, User]:
        filters = dict(
            email=email,
            is_valid=True,
            is_deleted=False,
        )
        return User.objects(**filters).first()

    @staticmethod
    def find_one_invalid(email: str) -> Union[None, User]:
        filters = dict(
            email=email,
            is_valid=False,
            is_deleted=False,
        )
        return User.objects(**filters).first()
