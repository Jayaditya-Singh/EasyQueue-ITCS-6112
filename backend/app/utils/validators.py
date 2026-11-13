import re

_PHONE_DIGITS = re.compile(r"\d")


def normalize_phone_number(phone_number: str) -> str:
    """Return the phone number as 10 digits, or raise ValueError.

    Accepts common formats like "(704) 555-1234", "704.555.1234" and
    "+1 704 555 1234".
    """
    digits = "".join(_PHONE_DIGITS.findall(phone_number or ""))

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        raise ValueError("Phone number must have 10 digits.")

    return digits


def clean_name(name: str) -> str:
    """Trim and collapse whitespace; raise ValueError if nothing is left."""
    cleaned = " ".join((name or "").split())

    if not cleaned:
        raise ValueError("Name is required.")

    if len(cleaned) > 100:
        raise ValueError("Name must be 100 characters or fewer.")

    return cleaned
