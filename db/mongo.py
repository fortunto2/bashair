from pymongo import MongoClient

from config import settings


def connection():
    return MongoClient(f'{settings.MONGO_HOST}:{settings.MONGO_PORT}',
                       username=settings.MONGO_USER,
                       password=settings.MONGO_PASSWORD)


db = connection()[settings.MONGO_DB]