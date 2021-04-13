from fastapi import FastAPI

from src.config import fastApiConfig
from src.db import create_connection
from src.routes import user_routes

app = FastAPI(**fastApiConfig)
db = create_connection()

app.include_router(user_routes)
