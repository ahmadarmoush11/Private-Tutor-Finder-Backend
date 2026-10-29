from app.core.exceptions import NotFoundException


class AreaNotFoundError(NotFoundException):
    error_code = "AREA_NOT_FOUND"
    message = "Area not found"
