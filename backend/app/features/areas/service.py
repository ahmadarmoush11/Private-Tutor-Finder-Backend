from app.features.areas.exceptions import AreaNotFoundError
from app.features.areas.model import Area
from app.features.areas.repository import AreaRepository
from app.features.areas.schemas import DistrictOut


class AreaService:
    def __init__(self, area_repository: AreaRepository):
        self.area_repository = area_repository

    def get_all(self, governorate: str | None, district: str | None) -> list[Area]:
        return self.area_repository.get_all(governorate, district)

    def get_by_id(self, area_id: int) -> Area:
        area = self.area_repository.get_by_id(area_id)
        if area is None:
            raise AreaNotFoundError()
        return area

    def get_governorates(self) -> list[str]:
        return self.area_repository.get_governorates()

    def get_districts(self, governorate: str | None) -> list[DistrictOut]:
        return [
            DistrictOut(name=name, governorate=district_governorate)
            for name, district_governorate in self.area_repository.get_districts(governorate)
        ]
