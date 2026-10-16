from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from app.features.client_requests.model import ClientRequest, RequestStatus
from app.features.client_profiles.model import ClientProfile
from app.features.tutor_posts.model import TutorPost
from app.features.tutor_profiles.model import TutorProfile
from app.core.exceptions import ClientRequestAlreadyExistsError



class ClientRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        client_request: ClientRequest,
    ):
        self.db.add(client_request)
        try:
            self.db.flush()
        except IntegrityError:
            raise ClientRequestAlreadyExistsError()
        self.db.refresh(client_request)

        return client_request

    def get_by_id_for_client(
        self,
        user_id: int,
        client_request_id: int,
    ):
        return self.db.scalar(
            select(ClientRequest)
            .options(
                selectinload(ClientRequest.tutor_post)
                .selectinload(TutorPost.tutor)
                .selectinload(TutorProfile.user),
                selectinload(ClientRequest.client).selectinload(ClientProfile.user),
            )
            .where(
                ClientRequest.id==client_request_id,
                ClientProfile.user_id==user_id,
                ClientRequest.client_id==ClientProfile.id,
            )

        )


    def get_by_id_for_tutor(
        self,
        user_id: int,
        client_request_id: int,
    ) -> ClientRequest | None:
        return self.db.scalar(
            select(ClientRequest)
            .join(ClientRequest.tutor_post)
            .join(TutorPost.tutor)
            .options(
                selectinload(ClientRequest.tutor_post)
                .selectinload(TutorPost.tutor)
                .selectinload(TutorProfile.user),
                selectinload(ClientRequest.client).selectinload(ClientProfile.user),
            )
            .where(
                ClientRequest.id == client_request_id,
                TutorProfile.user_id == user_id,
            )
        )


    def update_status(
        self,
        client_request: ClientRequest,
        status: RequestStatus
    ):
        client_request.status=status
        
        self.db.flush()
        self.db.refresh(client_request)
        return client_request
        


    def get_existing(
        self,
        client_profile_id: int,
        tutor_post_id: int,
    ):
        return self.db.scalar(
            select(ClientRequest)
            .where(ClientRequest.tutor_post_id==tutor_post_id,ClientRequest.client_id==client_profile_id)

        )

    def get_all_by_client_id(
        self,
        client_profile_id: int,
    ) -> list[ClientRequest]:
        return list(
            self.db.scalars(
                select(ClientRequest)
                .options(
                    selectinload(ClientRequest.tutor_post)
                    .selectinload(TutorPost.tutor)
                    .selectinload(TutorProfile.user),
                    selectinload(ClientRequest.tutor_post).selectinload(TutorPost.subjects),
                    selectinload(ClientRequest.tutor_post).selectinload(TutorPost.class_levels),
                    selectinload(ClientRequest.client).selectinload(ClientProfile.user),
                )
                .where(ClientRequest.client_id == client_profile_id)
                .order_by(ClientRequest.created_at.desc(), ClientRequest.id.desc())
            )
        )

    def delete(
        self,
        client_request: ClientRequest,
    ) -> None:
        self.db.delete(client_request)
        self.db.flush()

    def get_all_for_tutor(
        self,
        user_id: int,
    ) -> list[ClientRequest]:
        return list(
            self.db.scalars(
                select(ClientRequest)
                .join(ClientRequest.tutor_post)
                .join(TutorPost.tutor)
                .options(
                    selectinload(ClientRequest.tutor_post)
                    .selectinload(TutorPost.tutor)
                    .selectinload(TutorProfile.user),
                    selectinload(ClientRequest.tutor_post).selectinload(TutorPost.subjects),
                    selectinload(ClientRequest.tutor_post).selectinload(TutorPost.class_levels),
                    selectinload(ClientRequest.client).selectinload(ClientProfile.user),
                )
                .where(TutorProfile.user_id == user_id)
                .order_by(ClientRequest.created_at.desc(), ClientRequest.id.desc())
            )
        )
