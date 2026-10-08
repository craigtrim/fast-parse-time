"""Calendar boundaries, malformed tokens, and numeric interpretation checks."""

from calendar import isleap, monthrange
from datetime import date

import pytest

from fast_parse_time import extract_date_strings, parse_date_strings
from .cases import MONTHS


INVALID_DATES = [
    pytest.param(text, id=f'{year}-{month:02}-{day:02}-format-{index}')
    for year in (1900, 2000, 2011, 2024, 2100)
    for month in range(1, 13)
    for day in (0, monthrange(year, month)[1] + 1)
    for index, text in enumerate([
        f'{year}-{month:02}-{day:02}',
        f'{month}/{day}/{year}',
        f'{day}.{month}.{year}',
        f'{MONTHS[month - 1]} {day}, {year}',
        f'{day} {MONTHS[month - 1]} {year}',
        f'{MONTHS[month - 1][:3]}. {day} {year}',
    ])
]


@pytest.mark.parametrize('text', INVALID_DATES)
def test_invalid_full_date_does_not_fall_back_to_partial(text):
    assert extract_date_strings(f'Term date: [{text}].') == []
    assert parse_date_strings([text]) == []


@pytest.mark.parametrize('year', [1600, 1700, 1800, 1900, 2000, 2023, 2024, 2100, 2400])
@pytest.mark.parametrize('template', ['02/29/{year}', '29/02/{year}', '{year}-02-29', 'February 29, {year}'])
def test_gregorian_century_leap_rules(year, template):
    text = template.format(year=year)
    results = parse_date_strings(text)
    if isleap(year):
        assert results[0].date == date(year, 2, 29)
        assert extract_date_strings(text) == [text]
    else:
        assert results == []
        assert extract_date_strings(text) == []


@pytest.mark.parametrize('text', [
    'hello', 'March', 'Monday', '2025', 'March 2025', '2025-03',
    '03/2025', '3/28/11', '28/3/11', 'March 13, 25', 'March 13, 02025',
    '03/28/0000', '13/32/2025', '99/99', '0/10', '10/0', '30/2',
    'February 30', 'April 31', 'March 13st', 'March 11st', 'March 12nd',
    'March 21th', 'March 13thx', 'March 130', 'March 13, 20250',
    '3/28-2011', '2011/03-28', '3/28/20110', '20110-03-28',
    'v1.2.3', '192.168.1.1', 'account3/28/2011', '3/28/2011abc',
    'abcMarch 13', 'March_13', 'March 13_2025', '11/28/2025/7',
    '3//28//2011', '3--28--2011', '３/２８/２０１１',
    'APRİL 3', 'aprıl 3', 'ſeptember 13',
])
@pytest.mark.parametrize('wrapper', ['{}', '[{}]', 'before {} after', '({})'])
def test_non_dates_and_malformed_sequences_are_not_extracted(text, wrapper):
    source = wrapper.format(text)
    assert extract_date_strings(source) == []
    assert parse_date_strings(source) == []


@pytest.mark.parametrize('first', range(1, 13))
@pytest.mark.parametrize('second', range(1, 13))
@pytest.mark.parametrize('separator', ['/', '-', '.'])
def test_ambiguous_numeric_full_dates_retain_all_interpretations(first, second, separator):
    text = f'{first}{separator}{second}{separator}2025'
    expected = tuple(sorted({date(2025, first, second), date(2025, second, first)}))
    result, = parse_date_strings(text)
    assert result.candidates == expected
    assert result.date == (expected[0] if first == second else None)
    assert result.year == 2025
    assert result.month == (first if first == second else None)
    assert result.day == (second if first == second else None)


@pytest.mark.parametrize('year', [1, 999, 1000, 9999])
def test_python_calendar_year_limits(year):
    text = f'{year:04}-03-28'
    result, = parse_date_strings(text)
    assert result.date == date(year, 3, 28)


def test_full_date_has_priority_over_embedded_partial():
    texts = ['March 13, 2025', '13th of March 2025', '3/28/2011']
    assert extract_date_strings(texts) == texts
    assert len(parse_date_strings(texts)) == 3


def test_invalid_date_does_not_supply_range_boundary():
    results = parse_date_strings(['February 30, 2025', '4/14/2026', 'March 13'])
    assert [item.text for item in results] == ['4/14/2026', 'March 13']
    assert results[-1].year is None
