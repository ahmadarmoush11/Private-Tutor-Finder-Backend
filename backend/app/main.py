from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import api_router
from app.core.exception_handlers import register_exception_handlers
from app.db.session import engine


app = FastAPI(
    title="Private Tutor Finder API",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(api_router)

