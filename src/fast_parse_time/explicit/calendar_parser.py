"""Calendar dates and missing-year inference within an inclusive range.

See https://github.com/craigtrim/fast-parse-time/issues/73.
"""

from dataclasses import dataclass
from datetime import date
import re
from typing import Literal

from fast_parse_time.models import ParsedDate


DateOrder = Literal['auto', 'mdy', 'dmy']





_MONTH_NAMES = (
    'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december',
)
_MONTHS = {name: number for number, name in enumerate(_MONTH_NAMES, 1)}
_MONTHS.update({name[:3]: number for number, name in enumerate(_MONTH_NAMES, 1)})
_MONTHS['sept'] = 9
_MONTH_PATTERN = '|'.join(sorted(_MONTHS, key=len, reverse=True))
_DASHES = r'\-\u2010\u2011\u2012\u2013\u2014\u2015\u2212\ufe63\uff0d'
_LEFT = rf'(?<![\w/.{_DASHES}])'
_RIGHT = rf'(?!\w|[/{_DASHES}]|\.[0-9])'
_JOIN = rf'(?:\s+|\s*[{_DASHES}]\s*)'
_YEAR = rf'(?:(?:\s*,\s*|\s+|\s*[{_DASHES}]\s*)(?P<year>[0-9]+))?'
_DAY = r'(?P<day>[0-9]{1,2})(?P<ordinal>st|nd|rd|th)?'

# Consume complete numeric tokens, including invalid ones, before validation.
# This prevents an invalid full date from falling back to a valid partial date.
_NUMERIC = re.compile(
    _LEFT + rf'(?P<a>[0-9]{{1,4}})\s*(?P<sep>[/.{_DASHES}])\s*'
    r'(?P<b>[0-9]{1,4})(?:\s*(?P=sep)\s*(?P<c>[0-9]{1,4}))?' + _RIGHT
)
_MONTH_FIRST = re.compile(
    _LEFT + rf'(?P<month>{_MONTH_PATTERN})\.?' + _JOIN + _DAY + _YEAR + _RIGHT,
    re.IGNORECASE,
)
_DAY_FIRST = re.compile(
    _LEFT + _DAY + rf'(?:\s+(?:day\s+)?of\s+|{_JOIN})'
    + rf'(?P<month>{_MONTH_PATTERN})\.?' + _YEAR + _RIGHT,
    re.IGNORECASE,
)


@dataclass(frozen=True)
class _DateToken:
    text: str
    month_days: tuple[tuple[int, int], ...]
    year: int | None


def _calendar_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _month_days(a: int, b: int, order: DateOrder) -> tuple[tuple[int, int], ...]:
    pairs = [(a, b)] if order == 'mdy' else [(b, a)] if order == 'dmy' else [(a, b), (b, a)]
    # A leap year permits February 29 without inventing a year in the result.
    return tuple(sorted({pair for pair in pairs if _calendar_date(2000, *pair)}))


def _numeric_token(match: re.Match, order: DateOrder) -> _DateToken | None:
    a, b, c = match.group('a', 'b', 'c')
    year = None
    if c is None:
        if len(a) > 2 or len(b) > 2:
            return None  # month/year and year-only values are not complete dates
        pairs = _month_days(int(a), int(b), order)
    elif len(a) == 4 and len(b) <= 2 and len(c) <= 2:
        year = int(a)
        pairs = ((int(b), int(c)),)  # year-first dates always use YMD
    elif len(c) == 4 and len(a) <= 2 and len(b) <= 2:
        year = int(c)
        pairs = _month_days(int(a), int(b), order)
    else:
        return None  # no implicit century for short years
    if year is not None:
        pairs = tuple(pair for pair in pairs if _calendar_date(year, *pair))
    return _DateToken(match.group(), pairs, year) if pairs else None


def _written_token(match: re.Match) -> _DateToken | None:
    month = _MONTHS.get(match.group('month').lower())
    if month is None:
        return None  # Unicode case-fold lookalikes are not English month names
    day = int(match.group('day'))
    ordinal = match.group('ordinal')
    suffix = 'th' if 10 <= day % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    if ordinal and ordinal.lower() != suffix:
        return None
    raw_year = match.group('year')
    if raw_year is not None and len(raw_year) != 4:
        return None
    year = int(raw_year) if raw_year is not None else None
    if _calendar_date(year if year is not None else 2000, month, day) is None:
        return None
    text = match.group()
    if year is None and text.endswith('.') and match.group('month').lower() in _MONTH_NAMES:
        text = text[:-1]  # prose punctuation after a full month name
    return _DateToken(text, ((month, day),), year)


def _texts(texts: str | list[str]) -> list[str]:
    if isinstance(texts, str):
        return [texts]
    if not isinstance(texts, list) or any(not isinstance(text, str) for text in texts):
        raise TypeError('texts must be a string or a list of strings')
    return texts


def _scan(texts: list[str], order: DateOrder) -> list[_DateToken]:
    tokens = []
    for text in texts:
        matches = [
            (match.start(), -match.end(), pattern is _NUMERIC, match)
            for pattern in (_NUMERIC, _MONTH_FIRST, _DAY_FIRST)
            for match in pattern.finditer(text)
        ]
        covered_until = -1
        for start, negative_end, numeric, match in sorted(matches, key=lambda item: item[:2]):
            if start < covered_until:
                continue
            covered_until = -negative_end
            token = _numeric_token(match, order) if numeric else _written_token(match)
            if token is not None:
                tokens.append(token)
    return tokens


def _check_options(date_range: tuple[date, date] | None, date_order: DateOrder) -> None:
    if date_order not in ('auto', 'mdy', 'dmy'):
        raise ValueError("date_order must be 'auto', 'mdy', or 'dmy'")
    if date_range is not None:
        if (not isinstance(date_range, tuple) or len(date_range) != 2
                or any(type(bound) is not date for bound in date_range)):
            raise TypeError('date_range must be a tuple of two datetime.date values')
        if date_range[0] > date_range[1]:
            raise ValueError('date_range start must be on or before its end')


def extract_strings(texts: str | list[str]) -> list[str]:
    """Extract calendar-valid date text in source order, retaining duplicates."""
    return [token.text for token in _scan(_texts(texts), 'auto')]


def parse_strings(
    texts: str | list[str], *, date_range: tuple[date, date] | None = None,
    date_order: DateOrder = 'auto',
) -> list[ParsedDate]:
    """Parse date occurrences and infer missing years only inside a range."""
    _check_options(date_range, date_order)
    tokens = _scan(_texts(texts), date_order)
    if date_range is None:
        anchors = {
            date(token.year, *token.month_days[0]) for token in tokens
            if token.year is not None and len(token.month_days) == 1
        }
        if len(anchors) >= 2:
            date_range = min(anchors), max(anchors)

    results = []
    for token in tokens:
        if token.year is not None:
            candidates = tuple(sorted(date(token.year, *pair) for pair in token.month_days))
            # Preserve explicit facts; a range can narrow an ambiguous full date
            # only when at least one of its interpretations actually fits.
            if date_range is not None and len(candidates) > 1:
                inside = tuple(value for value in candidates if date_range[0] <= value <= date_range[1])
                candidates = inside or candidates
        elif date_range is not None:
            start, end = date_range
            candidates = tuple(sorted(
                value for year in range(start.year, end.year + 1)
                for pair in token.month_days
                if (value := _calendar_date(year, *pair)) is not None and start <= value <= end
            ))
        else:
            candidates = ()
        pairs = {(value.month, value.day) for value in candidates} or set(token.month_days)
        months = {month for month, _ in pairs}
        days = {day for _, day in pairs}
        results.append(ParsedDate(
            token.text,
            next(iter(months)) if len(months) == 1 else None,
            next(iter(days)) if len(days) == 1 else None,
            candidates,
        ))
    return results
