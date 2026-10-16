from app.core.exceptions import ConflictException


class ClientRequestAlreadyExistsError(ConflictException):
    error_code = "REQUEST_ALREADY_EXISTS"
    message = "A request to this tutor already exists"
