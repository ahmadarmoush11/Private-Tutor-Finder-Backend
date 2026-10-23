from fastapi import APIRouter, status
from app.features.auth.dependencies import ClientUser, CurrentUser
from app.features.notifications.dependencies import NotificationServiceDep
from app.features.notifications.schemas import(
    NotificationResponse
)



router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get(
    "",
    response_model=list[NotificationResponse],
)

def get_all_notifications(
    current_user: CurrentUser,
    service:NotificationServiceDep,
):
    return service.get_all(current_user.id)


@router.get(
    "/{id}",
    response_model=NotificationResponse,
)

def get_notification(
    current_user: CurrentUser,
    notification_id: int,
    service: NotificationServiceDep,
):
    return service.get_by_id(current_user.id,notification_id)


@router.post(
    "/{id}/mark-as-read",
    response_model=NotificationResponse
)

def mark_notfication_as_read(
    current_user: CurrentUser,
    notification_id: int,
    service: NotificationServiceDep,
):
    return service.mark_as_read(current_user.id,notification_id)


@router.delete(
    "/{id}",
)

def delete_notification(
    current_user: CurrentUser,
    notification_id: int,
    service: NotificationServiceDep,
):
    return service.delete(current_user.id, notification_id)




