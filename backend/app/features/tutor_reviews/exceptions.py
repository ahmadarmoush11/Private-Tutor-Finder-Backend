from app.core.exceptions import ConflictException, NotFoundException


class TutorReviewAlreadyExistsError(ConflictException):
    error_code = "TUTOR_REVIEW_ALREADY_EXISTS"
    message = "You already reviewed this tutor"


class TutorReviewNotFoundError(NotFoundException):
    error_code = "TUTOR_REVIEW_NOT_FOUND"
    message = "Tutor review not found"
