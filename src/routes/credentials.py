from typing import List

from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import UserInterface, CredentialInterface, QuestionInterface
from src.models import UserCredentials
from src.models.db_models.user import Question
from src.models.route_models.user import SecurityQuestion
from src.utils.encoder import BsonObject
from src.utils.messages import UserMessage, CredentialMessage, QuestionMessage
from src.utils.response import UJSONResponse

credential_routes = APIRouter(tags=['Credentials'])


@credential_routes.post('/user/credentials')
def validate_credentials(user: UserCredentials):
    user_found = UserInterface.find_one(user.email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    credentials = CredentialInterface.find_one(user_found)
    if not credentials:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)

    if credentials.password != user.password:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)
    data = {'otp_code': credentials.otp_code}
    return UJSONResponse(CredentialMessage.logged, HTTP_200_OK, data)


@credential_routes.get('/user/{email}/questions')
def find_security_questions(email: str):
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    security_question = QuestionInterface.find_one(user_found)
    if not security_question:
        return UJSONResponse(QuestionMessage.not_found, HTTP_400_BAD_REQUEST)
    data = [BsonObject.dict(q) for q in security_question.questions]
    return UJSONResponse(
        QuestionMessage.found,
        HTTP_200_OK,
        data
    )


@credential_routes.post('/user/{email}/questions')
def set_security_questions(email: str, questions: List[SecurityQuestion]):
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    security_question = QuestionInterface.find_one(user_found)
    if not security_question:
        return UJSONResponse(QuestionMessage.not_found, HTTP_400_BAD_REQUEST)

    security_question.questions = [
        Question(**question.dict()) for question in questions
    ]
    try:
        security_question.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(
        QuestionMessage.updated,
        HTTP_200_OK
    )


@credential_routes.post('/user/password')
def update_password(user: UserCredentials):
    user_found = UserInterface.find_one_active(user.email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    credentials = CredentialInterface.find_one(user_found)
    if not credentials:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)

    credentials.password = user.password
    try:
        credentials.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(CredentialMessage.pass_updated, HTTP_200_OK)


@credential_routes.post('/user/{email}/security_code')
def set_security_code(email: str, code: str):
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    credentials = CredentialInterface.find_one(user_found)
    if not credentials:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)

    credentials.security_code = code.strip()
    try:
        credentials.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(CredentialMessage.code_updated, HTTP_200_OK)


@credential_routes.get('/user/{email}/security_code')
def get_security_code(email: str):
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    credentials = CredentialInterface.find_one(user_found)
    if not credentials:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)

    data = {
        'security_code': credentials.security_code,
    }
    return UJSONResponse(CredentialMessage.code_found, HTTP_200_OK, data)
