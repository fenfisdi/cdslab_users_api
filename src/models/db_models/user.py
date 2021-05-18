from mongoengine import (
    StringField,
    IntField,
    DateField,
    ReferenceField,
    BooleanField,
    EmbeddedDocument,
    EmbeddedDocumentListField
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
    role = StringField(default="user")
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
