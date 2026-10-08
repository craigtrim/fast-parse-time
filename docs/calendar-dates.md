# Calendar dates and year inference

Use `extract_date_strings` to get a `list[str]` of date text, and
`parse_date_strings` to get parsed calendar dates. Both accept one prose string
or a `list[str]` containing dates, prose, and non-date text. Matches keep their
original spelling and internal whitespace, source order, and duplicate occurrences.

```python
from datetime import date
from fast_parse_time import extract_date_strings, parse_date_strings

texts = ['3/28/2011', '4/22/2011', 'Mar 28', 'Apr 22', 'not a date']

assert extract_date_strings(texts) == [
    '3/28/2011', '4/22/2011', 'Mar 28', 'Apr 22',
]
matches = parse_date_strings(texts)
assert [match.date for match in matches] == [
    date(2011, 3, 28), date(2011, 4, 22),
    date(2011, 3, 28), date(2011, 4, 22),
]
```

## Inferring a year from the range

A batch represents a single period. Two or more distinct, unambiguously parsed
full dates supply inclusive bounds: the earliest date and the latest date.
Their order in the input does not matter. Each partial date is checked against
the actual calendar inside those bounds.

```python
text = '11/28/2025 through 4/14/2026; Nov 22 and March 13'
matches = parse_date_strings(text)

assert matches[-1].date == date(2026, 3, 13)
assert matches[-1].year == 2026

# Neither November 22, 2025 nor November 22, 2026 is in that range.
assert matches[-2].month == 11
assert matches[-2].day == 22
assert matches[-2].year is None
assert matches[-2].date is None
```

The parser never fills in the current year or chooses the nearest year. One full
date, a repeated identical full date, a standalone year, or full dates with an
ambiguous month/day order do not establish a range by themselves. A partial date
remains in the output even when it has no valid occurrence inside the range.

If the input contains dates from unrelated periods, split it into separate
batches or provide bounds explicitly:

```python
matches = parse_date_strings(
    ['March 13', 'Nov 22'],
    date_range=(date(2025, 11, 28), date(2026, 4, 14)),
)
assert matches[0].date == date(2026, 3, 13)
assert matches[1].year is None
```

Explicit bounds override automatically detected bounds. They constrain missing
years and can narrow ambiguous numeric dates; they do not erase or change a
full date that explicitly states a different year. Equal start/end bounds are
allowed. Reversed bounds raise `ValueError`.

## Unresolved dates

`parse_date_strings` returns `list[ParsedDate]`. Each `ParsedDate` has:

| Attribute | Meaning |
|---|---|
| `text` | Original matched date text |
| `month` | Month number, or `None` if the month is ambiguous |
| `day` | Day number, or `None` if the day is ambiguous |
| `candidates` | Sorted, distinct tuple of supported `datetime.date` values |
| `date` | The single candidate, or `None` when there is no unique date |
| `year` | The year shared by all candidates, or `None` when unknown/ambiguous |

An empty `candidates` tuple means no concrete date can be resolved. It does not
mean the matched text was discarded. For example, `February 29` remains a valid
partial date even without a leap year in the range.

A range containing multiple occurrences preserves the alternatives:

```python
match = parse_date_strings(
    'March 13', date_range=(date(2024, 1, 1), date(2026, 12, 31)),
)[0]
assert match.candidates == (
    date(2024, 3, 13), date(2025, 3, 13), date(2026, 3, 13),
)
assert match.year is None
assert match.date is None

# Applications that only need resolved dates can filter explicitly.
resolved = [match.date for match in matches if match.date is not None]
```

Leap days are calendar-validated. A range from 2023 through 2026 resolves
`February 29` to 2024 because that is its only valid occurrence.

## Numeric date order

The default `date_order='auto'` retains both MDY and DMY interpretations when
both are calendar-valid. The range can remove an interpretation:

```python
match = parse_date_strings(['3/28/2011', '4/22/2011', '3/4'])[-1]
assert match.date == date(2011, 4, 3)
```

If both interpretations fit, `date` stays `None`. The year can still be known
when all remaining interpretations share that year. Callers that know their
source's convention can pass `date_order='mdy'` or `'dmy'`. Year-first numeric
dates always use YMD; named months are unaffected by this option.

```python
assert parse_date_strings('3/4/2011', date_order='mdy')[0].date == date(2011, 3, 4)
assert parse_date_strings('3/4/2011', date_order='dmy')[0].date == date(2011, 4, 3)
```

## Supported input and validation

- Numeric dates with `/`, `.`, `-`, or supported Unicode dashes, including spaces
  around delimiters. Delimiters within one numeric date must match.
- Full four-digit years in year-first or year-last form; Python calendar years
  0001 through 9999 are supported without a sliding current-year window.
- English full/abbreviated month names, case variations, `Sept`, abbreviation
  periods, ordinals, and month-first/day-first forms such as `March 13, 2026`,
  `13 Mar 2026`, and `13th of March`.
- Yearless month/day dates. Invalid full dates are rejected as a whole rather
  than being reinterpreted as partial dates.

This API requires a month and day. Standalone years, month/year expressions,
two-digit years, timestamps, and relative expressions are outside its contract.
Existing APIs remain available for their existing formats. ASCII numeric digits
and English month names are required. A syntactically valid numeric date cannot
always be distinguished from an unrelated numeric label without application context.

Invalid input types raise `TypeError`. `date_range` must be a tuple of two
`datetime.date` objects, not strings or `datetime.datetime` objects. An unsupported
`date_order` raises `ValueError`. Empty strings and empty lists return `[]`.

## Compatibility

These functions are additions to the public API. `parse_dates`,
`extract_explicit_dates`, `ExplicitDate`, and `ParseResult` retain their existing
signatures and return types. No event wrapper or external parsing dependency is
introduced.

Tracked in [issue #73](https://github.com/craigtrim/fast-parse-time/issues/73).
