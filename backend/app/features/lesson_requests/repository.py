from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.features.client_profiles.model import ClientProfile
from app.features.lesson_requests.exceptions import LessonRequestAlreadyExistsError
from app.features.lesson_requests.model import LessonRequest
from app.features.tutor_profiles.model import TutorProfile
from app.shared.enums import RequestStatus


def _load_details():
    return (
        selectinload(LessonRequest.client).selectinload(ClientProfile.user),
        selectinload(LessonRequest.tutor).selectinload(TutorProfile.user),
        selectinload(LessonRequest.subjects),
        selectinload(LessonRequest.class_level),
    )


class LessonRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, lesson_request: LessonRequest) -> LessonRequest:
        self.db.add(lesson_request)
        try:
            self.db.flush()
        except IntegrityError:
            raise LessonRequestAlreadyExistsError()
        self.db.refresh(lesson_request)
        return lesson_request

    def get_pending(
        self,
        client_profile_id: int,
        tutor_profile_id: int,
    ) -> LessonRequest | None:
        return self.db.scalar(
            select(LessonRequest).where(
                LessonRequest.client_id == client_profile_id,
                LessonRequest.tutor_id == tutor_profile_id,
                LessonRequest.status == RequestStatus.PENDING,
            )
        )

    def get_by_id_for_client(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest | None:
        return self.db.scalar(
            select(LessonRequest)
            .join(LessonRequest.client)
            .options(*_load_details())
            .where(
                LessonRequest.id == lesson_request_id,
                ClientProfile.user_id == user_id,
            )
        )

    def get_by_id_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest | None:
        return self.db.scalar(
            select(LessonRequest)
            .join(LessonRequest.tutor)
            .options(*_load_details())
            .where(
                LessonRequest.id == lesson_request_id,
                TutorProfile.user_id == user_id,
            )
        )

    def get_all_for_client(self, client_profile_id: int) -> list[LessonRequest]:
        return list(
            self.db.scalars(
                select(LessonRequest)
                .options(*_load_details())
                .where(LessonRequest.client_id == client_profile_id)
                .order_by(LessonRequest.created_at.desc(), LessonRequest.id.desc())
            )
        )

    def get_all_for_tutor(self, user_id: int) -> list[LessonRequest]:
        return list(
            self.db.scalars(
                select(LessonRequest)
                .join(LessonRequest.tutor)
                .options(*_load_details())
                .where(TutorProfile.user_id == user_id)
                .order_by(LessonRequest.created_at.desc(), LessonRequest.id.desc())
            )
        )

    def update_status(
        self,
        lesson_request: LessonRequest,
        status: RequestStatus,
    ) -> LessonRequest:
        lesson_request.status = status
        self.db.flush()
        self.db.refresh(lesson_request)
        return lesson_request

    def delete(self, lesson_request: LessonRequest) -> None:
        self.db.delete(lesson_request)
        self.db.flush()
