"""Internal numeric date component types."""

from enum import Enum, auto


class DateComponentType(Enum):
    YEAR = auto()  # e.g., now-100 < now < now+5
    MONTH = auto()  # e.g., 1-12 (with context)
    DAY = auto()  # e.g., 1-31 (with context)
    DAY_OR_MONTH = auto()  # e.g., 1-31 (without context)
