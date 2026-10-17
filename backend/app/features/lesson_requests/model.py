from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, Index, Table, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.shared.enums import LessonLocation, RequestStatus

if TYPE_CHECKING:
    from app.features.class_levels.model import ClassLevel
    from app.features.client_profiles.model import ClientProfile
    from app.features.subjects.model import Subject
    from app.features.tutor_profiles.model import TutorProfile


lesson_request_subjects = Table(
    "lesson_request_subjects",
    Base.metadata,
    Column(
        "lesson_request_id",
        ForeignKey("lesson_requests.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "subject_id",
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    ),
)


class LessonRequest(TimestampMixin, Base):
    __tablename__ = "lesson_requests"
    __table_args__ = (
        Index(
            "uq_lesson_requests_pending",
            "client_id",
            "tutor_id",
            unique=True,
            postgresql_where=text("status = 'pending'"),
            sqlite_where=text("status = 'pending'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("client_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor_profiles.id", ondelete="CASCADE"),
        index=True,
    )
    class_level_id: Mapped[int] = mapped_column(
        ForeignKey("class_levels.id", ondelete="RESTRICT"),
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
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RequestStatus] = mapped_column(
        Enum(
            RequestStatus,
            name="request_status",
            values_callable=lambda e: [member.value for member in e],
        ),
        default=RequestStatus.PENDING,
        server_default=RequestStatus.PENDING.value,
        index=True,
    )

    client: Mapped["ClientProfile"] = relationship(back_populates="lesson_requests")
    tutor: Mapped["TutorProfile"] = relationship(back_populates="lesson_requests")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=lesson_request_subjects,
        order_by="Subject.name",
    )
    class_level: Mapped["ClassLevel"] = relationship()
