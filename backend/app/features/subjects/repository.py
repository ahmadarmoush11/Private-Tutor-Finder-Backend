from sqlalchemy import exists, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import SubjectAlreadyExistsError, SubjectInUseError
from app.features.client_posts.model import client_post_subjects
from app.features.subjects.model import Subject
from app.features.tutor_posts.model import tutor_post_subjects


class SubjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Subject]:
        return list(self.db.scalars(select(Subject).order_by(Subject.name)))

    def get_by_id(self, subject_id: int) -> Subject | None:
        return self.db.get(Subject, subject_id)

    def get_by_ids(self, subject_ids: list[int]) -> list[Subject]:
        return list(
            self.db.scalars(
                select(Subject)
                .where(Subject.id.in_(subject_ids))
                .order_by(Subject.name)
            )
        )

    def get_by_name(self, name: str) -> Subject | None:
        return self.db.scalar(
            select(Subject).where(func.lower(Subject.name) == name.strip().lower())
        )

    def is_in_use(self, subject_id: int) -> bool:
        return bool(
            self.db.scalar(
                select(
                    or_(
                        exists().where(client_post_subjects.c.subject_id == subject_id),
                        exists().where(tutor_post_subjects.c.subject_id == subject_id),
                    )
                )
            )
        )

    def create(self, subject: Subject) -> Subject:
        self.db.add(subject)
        try:
            self.db.flush()
        except IntegrityError:
            raise SubjectAlreadyExistsError()
        self.db.refresh(subject)
        return subject

    def update(self, subject: Subject, values: dict) -> Subject:
        for field, value in values.items():
            setattr(subject, field, value)
        try:
            self.db.flush()
        except IntegrityError:
            raise SubjectAlreadyExistsError()
        self.db.refresh(subject)
        return subject

    def delete(self, subject: Subject) -> None:
        self.db.delete(subject)
        try:
            self.db.flush()
        except IntegrityError:
            raise SubjectInUseError()
