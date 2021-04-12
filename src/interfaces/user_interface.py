from typing import Union

from src.models import User


class UserInterface:

    @staticmethod
    def find_one(email: str) -> Union[None, User]:
        return User.objects(email=email).first()
