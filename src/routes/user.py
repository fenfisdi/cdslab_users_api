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
from src.models.general.user_constants import UserRoles

user_routes = APIRouter(tags=['User'])


@user_routes.post('/user')
def create_user(user: NewUser):
    """
    Create a invalid user in database including its credentials and
    security questions.

    \f
    :param user: User input
    """
    user_found = UserInterface.find_one(email=user.email)
    if user_found:
        return UJSONResponse(UserMessage.exist, HTTP_400_BAD_REQUEST)

    user_dict = user.dict(
        exclude={'password', 'otp_code', 'security_questions'}
    )
    new_user = User(**user_dict)
    new_user.role = user.role.value
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
    user_found = UserInterface.find_one(email=email, is_valid=False)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)
    user_found.is_valid = True
    user_found.save()

    return UJSONResponse(UserMessage.validated, HTTP_200_OK)


@user_routes.get('/user/{email}')
def find_user(email: str, is_valid: bool = True):
    """
    Find user in database, depends of invalid param, could be a valid or invalid
    user, if user did not exist, will return user not found.

    \f
    :param email: email from the user to find.
    :param is_valid: if valid state user is valid or invalid.
    """
    user = UserInterface.find_one(email, is_valid=is_valid)
    if not user:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    return UJSONResponse(UserMessage.found, HTTP_200_OK, BsonObject.dict(user))


@user_routes.get('/user')
def list_users(is_valid: bool = True, name: str = "", 
        email: str = "", role: UserRoles = None ):
    """
    return a list of users that satisfy the search parameters. 

    \f
    :param is_valid: Field that verifies that the user is valid.
    :param name: Name for the search
    :param email: Email for the search
    :param role: Role for the search
    """
    
    users = UserInterface.find_all(is_valid = is_valid, name = name, email = email, role = "" if role is None else role.value)
    if not users:
        return UJSONResponse(UserMessage.found, HTTP_200_OK, BsonObject.dict(users))

    return UJSONResponse(UserMessage.found, HTTP_200_OK, BsonObject.dict(users))


@user_routes.put('/user/{email}')
def update_user(email: str, user: UpdateUser):
    """
    Update data user information, except email and credentials information, all
    null fields will be ignored.

    \f
    :param email: email from the user to update.
    :param user: user data to update.
    """
    user_found = UserInterface.find_one(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)
    
    user.role = user.role.value
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
    user_found = UserInterface.find_one(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    user_found.is_deleted = True
    user_found.save()
    return UJSONResponse(UserMessage.deleted, HTTP_200_OK)


@user_routes.post('/user/{email}/disable')
def disable_user(email: str):
    """

    :param email:
    """
    user_found = UserInterface.find_one(email)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    user_found.is_enabled = False
    user_found.save()
    return UJSONResponse(UserMessage.disabled, HTTP_200_OK)


@user_routes.post('/user/{email}/enable')
def enable_user(email: str):
    """

    :param email:
    """
    user_found = UserInterface.find_one(email, is_enabled=False)
    if not user_found:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    user_found.is_enabled = True
    user_found.save()
    return UJSONResponse(UserMessage.enabled, HTTP_200_OK)
