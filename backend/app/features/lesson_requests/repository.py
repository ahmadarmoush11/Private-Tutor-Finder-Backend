from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from app.features.lesson_requests.model import LessonRequest, RequestStatus
from app.features.client_profiles.model import ClientProfile
from app.features.tutor_posts.model import TutorPost
from app.features.tutor_profiles.model import TutorProfile
from app.features.lesson_requests.exceptions import LessonRequestAlreadyExistsError



class LessonRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        lesson_request: LessonRequest,
    ):
        self.db.add(lesson_request)
        try:
            self.db.flush()
        except IntegrityError:
            raise LessonRequestAlreadyExistsError()
        self.db.refresh(lesson_request)

        return lesson_request

    def get_by_id_for_client(
        self,
        user_id: int,
        lesson_request_id: int,
    ):
        return self.db.scalar(
            select(LessonRequest)
            .options(
                selectinload(LessonRequest.tutor_post)
                .selectinload(TutorPost.tutor)
                .selectinload(TutorProfile.user),
                selectinload(LessonRequest.client).selectinload(ClientProfile.user),
            )
            .where(
                LessonRequest.id==lesson_request_id,
                ClientProfile.user_id==user_id,
                LessonRequest.client_id==ClientProfile.id,
            )

        )


    def get_by_id_for_tutor(
        self,
        user_id: int,
        lesson_request_id: int,
    ) -> LessonRequest | None:
        return self.db.scalar(
            select(LessonRequest)
            .join(LessonRequest.tutor_post)
            .join(TutorPost.tutor)
            .options(
                selectinload(LessonRequest.tutor_post)
                .selectinload(TutorPost.tutor)
                .selectinload(TutorProfile.user),
                selectinload(LessonRequest.client).selectinload(ClientProfile.user),
            )
            .where(
                LessonRequest.id == lesson_request_id,
                TutorProfile.user_id == user_id,
            )
        )


    def update_status(
        self,
        lesson_request: LessonRequest,
        status: RequestStatus
    ):
        lesson_request.status=status
        
        self.db.flush()
        self.db.refresh(lesson_request)
        return lesson_request
        


    def get_existing(
        self,
        client_profile_id: int,
        tutor_post_id: int,
    ):
        return self.db.scalar(
            select(LessonRequest)
            .where(LessonRequest.tutor_post_id==tutor_post_id,LessonRequest.client_id==client_profile_id)

        )

    def get_all_by_client_id(
        self,
        client_profile_id: int,
    ) -> list[LessonRequest]:
        return list(
            self.db.scalars(
                select(LessonRequest)
                .options(
                    selectinload(LessonRequest.tutor_post)
                    .selectinload(TutorPost.tutor)
                    .selectinload(TutorProfile.user),
                    selectinload(LessonRequest.tutor_post).selectinload(TutorPost.subjects),
                    selectinload(LessonRequest.tutor_post).selectinload(TutorPost.class_levels),
                    selectinload(LessonRequest.client).selectinload(ClientProfile.user),
                )
                .where(LessonRequest.client_id == client_profile_id)
                .order_by(LessonRequest.created_at.desc(), LessonRequest.id.desc())
            )
        )

    def delete(
        self,
        lesson_request: LessonRequest,
    ) -> None:
        self.db.delete(lesson_request)
        self.db.flush()

    def get_all_for_tutor(
        self,
        user_id: int,
    ) -> list[LessonRequest]:
        return list(
            self.db.scalars(
                select(LessonRequest)
                .join(LessonRequest.tutor_post)
                .join(TutorPost.tutor)
                .options(
                    selectinload(LessonRequest.tutor_post)
                    .selectinload(TutorPost.tutor)
                    .selectinload(TutorProfile.user),
                    selectinload(LessonRequest.tutor_post).selectinload(TutorPost.subjects),
                    selectinload(LessonRequest.tutor_post).selectinload(TutorPost.class_levels),
                    selectinload(LessonRequest.client).selectinload(ClientProfile.user),
                )
                .where(TutorProfile.user_id == user_id)
                .order_by(LessonRequest.created_at.desc(), LessonRequest.id.desc())
            )
        )
