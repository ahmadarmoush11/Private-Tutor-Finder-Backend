from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import ForbiddenException, InvalidTokenError, UnauthorizedException
from app.core.security import decode_access_token
from app.db.dependencies import UnitOfWorkDep
from app.features.auth.service import AuthService
from app.features.users.dependencies import UserRepositoryDep
from app.features.users.model import User, UserRole


bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(
    user_repository: UserRepositoryDep,
    uow: UnitOfWorkDep,
) -> AuthService:
    return AuthService(user_repository, uow)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


def get_current_user(
    user_repository: UserRepositoryDep,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ] = None,
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


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole):
    def checker(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise ForbiddenException()
        return current_user

    return checker


require_admin = require_roles(UserRole.ADMIN)
require_client = require_roles(UserRole.CLIENT)
require_tutor = require_roles(UserRole.TUTOR)

AdminUser = Annotated[User, Depends(require_admin)]
ClientUser = Annotated[User, Depends(require_client)]
TutorUser = Annotated[User, Depends(require_tutor)]
