from typing import Union

from src.models.db_models.user import SecurityQuestions
from src.models.db_models.user import User


class QuestionInterface:
    '''
        Interface to consult question in DB
    '''
    @staticmethod
    def find_one(user: User) -> Union[None, SecurityQuestions]:
        filters = dict(
            user=user
        )
        '''
        Find the credentials of a user

        \f
        :param user: user information
        '''
        return SecurityQuestions.objects(**filters).first()
