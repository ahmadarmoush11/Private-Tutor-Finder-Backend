from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_profiles.dependencies import ClientProfileServiceDep
from app.features.lesson_requests.repository import LessonRequestRepository
from app.features.lesson_requests.service import LessonRequestService
from app.features.tutor_posts.dependencies import (
    TutorPostRepositoryDep,
    TutorPostServiceDep,
)


def get_lesson_request_repository(db: DbSession) -> LessonRequestRepository:
    return LessonRequestRepository(db)


LessonRequestRepositoryDep = Annotated[
    LessonRequestRepository, Depends(get_lesson_request_repository)
]


def get_lesson_request_service(
    lesson_request_repository: LessonRequestRepositoryDep,
    client_profile_service: ClientProfileServiceDep,
    tutor_post_repository: TutorPostRepositoryDep,
    tutor_post_service: TutorPostServiceDep,
    uow: UnitOfWorkDep,
) -> LessonRequestService:
    return LessonRequestService(
        lesson_request_repository,
        client_profile_service,
        tutor_post_repository,
        tutor_post_service,
        uow,
    )


LessonRequestServiceDep = Annotated[
    LessonRequestService, Depends(get_lesson_request_service)
]
