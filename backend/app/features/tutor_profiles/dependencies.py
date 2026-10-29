from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.areas.dependencies import AreaRepositoryDep
from app.features.class_levels.dependencies import ClassLevelRepositoryDep
from app.features.subjects.dependencies import SubjectRepositoryDep
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_profiles.service import TutorProfileService
from app.features.tutor_reviews.repository import TutorReviewRepository


def get_tutor_profile_repository(db: DbSession) -> TutorProfileRepository:
    return TutorProfileRepository(db)


TutorProfileRepositoryDep = Annotated[
    TutorProfileRepository, Depends(get_tutor_profile_repository)
]


def get_tutor_profile_service(
    tutor_profile_repository: TutorProfileRepositoryDep,
    class_level_repository: ClassLevelRepositoryDep,
    subject_repository: SubjectRepositoryDep,
    db: DbSession,
    area_repository: AreaRepositoryDep,
    uow: UnitOfWorkDep,
) -> TutorProfileService:
    return TutorProfileService(
        tutor_profile_repository,
        class_level_repository,
        subject_repository,
        TutorReviewRepository(db),
        area_repository,
        uow,
    )


TutorProfileServiceDep = Annotated[
    TutorProfileService, Depends(get_tutor_profile_service)
]
