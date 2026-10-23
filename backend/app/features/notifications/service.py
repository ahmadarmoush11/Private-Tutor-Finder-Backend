from app.features.notifications.model import Notification
from app.features.notifications.exceptions import(
    NotificationNotFoundError,
    NotificationAlreadyReadError
)
from app.features.notifications.repository import NotificationRepository
from app.db.unit_of_work import UnitOfWork
from app.features.lesson_requests.model import LessonRequest
from app.shared.enums import (
    NotificationType
)
from app.features.client_posts.model import ClientPost
from app.features.client_profiles.repository import ClientProfileRepository
from app.features.tutor_profiles.repository import TutorProfileRepository



class NotificationService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        uow: UnitOfWork
        ):
        self.notification_repository=notification_repository
        self.uow=uow


    def create_for_lesson_request_received(
        self,
        lesson_request: LessonRequest,

    )->Notification:

        recipient_id=lesson_request.tutor.user_id
        actor_id=lesson_request.client.user_id

        notification=Notification(
            recipient_id=recipient_id,
            actor_id=actor_id,
            type=NotificationType.LESSON_REQUEST_RECEIVED,
            lesson_request_id=lesson_request.id,
        )

        with self.uow:
            notification= self.notification_repository.create(notification)

        return notification

    def create_for_lesson_request_accepted(
        self,
        lesson_request: LessonRequest,

    )->Notification:
        notification=Notification(
            actor_id=lesson_request.tutor.user_id,
            recipient_id=lesson_request.client.user_id,
            type=NotificationType.LESSON_REQUEST_ACCEPTED,
            lesson_request_id=lesson_request.id,
        )

        with self.uow:
            notification= self.notification_repository.create(notification)

        return notification

    def create_for_lesson_request_rejected(
        self,
        lesson_request: LessonRequest,

    )->Notification:
        notification=Notification(
            actor_id=lesson_request.tutor.user_id,
            recipient_id=lesson_request.client.user_id,
            type=NotificationType.LESSON_REQUEST_REJECTED,
            lesson_request_id=lesson_request.id,
        )

        with self.uow:
            notification= self.notification_repository.create(notification)

        return notification


    def create_for_tutor_avaiable(
        self,
        tutor_user_id: int,
        client_post: ClientPost
    )->Notification:

        notification=Notification(
            recipient_id=client_post.client.user_id,
            actor_id=tutor_user_id,
            type=NotificationType.TUTOR_AVAILABLE,
            client_post_id=client_post.id,

        )
        with self.uow:
            notification= self.notification_repository.create(notification)

        return notification


    def get_by_id(self, user_id: int, notification_id: int)->Notification:
        notification= self._get_notification(user_id,notification_id)

        return notification
    

    def get_all(
        self,
        user_id: int,
    )->list[Notification]:

        notifications=self.notification_repository.get_all(user_id)

        if notifications is None:
            return []

        return notifications
        

    def mark_as_read(
        self,
        user_id: int,
        notification_id: int,
    )->Notification:
        notification=self._get_notification(user_id, notification_id)

        if notification.is_read:
            raise NotificationAlreadyReadError()

        with self.uow:
            notification=self.notification_repository.mark_as_read(notification)

        return notification

    

    def delete(self, user_id: int, notification_id: int)->None:
        notification= self._get_notification(user_id,notification_id)

        self.notification_repository.delete(notification)
              


    def _get_notification(self, user_id: int, notification_id: int)->Notification |None:
        notification=self.notification_repository.get_by_id_for_user(user_id,notification_id)

        if notification is None:
            raise NotificationNotFoundError()

        return notification



        
    
        
        

        

        



