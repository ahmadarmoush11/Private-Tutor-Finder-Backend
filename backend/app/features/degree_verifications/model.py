from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import VerificationStatus

if TYPE_CHECKING:
    from app.features.tutor_profiles.model import TutorProfile
    from app.features.users.model import User


class DegreeVerification(TimestampMixin, Base):
    __tablename__ = "degree_verifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_profile_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    degree: Mapped[str] = mapped_column(String(150))
    status: Mapped[VerificationStatus] = mapped_column(
        Enum(
            VerificationStatus,
            name="verification_status",
            values_callable=lambda e: [member.value for member in e],
        ),
        default=VerificationStatus.PENDING,
        server_default=VerificationStatus.PENDING.value,
        index=True,
    )
    reviewed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    tutor_profile: Mapped["TutorProfile"] = relationship()
    reviewed_by: Mapped["User | None"] = relationship()
    degree_photos: Mapped[list["DegreePhoto"]] = relationship(
        back_populates="degree_verification",
        cascade="all, delete-orphan",
        order_by="DegreePhoto.id",
    )
    national_id_photos: Mapped[list["NationalIdPhoto"]] = relationship(
        back_populates="degree_verification",
        cascade="all, delete-orphan",
        order_by="NationalIdPhoto.id",
    )


class DegreePhoto(Base):
    __tablename__ = "degree_photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    degree_verification_id: Mapped[int] = mapped_column(
        ForeignKey("degree_verifications.id", ondelete="CASCADE"),
        index=True,
    )
    photo_path: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    degree_verification: Mapped["DegreeVerification"] = relationship(
        back_populates="degree_photos"
    )


class NationalIdPhoto(Base):
    __tablename__ = "national_id_photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    degree_verification_id: Mapped[int] = mapped_column(
        ForeignKey("degree_verifications.id", ondelete="CASCADE"),
        index=True,
    )
    photo_path: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    degree_verification: Mapped["DegreeVerification"] = relationship(
        back_populates="national_id_photos"
    )
