from fastapi import APIRouter, status

from app.features.auth.dependencies import AuthServiceDep, CurrentUser
from app.features.auth.schemas import AuthResponse, UserLogin, UserRegister
from app.features.users.schemas import UserOut


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserRegister, auth_service: AuthServiceDep):
    return auth_service.register(data)


@router.post("/login", response_model=AuthResponse)
def login(data: UserLogin, auth_service: AuthServiceDep):
    return auth_service.login(data.email, data.password)


@router.get("/me", response_model=UserOut)
def read_me(current_user: CurrentUser):
    return current_user
