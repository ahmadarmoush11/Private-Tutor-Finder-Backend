from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.client_profiles.dependencies import ClientProfileRepositoryDep
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep
from app.features.tutor_reviews.repository import TutorReviewRepository
from app.features.tutor_reviews.service import TutorReviewService


def get_tutor_review_repository(db: DbSession) -> TutorReviewRepository:
    return TutorReviewRepository(db)


TutorReviewRepositoryDep = Annotated[
    TutorReviewRepository, Depends(get_tutor_review_repository)
]


def get_tutor_review_service(
    tutor_review_repository: TutorReviewRepositoryDep,
    client_profile_repository: ClientProfileRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    uow: UnitOfWorkDep,
) -> TutorReviewService:
    return TutorReviewService(
        tutor_review_repository,
        client_profile_repository,
        tutor_profile_repository,
        uow,
    )


TutorReviewServiceDep = Annotated[
    TutorReviewService, Depends(get_tutor_review_service)
]
