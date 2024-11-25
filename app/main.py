import os
from tortoise import Tortoise
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.adapters.api.v1.routes.group_route import groupRouter
from .adapters.data.orm.config.db_config import DATABASE_CONFIG
from .adapters.data.orm.config.db_config import init_db


load_dotenv()

app = FastAPI()
app = FastAPI(
    title="GiftLinkApi",
    version="1.0.0",
    openapi_url="/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groupRouter.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)