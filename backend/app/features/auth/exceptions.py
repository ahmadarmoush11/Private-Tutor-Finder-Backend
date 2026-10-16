from app.core.exceptions import UnauthorizedException


class InvalidCredentialsError(UnauthorizedException):
    error_code = "INVALID_CREDENTIALS"
    message = "Incorrect email or password"


class InvalidTokenError(UnauthorizedException):
    error_code = "INVALID_TOKEN"
    message = "Could not validate credentials"
