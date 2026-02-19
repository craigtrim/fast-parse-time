# Functions

All public functions exported from `fast_parse_time`.

---

## Primary

### `parse_dates(text: str) -> ParseResult`

Extract all temporal information from text - both explicit dates and relative time expressions. This is the recommended entry point for most use cases.

```python
from fast_parse_time import parse_dates

result = parse_dates("Meeting on 04/08/2024 about issues from 5 days ago")

result.explicit_dates
# [ExplicitDate(text='04/08/2024', date_type='FULL_EXPLICIT_DATE')]

result.relative_times
# [RelativeTime(cardinality=5, frame='day', tense='past')]

result.has_dates
# True
```

---

## Extraction

### `parse_time_references(text: str) -> List[RelativeTime]`

Extract relative time expressions. Equivalent to `extract_relative_times()` - prefer this name for clarity at call sites.

```python
from fast_parse_time import parse_time_references

parse_time_references("Show me data from 5 days ago and last week")
# [RelativeTime(cardinality=5, frame='day', tense='past'),
#  RelativeTime(cardinality=1, frame='week', tense='past')]
```

### `extract_explicit_dates(text: str) -> Dict[str, str]`

Extract explicit dates - both numeric formats and written month formats. Returns an empty dict if none found.

```python
from fast_parse_time import extract_explicit_dates

# Numeric with delimiter
extract_explicit_dates("Event on 04/08/2024")       # {'04/08/2024': 'FULL_EXPLICIT_DATE'}
extract_explicit_dates("Event on 2024-06-05")        # {'2024-06-05': 'FULL_EXPLICIT_DATE'}

# Partial numeric
extract_explicit_dates("Event on 3/24")              # {'3/24': 'MONTH_DAY'}
extract_explicit_dates("Copyright 2024")             # {'2024': 'YEAR_ONLY'}
extract_explicit_dates("Filed in 2019")              # {'2019': 'YEAR_ONLY'}

# Ambiguous
extract_explicit_dates("Meeting 4/8")                # {'4/8': 'DAY_MONTH_AMBIGUOUS'}

# Written month
extract_explicit_dates("Event on March 15, 2024")   # {'March 15, 2024': 'FULL_EXPLICIT_DATE'}
extract_explicit_dates("Event on Mar 15, 2024")     # {'Mar 15, 2024': 'FULL_EXPLICIT_DATE'}
extract_explicit_dates("Event on 15 March 2024")    # {'15 March 2024': 'FULL_EXPLICIT_DATE'}

# Year ranges
extract_explicit_dates("Active 2014-2015")           # {'2014-2015': 'YEAR_RANGE'}
extract_explicit_dates("From 2010 to 2020")          # {'2010 to 2020': 'YEAR_RANGE'}
extract_explicit_dates("From 2018 through 2022")     # {'2018 through 2022': 'YEAR_RANGE'}  # 'through' accepted
extract_explicit_dates("Revenue grew 2019\u20132023")  # {'2019-2023': 'YEAR_RANGE'}  # en dash normalized
extract_explicit_dates("Contract 2023-24")           # {'2023-24': 'YEAR_RANGE'}  # abbreviated year
```

### `extract_relative_times(text: str) -> List[RelativeTime]`

Low-level extraction of relative time expressions. Returns an empty list if none found.

```python
from fast_parse_time import extract_relative_times

extract_relative_times("5 days ago")             # cardinality=5, frame='day', tense='past'
extract_relative_times("last week")              # cardinality=1, frame='week', tense='past'
extract_relative_times("next 3 months")          # cardinality=3, frame='month', tense='future'
extract_relative_times("couple of hours ago")    # cardinality=2, frame='hour', tense='past'
extract_relative_times("half an hour ago")       # cardinality=1, frame='hour', tense='past'
extract_relative_times("a few days ago")         # cardinality=3, frame='day', tense='past'
extract_relative_times("last Monday")            # cardinality=1, frame='week', tense='past'
extract_relative_times("this morning")           # cardinality=1, frame='day', tense='past'
```

---

## Filtered Extraction

### `parse_dates_with_type(text: str, date_type: Optional[str] = None) -> Dict[str, str]`

Extract explicit dates, optionally filtered to a specific `DateType` string. See [types.md](https://github.com/craigtrim/fast-parse-time/blob/master/docs/types.md) for all valid type names.

```python
from fast_parse_time import parse_dates_with_type

parse_dates_with_type("Event 04/08/2024 or maybe 3/24", 'FULL_EXPLICIT_DATE')
# {'04/08/2024': 'FULL_EXPLICIT_DATE'}

parse_dates_with_type("Event 04/08/2024 or maybe 3/24")  # no filter
# {'04/08/2024': 'FULL_EXPLICIT_DATE', '3/24': 'MONTH_DAY'}
```

### `extract_past_references(text: str) -> List[RelativeTime]`

Extract only past-tense time references. Future references are excluded.

```python
extract_past_references("Show data from 5 days ago and next week")
# [RelativeTime(cardinality=5, frame='day', tense='past')]
```

### `extract_future_references(text: str) -> List[RelativeTime]`

Extract only future-tense time references. Past references are excluded.

```python
extract_future_references("Reminder in 5 days and last week")
# [RelativeTime(cardinality=5, frame='day', tense='future')]
```

### `extract_full_dates_only(text: str) -> Dict[str, str]`

Extract only complete dates (year + month + day). Partial dates like year-only or month/day are excluded.

```python
extract_full_dates_only("Event 04/08/2024 or maybe 3/24")
# {'04/08/2024': 'FULL_EXPLICIT_DATE'}
```

### `extract_ambiguous_dates(text: str) -> Dict[str, str]`

Extract only ambiguous dates - those that could be interpreted multiple ways. Useful for prompting users for clarification.

```python
extract_ambiguous_dates("Meeting 4/8 or 04/08/2024")
# {'4/8': 'DAY_MONTH_AMBIGUOUS'}
```

### `has_temporal_info(text: str) -> bool`

Quick check whether text contains any extractable temporal information. More efficient than full parsing when you only need a yes/no answer.

```python
has_temporal_info("Meeting on 04/08/2024")    # True
has_temporal_info("Show data from last week") # True
has_temporal_info("Meeting tomorrow")         # False - 'tomorrow' is not currently supported
has_temporal_info("Hello world")              # False
```

---

## Resolution

### `resolve_to_datetime(text: str, reference: datetime = None) -> List[datetime]`

Extract relative time references and resolve them to absolute `datetime` objects.

**Args:**
- `reference` - The point in time to calculate from. Defaults to `datetime.now()`.

```python
from datetime import datetime
from fast_parse_time import resolve_to_datetime

resolve_to_datetime("Show me data from 5 days ago")
# [datetime(2026, 2, 12, ...)]  - 5 days before today

# With explicit reference point
ref = datetime(2026, 1, 1)
resolve_to_datetime("3 weeks ago", reference=ref)
# [datetime(2025, 12, 11, ...)]
```

### `resolve_to_timedelta(text: str) -> List[timedelta]`

Extract relative time references and return them as `timedelta` offsets. Past references produce negative deltas, future references produce positive.

```python
from fast_parse_time import resolve_to_timedelta

resolve_to_timedelta("5 days ago")   # [timedelta(days=-5)]
resolve_to_timedelta("next 2 weeks") # [timedelta(weeks=2)]
```

---

## Recipes

### `parse_and_resolve(text: str, reference: datetime = None) -> Dict`

Parse all temporal info and resolve relative times to absolute datetimes in a single call.

Returns: `{'explicit': List[str], 'resolved': List[datetime]}`

```python
from fast_parse_time import parse_and_resolve

parse_and_resolve("Meeting 04/08/2024 about issues from 5 days ago")
# {
#     'explicit': ['04/08/2024'],
#     'resolved': [datetime(2026, 2, 12, ...)]
# }
```

### `get_date_range(text: str) -> Optional[Tuple[datetime, datetime]]`

Extract a date range from text containing exactly two relative time references. Returns `(start, end)` sorted chronologically, or `None` if the text does not contain exactly two references.

```python
from fast_parse_time import get_date_range

get_date_range("show data from 7 days ago to 3 days ago")
# (datetime(2026, 2, 10, ...), datetime(2026, 2, 14, ...))

get_date_range("only one reference: 5 days ago")
# None
```

---

## Backward Compatibility

`extract_numeric_dates(text)` is a legacy alias maintained for backward compatibility. Use `extract_explicit_dates()` instead - it is a superset that also handles written month formats.
