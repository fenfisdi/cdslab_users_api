from mongoengine import (
    BooleanField,
    DateField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EnumField,
    IntField,
    ReferenceField,
    StringField
)

from .base import BaseDocument
from ..general.user_constants import UserRoles


class User(BaseDocument):
    name = StringField()
    last_name = StringField()
    email = StringField(unique=True)
    phone = IntField()
    phone_prefix = StringField()
    institution = StringField()
    institution_role = StringField()
    profession = StringField()
    gender = StringField()
    birthday = DateField()
    role = EnumField(UserRoles)
    is_deleted = BooleanField(default=False)
    is_valid = BooleanField(default=False)
    is_enabled = BooleanField(default=True)
    notify_removal = BooleanField(default=True)
    notify_simulation_done = BooleanField(default=True)


class Question(EmbeddedDocument):
    question = StringField()
    answer = StringField()


class SecurityQuestions(BaseDocument):
    user = ReferenceField(User, unique=True)
    questions = EmbeddedDocumentListField(Question)


class Credentials(BaseDocument):
    user = ReferenceField(User, unique=True)
    password = StringField()
    security_code = StringField()
    otp_code = StringField()
