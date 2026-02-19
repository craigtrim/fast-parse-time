# Types

Data classes and enumerations exported from `fast_parse_time`.

---

## Data Classes

### `RelativeTime`

Represents a relative time expression extracted from text.

```python
@dataclass
class RelativeTime:
    cardinality: int  # The numeric quantity (e.g., 5 for "5 days ago")
    frame: str        # Time unit: 'second', 'minute', 'hour', 'day', 'week', 'month', 'year'
    tense: str        # 'past' or 'future'

    def to_timedelta(self) -> timedelta: ...
    def to_datetime(self, reference: datetime = None) -> datetime: ...
```

**Example:**
```python
rt = RelativeTime(cardinality=5, frame='day', tense='past')
rt.to_timedelta()              # timedelta(days=-5)
rt.to_datetime()               # datetime 5 days before now
rt.to_datetime(ref_datetime)   # datetime 5 days before ref_datetime
```

### `ExplicitDate`

Represents an explicit date string found in text.

```python
@dataclass
class ExplicitDate:
    text: str       # The original matched string, e.g. '04/08/2024' or 'March 15, 2024'
    date_type: str  # DateType name, e.g. 'FULL_EXPLICIT_DATE'
```

### `ParseResult`

Combined result returned by `parse_dates()`.

```python
@dataclass
class ParseResult:
    explicit_dates: List[ExplicitDate]
    relative_times: List[RelativeTime]
    has_dates: bool  # Property: True if any temporal info found
```

---

## DateType

The `DateType` enum defines all possible classifications for extracted dates. The `date_type` field on `ExplicitDate` contains the `.name` of the matching enum member.

### Implemented (returned by extraction functions)

| Name | Example | Notes |
|---|---|---|
| `FULL_EXPLICIT_DATE` | `04/08/2024`, `March 15, 2024` | Complete date with year, month, and day |
| `YEAR_ONLY` | `2024` | Four-digit year standing alone |
| `MONTH_DAY` | `3/24` | Month and day, no year |
| `DAY_MONTH` | `15/3` | Day and month, European-style |
| `DAY_MONTH_AMBIGUOUS` | `4/8` | Could be April 8 or August 4 |
| `MONTH_YEAR` | `12/2024` | Month and year, no day |
| `YEAR_MONTH` | `2024-03` | ISO-style year then month |
| `YEAR_RANGE` | `2014-2015`, `2010 to 2020`, `2023-24` | Span of two years; accepts en/em dash, `to`, `through`, abbreviated second year |

### Defined but not yet extracted

These members exist in the enum but the library does not currently produce them.

| Name | Example |
|---|---|
| `SEASON_YEAR` | `Summer 2013` |
| `TIMEFRAME_RELATIVE_TO_NOW` | `5 days ago` (handled via `RelativeTime`) |
| `NON_SPECIFIC_FUTURE_PAST` | `a long time ago` |
| `EVENT_BASED_RELATIVE_DATE` | `the day after New Year's` |
| `SEASONAL_OR_QUARTERLY` | `Q1`, `this winter` |
| `RECURRENT_DATE` | `every Monday` |
| `FUZZY_DATE` | `late March`, `early 2020s` |
| `NO_DATE` | (no temporal content found) |

---

## Supported Time Frames

For relative time expressions, the `frame` field on `RelativeTime` will be one of:

| Frame | Example expressions |
|---|---|
| `second` | `30 seconds ago` |
| `minute` | `10 minutes ago` |
| `hour` | `3 hours ago`, `half an hour ago`, `this morning` |
| `day` | `5 days ago`, `last Monday`, `yesterday` |
| `week` | `last week`, `2 weeks ago` |
| `month` | `last month`, `3 months ago` |
| `year` | `last year`, `2 years ago` |

---

## Supported Delimiters

For explicit numeric dates:

| Delimiter | Example |
|---|---|
| `/` | `04/08/2024` |
| `-` | `2024-06-05` |
| `.` | `02.14.2024` |

> **Note:** Only one delimiter type is processed per extraction call. See [BOUNDARIES.md](https://github.com/craigtrim/fast-parse-time/blob/master/BOUNDARIES.md#1-single-delimiter-type-per-extraction).

> **Unicode normalization:** En dash (–), em dash (—), and other Unicode hyphen variants are normalized to ASCII `-` before extraction. Space-padded hyphens (`2014 - 2015`) are also collapsed. This applies automatically; no special handling is required by callers.
