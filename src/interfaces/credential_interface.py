from typing import Union

from src.models import Credentials, User


class CredentialInterface:
    '''
        Interface to consult credencials in DB
    '''
    @staticmethod
    def find_one(user: User) -> Union[None, Credentials]:
        filters = dict(
            user=user
        )
        '''
        Find the credentials of a user

        :param user: User Data
        '''
        return Credentials.objects(**filters).first()
