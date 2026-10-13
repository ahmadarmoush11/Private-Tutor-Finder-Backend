import logging

from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Subject


logger = logging.getLogger(__name__)

SUBJECT_NAMES = [
    "Arabic",
    "English",
    "Math",
    "Physics",
    "Chemistry",
    "Life and Earth Science",
    "Geography",
    "History",
]


def seed_subjects(db: Session) -> int:
    if db.scalar(select(exists().select_from(Subject))):
        return 0

    db.add_all(Subject(name=name) for name in SUBJECT_NAMES)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return 0

    logger.info("Seeded %d subjects", len(SUBJECT_NAMES))
    return len(SUBJECT_NAMES)
