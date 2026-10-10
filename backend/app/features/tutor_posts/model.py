from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import LessonLocation, PostStatus

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.tutor_profiles.model import TutorProfile


tutor_post_class_levels = Table(
    "tutor_post_class_levels",
    Base.metadata,
    Column(
        "tutor_post_id",
        ForeignKey("tutor_posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "class_level_id",
        ForeignKey("class_levels.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    ),
)


class TutorPost(TimestampMixin, Base):
    __tablename__ = "tutor_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    lesson_location: Mapped[LessonLocation] = mapped_column(
        Enum(
            LessonLocation,
            name="lesson_location",
            values_callable=lambda e: [member.value for member in e],
        ),
        default=LessonLocation.ANY,
        server_default=LessonLocation.ANY.value,
        index=True,
    )
    status: Mapped[PostStatus] = mapped_column(
        Enum(
            PostStatus,
            name="post_status",
            values_callable=lambda e: [member.value for member in e],
        ),
        default=PostStatus.ACTIVE,
        server_default=PostStatus.ACTIVE.value,
        index=True,
    )
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address_details: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)

    tutor: Mapped["TutorProfile"] = relationship(back_populates="posts")
    class_levels: Mapped[list["ClassLevel"]] = relationship(
        secondary=tutor_post_class_levels,
        back_populates="tutor_posts",
    )
