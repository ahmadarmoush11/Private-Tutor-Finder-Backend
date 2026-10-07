from app.core.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse
from app.schemas.user import UserOut, UserRegister


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, data: UserRegister) -> AuthResponse:
        if self.user_repository.get_by_email(data.email):
            raise EmailAlreadyRegisteredError()

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hash_password(data.password),
            phone_number=data.phone_number,
            role=UserRole(data.role),
        )
        user = self.user_repository.create(user)
        return self._build_auth_response(user)

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        return user

    def login(self, email: str, password: str) -> AuthResponse:
        user = self.authenticate(email, password)
        return self._build_auth_response(user)

    @staticmethod
    def _build_auth_response(user: User) -> AuthResponse:
        token = create_access_token(user.id, user.role.value)
        return AuthResponse(access_token=token, user=UserOut.model_validate(user))
