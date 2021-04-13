from typing import Union

from src.models import Credentials, User


class CredentialInterface:

    @staticmethod
    def find_one(user: User) -> Union[None, Credentials]:
        filters = dict(
            user=user
        )
        return Credentials.objects(**filters).first()
