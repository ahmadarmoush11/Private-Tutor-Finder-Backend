from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.class_levels.dependencies import ClassLevelRepositoryDep
from app.features.client_posts.repository import ClientPostRepository
from app.features.client_posts.service import ClientPostService
from app.features.client_profiles.dependencies import ClientProfileRepositoryDep


def get_client_post_repository(db: DbSession) -> ClientPostRepository:
    return ClientPostRepository(db)


ClientPostRepositoryDep = Annotated[
    ClientPostRepository, Depends(get_client_post_repository)
]


def get_client_post_service(
    client_post_repository: ClientPostRepositoryDep,
    client_profile_repository: ClientProfileRepositoryDep,
    class_level_repository: ClassLevelRepositoryDep,
    uow: UnitOfWorkDep,
) -> ClientPostService:
    return ClientPostService(
        client_post_repository,
        client_profile_repository,
        class_level_repository,
        uow,
    )


ClientPostServiceDep = Annotated[ClientPostService, Depends(get_client_post_service)]
