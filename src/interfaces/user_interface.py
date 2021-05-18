from typing import Optional

from mongoengine.queryset.visitor import Q

from src.models import User
from src.models.general.user_constants import UserRoles


class UserInterface:

    @staticmethod
    def find_one(
        email: str,
        is_enabled: bool = True,
        is_valid: bool = True
    ) -> Optional[User]:
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
