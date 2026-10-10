from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.class_levels.dependencies import ClassLevelRepositoryDep
from app.features.tutor_posts.repository import TutorPostRepository
from app.features.tutor_posts.service import TutorPostService
from app.features.tutor_profiles.dependencies import TutorProfileRepositoryDep


def get_tutor_post_repository(db: DbSession) -> TutorPostRepository:
    return TutorPostRepository(db)


TutorPostRepositoryDep = Annotated[
    TutorPostRepository, Depends(get_tutor_post_repository)
]


def get_tutor_post_service(
    tutor_post_repository: TutorPostRepositoryDep,
    tutor_profile_repository: TutorProfileRepositoryDep,
    class_level_repository: ClassLevelRepositoryDep,
    uow: UnitOfWorkDep,
) -> TutorPostService:
    return TutorPostService(
        tutor_post_repository,
        tutor_profile_repository,
        class_level_repository,
        uow,
    )


TutorPostServiceDep = Annotated[TutorPostService, Depends(get_tutor_post_service)]
