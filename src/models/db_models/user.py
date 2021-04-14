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
    is_deleted = BooleanField(default=False)
    is_active = BooleanField(default=False)


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
