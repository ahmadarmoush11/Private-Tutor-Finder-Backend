from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, Numeric, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import Currency, LessonLocation, PostStatus, PriceUnit

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.client_profiles.model import ClientProfile
    from app.features.subjects.model import Subject
    from app.features.applications.model import Application
    from app.features.users.model import User


client_post_subjects = Table(
    "client_post_subjects",
    Base.metadata,
    Column(
        "client_post_id",
        ForeignKey("client_posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "subject_id",
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    ),
)


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
    budget_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    budget_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
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

    client: Mapped["ClientProfile"] = relationship(back_populates="posts")
    class_level: Mapped["ClassLevel"] = relationship(back_populates="posts")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=client_post_subjects,
        back_populates="client_posts",
        order_by="Subject.name",
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="client_post",
        cascade="all, delete-orphan",
    )

    @property
    def author(self) -> "User":
        return self.client.user
