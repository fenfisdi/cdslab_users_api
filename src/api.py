from fastapi import FastAPI

from src.config import fastApiConfig
from src.routes import user_routes

app = FastAPI(**fastApiConfig)

app.include_router(user_routes)
