from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException,
)

class NotificationNotFoundError(NotFoundException):
    error_code="NOTIFICATION_NOT_FOUND"
    message="The notification does not exist"

class NotificationAlreadyExistsError(ConflictException):
    error_code="NOTIFICATION_ALREADY_EXISTS"
    message="Notification already exists"

class NotificationAlreadyReadError(BadRequestException):
    error_code="NOTIFICATION_ALREADY_READ"
    message="Notification has been already read"

    
