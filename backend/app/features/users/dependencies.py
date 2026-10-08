from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession
from app.features.users.repository import UserRepository


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
