from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.degree_verifications.repository import DegreeVerificationRepository
from app.features.degree_verifications.service import DegreeVerificationService
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep


def get_degree_verification_repository(db: DbSession) -> DegreeVerificationRepository:
    return DegreeVerificationRepository(db)


DegreeVerificationRepositoryDep = Annotated[
    DegreeVerificationRepository, Depends(get_degree_verification_repository)
]


def get_degree_verification_service(
    degree_verification_repository: DegreeVerificationRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    uow: UnitOfWorkDep,
) -> DegreeVerificationService:
    return DegreeVerificationService(
        degree_verification_repository,
        tutor_profile_repository,
        uow,
    )


DegreeVerificationServiceDep = Annotated[
    DegreeVerificationService, Depends(get_degree_verification_service)
]
