from app.core.exceptions import ConflictException


class ApplicationAlreadyExistsError(ConflictException):
    error_code = "APPLICATION_ALREADY_EXISTS"
    message = "You already applied to this post"
