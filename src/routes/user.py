from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import UserInterface
from src.models import User, Credentials, NewUser
from src.utils.messages import UserMessage
from src.utils.response import UJSONResponse

user_routes = APIRouter()


@user_routes.post('/user')
def create_user(user: NewUser):
    user_found = UserInterface.find_one(email=user.email)
    if user_found:
        return UJSONResponse(UserMessage.exist, HTTP_400_BAD_REQUEST)

    user_dict = user.dict(exclude={'password'})
    new_user = User(**user_dict)
    credential = Credentials(user=new_user, password=user.password)

    try:
        new_user.save()
        credential.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    # TODO: Return User Information
    return UJSONResponse(UserMessage.created, HTTP_201_CREATED)


@user_routes.get('/user/{email}')
def find_user(email: str):
    user = UserInterface.find_one(email)
    if not user:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)
    # TODO: Return User Information
    return UJSONResponse(UserMessage.found, HTTP_200_OK)
