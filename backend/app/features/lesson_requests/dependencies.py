from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.class_levels.dependencies import ClassLevelRepositoryDep
from app.features.client_profiles.dependencies import ClientProfileServiceDep
from app.features.lesson_requests.repository import LessonRequestRepository
from app.features.lesson_requests.service import LessonRequestService
from app.features.subjects.dependencies import SubjectRepositoryDep
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep


def get_lesson_request_repository(db: DbSession) -> LessonRequestRepository:
    return LessonRequestRepository(db)


LessonRequestRepositoryDep = Annotated[
    LessonRequestRepository, Depends(get_lesson_request_repository)
]


def get_lesson_request_service(
    lesson_request_repository: LessonRequestRepositoryDep,
    client_profile_service: ClientProfileServiceDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    subject_repository: SubjectRepositoryDep,
    class_level_repository: ClassLevelRepositoryDep,
    uow: UnitOfWorkDep,
) -> LessonRequestService:
    return LessonRequestService(
        lesson_request_repository,
        client_profile_service,
        tutor_profile_repository,
        subject_repository,
        class_level_repository,
        uow,
    )


LessonRequestServiceDep = Annotated[
    LessonRequestService, Depends(get_lesson_request_service)
]
