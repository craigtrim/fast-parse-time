"""Public result types; independent of parsing services and lookup tables."""


from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum, auto
from typing import List, Optional


class DateType(Enum):

    # Full Explicit Date:
    FULL_EXPLICIT_DATE = auto()  # e.g., 03/19/2023, March 19, 2023

    # Partial Explicit Dates:
    YEAR_ONLY = auto()  # e.g., 2024
    DAY_MONTH = auto()  # e.g., March 15th
    MONTH_DAY = auto()  # e.g., 15th of March
    DAY_MONTH_AMBIGUOUS = auto()  # e.g., 4/8
    MONTH_YEAR = auto()  # e.g., March 2023
    YEAR_MONTH = auto()  # e.g., 2023-MARCH

    YEAR_RANGE = auto()  # e.g., 2014-2015
    SEASON_YEAR = auto()  # e.g., Summer 2013
    TIMEFRAME_RELATIVE_TO_NOW = auto()  # e.g., 5 days ago, next week
    NON_SPECIFIC_FUTURE_PAST = auto()  # e.g., in the future, a long time ago
    EVENT_BASED_RELATIVE_DATE = auto()  # e.g., the day after New Year's
    SEASONAL_OR_QUARTERLY = auto()  # e.g., this winter, Q1
    RECURRENT_DATE = auto()  # e.g., every Monday, annually on July 4th
    FUZZY_DATE = auto()  # e.g., late March, early 2020s
    NO_DATE = auto()  # Text chunks with no date information

    def find(input_text: str) -> Optional['DateType']:

        if not isinstance(input_text, str):
            return None

        input_text = input_text.upper().strip()
        for date_type in DateType:
            if date_type.name == input_text:
                return date_type


@dataclass
class RelativeTime:
    """Represents a relative time reference like '5 days ago'"""
    cardinality: int
    frame: str  # 'day', 'week', 'month', 'year', 'hour', 'minute', 'second'
    tense: str  # 'past' or 'future'

    def to_timedelta(self) -> timedelta:
        """Convert to Python timedelta object"""
        x = self.cardinality
        if self.tense == 'past':
            x *= -1

        if self.frame == 'year':
            x *= 365
            return timedelta(days=x)

        if self.frame == 'month':
            x *= 30  # ave. of 30 days/mo
            # if you want to get clever find the current month, then step forward or backward % 12 and get 28,29,30,31 :/
            return timedelta(days=x)

        if self.frame == 'week':
            x *= 7
            return timedelta(days=x)

        if self.frame == 'day':
            return timedelta(days=x)

        if self.frame == 'hour':
            return timedelta(hours=x)

        if self.frame == 'minute':
            return timedelta(minutes=x)

        if self.frame == 'second':
            return timedelta(seconds=x)

        raise NotImplementedError(self.frame)

    def to_datetime(self, reference: Optional[datetime] = None) -> datetime:
        """
        Convert to absolute datetime

        Args:
            reference: Reference point for calculation (defaults to now)
        """
        if reference is None:
            reference = datetime.now()
        delta = self.to_timedelta()
        # Note: to_timedelta() already handles the sign based on tense
        # (past = negative, future = positive)
        return reference + delta


@dataclass
class ExplicitDate:
    """Represents an explicit date found in text"""
    text: str  # Original text (e.g., '04/08/2024')
    date_type: str  # DateType name (e.g., 'FULL_EXPLICIT_DATE')


@dataclass
class ParseResult:
    """Combined result containing all temporal information found"""
    explicit_dates: List[ExplicitDate]
    relative_times: List[RelativeTime]

    @property
    def has_dates(self) -> bool:
        """Returns True if any temporal information was found"""
        return len(self.explicit_dates) > 0 or len(self.relative_times) > 0


@dataclass(frozen=True)
class ParsedDate:
    """One original date occurrence, including any unresolved ambiguity.

    ``candidates`` contains calendar-valid dates supported by the text/range.
    ``date`` is None unless exactly one candidate remains. Month/day/year are
    None when that component is unknown or differs between interpretations.
    A yearless date without a usable range has no concrete candidates.
    """

    text: str
    month: int | None
    day: int | None
    candidates: tuple[date, ...] = ()

    @property
    def date(self) -> date | None:
        return self.candidates[0] if len(self.candidates) == 1 else None

    @property
    def year(self) -> int | None:
        years = {candidate.year for candidate in self.candidates}
        return next(iter(years)) if len(years) == 1 else None
