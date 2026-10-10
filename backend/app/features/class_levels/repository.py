from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.class_levels.model import ClassLevel


class ClassLevelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, class_level_id: int) -> ClassLevel | None:
        return self.db.get(ClassLevel, class_level_id)

    def get_by_ids(self, class_level_ids: list[int]) -> list[ClassLevel]:
        return list(
            self.db.scalars(
                select(ClassLevel)
                .where(ClassLevel.id.in_(class_level_ids))
                .order_by(ClassLevel.id)
            )
        )
