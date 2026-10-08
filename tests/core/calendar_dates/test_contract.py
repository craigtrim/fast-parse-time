"""Issue examples, public integration, ambiguity policy, and input contracts."""

from datetime import date, datetime
from itertools import permutations

import pytest

import fast_parse_time
from fast_parse_time import (
    ParsedDate, extract_date_strings, parse_date_strings, parse_dates,
    extract_explicit_dates,
)
from fast_parse_time.api import parse_date_strings as api_parse_date_strings


def test_term_start_end_and_partial_dates():
    texts = ['3/28/2011', '4/22/2011', 'Mar 28', 'Apr 22']
    assert extract_date_strings(texts) == texts
    results = parse_date_strings(texts)
    assert [result.date for result in results] == [
        date(2011, 3, 28), date(2011, 4, 22), date(2011, 3, 28), date(2011, 4, 22),
    ]
    assert [result.year for result in results] == [2011] * 4


def test_cross_year_user_example_in_prose():
    text = 'blah blah 11/28/2025 blah blah 4/14/2026 and Nov 22 and blah blah March 13'
    assert extract_date_strings(text) == ['11/28/2025', '4/14/2026', 'Nov 22', 'March 13']
    results = parse_date_strings(text)
    assert [result.date for result in results] == [
        date(2025, 11, 28), date(2026, 4, 14), None, date(2026, 3, 13),
    ]
    assert results[2].year is None
    assert (results[2].month, results[2].day) == (11, 22)


@pytest.mark.parametrize('texts', list(permutations(['3/28/2011', '4/22/2011', 'April 3'])))
def test_batch_order_does_not_change_inference(texts):
    results = parse_date_strings(list(texts))
    result, = [item for item in results if item.text == 'April 3']
    assert result.date == date(2011, 4, 3)
    assert [item.text for item in results] == list(texts)


def test_explicit_range_overrides_unrelated_full_dates():
    results = parse_date_strings(
        ['11/28/2025', '4/14/2026', 'March 13'],
        date_range=(date(2011, 3, 28), date(2011, 4, 22)),
    )
    assert [item.date for item in results[:2]] == [date(2025, 11, 28), date(2026, 4, 14)]
    assert results[-1].year is None
    assert results[-1].candidates == ()


@pytest.mark.parametrize('anchors', [
    [], ['3/28/2011'], ['3/28/2011', '3/28/2011'],
    ['2011'], ['3/2011'], ['3/4/2011', '4/5/2011'],
    ['2/30/2011', '4/22/2011'],
])
def test_insufficient_or_ambiguous_anchors_do_not_guess(anchors):
    result = parse_date_strings(anchors + ['April 3'])[-1]
    assert result.year is None
    assert result.date is None
    assert result.candidates == ()


def test_multiple_explicit_dates_use_outer_bounds():
    results = parse_date_strings(['2011-03-28', '2011-04-01', '2011-04-22', 'April 3'])
    assert results[-1].date == date(2011, 4, 3)


def test_multiple_year_candidates_do_not_choose_a_year():
    result = parse_date_strings(['2024-01-01', '2026-12-31', 'March 13'])[-1]
    assert result.candidates == (date(2024, 3, 13), date(2025, 3, 13), date(2026, 3, 13))
    assert result.date is None
    assert result.year is None


def test_range_can_disambiguate_month_and_day():
    result = parse_date_strings(['3/28/2011', '4/22/2011', '3/4'])[-1]
    assert result.date == date(2011, 4, 3)
    assert (result.month, result.day, result.year) == (4, 3, 2011)


def test_same_year_numeric_ambiguity_preserves_year_only():
    result, = parse_date_strings('3/4', date_range=(date(2011, 1, 1), date(2011, 12, 31)))
    assert result.candidates == (date(2011, 3, 4), date(2011, 4, 3))
    assert result.year == 2011
    assert result.date is None
    assert result.month is None and result.day is None


@pytest.mark.parametrize('order,expected', [
    ('auto', (date(2011, 3, 4), date(2011, 4, 3))),
    ('mdy', (date(2011, 3, 4),)),
    ('dmy', (date(2011, 4, 3),)),
])
def test_explicit_numeric_date_order(order, expected):
    result, = parse_date_strings('3/4/2011', date_order=order)
    assert result.candidates == expected
    assert result.year == 2011


def test_equal_numeric_components_are_unambiguous():
    result, = parse_date_strings('4/4/2011')
    assert result.date == date(2011, 4, 4)
    assert result.candidates == (date(2011, 4, 4),)


def test_range_can_disambiguate_full_numeric_date():
    result, = parse_date_strings('3/4/2011', date_range=(date(2011, 4, 1), date(2011, 4, 22)))
    assert result.date == date(2011, 4, 3)


def test_range_does_not_erase_explicit_full_date():
    result, = parse_date_strings('3/4/2011', date_range=(date(2026, 4, 1), date(2026, 4, 22)))
    assert result.candidates == (date(2011, 3, 4), date(2011, 4, 3))


def test_duplicate_occurrences_and_input_are_preserved():
    texts = ['3/28/2011', '4/22/2011', 'April 3 and April 3', 'April 3']
    original = texts.copy()
    assert extract_date_strings(texts) == ['3/28/2011', '4/22/2011'] + ['April 3'] * 3
    results = parse_date_strings(texts)
    assert [item.date for item in results[2:]] == [date(2011, 4, 3)] * 3
    assert texts == original


def test_no_context_leaks_between_calls():
    assert parse_date_strings(['2011-03-28', '2011-04-22', 'April 3'])[-1].year == 2011
    assert parse_date_strings('April 3')[0].year is None


@pytest.mark.parametrize('texts', [[], '', 'ordinary words', ['ordinary words', '']])
def test_empty_results(texts):
    assert extract_date_strings(texts) == []
    assert parse_date_strings(texts) == []


@pytest.mark.parametrize('texts', [None, 42, b'3/28/2011', ('3/28/2011',), [None], ['March 13', 42]])
def test_invalid_input_types(texts):
    with pytest.raises(TypeError):
        extract_date_strings(texts)
    with pytest.raises(TypeError):
        parse_date_strings(texts)


@pytest.mark.parametrize('order', ['MDY', 'ymd', '', None, 3, []])
def test_invalid_date_order(order):
    with pytest.raises(ValueError):
        parse_date_strings([], date_order=order)


@pytest.mark.parametrize('bounds', [
    [], (), (date(2024, 1, 1),), ('2024-01-01', '2024-12-31'),
    [date(2024, 1, 1), date(2024, 12, 31)],
    (datetime(2024, 1, 1), datetime(2024, 12, 31)),
    (date(2024, 1, 1), None),
])
def test_invalid_range_types(bounds):
    with pytest.raises(TypeError):
        parse_date_strings([], date_range=bounds)


def test_reversed_explicit_bounds_are_rejected():
    with pytest.raises(ValueError):
        parse_date_strings([], date_range=(date(2026, 4, 14), date(2025, 11, 28)))


def test_public_exports_and_existing_api_compatibility():
    assert api_parse_date_strings is fast_parse_time.parse_date_strings
    assert isinstance(parse_date_strings('3/28/2011')[0], ParsedDate)
    assert extract_explicit_dates('3/28/2011')['3/28/2011'] == 'FULL_EXPLICIT_DATE'
    result = parse_dates('Term starts on 3/28/2011 about five days ago')
    assert result.explicit_dates[0].text == '3/28/2011'
    assert result.relative_times[0].cardinality == 5
