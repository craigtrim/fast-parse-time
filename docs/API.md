# API Reference

Complete documentation for all available functions.

## Primary Function

### `parse_dates(text: str) -> ParseResult`

Extract all temporal information from text.

**Returns:**
- `ParseResult` object with `explicit_dates` and `relative_times` lists

**Example:**
```python
from fast_parse_time import parse_dates

result = parse_dates("Meeting on 04/08/2024 about issues from 5 days ago")
print(result.explicit_dates)  # [ExplicitDate(...)]
print(result.relative_times)  # [RelativeTime(...)]
```

---

## Specialized Extraction Functions

### `extract_explicit_dates(text: str) -> Dict[str, str]`

Extract only numeric/explicit dates.

**Returns:** Dictionary mapping date strings to their type classifications

**Example:**
```python
dates = extract_explicit_dates("Event on 04/08/2024 or maybe 3/24")
# {'04/08/2024': 'FULL_EXPLICIT_DATE', '3/24': 'MONTH_DAY'}
```

### `parse_time_references(text: str) -> List[RelativeTime]`

Extract only relative time references.

**Returns:** List of `RelativeTime` objects

**Example:**
```python
times = parse_time_references("show me data from 5 days ago")
# [RelativeTime(cardinality=5, frame='day', tense='past')]
```

### `resolve_to_datetime(text: str, reference: datetime = None) -> List[datetime]`

Extract relative times and convert to absolute datetimes.

**Returns:** List of `datetime` objects

**Example:**
```python
datetimes = resolve_to_datetime("5 days ago")
# [datetime.datetime(2025, 11, 14, ...)]
```

### `resolve_to_timedelta(text: str) -> List[timedelta]`

Extract relative times and convert to timedeltas.

**Returns:** List of `timedelta` objects

**Example:**
```python
deltas = resolve_to_timedelta("5 days ago")
# [timedelta(days=-5)]
```

---

## Filter Functions

### `extract_past_references(text: str) -> List[RelativeTime]`

Extract only past time references.

### `extract_future_references(text: str) -> List[RelativeTime]`

Extract only future time references.

### `extract_full_dates_only(text: str) -> Dict[str, str]`

Extract only complete dates (with year, month, day).

### `extract_ambiguous_dates(text: str) -> Dict[str, str]`

Extract only ambiguous dates (e.g., `4/8` which could be April 8 or August 4).

### `has_temporal_info(text: str) -> bool`

Quick check if text contains any temporal information.

---

## Recipe Functions

### `parse_and_resolve(text: str, reference: datetime = None) -> Dict`

Parse all temporal info and resolve relatives to datetimes.

**Returns:** Dict with `'explicit'` (list of strings) and `'resolved'` (list of datetimes)

### `get_date_range(text: str) -> Optional[Tuple[datetime, datetime]]`

Extract a date range from text with two relative time references.

**Returns:** Tuple of `(start_date, end_date)` or `None`

---

## Data Classes

### `RelativeTime`

```python
@dataclass
class RelativeTime:
    cardinality: int  # e.g., 5
    frame: str        # 'day', 'week', 'month', 'year', 'hour', 'minute', 'second'
    tense: str        # 'past' or 'future'

    def to_datetime(reference: datetime = None) -> datetime
    def to_timedelta() -> timedelta
```

### `ExplicitDate`

```python
@dataclass
class ExplicitDate:
    text: str       # Original text (e.g., '04/08/2024')
    date_type: str  # DateType classification
```

### `ParseResult`

```python
@dataclass
class ParseResult:
    explicit_dates: List[ExplicitDate]
    relative_times: List[RelativeTime]
    has_dates: bool  # Property: True if any temporal info found
```

---

## Date Type Classifications

When extracting explicit dates, the following types are identified:

- `FULL_EXPLICIT_DATE` - Complete date with year, month, day (e.g., `04/08/2024`)
- `MONTH_DAY` - Month and day only (e.g., `3/24`)
- `DAY_MONTH` - Day and month (European format)
- `YEAR_ONLY` - Just a year (e.g., `2024`)
- `MONTH_YEAR` - Month and year (e.g., `12/2024`)
- `YEAR_MONTH` - Year and month (ISO format)
- `DAY_MONTH_AMBIGUOUS` - Ambiguous date needing clarification (e.g., `4/8`)
- And more (see source for complete list)

---

## Supported Time Frames

For relative time references:

- `second`, `minute`, `hour`
- `day`, `week`, `month`, `year`

## Supported Delimiters

For explicit dates:

- `/` (forward slash)
- `-` (hyphen)
- `.` (period)

## Known Limitations

See [BOUNDARIES.md](../BOUNDARIES.md) for detailed system boundaries and design decisions.
