from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_current_user
from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.models.user import User
from app.schemas.auth import AuthResponse
from app.schemas.user import UserLogin, UserOut, UserRegister
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return auth_service.register(data)
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )


@router.post("/login", response_model=AuthResponse)
def login(
    data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return auth_service.login(data.email, data.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
