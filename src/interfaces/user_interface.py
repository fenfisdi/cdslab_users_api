from typing import Optional

from mongoengine.queryset.visitor import Q

from src.models import User
from src.models.general.user_constants import UserRoles


class UserInterface:
    '''
        Interface to consult Users in DB
    '''
    @staticmethod
    def find_one(
        email: str,
        is_enabled: bool = True,
        is_valid: bool = True
    ) -> Optional[User]:
        '''
        search for a user

        :param email: user email
        :param  is_enabled: user status
        :param  is_valid: user valid
        '''
        filters = dict(
            email=email,
            is_enabled=is_enabled,
            is_valid=is_valid,
            is_deleted=False
        )
        return User.objects(**filters).first()

    @classmethod
    def find_all(
        cls,
        is_enabled: bool = True,
        is_valid: bool = True,
        name: Optional[str] = None,
        role: UserRoles = UserRoles.USER
    ):
        '''
        find all matching users

        :param is_enabled: user status
        :param is_valid: user valid
        :param name: user name
        :param role: user role
            
        '''
        filters = dict(
            is_enabled=is_enabled,
            is_valid=is_valid,
            is_deleted=False,
            role=role,
        )
        if name:
            name_q = dict(
                **filters,
                name__icontains=name,
            )
            last_name_q = dict(
                **filters,
                last_name__icontains=name,
            )
            email_q = dict(
                **filters,
                email__icontains=name,
            )
            query = Q(**name_q) | Q(**last_name_q) | Q(**email_q)
            return User.objects(query)
        return User.objects(**filters).all()
