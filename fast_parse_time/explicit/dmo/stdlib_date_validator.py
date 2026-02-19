#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Stdlib-based date validator to replace the dateparser dependency.

All usages of dateparser in this codebase were validation gates only —
the parsed result was never used semantically, only checked for truthiness.
This module replaces those usages with explicit strptime format probing.

Related GitHub Issue:
    #29 - Remove dateparser dependency: replace with stdlib datetime
    https://github.com/craigtrim/fast-parse-time/issues/29
"""

from datetime import datetime

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
