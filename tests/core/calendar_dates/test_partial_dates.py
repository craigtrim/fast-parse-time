"""1,464 partial-date cases: no clock-dependent default year."""

import pytest

from fast_parse_time import extract_date_strings, parse_date_strings
from .cases import WRAPPERS, calendar_days, partial_formats


CASES = [
    pytest.param(value, text, order, WRAPPERS[(value.month + index) % len(WRAPPERS)],
                 id=f'{value.month:02}-{value.day:02}-format-{index}')
    for value in calendar_days(2000)
    for index, (text, order) in enumerate(partial_formats(value))
]


@pytest.mark.parametrize('value,text,order,wrapper', CASES)
def test_partial_date_stays_yearless_without_range(value, text, order, wrapper):
    source = wrapper.format(text)
    assert extract_date_strings(source) == [text]
    result, = parse_date_strings(source, date_order=order)
    assert result.text == text
    assert (result.month, result.day) == (value.month, value.day)
    assert result.year is None
    assert result.date is None
    assert result.candidates == ()
