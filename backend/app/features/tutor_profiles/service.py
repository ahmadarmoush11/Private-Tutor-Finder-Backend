from app.core.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError
from app.db.unit_of_work import UnitOfWork
from app.features.tutor_profiles.model import TutorProfile
from app.features.users.model import User
from app.features.tutor_profiles.repository import TutorProfileRepository
from app.features.tutor_profiles.schemas import TutorProfileCreate, TutorProfileUpdate


class TutorProfileService:
    def __init__(self, tutor_profile_repository: TutorProfileRepository, uow: UnitOfWork):
        self.tutor_profile_repository = tutor_profile_repository
        self.uow = uow

    def get_by_user_id(self, user_id: int) -> TutorProfile:
        profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return profile

    def create(self, user: User, data: TutorProfileCreate) -> TutorProfile:
        if self.tutor_profile_repository.get_by_user_id(user.id):
            raise ProfileAlreadyExistsError()
        profile = TutorProfile(user_id=user.id, **data.model_dump())
        with self.uow:
            profile = self.tutor_profile_repository.create(profile)
        return profile

    def update(self, user: User, data: TutorProfileUpdate) -> TutorProfile:
        profile = self.get_by_user_id(user.id)
        values = data.model_dump(exclude_unset=True)
        with self.uow:
            profile = self.tutor_profile_repository.update(profile, values)
        return profile
