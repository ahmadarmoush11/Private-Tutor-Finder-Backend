from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_error

    payload = decode_access_token(credentials.credentials)
    if payload is None or "sub" not in payload:
        raise credentials_error

    try:
        user_id = int(payload["sub"])
    except (TypeError, ValueError):
        raise credentials_error

    user = user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_error
    return user


def require_roles(*roles: UserRole):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to do this",
            )
        return current_user

    return checker
