from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.db import models
from app.db.seeds.run import run_seeds


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_seeds()
    yield


app = FastAPI(
    title="Private Tutor Finder API",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_PREFIX)
