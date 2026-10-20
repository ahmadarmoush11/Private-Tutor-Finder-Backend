from app.core.exceptions import ConflictException, NotFoundException


class SubjectNotFoundError(NotFoundException):
    error_code = "SUBJECT_NOT_FOUND"
    message = "Subject not found"


class SubjectAlreadyExistsError(ConflictException):
    error_code = "SUBJECT_ALREADY_EXISTS"
    message = "A subject with this name already exists"


class SubjectInUseError(ConflictException):
    error_code = "SUBJECT_IN_USE"
    message = "This subject is in use by posts, lesson requests or tutor profiles and cannot be deleted"
