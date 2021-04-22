from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)

from src.interfaces import UserInterface
from src.models import User, Credentials, NewUser, UpdateUser, SecurityQuestions
from src.utils.encoder import BsonObject
from src.utils.messages import UserMessage
from src.utils.response import UJSONResponse

user_routes = APIRouter(tags=['User'])


@user_routes.post('/user')
def create_user(user: NewUser):
    """
    Create a invalid user in database including its credentials and
    security questions.

    \f
    :param user: User input
    :return: UJSONResponse
    """
    user_found = UserInterface.find_one(email=user.email)
    if user_found:
        return UJSONResponse(UserMessage.exist, HTTP_400_BAD_REQUEST)

    user_dict = user.dict(
        exclude={'password', 'otp_code', 'security_questions'}
    )
    new_user = User(**user_dict)
    credential = Credentials(
        user=new_user,
        password=user.password,
        otp_code=user.otp_code
    )
    security_questions = SecurityQuestions(
        user=new_user,
        questions=[question.dict() for question in user.security_questions]
    )

    try:
        new_user.save()
        credential.save()
        security_questions.save()
    except Exception as error:
        return UJSONResponse(str(error), HTTP_400_BAD_REQUEST)
    return UJSONResponse(
        UserMessage.created,
        HTTP_201_CREATED,
        BsonObject.dict(new_user)
    )


@user_routes.get('/user/{email}/validate')
def validate_user(email: str):
    """
    Validate user if the state user is invalid, if is valid, will return
    user not found.

    \f
    :param email: email from the user to validate.
    """
    user_found = UserInterface.find_one_inactive(email=email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)
    user_found.is_active = True
    user_found.save()

    return UJSONResponse(UserMessage.validated, HTTP_200_OK)


@user_routes.get('/user/{email}')
def find_user(email: str, invalid: bool = False):
    """
    Find user in database, depends of invalid param, could be a valid or invalid
    user, if user did not exist, will return user not found.

    \f
    :param email: email from the user to find.
    :param invalid: if valid state user is valid or invalid.
    """
    if invalid:
        user = UserInterface.find_one_inactive(email)
    else:
        user = UserInterface.find_one_active(email)
    if not user:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(UserMessage.found, HTTP_200_OK, BsonObject.dict(user))


@user_routes.put('/user/{email}')
def update_user(email: str, user: UpdateUser):
    """
    Update data user information, except email and credentials information, all
    null fields will be ignored.

    \f
    :param email: email from the user to update.
    :param user: user data to update.
    """
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    user_found.update(**user.dict(exclude_none=True))
    user_found.save().reload()

    return UJSONResponse(
        UserMessage.updated,
        HTTP_200_OK,
        BsonObject.dict(user_found)
    )


@user_routes.delete('/user/{email}')
def delete_user(email: str):
    """
    Delete user data from database as logic field, if user has been deleted
    before, will return user not found or return user deleted successfully.

    \f
    :param email: email from the user to delete.
    """
    user_found = UserInterface.find_one_active(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    user_found.is_deleted = True
    user_found.save()
    return UJSONResponse(UserMessage.deleted, HTTP_200_OK)
