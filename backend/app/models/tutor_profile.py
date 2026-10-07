import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class ExperienceLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERIENCED = "experienced"
    EXPERT = "expert"


class TutorProfile(TimestampMixin, Base):
    __tablename__ = "tutor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    workplace: Mapped[str | None] = mapped_column(String(150), nullable=True)
    degree: Mapped[str | None] = mapped_column(String(150), nullable=True)
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        Enum(
            ExperienceLevel,
            name="experience_level",
            values_callable=lambda e: [member.value for member in e],
        ),
    )

    user: Mapped["User"] = relationship(back_populates="tutor_profile")
