from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_posts.dependencies import ClientPostRepositoryDep
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep
from app.features.applications.repository import ApplicationRepository
from app.features.applications.service import ApplicationService


def get_application_repository(db: DbSession) -> ApplicationRepository:
    return ApplicationRepository(db)


ApplicationRepositoryDep = Annotated[
    ApplicationRepository, Depends(get_application_repository)
]


def get_application_service(
    application_repository: ApplicationRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    client_post_repository: ClientPostRepositoryDep,
    uow: UnitOfWorkDep,
) -> ApplicationService:
    return ApplicationService(
        application_repository,
        tutor_profile_repository,
        client_post_repository,
        uow,
    )


ApplicationServiceDep = Annotated[
    ApplicationService, Depends(get_application_service)
]
