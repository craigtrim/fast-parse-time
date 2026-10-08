"""4,386 calendar/format cases covering every day of 2011 and leap year 2024."""

import pytest

from fast_parse_time import ParsedDate, extract_date_strings, parse_date_strings
from .cases import WRAPPERS, calendar_days, full_formats


CASES = [
    pytest.param(value, text, order, WRAPPERS[(value.day + index) % len(WRAPPERS)],
                 id=f'{value.isoformat()}-format-{index}')
    for year in (2011, 2024)
    for value in calendar_days(year)
    for index, (text, order) in enumerate(full_formats(value))
]


@pytest.mark.parametrize('value,text,order,wrapper', CASES)
def test_full_calendar_dates(value, text, order, wrapper):
    source = wrapper.format(text)
    assert extract_date_strings([source]) == [text]
    result, = parse_date_strings([source], date_order=order)
    assert isinstance(result, ParsedDate)
    assert result.text == text
    assert result.date == value
    assert result.year == value.year
    assert (result.month, result.day) == (value.month, value.day)
    assert result.candidates == (value,)
