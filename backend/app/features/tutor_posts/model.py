from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import Column, Enum, ForeignKey, Numeric, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import Currency, LessonLocation, PostStatus, PriceUnit

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.client_requests.model import ClientRequest
    from app.features.subjects.model import Subject
    from app.features.tutor_profiles.model import TutorProfile
    from app.features.users.model import User


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


tutor_post_subjects = Table(
    "tutor_post_subjects",
    Base.metadata,
    Column(
        "tutor_post_id",
        ForeignKey("tutor_posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "subject_id",
        ForeignKey("subjects.id", ondelete="RESTRICT"),
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
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[Currency | None] = mapped_column(
        Enum(
            Currency,
            name="currency",
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=True,
    )
    price_unit: Mapped[PriceUnit | None] = mapped_column(
        Enum(
            PriceUnit,
            name="price_unit",
            values_callable=lambda e: [member.value for member in e],
        ),
        nullable=True,
    )

    tutor: Mapped["TutorProfile"] = relationship(back_populates="posts")
    requests: Mapped[list["ClientRequest"]] = relationship(
        back_populates="tutor_post",
        cascade="all, delete-orphan",
    )
    class_levels: Mapped[list["ClassLevel"]] = relationship(
        secondary=tutor_post_class_levels,
        back_populates="tutor_posts",
    )
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=tutor_post_subjects,
        back_populates="tutor_posts",
        order_by="Subject.name",
    )

    @property
    def author(self) -> "User":
        return self.tutor.user
