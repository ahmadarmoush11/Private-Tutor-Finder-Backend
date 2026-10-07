from app.core.exceptions import ProfileAlreadyExistsError, ProfileNotFoundError
from app.models.tutor_profile import TutorProfile
from app.models.user import User
from app.repositories.tutor_profile_repository import TutorProfileRepository
from app.schemas.tutor_profile import TutorProfileCreate, TutorProfileUpdate


class TutorProfileService:
    def __init__(self, tutor_profile_repository: TutorProfileRepository):
        self.tutor_profile_repository = tutor_profile_repository

    def get_by_user_id(self, user_id: int) -> TutorProfile:
        profile = self.tutor_profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFoundError("Tutor profile not found")
        return profile

    def create(self, user: User, data: TutorProfileCreate) -> TutorProfile:
        if self.tutor_profile_repository.get_by_user_id(user.id):
            raise ProfileAlreadyExistsError()
        profile = TutorProfile(user_id=user.id, **data.model_dump())
        return self.tutor_profile_repository.create(profile)

    def update(self, user: User, data: TutorProfileUpdate) -> TutorProfile:
        profile = self.get_by_user_id(user.id)
        values = data.model_dump(exclude_unset=True)
        return self.tutor_profile_repository.update(profile, values)
