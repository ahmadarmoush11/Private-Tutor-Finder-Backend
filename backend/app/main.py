from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import auth
from app.db.session import engine


app = FastAPI(
    title="Private Tutor Finder API",
    version="1.0.0",
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Private Tutor Finder API"}


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}
