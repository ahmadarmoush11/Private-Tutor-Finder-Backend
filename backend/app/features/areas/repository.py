from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.areas.model import Area


class AreaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, area_id: int) -> Area | None:
        return self.db.get(Area, area_id)

    def get_all(self, governorate: str | None, district: str | None) -> list[Area]:
        statement = select(Area)
        if governorate:
            statement = statement.where(Area.governorate == governorate)
        if district:
            statement = statement.where(Area.district == district)
        return list(
            self.db.scalars(statement.order_by(Area.governorate, Area.district, Area.name))
        )

    def get_governorates(self) -> list[str]:
        return list(
            self.db.scalars(select(Area.governorate).distinct().order_by(Area.governorate))
        )

    def get_districts(self, governorate: str | None) -> list[tuple[str, str]]:
        statement = select(Area.district, Area.governorate).distinct()
        if governorate:
            statement = statement.where(Area.governorate == governorate)
        return [
            (district, district_governorate)
            for district, district_governorate in self.db.execute(
                statement.order_by(Area.governorate, Area.district)
            )
        ]
