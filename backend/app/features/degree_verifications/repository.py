from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.features.degree_verifications.model import DegreeVerification
from app.features.tutor_profiles.model import TutorProfile
from app.shared.enums import VerificationStatus

def _load_details():
    return (
        selectinload(DegreeVerification.degree_photos),
        selectinload(DegreeVerification.national_id_photos),
        selectinload(DegreeVerification.tutor_profile).selectinload(TutorProfile.user),
        selectinload(DegreeVerification.reviewed_by),
    )


class DegreeVerificationRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db=db

    def create(self, degree_verification: DegreeVerification)-> DegreeVerification:
        self.db.add(degree_verification)
        self.db.flush()
        self.db.refresh(degree_verification)
        return degree_verification

        

    def get_by_id_for_admin(self, degree_verification_id: int)->DegreeVerification:
        return self.db.scalar(
            select(DegreeVerification)
            .options(*_load_details())
            .where(DegreeVerification.id==degree_verification_id, DegreeVerification.status != VerificationStatus.CANCELLED)
        )

    
    def get_by_id_for_tutor(self, tutor_profile_id: int, degree_verification_id: int)->DegreeVerification:
        return self.db.scalar(
            select(DegreeVerification)
            .options(*_load_details())
            .where(DegreeVerification.id==degree_verification_id, DegreeVerification.tutor_profile_id==tutor_profile_id)
        )

    def get_all_for_admin(self, status: VerificationStatus | None, tutor_profile_id: int | None)->list[DegreeVerification]:
        statement= (select(DegreeVerification)
            .options(*_load_details())
        )

        if tutor_profile_id is not None:
            statement= statement.where(DegreeVerification.tutor_profile_id== tutor_profile_id)

        if status is None:
            statement = statement.where(DegreeVerification.status != VerificationStatus.CANCELLED)
        
        else:
            statement= statement.where(DegreeVerification.status== status)

        return list(self.db.scalars(statement.order_by(DegreeVerification.created_at.desc(), DegreeVerification.id.desc())))

    def get_all_for_tutor(self, tutor_profile_id: int, status: VerificationStatus | None)->list[DegreeVerification]:
        statement=(
            select(DegreeVerification)
            .options(*_load_details())
            .where(DegreeVerification.tutor_profile_id==tutor_profile_id)
        )

        if status is not None:
            statement= statement.where(DegreeVerification.status == status)

        return list(self.db.scalars(statement.order_by(DegreeVerification.created_at.desc(), DegreeVerification.id.desc())))

    

    def update(self, degree_verification: DegreeVerification)->DegreeVerification:
        self.db.flush()
        self.db.refresh(degree_verification)
        return degree_verification

    def verify(self, degree_verification: DegreeVerification)->DegreeVerification:
        self.db.flush()
        self.db.refresh(degree_verification)
        return degree_verification


    def delete(self, degree_verification: DegreeVerification)->None:

        self.db.delete(degree_verification)
        self.db.flush()

    


