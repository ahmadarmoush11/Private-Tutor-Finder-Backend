from typing import Annotated, Any

from pydantic import BeforeValidator, StringConstraints


def _strip_to_none(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


OptionalText = Annotated[
    Annotated[str, StringConstraints(max_length=150)] | None,
    BeforeValidator(_strip_to_none),
]
