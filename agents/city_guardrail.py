"""Input validation guardrail for city names.

This keeps the workflow from sending obviously invalid input into the agent
pipeline, which avoids hallucinated output when the user does not provide a
real city name.
"""

import re


class CityNameValidationError(ValueError):
    """Raised when the supplied city input is not a valid city name."""


_CITY_NAME_PATTERN = re.compile(r"^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’\-\.\s,]{0,78}$")
_REQUEST_WORDS = {
    "please",
    "weather",
    "forecast",
    "brief",
    "report",
    "city",
    "show",
    "give",
    "tell",
    "check",
    "run",
    "generate",
    "about",
    "today",
    "tomorrow",
    "next",
    "hour",
    "risk",
}


def validate_city_name(city: str) -> str:
    """Return a normalized city name or raise CityNameValidationError."""
    if city is None:
        raise CityNameValidationError("Please type a city name, for example: Mumbai or New York.")

    normalized_city = " ".join(city.strip().split())
    if not normalized_city:
        raise CityNameValidationError("Please type a city name, for example: Mumbai or New York.")

    if len(normalized_city) > 80:
        raise CityNameValidationError("City name is too long. Please type only the city name.")

    lowered = normalized_city.lower()
    if any(marker in lowered for marker in ("http://", "https://", "www.", "@", "/", "\\")):
        raise CityNameValidationError("Please type only a city name, not a URL or email address.")

    if not _CITY_NAME_PATTERN.fullmatch(normalized_city):
        raise CityNameValidationError("Please type only a city name using letters and spaces.")

    tokens = [token.strip(".,") for token in re.split(r"[\s,]+", normalized_city) if token.strip(".,")]
    if not tokens:
        raise CityNameValidationError("Please type a city name, for example: Mumbai or New York.")

    if len(tokens) > 4:
        raise CityNameValidationError("Please type only the city name, not a full sentence.")

    if any(token.lower() in _REQUEST_WORDS for token in tokens):
        raise CityNameValidationError("Please type only a city name, such as Mumbai or New York.")

    if any(any(character.isdigit() for character in token) for token in tokens):
        raise CityNameValidationError("Please type a city name without numbers.")

    return normalized_city