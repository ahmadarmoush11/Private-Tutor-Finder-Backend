from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.features.client_posts.model import ClientPost
from app.features.client_profiles.model import ClientProfile
from app.features.tutor_profiles.model import TutorProfile
from app.features.tutor_requests.model import TutorRequest
from app.shared.enums import RequestStatus


def _load_details():
    return (
        selectinload(TutorRequest.tutor).selectinload(TutorProfile.user),
        selectinload(TutorRequest.client_post)
        .selectinload(ClientPost.client)
        .selectinload(ClientProfile.user),
        selectinload(TutorRequest.client_post).selectinload(ClientPost.class_level),
        selectinload(TutorRequest.client_post).selectinload(ClientPost.subjects),
    )


class TutorRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tutor_request: TutorRequest) -> TutorRequest:
        self.db.add(tutor_request)
        self.db.flush()
        self.db.refresh(tutor_request)
        return tutor_request

    def get_existing(
        self,
        tutor_profile_id: int,
        client_post_id: int,
    ) -> TutorRequest | None:
        return self.db.scalar(
            select(TutorRequest).where(
                TutorRequest.tutor_id == tutor_profile_id,
                TutorRequest.client_post_id == client_post_id,
            )
        )

    def get_by_id_for_tutor(
        self,
        user_id: int,
        tutor_request_id: int,
    ) -> TutorRequest | None:
        return self.db.scalar(
            select(TutorRequest)
            .join(TutorRequest.tutor)
            .options(*_load_details())
            .where(
                TutorRequest.id == tutor_request_id,
                TutorProfile.user_id == user_id,
            )
        )

    def get_all_for_tutor(self, tutor_profile_id: int) -> list[TutorRequest]:
        return list(
            self.db.scalars(
                select(TutorRequest)
                .options(*_load_details())
                .where(TutorRequest.tutor_id == tutor_profile_id)
                .order_by(TutorRequest.created_at.desc(), TutorRequest.id.desc())
            )
        )

    def get_by_id_for_client(
        self,
        user_id: int,
        tutor_request_id: int,
    ) -> TutorRequest | None:
        return self.db.scalar(
            select(TutorRequest)
            .join(TutorRequest.client_post)
            .join(ClientPost.client)
            .options(*_load_details())
            .where(
                TutorRequest.id == tutor_request_id,
                ClientProfile.user_id == user_id,
            )
        )

    def get_all_for_client(self, user_id: int) -> list[TutorRequest]:
        return list(
            self.db.scalars(
                select(TutorRequest)
                .join(TutorRequest.client_post)
                .join(ClientPost.client)
                .options(*_load_details())
                .where(ClientProfile.user_id == user_id)
                .order_by(TutorRequest.created_at.desc(), TutorRequest.id.desc())
            )
        )

    def update_status(
        self,
        tutor_request: TutorRequest,
        status: RequestStatus,
    ) -> TutorRequest:
        tutor_request.status = status
        self.db.flush()
        self.db.refresh(tutor_request)
        return tutor_request

    def delete(self, tutor_request: TutorRequest) -> None:
        self.db.delete(tutor_request)
        self.db.flush()
