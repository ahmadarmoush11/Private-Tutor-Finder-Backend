from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_current_user
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
    return auth_service.register(data)


@router.post("/login", response_model=AuthResponse)
def login(
    data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(data.email, data.password)


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
