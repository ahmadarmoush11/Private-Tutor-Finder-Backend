from app.core.exceptions import ConflictException


class LessonRequestAlreadyExistsError(ConflictException):
    error_code = "LESSON_REQUEST_ALREADY_EXISTS"
    message = "You already have a pending request to this tutor"
