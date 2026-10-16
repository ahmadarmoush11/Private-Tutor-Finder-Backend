from app.core.exceptions import ConflictException


class TutorRequestAlreadyExistsError(ConflictException):
    error_code = "REQUEST_ALREADY_EXISTS"
    message = "You already sent a request for this post"
