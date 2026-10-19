from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_posts.dependencies import ClientPostRepositoryDep
from app.features.post_availabilities.repository import PostAvailabilityRepository
from app.features.post_availabilities.service import PostAvailabilityService
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep


def get_post_availability_repository(db: DbSession) -> PostAvailabilityRepository:
    return PostAvailabilityRepository(db)


PostAvailabilityRepositoryDep = Annotated[
    PostAvailabilityRepository, Depends(get_post_availability_repository)
]


def get_post_availability_service(
    post_availability_repository: PostAvailabilityRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    client_post_repository: ClientPostRepositoryDep,
    uow: UnitOfWorkDep,
) -> PostAvailabilityService:
    return PostAvailabilityService(
        post_availability_repository,
        tutor_profile_repository,
        client_post_repository,
        uow,
    )


PostAvailabilityServiceDep = Annotated[
    PostAvailabilityService, Depends(get_post_availability_service)
]
