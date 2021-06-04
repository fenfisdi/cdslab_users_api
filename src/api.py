from fastapi import FastAPI

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import credential_routes, root_routes, user_routes

app = FastAPI(**fastApiConfig)
db = MongoEngine().get_connection()

app.include_router(user_routes)
app.include_router(credential_routes)
app.include_router(root_routes)
