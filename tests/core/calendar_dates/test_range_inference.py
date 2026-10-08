"""1,830 range cases compared with an independently enumerated calendar."""

from datetime import date

import pytest

from fast_parse_time import extract_date_strings, parse_date_strings
from .cases import calendar_days, dates_by_month_day, partial_formats


RANGES = [
    (date(2011, 3, 28), date(2011, 4, 22)),
    (date(2025, 11, 28), date(2026, 4, 14)),
    (date(2024, 1, 1), date(2024, 12, 31)),
    (date(2023, 1, 1), date(2027, 12, 31)),
    (date(2024, 2, 29), date(2024, 2, 29)),
]
ORACLES = [dates_by_month_day(*bounds) for bounds in RANGES]
CASES = [
    pytest.param(value, range_index, id=f'{value.month:02}-{value.day:02}-range-{range_index}')
    for value in calendar_days(2000)
    for range_index in range(len(RANGES))
]


@pytest.mark.parametrize('value,range_index', CASES)
def test_range_supported_calendar_candidates(value, range_index):
    start, end = RANGES[range_index]
    text, order = partial_formats(value)[value.day % 4]
    expected = ORACLES[range_index].get((value.month, value.day), ())
    if start == end or value.day % 2:
        results = parse_date_strings([text], date_range=(start, end), date_order=order)
        result, = results
    else:
        # Reversed and interleaved anchors must have the same meaning.
        source = [end.isoformat(), f'Class on {text}.', start.isoformat()]
        assert extract_date_strings(source) == [end.isoformat(), text, start.isoformat()]
        result = parse_date_strings(source, date_order=order)[1]
    assert result.text == text
    assert result.candidates == expected
    assert (result.month, result.day) == (value.month, value.day)
    assert result.date == (expected[0] if len(expected) == 1 else None)
    assert result.year == (expected[0].year if len(expected) == 1 else None)
