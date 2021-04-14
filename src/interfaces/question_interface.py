from typing import Union

from src.models.db_models.user import SecurityQuestions
from src.models.db_models.user import User


class QuestionInterface:

    @staticmethod
    def find_one(user: User) -> Union[None, SecurityQuestions]:
        filters = dict(
            user=user
        )
        return SecurityQuestions.objects(**filters).first()
