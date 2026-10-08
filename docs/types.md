# Result types

The public result types are available from `fast_parse_time`. Choose a type
based on whether you need a calendar interpretation, a classification, or a
relative offset.

## ParsedDate

`parse_date_strings` returns a `ParsedDate` for each calendar-date occurrence.
The record is frozen. It retains the matched text even when the year or numeric
order remains unresolved.

| Attribute | Type | Meaning |
|---|---|---|
| `text` | `str` | Original matched text |
| `month` | `int` or `None` | Month number when known |
| `day` | `int` or `None` | Day number when known |
| `candidates` | `tuple[date, ...]` | Supported calendar interpretations |
| `date` | `date` or `None` | The only candidate, if exactly one remains |
| `year` | `int` or `None` | The year shared by all candidates, if any |

A year can be known while the month and day remain ambiguous. An empty
`candidates` tuple means the parser could not resolve a concrete date from the
available text and bounds.

```python
from datetime import date
from fast_parse_time import parse_date_strings

match = parse_date_strings('3/4/2011')[0]

assert match.text == '3/4/2011'
assert match.candidates == (date(2011, 3, 4), date(2011, 4, 3))
assert match.year == 2011
assert match.month is None
assert match.day is None
assert match.date is None
```

See [Calendar dates and year inference](calendar-dates.md) for partial dates,
range selection, and unresolved years.

## ExplicitDate

An `ExplicitDate` contains `text: str` and `date_type: str`. The
`parse_dates` function returns these records in `result.explicit_dates`.
The classification is a `DateType` member name.

Text can reflect normalization performed during extraction. An `ExplicitDate`
does not contain a Python `date`, and a complete-date classification does not
establish the numeric month/day order.

```python
from fast_parse_time import ExplicitDate, parse_dates

assert parse_dates('From 2010 to 2020').explicit_dates == [
    ExplicitDate(text='2010-2020', date_type='YEAR_RANGE'),
]
```

## RelativeTime

A `RelativeTime` describes an extracted quantity, unit, and tense.

| Field | Meaning |
|---|---|
| `cardinality` | Quantity, such as 5 in `5 days ago` |
| `frame` | `second`, `minute`, `hour`, `day`, `week`, `month`, or `year` |
| `tense` | `past`, `future`, or `present` |

`to_timedelta()` returns a signed duration. `to_datetime(reference=None)`
adds that duration to the supplied datetime, defaulting to `datetime.now()`.

```python
from datetime import datetime, timedelta
from fast_parse_time import RelativeTime

relative = RelativeTime(cardinality=5, frame='day', tense='past')

assert relative.to_timedelta() == timedelta(days=-5)
assert relative.to_datetime(datetime(2026, 1, 1)) == datetime(2025, 12, 27)
```

Weeks use seven days, months use 30 days, and years use 365 days. These
conversions do not follow varying calendar-month lengths or leap years.
Unsupported frame values raise `NotImplementedError` during conversion.

Extraction can normalize the quantity and frame. For example, `half an hour
ago` becomes 30 minutes, and `this morning` becomes a zero-day present
reference without a clock time. Named weekdays use the local date at extraction
time. Decimal quantities are truncated before matching.

## ParseResult

`parse_dates` returns a `ParseResult` with two lists:

| Attribute | Type | Meaning |
|---|---|---|
| `explicit_dates` | `list[ExplicitDate]` | Explicit text and classification records |
| `relative_times` | `list[RelativeTime]` | Relative quantities and units |
| `has_dates` | `bool` | Property that is true when either list is nonempty |

```python
from fast_parse_time import parse_dates

result = parse_dates('Hello world')

assert result.explicit_dates == []
assert result.relative_times == []
assert not result.has_dates
```

## DateType

Classification functions return the names of `DateType` members. Pass
`DateType.FULL_EXPLICIT_DATE.name`, for example, to `parse_dates_with_type`.
The enum names describe extraction categories; use `ParsedDate` to inspect
concrete calendar interpretations.

| Name | Input example | Classification |
|---|---|---|
| `FULL_EXPLICIT_DATE` | `04/08/2024`, `March 15, 2024` | Complete date expression |
| `YEAR_ONLY` | `in 2019` | Year recognized in context |
| `MONTH_DAY` | `3/24` | Month followed by day |
| `DAY_MONTH` | `15/3` | Day followed by month |
| `DAY_MONTH_AMBIGUOUS` | `4/8`, `March 13` | Ambiguous numeric order or a named-month expression requiring further context |
| `MONTH_YEAR` | `March 2024`, `Oct-23` | Month and year |
| `YEAR_MONTH` | `2023-Oct` | Year and month |
| `YEAR_RANGE` | `2014-2015`, `From 2010 to 2020` | Year span |

The enum also defines `SEASON_YEAR`, `TIMEFRAME_RELATIVE_TO_NOW`,
`NON_SPECIFIC_FUTURE_PAST`, `EVENT_BASED_RELATIVE_DATE`,
`SEASONAL_OR_QUARTERLY`, `RECURRENT_DATE`, `FUZZY_DATE`, and `NO_DATE`.
The public classification functions do not currently emit those labels.
Relative expressions are represented by `RelativeTime`; an input with no
matches produces empty collections.

`DateType.find(name)` accepts a name with surrounding whitespace or different
capitalization. It returns the member, or `None` for an unrecognized name.

```python
from fast_parse_time import DateType

assert DateType.find(' full_explicit_date ') is DateType.FULL_EXPLICIT_DATE
assert DateType.find('unknown') is None
```
