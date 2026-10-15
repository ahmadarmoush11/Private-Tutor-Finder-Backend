from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_profiles.dependencies import ClientProfileServiceDep
from app.features.client_requests.repository import ClientRequestRepository
from app.features.client_requests.service import ClientRequestService
from app.features.tutor_posts.dependencies import (
    TutorPostRepositoryDep,
    TutorPostServiceDep,
)


def get_client_request_repository(db: DbSession) -> ClientRequestRepository:
    return ClientRequestRepository(db)


ClientRequestRepositoryDep = Annotated[
    ClientRequestRepository, Depends(get_client_request_repository)
]


def get_client_request_service(
    client_request_repository: ClientRequestRepositoryDep,
    client_profile_service: ClientProfileServiceDep,
    tutor_post_repository: TutorPostRepositoryDep,
    tutor_post_service: TutorPostServiceDep,
    uow: UnitOfWorkDep,
) -> ClientRequestService:
    return ClientRequestService(
        client_request_repository,
        client_profile_service,
        tutor_post_repository,
        tutor_post_service,
        uow,
    )


ClientRequestServiceDep = Annotated[
    ClientRequestService, Depends(get_client_request_service)
]
