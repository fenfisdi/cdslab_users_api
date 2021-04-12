from mongoengine import Document, DateTimeField, StringField, IntField, \
    DateField, ListField

from src.utils import DateTime


class BaseDocument(Document):
    inserted_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {'abstract': True, 'strict': False, 'allow_inheritance': True}

    def clean(self):
        if not self.inserted_at:
            self.inserted_at = DateTime.current_datetime()
        self.updated_at = DateTime.current_datetime()


class User(BaseDocument):
    name = StringField()
    last_name = StringField()
    email = StringField()
    phone = IntField()
    phone_prefix = StringField()
    institution = StringField()
    institution_role = StringField()
    profession = StringField()
    gender = StringField()
    birthday = DateField()
    security_questions = ListField()
