from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import UserInterface
from src.models.general.user_constants import UserRoles
from src.utils.messages import UserMessage
from src.utils.response import UJSONResponse

root_routes = APIRouter(prefix='/root', tags=['Root'])


@root_routes.post('/user')
def create_root_user(email: str):
    """
    Create a user root
    \f
    :param email: user email
    """
    user_found = UserInterface.find_one(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    try:
        user_found.update(role=UserRoles.ROOT)
        user_found.reload()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)

    return UJSONResponse(UserMessage.updated, HTTP_200_OK)
