from mongoengine import Document, DateTimeField

from src.utils import DateTime


class BaseDocument(Document):
    inserted_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {'allow_inheritance': True, 'abstract': True}

    def clean(self):
        if not self.inserted_at:
            self.inserted_at = DateTime.current_datetime()
        self.updated_at = DateTime.current_datetime()
