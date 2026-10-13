from datetime import date


def calculate_age(date_of_birth: date, today: date | None = None) -> int:
    today = today or date.today()
    had_birthday_this_year = (today.month, today.day) >= (
        date_of_birth.month,
        date_of_birth.day,
    )
    return today.year - date_of_birth.year - (0 if had_birthday_this_year else 1)
