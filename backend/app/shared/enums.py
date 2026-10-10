import enum


class PostStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class LessonLocation(str, enum.Enum):
    CLIENT_HOME = "client_home"
    TUTOR_HOME = "tutor_home"
    ANY = "any"
