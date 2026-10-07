from typing import Any


class AppException(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_SERVER_ERROR"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        details: Any = None,
        headers: dict[str, str] | None = None,
    ):
        self.message = message or self.message
        self.details = details
        self.headers = headers
        super().__init__(self.message)


class BadRequestException(AppException):
    status_code = 400
    error_code = "BAD_REQUEST"
    message = "Bad request"


class UnauthorizedException(AppException):
    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "Authentication is required"

    def __init__(self, message: str | None = None, details: Any = None):
        super().__init__(message, details, headers={"WWW-Authenticate": "Bearer"})


class ForbiddenException(AppException):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "You don't have permission to do this"


class NotFoundException(AppException):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class ConflictException(AppException):
    status_code = 409
    error_code = "CONFLICT"
    message = "Resource already exists"


class ValidationException(AppException):
    status_code = 422
    error_code = "VALIDATION_ERROR"
    message = "Invalid input"


class InternalServerException(AppException):
    pass


class EmailAlreadyRegisteredError(ConflictException):
    error_code = "EMAIL_ALREADY_REGISTERED"
    message = "An account with this email already exists"


class InvalidCredentialsError(UnauthorizedException):
    error_code = "INVALID_CREDENTIALS"
    message = "Incorrect email or password"


class InvalidTokenError(UnauthorizedException):
    error_code = "INVALID_TOKEN"
    message = "Could not validate credentials"


class ProfileAlreadyExistsError(ConflictException):
    error_code = "PROFILE_ALREADY_EXISTS"
    message = "You already have a profile"


class ProfileNotFoundError(NotFoundException):
    error_code = "PROFILE_NOT_FOUND"
    message = "Profile not found"
