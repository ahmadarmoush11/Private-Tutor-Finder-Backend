from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, InvalidTokenError, UnauthorizedException
from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.repositories.client_profile_repository import ClientProfileRepository
from app.repositories.tutor_profile_repository import TutorProfileRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.client_profile_service import ClientProfileService
from app.services.tutor_profile_service import TutorProfileService


bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_client_profile_repository(
    db: Session = Depends(get_db),
) -> ClientProfileRepository:
    return ClientProfileRepository(db)


def get_tutor_profile_repository(
    db: Session = Depends(get_db),
) -> TutorProfileRepository:
    return TutorProfileRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)


def get_client_profile_service(
    client_profile_repository: ClientProfileRepository = Depends(
        get_client_profile_repository
    ),
) -> ClientProfileService:
    return ClientProfileService(client_profile_repository)


def get_tutor_profile_service(
    tutor_profile_repository: TutorProfileRepository = Depends(
        get_tutor_profile_repository
    ),
) -> TutorProfileService:
    return TutorProfileService(tutor_profile_repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    if credentials is None:
        raise UnauthorizedException()

    payload = decode_access_token(credentials.credentials)
    if payload is None or "sub" not in payload:
        raise InvalidTokenError()

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise InvalidTokenError()

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise InvalidTokenError()
    return user


def require_roles(*roles: UserRole):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenException()
        return current_user

    return checker


require_admin = require_roles(UserRole.ADMIN)
require_client = require_roles(UserRole.CLIENT)
require_tutor = require_roles(UserRole.TUTOR)
