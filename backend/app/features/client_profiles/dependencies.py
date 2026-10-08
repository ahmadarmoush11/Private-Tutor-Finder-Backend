from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_profiles.repository import ClientProfileRepository
from app.features.client_profiles.service import ClientProfileService


def get_client_profile_repository(db: DbSession) -> ClientProfileRepository:
    return ClientProfileRepository(db)


ClientProfileRepositoryDep = Annotated[
    ClientProfileRepository, Depends(get_client_profile_repository)
]


def get_client_profile_service(
    client_profile_repository: ClientProfileRepositoryDep,
    uow: UnitOfWorkDep,
) -> ClientProfileService:
    return ClientProfileService(client_profile_repository, uow)


ClientProfileServiceDep = Annotated[
    ClientProfileService, Depends(get_client_profile_service)
]
