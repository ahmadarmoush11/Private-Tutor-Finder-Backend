from app.core.exceptions import(
    NotFoundException,
    ConflictException,
    BadRequestException
)


class DegreeVerificationRequestNotFound(NotFoundException):
    error_code="DEGREE_VERIFICATION_REQUEST_NOT_FOUND"
    message="The degree verification request was not found"

class DegreeVerificationResponseError(BadRequestException):
    error_code="DEGREE_VERIFICATION_RESPONSE_ERROR"
    message="The review status must be verified or rejected"

class DegreeVerificationIsCancelledError(ConflictException):
    error_code = "DEGREE_VERIFICATION_IS_CANCELLED"
    message = "This verification request is cancelled"

class DegreeVerificationIsNotPendingError(ConflictException):
    error_code = "DEGREE_VERIFICATION_NOT_PENDING"
    message = "This verification request is no longer pending"