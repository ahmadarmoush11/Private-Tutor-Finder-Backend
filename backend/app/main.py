from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import auth
from app.db.session import engine


app = FastAPI(
    title="Private Tutor Finder API",
    version="1.0.0",
)

app.include_router(auth.router)

