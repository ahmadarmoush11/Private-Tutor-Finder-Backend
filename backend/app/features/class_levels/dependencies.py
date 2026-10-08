from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession
from app.features.class_levels.repository import ClassLevelRepository


def get_class_level_repository(db: DbSession) -> ClassLevelRepository:
    return ClassLevelRepository(db)


ClassLevelRepositoryDep = Annotated[
    ClassLevelRepository, Depends(get_class_level_repository)
]
