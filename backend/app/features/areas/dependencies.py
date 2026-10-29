from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession
from app.features.areas.repository import AreaRepository
from app.features.areas.service import AreaService


def get_area_repository(db: DbSession) -> AreaRepository:
    return AreaRepository(db)


AreaRepositoryDep = Annotated[AreaRepository, Depends(get_area_repository)]


def get_area_service(area_repository: AreaRepositoryDep) -> AreaService:
    return AreaService(area_repository)


AreaServiceDep = Annotated[AreaService, Depends(get_area_service)]
