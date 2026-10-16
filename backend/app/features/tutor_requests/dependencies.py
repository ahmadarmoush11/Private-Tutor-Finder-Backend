from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_posts.dependencies import ClientPostRepositoryDep
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep
from app.features.tutor_requests.repository import TutorRequestRepository
from app.features.tutor_requests.service import TutorRequestService


def get_tutor_request_repository(db: DbSession) -> TutorRequestRepository:
    return TutorRequestRepository(db)


TutorRequestRepositoryDep = Annotated[
    TutorRequestRepository, Depends(get_tutor_request_repository)
]


def get_tutor_request_service(
    tutor_request_repository: TutorRequestRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    client_post_repository: ClientPostRepositoryDep,
    uow: UnitOfWorkDep,
) -> TutorRequestService:
    return TutorRequestService(
        tutor_request_repository,
        tutor_profile_repository,
        client_post_repository,
        uow,
    )


TutorRequestServiceDep = Annotated[
    TutorRequestService, Depends(get_tutor_request_service)
]
