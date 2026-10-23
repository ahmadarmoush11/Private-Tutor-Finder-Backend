from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.features.notifications.model import Notification

from app.features.users.model import User
from app.features.client_profiles.model import ClientProfile
from app.features.tutor_profiles.model import TutorProfile
from app.features.notifications.exceptions import NotificationAlreadyExistsError


class NotificationRepository:

    def __init__(
        self,
        db: Session,  
    ):
        self.db=db


    def create(self, notification: Notification)->Notification:
        self._check_existing(notification)
        
        self.db.add(notification)
        self.db.flush()
        self.db.refresh(notification)

        return notification

    def get_by_id(self, notification_id: int)->Notification:

        return self.db.scalar(
            select(Notification)
            .options(
                selectinload(Notification.recipient),
                selectinload(Notification.actor),
                selectinload(Notification.lesson_request),
                selectinload(Notification.client_post)
            )
            .where(Notification.id==notification_id)
        )

    def get_by_id_for_user(self, user_id: int, notification_id: int)->Notification:

        return self.db.scalar(
            select(Notification)
            .options(
                selectinload(Notification.recipient),
                selectinload(Notification.actor),
                selectinload(Notification.lesson_request),
                selectinload(Notification.client_post)
            )
            .where(Notification.id==notification_id, Notification.recipient_id==user_id)
        )

    

    def get_all(self, user_id:int)->list[Notification]:
        return self.db.scalars(
            select(Notification)
            .options(
                selectinload(Notification.recipient),
                selectinload(Notification.actor),
                selectinload(Notification.lesson_request),
                selectinload(Notification.client_post)
            )
            .where(Notification.recipient_id==user_id)
        )


    def mark_as_read(self,notification: Notification)->Notification:

        notification.is_read=True

        self.db.flush()
        self.db.refresh(notification)
        return notification

    
    def delete_for_user(self, notification: Notification)->None:
        self.db.delete(notification)
        self.db.flush()


    def _check_existing(self, notification: Notification)->None:
        existing_notification=self.db.scalar(
            select(Notification)
            .where(
                Notification.recipient_id==notification.recipient_id,
                Notification.actor_id==notification.actor_id,
                Notification.type==notification.type,
                or_(
                    Notification.lesson_request_id==notification.lesson_request_id,
                    Notification.client_post_id==notification.client_post_id,
                ),
                )
        )

        if existing_notification is not None:
            raise NotificationAlreadyExistsError()

            

    


