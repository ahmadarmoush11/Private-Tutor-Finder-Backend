import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Area


logger = logging.getLogger(__name__)

AREAS_FILE = Path(__file__).resolve().parents[3] / "data" / "locations" / "lebanon_locations.json"


def seed_areas(db: Session) -> int:
    if not AREAS_FILE.exists():
        logger.warning("Areas file not found at %s, skipping area seed", AREAS_FILE)
        return 0

    rows = json.loads(AREAS_FILE.read_text(encoding="utf-8"))
    existing = set(db.execute(select(Area.name, Area.district)).all())
    missing = [row for row in rows if (row["name"], row["district"]) not in existing]

    if not missing:
        return 0

    db.add_all(
        Area(
            name=row["name"],
            district=row["district"],
            governorate=row["governorate"],
            latitude=row["latitude"],
            longitude=row["longitude"],
        )
        for row in missing
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return 0

    logger.info("Seeded %d areas", len(missing))
    return len(missing)
