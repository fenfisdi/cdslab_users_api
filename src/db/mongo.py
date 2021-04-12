from mongoengine import connect

from src.config import config


def create_connection():
    return connect(host=config.get('MONGO_URI'))
