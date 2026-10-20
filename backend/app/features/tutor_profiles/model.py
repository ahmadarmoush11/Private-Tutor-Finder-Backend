import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.subjects.model import Subject
    from app.features.tutor_posts.model import TutorPost
    from app.features.lesson_requests.model import LessonRequest
    from app.features.post_availabilities.model import PostAvailability
    from app.features.users.model import User


tutor_profile_class_levels = Table(
    "tutor_profile_class_levels",
    Base.metadata,
    Column(
        "tutor_profile_id",
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "class_level_id",
        ForeignKey("class_levels.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    ),
)

tutor_profile_subjects = Table(
    "tutor_profile_subjects",
    Base.metadata,
    Column(
        "tutor_profile_id",
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "subject_id",
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    ),
)


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
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        Enum(
            ExperienceLevel,
            name="experience_level",
            values_callable=lambda e: [member.value for member in e],
        ),
    )

    user: Mapped["User"] = relationship(back_populates="tutor_profile")
    class_levels: Mapped[list["ClassLevel"]] = relationship(
        secondary=tutor_profile_class_levels,
        order_by="ClassLevel.id",
        lazy="selectin",
    )
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=tutor_profile_subjects,
        order_by="Subject.name",
        lazy="selectin",
    )
    posts: Mapped[list["TutorPost"]] = relationship(
        back_populates="tutor",
        cascade="all, delete-orphan",
    )
    post_availabilities: Mapped[list["PostAvailability"]] = relationship(
        back_populates="tutor",
        cascade="all, delete-orphan",
    )
    lesson_requests: Mapped[list["LessonRequest"]] = relationship(
        back_populates="tutor",
        cascade="all, delete-orphan",
    )
