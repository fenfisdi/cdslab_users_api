from mongoengine import connect

from src.config import config
from src.utils.patterns import Singleton


class MongoEngine(metaclass=Singleton):
    def __init__(self):
        self.mongo_uri = config.get('MONGO_URI')

    def get_connection(self):
        return connect(host=self.mongo_uri)
