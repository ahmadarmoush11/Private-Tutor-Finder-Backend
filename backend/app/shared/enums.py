import enum


class PostStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class LessonLocation(str, enum.Enum):
    CLIENT_HOME = "client_home"
    TUTOR_HOME = "tutor_home"
    ANY = "any"

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class Currency(str, enum.Enum):
    USD = "USD"
    LBP = "LBP"


class PriceUnit(str, enum.Enum):
    HOUR = "hour"
    SESSION = "session"
    WEEK = "week"
    MONTH = "month"


class NotificationType(str, enum.Enum):
    TUTOR_AVAILABLE = "tutor_available"
    LESSON_REQUEST_RECEIVED = "lesson_request_received"
    LESSON_REQUEST_ACCEPTED = "lesson_request_accepted"
    LESSON_REQUEST_REJECTED = "lesson_request_rejected"
    LESSON_REQUEST_CONFIRMED = "lesson_request_confirmed"
