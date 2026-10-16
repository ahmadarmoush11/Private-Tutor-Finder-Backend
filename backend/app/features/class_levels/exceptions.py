from app.core.exceptions import NotFoundException


class ClassLevelNotFoundError(NotFoundException):
    error_code = "CLASS_LEVEL_NOT_FOUND"
    message = "Class level not found"
