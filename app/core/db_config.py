from urllib.parse import quote_plus

from pymongo import AsyncMongoClient

from app.core.settings import settings

MONGO_URL = f"mongodb+srv://{quote_plus(settings.MONGO_USER_NAME)}:{quote_plus(settings.MONGO_USER_PASSWORD)}@{settings.MONGO_CLUSTER}/?appName={settings.MONGO_APP_NAME}&retryWrites=true&w=majority&authSource=admin"
DATABASE_NAME = settings.MONGO_DATABASE

client = AsyncMongoClient(MONGO_URL)
db = client[DATABASE_NAME]