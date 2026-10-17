from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.features.client_posts.model import ClientPost
from app.features.client_profiles.model import ClientProfile
from app.features.tutor_profiles.model import TutorProfile
from app.features.applications.model import Application
from app.shared.enums import RequestStatus


def _load_details():
    return (
        selectinload(Application.tutor).selectinload(TutorProfile.user),
        selectinload(Application.client_post)
        .selectinload(ClientPost.client)
        .selectinload(ClientProfile.user),
        selectinload(Application.client_post).selectinload(ClientPost.class_level),
        selectinload(Application.client_post).selectinload(ClientPost.subjects),
    )


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, application: Application) -> Application:
        self.db.add(application)
        self.db.flush()
        self.db.refresh(application)
        return application

    def get_existing(
        self,
        tutor_profile_id: int,
        client_post_id: int,
    ) -> Application | None:
        return self.db.scalar(
            select(Application).where(
                Application.tutor_id == tutor_profile_id,
                Application.client_post_id == client_post_id,
            )
        )

    def get_by_id_for_tutor(
        self,
        user_id: int,
        application_id: int,
    ) -> Application | None:
        return self.db.scalar(
            select(Application)
            .join(Application.tutor)
            .options(*_load_details())
            .where(
                Application.id == application_id,
                TutorProfile.user_id == user_id,
            )
        )

    def get_all_for_tutor(self, tutor_profile_id: int) -> list[Application]:
        return list(
            self.db.scalars(
                select(Application)
                .options(*_load_details())
                .where(Application.tutor_id == tutor_profile_id)
                .order_by(Application.created_at.desc(), Application.id.desc())
            )
        )

    def get_by_id_for_client(
        self,
        user_id: int,
        application_id: int,
    ) -> Application | None:
        return self.db.scalar(
            select(Application)
            .join(Application.client_post)
            .join(ClientPost.client)
            .options(*_load_details())
            .where(
                Application.id == application_id,
                ClientProfile.user_id == user_id,
            )
        )

    def get_all_for_client(self, user_id: int) -> list[Application]:
        return list(
            self.db.scalars(
                select(Application)
                .join(Application.client_post)
                .join(ClientPost.client)
                .options(*_load_details())
                .where(ClientProfile.user_id == user_id)
                .order_by(Application.created_at.desc(), Application.id.desc())
            )
        )

    def update_status(
        self,
        application: Application,
        status: RequestStatus,
    ) -> Application:
        application.status = status
        self.db.flush()
        self.db.refresh(application)
        return application

    def delete(self, application: Application) -> None:
        self.db.delete(application)
        self.db.flush()
