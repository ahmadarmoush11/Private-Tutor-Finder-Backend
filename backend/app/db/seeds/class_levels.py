import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import ClassLevel


logger = logging.getLogger(__name__)

CLASS_LEVEL_NAMES = [
    "KG1",
    "KG2",
    "KG3",
    *[f"Grade {grade}" for grade in range(1, 13)],
    "University",
]


def seed_class_levels(db: Session) -> int:
    existing_names = set(db.scalars(select(ClassLevel.name)))
    missing_names = [name for name in CLASS_LEVEL_NAMES if name not in existing_names]

    if not missing_names:
        return 0

    db.add_all(ClassLevel(name=name) for name in missing_names)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return 0

    logger.info("Seeded %d class levels", len(missing_names))
    return len(missing_names)
