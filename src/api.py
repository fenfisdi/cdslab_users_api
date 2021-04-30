from fastapi import FastAPI

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import user_routes, credential_routes, role_routes

app = FastAPI(**fastApiConfig)
db = MongoEngine().get_connection()

app.include_router(user_routes)
app.include_router(credential_routes)
app.include_router(role_routes)
