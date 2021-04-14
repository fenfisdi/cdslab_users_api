from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import UserInterface, CredentialInterface
from src.models import UserCredentials
from src.utils.messages import UserMessage, CredentialMessage
from src.utils.response import UJSONResponse

credential_routes = APIRouter()


@credential_routes.post('/user/credentials')
def validate_credentials(user: UserCredentials):
    user_found = UserInterface.find_one(user.email)
    if not user_found:
        return UJSONResponse(UserMessage.exist, HTTP_404_NOT_FOUND)

    credentials = CredentialInterface.find_one(user_found)
    if not credentials:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)

    if credentials.password != user.password:
        return UJSONResponse(CredentialMessage.invalid, HTTP_400_BAD_REQUEST)
    return UJSONResponse(CredentialMessage.logged, HTTP_200_OK)
