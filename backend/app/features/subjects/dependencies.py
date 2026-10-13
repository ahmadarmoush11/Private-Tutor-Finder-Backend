from typing import Annotated

from fastapi import Depends

from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.subjects.repository import SubjectRepository
from app.features.subjects.service import SubjectService


def get_subject_repository(db: DbSession) -> SubjectRepository:
    return SubjectRepository(db)


SubjectRepositoryDep = Annotated[SubjectRepository, Depends(get_subject_repository)]


def get_subject_service(
    subject_repository: SubjectRepositoryDep,
    uow: UnitOfWorkDep,
) -> SubjectService:
    return SubjectService(subject_repository, uow)


SubjectServiceDep = Annotated[SubjectService, Depends(get_subject_service)]
