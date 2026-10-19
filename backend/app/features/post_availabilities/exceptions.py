from app.core.exceptions import ConflictException, NotFoundException


class AlreadyAvailableError(ConflictException):
    error_code = "ALREADY_AVAILABLE"
    message = "You are already marked as available for this post"


class AvailabilityNotFoundError(NotFoundException):
    error_code = "AVAILABILITY_NOT_FOUND"
    message = "You are not marked as available for this post"


class PostNotActiveError(ConflictException):
    error_code = "POST_NOT_ACTIVE"
    message = "This post is no longer active"
