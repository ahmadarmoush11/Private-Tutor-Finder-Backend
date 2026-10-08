import enum
import re
from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.base import Base

if TYPE_CHECKING:
    from app.features.client_posts.model import ClientPost


class EducationLevel(str, enum.Enum):
    PRESCHOOL = "preschool"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    SECONDARY = "secondary"
    HIGHER_EDUCATION = "higher_education"


def determine_education_level(name: str) -> EducationLevel:
    normalized = name.strip().lower()

    if re.fullmatch(r"kg\s*[1-3]", normalized):
        return EducationLevel.PRESCHOOL

    grade_match = re.fullmatch(r"grade\s*(\d{1,2})", normalized)
    if grade_match:
        grade = int(grade_match.group(1))
        if 1 <= grade <= 6:
            return EducationLevel.ELEMENTARY
        if 7 <= grade <= 9:
            return EducationLevel.INTERMEDIATE
        if 10 <= grade <= 12:
            return EducationLevel.SECONDARY

    if "university" in normalized:
        return EducationLevel.HIGHER_EDUCATION

    raise ValueError(f"Cannot determine education level for class level '{name}'")


class ClassLevel(Base):
    __tablename__ = "class_levels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    level: Mapped[EducationLevel] = mapped_column(
        Enum(
            EducationLevel,
            name="education_level",
            values_callable=lambda e: [member.value for member in e],
        ),
        index=True,
    )

    posts: Mapped[list["ClientPost"]] = relationship(back_populates="class_level")

    @validates("name")
    def _set_level_from_name(self, key: str, value: str) -> str:
        value = value.strip()
        self.level = determine_education_level(value)
        return value

    def __repr__(self) -> str:
        return f"<ClassLevel id={self.id} name={self.name!r} level={self.level.value}>"
