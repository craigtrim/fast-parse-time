# Functions

Import these functions from `fast_parse_time`. Calendar-date functions accept
one string or a `list[str]`; the other functions accept one string. The
[result types](types.md) page describes the objects returned by each call.

## Calendar dates

### `extract_date_strings(texts: str | list[str]) -> list[str]`

Returns calendar-date text in source order, including repeated occurrences.
Each match must contain a month and day. Full dates are checked for calendar
validity; partial dates can include February 29 without specifying a year.

```python
from fast_parse_time import extract_date_strings

assert extract_date_strings(['3/28/2011', 'Mar 28 and Mar 28', 'No date']) == [
    '3/28/2011', 'Mar 28', 'Mar 28',
]
assert extract_date_strings('February 30, 2026') == []
```

### `parse_date_strings(texts, *, date_range=None, date_order='auto') -> list[ParsedDate]`

Returns parsed occurrences, using inclusive bounds to infer missing years.
`date_range` accepts a tuple of two `datetime.date` values. Without supplied
bounds, at least two distinct, unambiguous full dates establish the range.

`date_order` accepts `'auto'`, `'mdy'`, or `'dmy'`. The default preserves
both valid numeric interpretations. Year-first dates always use year/month/day.

```python
from datetime import date
from fast_parse_time import parse_date_strings

match = parse_date_strings(
    'March 13',
    date_range=(date(2025, 11, 28), date(2026, 4, 14)),
)[0]

assert match.date == date(2026, 3, 13)
assert parse_date_strings('March 13')[0].year is None
```

See [Calendar dates and year inference](calendar-dates.md) for unresolved
results, explicit dates outside the range, and input validation.

## Explicit dates and relative expressions

### `parse_dates(text: str) -> ParseResult`

Combines explicit date classifications and relative references. Explicit
results contain text and classification names. Relative results contain a
quantity, unit, and tense.

```python
from fast_parse_time import ExplicitDate, RelativeTime, parse_dates

result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')

assert result.explicit_dates == [
    ExplicitDate(text='04/08/2024', date_type='FULL_EXPLICIT_DATE'),
]
assert result.relative_times == [
    RelativeTime(cardinality=5, frame='day', tense='past'),
]
assert result.has_dates
```

### `extract_explicit_dates(text: str) -> dict[str, str]`

Maps explicit expressions to classification names. Supported forms include
numeric dates, named months, ISO timestamps, and some expressions containing
only a year or a month and year. The result is `{}` when no expression matches.

The dictionary can contain normalized text. Repeated identical keys occur
once. Numeric extraction processes one delimiter type per call; use the
calendar-date functions when you need complete or partial month/day dates
with mixed delimiters in the same input.

```python
from fast_parse_time import extract_explicit_dates

assert extract_explicit_dates('Event on March 15, 2024') == {
    'March 15, 2024': 'FULL_EXPLICIT_DATE',
}
assert extract_explicit_dates('Filed in 2019') == {'2019': 'YEAR_ONLY'}
assert extract_explicit_dates('March 2024') == {'March 2024': 'MONTH_YEAR'}
assert extract_explicit_dates('From 2010 to 2020') == {'2010-2020': 'YEAR_RANGE'}
```

A `FULL_EXPLICIT_DATE` label identifies a complete expression without
choosing its numeric order. Use `parse_date_strings` for calendar
interpretations.

### `extract_relative_times(text: str) -> list[RelativeTime]`

### `parse_time_references(text: str) -> list[RelativeTime]`

Both functions extract relative expressions and return `[]` when none match.
The quantity and unit can differ from the wording: `half an hour ago`
normalizes to 30 minutes.

```python
from fast_parse_time import RelativeTime, extract_relative_times, parse_time_references

assert extract_relative_times('5 days ago and last week') == [
    RelativeTime(5, 'day', 'past'),
    RelativeTime(1, 'week', 'past'),
]
assert parse_time_references('half an hour ago') == [
    RelativeTime(30, 'minute', 'past'),
]
assert extract_relative_times('tomorrow') == [RelativeTime(1, 'day', 'future')]
```

Named weekdays use the local date during extraction. Decimal quantities are
truncated: `1.5 days ago` produces a quantity of 1 day.

## Filtering

### `parse_dates_with_type(text: str, date_type: str | None = None) -> dict[str, str]`

Filters explicit expressions by a `DateType` member name. Pass the name as a
string, such as `'FULL_EXPLICIT_DATE'`. Omitting `date_type` returns all
explicit classifications.

```python
from fast_parse_time import DateType, parse_dates_with_type

assert parse_dates_with_type(
    'Event 04/08/2024 or maybe 3/24',
    DateType.FULL_EXPLICIT_DATE.name,
) == {'04/08/2024': 'FULL_EXPLICIT_DATE'}
```

### `extract_full_dates_only(text: str) -> dict[str, str]`

Selects expressions classified as `FULL_EXPLICIT_DATE`.

### `extract_ambiguous_dates(text: str) -> dict[str, str]`

Selects expressions classified as `DAY_MONTH_AMBIGUOUS`. This filter does not
report every form of ambiguity. A complete numeric date can have ambiguous
order while retaining the `FULL_EXPLICIT_DATE` label.

```python
from fast_parse_time import extract_ambiguous_dates, extract_full_dates_only

text = 'Meeting 4/8 or 04/08/2024'

assert extract_full_dates_only(text) == {'04/08/2024': 'FULL_EXPLICIT_DATE'}
assert extract_ambiguous_dates(text) == {'4/8': 'DAY_MONTH_AMBIGUOUS'}
```

### `extract_past_references(text: str) -> list[RelativeTime]`

### `extract_future_references(text: str) -> list[RelativeTime]`

Select relative references whose tense is `'past'` or `'future'`,
respectively. References with `'present'` tense are absent from both results.

```python
from fast_parse_time import RelativeTime, extract_future_references, extract_past_references

text = 'Show data from 5 days ago and next week'

assert extract_past_references(text) == [RelativeTime(5, 'day', 'past')]
assert extract_future_references(text) == [RelativeTime(1, 'week', 'future')]
```

### `has_temporal_info(text: str) -> bool`

Returns whether `parse_dates(text)` found an explicit or relative expression.
It runs the same parsing work and returns the result's `has_dates` property.

```python
from fast_parse_time import has_temporal_info

assert has_temporal_info('Meeting tomorrow')
assert has_temporal_info('Meeting on 04/08/2024')
assert not has_temporal_info('Hello world')
```

## Resolving relative expressions

### `resolve_to_datetime(text: str, reference: datetime | None = None) -> list[datetime]`

Applies each relative offset to `reference`, which defaults to
`datetime.now()`. Use an explicit reference for repeatable offset arithmetic.
It does not change the date used to interpret named weekdays during extraction.

```python
from datetime import datetime
from fast_parse_time import resolve_to_datetime

assert resolve_to_datetime('3 weeks ago', reference=datetime(2026, 1, 1)) == [
    datetime(2025, 12, 11),
]
```

### `resolve_to_timedelta(text: str) -> list[timedelta]`

Returns signed offsets. Past references produce negative durations. A month
uses 30 days and a year uses 365 days; these are fixed durations rather than
calendar-aware month or year arithmetic.

```python
from datetime import timedelta
from fast_parse_time import resolve_to_timedelta

assert resolve_to_timedelta('5 days ago') == [timedelta(days=-5)]
assert resolve_to_timedelta('next 2 weeks') == [timedelta(weeks=2)]
```

## Combined results and ranges

### `parse_and_resolve(text: str, reference: datetime | None = None) -> dict`

Returns two keys: `explicit` contains `list[str]`, and `resolved` contains
`list[datetime]`. The explicit strings keep the classification API's text
representation; only the relative expressions are resolved to datetimes.

```python
from datetime import datetime
from fast_parse_time import parse_and_resolve

assert parse_and_resolve(
    'Meeting 04/08/2024 about issues from 5 days ago',
    reference=datetime(2026, 1, 1),
) == {
    'explicit': ['04/08/2024'],
    'resolved': [datetime(2025, 12, 27)],
}
```

### `get_date_range(text: str) -> tuple[datetime, datetime] | None`

Resolves exactly two relative references against the current time and returns
them in chronological order. Other result counts return `None`. This function
has no `reference` parameter and does not infer years for calendar dates.

```python
from fast_parse_time import get_date_range

bounds = get_date_range('Show data from 7 days ago to 3 days ago')
assert bounds is not None
assert bounds[0] < bounds[1]
assert get_date_range('Only one reference: 5 days ago') is None
```

## Legacy numeric extraction

### `extract_numeric_dates(input_text: str)`

Calls the numeric extractor directly. Its return value can be `None` when
there is no match. Use `extract_explicit_dates` for an empty dictionary in that
case and for additional written-date formats.

```python
from fast_parse_time import extract_numeric_dates

assert extract_numeric_dates('Event on 3/28/2011') == {
    '3/28/2011': 'FULL_EXPLICIT_DATE',
}
assert extract_numeric_dates('Hello world') is None
```

`ExplicitTimeExtractor` is also exported for callers that use the extraction
class directly.
