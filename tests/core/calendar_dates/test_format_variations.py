"""Whitespace, punctuation, Unicode separators, ordinals, and prose lists."""

from datetime import date

import pytest

from fast_parse_time import extract_date_strings, parse_date_strings
from .cases import MONTHS, ordinal


@pytest.mark.parametrize('separator', ['/', '.', '-', '\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2212', '\ufe63', '\uff0d'])
@pytest.mark.parametrize('spacing', ['', ' ', '\t', '\u00a0'])
@pytest.mark.parametrize('template,order', [
    ('2011{s}3{s}28', 'auto'),
    ('3{s}28{s}2011', 'auto'),
    ('28{s}3{s}2011', 'auto'),
])
def test_numeric_separators_preserve_exact_source(separator, spacing, template, order):
    text = template.format(s=f'{spacing}{separator}{spacing}')
    assert extract_date_strings(f'From [{text}], onward.') == [text]
    result, = parse_date_strings(text, date_order=order)
    assert result.text == text
    assert result.date == date(2011, 3, 28)


@pytest.mark.parametrize('month', range(1, 13))
@pytest.mark.parametrize('day', [1, 2, 3, 11, 12, 13, 21, 22, 23, 28])
@pytest.mark.parametrize('style', ['lower', 'upper', 'abbrev', 'reverse'])
def test_written_month_casing_abbreviations_and_ordinals(month, day, style):
    name = MONTHS[month - 1]
    if style == 'lower':
        text = f'{name.lower()} {ordinal(day)}, 2024'
    elif style == 'upper':
        text = f'{name.upper()}\n{day}\t2024'
    elif style == 'abbrev':
        text = f'{name[:3]}. {day},2024'
    else:
        text = f'{ordinal(day)} of {name}, 2024'
    assert extract_date_strings([f'Deadline: "{text}"']) == [text]
    result, = parse_date_strings(text)
    assert result.date == date(2024, month, day)


@pytest.mark.parametrize('month', ['Sep', 'Sept', 'September', 'sep', 'SEPT', 'SEPTEMBER'])
@pytest.mark.parametrize('text_template', ['{month} 13', '13 {month}', '{month}. 13th', '13th of {month}'])
def test_september_aliases(month, text_template):
    text = text_template.format(month=month)
    result, = parse_date_strings(text, date_range=(date(2026, 9, 1), date(2026, 9, 30)))
    assert result.text == text
    assert result.date == date(2026, 9, 13)


@pytest.mark.parametrize('separator', [' and ', ', ', '; ', '\n', '\t', ' / ', ' - ', ' ... '])
def test_multiple_dates_in_one_string_match_batch_behavior(separator):
    texts = ['3/28/2011', 'Mar 28', '4/22/2011', 'Apr 22']
    source = separator.join(texts)
    assert extract_date_strings(source) == texts
    assert parse_date_strings(source) == parse_date_strings(texts)


@pytest.mark.parametrize('text', ['3/28/2011', 'Mar 28', 'April 3', '4/22/2011'])
@pytest.mark.parametrize('wrapper', [chr(96) + '{}' + chr(96), "'{}'", '"{}"', '({})', '[{}]', '{{{}}}', 'Date:{}', '{}!', '{}?'])
def test_punctuation_boundaries(text, wrapper):
    assert extract_date_strings(wrapper.format(text)) == [text]
