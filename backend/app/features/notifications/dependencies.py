from typing import Annotated
from fastapi import Depends
from app.db.dependencies import DbSession, UnitOfWorkDep
from app.features.notifications.repository import NotificationRepository
from app.features.notifications.service import NotificationService


def get_notification_repository(db: DbSession)->NotificationRepository:
    return NotificationRepository(db)

NotificationRepositoryDep= Annotated[
    NotificationRepository, Depends(get_notification_repository)
]


def get_notification_service(notification_repository:NotificationRepositoryDep, uow: UnitOfWorkDep)->NotificationService:
    return NotificationService(
        notification_repository,
        uow,
    )

NotificationServiceDep=Annotated[
    NotificationService, Depends(get_notification_service)
]

