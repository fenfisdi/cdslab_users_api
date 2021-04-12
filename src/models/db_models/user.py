from mongoengine import (
    StringField,
    IntField,
    DateField,
    ListField,
    ReferenceField,
    BooleanField
)

from .base import BaseDocument


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
    security_questions = ListField()
    is_deleted = BooleanField(default=False)
    is_active = BooleanField(default=False)


class SecurityQuestions(BaseDocument):
    pass


class Credentials(BaseDocument):
    user = ReferenceField(User)
    password = StringField()
