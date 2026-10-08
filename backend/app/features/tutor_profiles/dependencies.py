from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_profiles.service import TutorProfileService


def get_tutor_profile_repository(db: DbSession) -> TutorProfileRepository:
    return TutorProfileRepository(db)


TutorProfileRepositoryDep = Annotated[
    TutorProfileRepository, Depends(get_tutor_profile_repository)
]


def get_tutor_profile_service(
    tutor_profile_repository: TutorProfileRepositoryDep,
    uow: UnitOfWorkDep,
) -> TutorProfileService:
    return TutorProfileService(tutor_profile_repository, uow)


TutorProfileServiceDep = Annotated[
    TutorProfileService, Depends(get_tutor_profile_service)
]
