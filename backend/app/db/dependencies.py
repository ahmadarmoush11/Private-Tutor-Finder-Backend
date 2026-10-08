from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.unit_of_work import UnitOfWork


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


def get_unit_of_work(db: DbSession) -> UnitOfWork:
    return UnitOfWork(db)


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]
