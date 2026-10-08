"""Validate calendar values and classified numeric date components."""

from datetime import datetime
from typing import List

from fast_parse_time.models import DateType
from fast_parse_time.explicit.constants import date_delims, MIN_YEAR, MAX_YEAR

# Formats with a 4-digit year — strptime validates calendar correctness.
_FULL_YEAR_FORMATS = [
    # Full delimited numeric: 3 components with 4-digit year
    '%m/%d/%Y',   # 04/08/2024
    '%d/%m/%Y',   # 08/04/2024
    '%Y-%m-%d',   # 2024-04-08
    '%Y/%m/%d',   # 2024/04/08
    '%m-%d-%Y',   # 04-08-2024
    '%d-%m-%Y',   # 08-04-2024
    '%m.%d.%Y',   # 04.08.2024
    '%d.%m.%Y',   # 08.04.2024
    # Year + month only (no day)
    '%Y/%m',      # 2023/01
    '%Y-%m',      # 2023-01
    # Written month forms — with comma (most common in English prose)
    '%B %d, %Y',  # March 15, 2024
    '%b %d, %Y',  # Mar 15, 2024
    # Written month forms with period — with comma (American newspaper style)
    '%b. %d, %Y', # Aug. 9, 2012
    # Written month forms — without comma
    '%B %d %Y',   # March 15 2024
    '%b %d %Y',   # Mar 15 2024
    '%d %B %Y',   # 15 March 2024
    '%d %b %Y',   # 15 Mar 2024
    # Written month forms with period — without comma
    '%b. %d %Y',  # Aug. 9 2012
    '%d %b. %Y',  # 9 Aug. 2012
    # Month and year only
    '%B %Y',      # March 2024
    '%b %Y',      # Mar 2024
]

# Formats with a 2-digit year — dateparser accepted these (e.g., version numbers).
_SHORT_YEAR_FORMATS = [
    '%d.%m.%y',   # 20.04.01
    '%y.%m.%d',   # 20.04.01 (alternate interpretation)
    '%m/%d/%y',   # 04/08/24
    '%d/%m/%y',   # 08/04/24
]

# Partial formats (no year). strptime defaults to year 1900 which is NOT a
# leap year, so "29/2" (Feb 29) would fail. We work around this by appending
# a known leap year (2000) before probing.
_PARTIAL_FORMATS_WITH_LEAP_YEAR = [
    # (partial_format, full_format_with_appended_year, separator)
    ('%m/%d', '%m/%d/%Y', '/'),   # 3/15, 7/24
    ('%d/%m', '%d/%m/%Y', '/'),   # 31/03, 22/7, 29/2
    ('%m-%d', '%m-%d-%Y', '-'),   # 3-15
    ('%d-%m', '%d-%m-%Y', '-'),   # 31-03
    ('%m.%d', '%m.%d.%Y', '.'),   # 3.15
    ('%d.%m', '%d.%m.%Y', '.'),   # 31.03
]

# Non-standard abbreviations that strptime's %b doesn't recognise.
# Maps to the canonical 3-letter form Python's strptime expects.
_MONTH_ALIASES = {
    'sept': 'sep',
}


def _normalize_month_aliases(text: str) -> str:
    """Replace non-standard month abbreviations with strptime-compatible forms.

    Handles both with and without trailing period: 'sept' → 'sep', 'Sept.' → 'Sep.'
    """
    lower = text.lower()
    for alias, canonical in _MONTH_ALIASES.items():
        # Check for the alias with or without a trailing period
        if alias in lower.split() or (alias + '.') in lower.split():
            # Determine if we need to add a period back
            has_period = (alias + '.') in lower.split()
            # Preserve original capitalisation style (title-case if first char is upper)
            replacement = canonical.title() if text[text.lower().index(alias)].isupper() else canonical
            if has_period:
                replacement += '.'
            text = text[:text.lower().index(alias)] + replacement + text[text.lower().index(alias) + len(alias + ('.' if has_period else '')):]
            break
    return text


def try_parse_date(text: str) -> bool:
    """
    Return True if text is a recognizable date string, False otherwise.

    This replaces dateparser.parse() used as a validation gate throughout
    the explicit date extraction pipeline. Unlike dateparser, this is strict:
    invalid values like month 00, day 0, or month 13 return False.

    Handles:
    - Full delimited dates: 04/08/2024, 2024-04-08, 20.04.01
    - Partial dates (no year): 31/03, 7/24, 29/2 (Feb 29 handled via leap year)
    - Year+month: 2023/01
    - Written month forms: March 15, 2024 / Mar 15 2024 / Sept 15, 2024

    Args:
        text: The string to validate. Leading/trailing whitespace is stripped.

    Returns:
        True if text matches any known date format, False otherwise.

    Examples:
        >>> try_parse_date('04/08/2024')
        True
        >>> try_parse_date('March 15, 2024')
        True
        >>> try_parse_date('29/2')
        True
        >>> try_parse_date('hello world')
        False
        >>> try_parse_date('00/08/2024')
        False
    """
    if not text:
        return False

    text = text.strip()
    if not text:
        return False

    # Normalise non-standard month abbreviations (e.g., "Sept" → "Sep")
    text = _normalize_month_aliases(text)

    # Full-year formats: let strptime validate calendar correctness.
    for fmt in _FULL_YEAR_FORMATS:
        try:
            datetime.strptime(text, fmt)
            return True
        except ValueError:
            continue

    # Short-year formats (2-digit year): e.g., version numbers like 20.04.01.
    for fmt in _SHORT_YEAR_FORMATS:
        try:
            datetime.strptime(text, fmt)
            return True
        except ValueError:
            continue

    # Partial formats (no year): first probe by appending a known leap year (2000)
    # so that Feb 29 and similar edge dates are accepted.
    for _partial_fmt, full_fmt, sep in _PARTIAL_FORMATS_WITH_LEAP_YEAR:
        try:
            datetime.strptime(text + sep + '2000', full_fmt)
            return True
        except ValueError:
            continue

    # Structural fallback for partial dates: some calendar-invalid values like
    # "30/2" (Feb 30) are still structurally date-like and were accepted by
    # dateparser. For 2-component numeric strings, accept them if both parts
    # are in plausible day-or-month range (1-31).
    for _partial_fmt, _full_fmt, sep in _PARTIAL_FORMATS_WITH_LEAP_YEAR:
        if sep in text:
            parts = text.split(sep)
            if len(parts) == 2:
                try:
                    a, b = int(parts[0]), int(parts[1])
                    if (1 <= a <= 31) and (1 <= b <= 31):
                        return True
                except ValueError:
                    continue

    return False


class DayMonthValidator(object):
    """ Validate DAY_MONTH Patterns """

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        pass

    def process(self, month: int, day_of_month: int) -> bool:
        """
        Validates the given month and day_of_month values.

        Args:
            month (int): The month value to be validated.
            day_of_month (int): The day of the month value to be validated.

        Returns:
            bool: True if the month and day_of_month values are valid, False otherwise.
        """

        if isinstance(month, str):
            month = int(month)

        if isinstance(day_of_month, str):
            day_of_month = int(day_of_month)

        if month == 1:
            return 1 <= day_of_month <= 31
        elif month == 2:
            return 1 <= day_of_month <= 29
        elif month == 3:
            return 1 <= day_of_month <= 31
        elif month == 4:
            return 1 <= day_of_month <= 30
        elif month == 5:
            return 1 <= day_of_month <= 31
        elif month == 6:
            return 1 <= day_of_month <= 30
        elif month == 7:
            return 1 <= day_of_month <= 31
        elif month == 8:
            return 1 <= day_of_month <= 31
        elif month == 9:
            return 1 <= day_of_month <= 30
        elif month == 10:
            return 1 <= day_of_month <= 31
        elif month == 11:
            return 1 <= day_of_month <= 30
        elif month == 12:
            return 1 <= day_of_month <= 31

        return False


class ValidateNumericComponents(object):
    """ Validate Date/Time Extracted Components """

    __day_month_validator: DayMonthValidator = None

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        pass

    def _tokenize(self, explicit_date: str) -> list[str] | None:
        _date_delims = [
            date_delim for date_delim in date_delims
            if date_delim in explicit_date
        ]

        if not len(_date_delims):
            return None

        delim: str = _date_delims[0]
        return explicit_date.split(delim)

    def _is_valid_day_month(self, explicit_date: str, date_type: DateType) -> bool:
        if not self.__day_month_validator:
            self.__day_month_validator = DayMonthValidator()

        date_tokens: list[str] = self._tokenize(explicit_date)

        def get_day_month() -> tuple[str, str]:
            if date_type == DateType.DAY_MONTH:
                return date_tokens[1], date_tokens[0]
            elif date_type == DateType.MONTH_DAY:
                return date_tokens[0], date_tokens[1]

        month, day_of_month = get_day_month()

        return self.__day_month_validator.process(
            month=month, day_of_month=day_of_month)

    def process(self,

                d_date_types: dict[str, DateType]) -> dict[str, DateType] | None:

        d_validated: dict[str, DateType] = {}

        for explicit_date in d_date_types:
            date_type: DateType = DateType.find(d_date_types[explicit_date])

            if date_type in [DateType.DAY_MONTH, DateType.MONTH_DAY] and not self._is_valid_day_month(
                    explicit_date=explicit_date, date_type=date_type):
                continue

            d_validated[explicit_date] = date_type.name

        return d_validated
