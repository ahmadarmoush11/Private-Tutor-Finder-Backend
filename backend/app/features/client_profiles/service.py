from app.core.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError
from app.db.unit_of_work import UnitOfWork
from app.features.client_profiles.model import ClientProfile
from app.features.users.model import User
from app.features.client_profiles.repository import ClientProfileRepository
from app.features.client_profiles.schemas import ClientProfileCreate, ClientProfileUpdate


class ClientProfileService:
    def __init__(self, client_profile_repository: ClientProfileRepository, uow: UnitOfWork):
        self.client_profile_repository = client_profile_repository
        self.uow = uow

    def get_by_user_id(self, user_id: int) -> ClientProfile:
        profile = self.client_profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFoundError("Client profile not found")
        return profile

    def get_client_profile(
        self,
        client_id: int,
    )->ClientProfile:
        profile=self.client_profile_repository.get_client_profile(client_id)

        if profile is None:
            raise ProfileNotFoundError("Client profile not found")

        return profile

        

    def create(self, user: User, data: ClientProfileCreate) -> ClientProfile:
        if self.client_profile_repository.get_by_user_id(user.id):
            raise ProfileAlreadyExistsError()
        profile = ClientProfile(user_id=user.id, **data.model_dump())
        with self.uow:
            profile = self.client_profile_repository.create(profile)
        return profile

    def update(self, user: User, data: ClientProfileUpdate) -> ClientProfile:
        profile = self.get_by_user_id(user.id)
        values = data.model_dump(exclude_unset=True)
        with self.uow:
            profile = self.client_profile_repository.update(profile, values)
        return profile
