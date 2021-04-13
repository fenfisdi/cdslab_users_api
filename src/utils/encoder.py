from datetime import datetime
from json import JSONEncoder

from bson import ObjectId
from mongoengine import Document
from ujson import loads


class BsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)


class BsonObject:

    @staticmethod
    def dict(document: Document):
        raw = BsonEncoder().encode(document.to_mongo())
        document_dict = loads(raw)

        invalid_keys = {
            "_id", "_cls", "inserted_at", "updated_at", "is_deleted"
        }
        for k in document_dict.copy().keys():
            if k in invalid_keys:
                del document_dict[k]
        return document_dict
