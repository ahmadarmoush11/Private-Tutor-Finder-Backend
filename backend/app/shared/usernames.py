import re

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30
USERNAME_PATTERN = re.compile(r"^[a-z0-9._]+$")


def normalize_username(value: str) -> str:
    value = value.strip().lower()
    if not USERNAME_MIN_LENGTH <= len(value) <= USERNAME_MAX_LENGTH:
        raise ValueError(
            f"must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters"
        )
    if not USERNAME_PATTERN.match(value):
        raise ValueError("may only contain letters, numbers, dots and underscores")
    return value

