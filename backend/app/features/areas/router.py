from fastapi import APIRouter

from app.features.areas.dependencies import AreaServiceDep
from app.features.areas.schemas import AreaOut, DistrictOut


router = APIRouter(prefix="/areas", tags=["Areas"])


@router.get("/governorates", response_model=list[str])
def get_governorates(service: AreaServiceDep):
    return service.get_governorates()


@router.get("/districts", response_model=list[DistrictOut])
def get_districts(service: AreaServiceDep, governorate: str | None = None):
    return service.get_districts(governorate)


@router.get("", response_model=list[AreaOut])
def get_areas(
    service: AreaServiceDep,
    governorate: str | None = None,
    district: str | None = None,
):
    return service.get_all(governorate, district)


@router.get("/{area_id}", response_model=AreaOut)
def get_area(area_id: int, service: AreaServiceDep):
    return service.get_by_id(area_id)
