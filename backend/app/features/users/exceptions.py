from app.core.exceptions import ConflictException


class EmailAlreadyRegisteredError(ConflictException):
    error_code = "EMAIL_ALREADY_REGISTERED"
    message = "An account with this email already exists"


class UsernameAlreadyTakenError(ConflictException):
    error_code = "USERNAME_ALREADY_TAKEN"
    message = "This username is already taken"
