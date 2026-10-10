from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import LessonLocation, PostStatus

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.client_profiles.model import ClientProfile


class ClientPost(TimestampMixin, Base):
    __tablename__ = "client_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    class_level_id: Mapped[int] = mapped_column(
        ForeignKey("class_levels.id", ondelete="RESTRICT"),
        index=True,
    )
    school_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
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
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address_details: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)

    client: Mapped["ClientProfile"] = relationship(back_populates="posts")
    class_level: Mapped["ClassLevel"] = relationship(back_populates="posts")
