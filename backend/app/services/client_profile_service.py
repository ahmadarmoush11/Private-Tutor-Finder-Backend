from app.core.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError
from app.models.client_profile import ClientProfile
from app.models.user import User
from app.repositories.client_profile_repository import ClientProfileRepository
from app.schemas.client_profile import ClientProfileCreate, ClientProfileUpdate


class ClientProfileService:
    def __init__(self, client_profile_repository: ClientProfileRepository):
        self.client_profile_repository = client_profile_repository

    def get_by_user_id(self, user_id: int) -> ClientProfile:
        profile = self.client_profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFoundError("Client profile not found")
        return profile

    def create(self, user: User, data: ClientProfileCreate) -> ClientProfile:
        if self.client_profile_repository.get_by_user_id(user.id):
            raise ProfileAlreadyExistsError()
        profile = ClientProfile(user_id=user.id, **data.model_dump())
        return self.client_profile_repository.create(profile)

    def update(self, user: User, data: ClientProfileUpdate) -> ClientProfile:
        profile = self.get_by_user_id(user.id)
        values = data.model_dump(exclude_unset=True)
        return self.client_profile_repository.update(profile, values)
