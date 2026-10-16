from app.features.subjects.exceptions import (
    SubjectAlreadyExistsError,
    SubjectInUseError,
    SubjectNotFoundError,
)
from app.db.unit_of_work import UnitOfWork
from app.features.subjects.model import Subject
from app.features.subjects.repository import SubjectRepository
from app.features.subjects.schemas import SubjectCreate, SubjectUpdate


class SubjectService:
    def __init__(self, subject_repository: SubjectRepository, uow: UnitOfWork):
        self.subject_repository = subject_repository
        self.uow = uow

    def get_all(self) -> list[Subject]:
        return self.subject_repository.get_all()

    def get_by_id(self, subject_id: int) -> Subject:
        subject = self.subject_repository.get_by_id(subject_id)
        if subject is None:
            raise SubjectNotFoundError()
        return subject

    def create(self, data: SubjectCreate) -> Subject:
        self._ensure_name_is_free(data.name)
        subject = Subject(name=data.name)

        with self.uow:
            subject = self.subject_repository.create(subject)
        return subject

    def update(self, subject_id: int, data: SubjectUpdate) -> Subject:
        subject = self.get_by_id(subject_id)
        self._ensure_name_is_free(data.name, exclude_id=subject.id)

        with self.uow:
            subject = self.subject_repository.update(subject, {"name": data.name})
        return subject

    def delete(self, subject_id: int) -> None:
        subject = self.get_by_id(subject_id)
        if self.subject_repository.is_in_use(subject.id):
            raise SubjectInUseError()

        with self.uow:
            self.subject_repository.delete(subject)

    def _ensure_name_is_free(self, name: str, exclude_id: int | None = None) -> None:
        existing = self.subject_repository.get_by_name(name)
        if existing is not None and existing.id != exclude_id:
            raise SubjectAlreadyExistsError()
