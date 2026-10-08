# API reference

Import public functions from `fast_parse_time`. The calendar-date functions
accept a string or `list[str]`. The remaining functions accept one string.

## Calendar dates

| Function | Returns | Behavior |
|---|---|---|
| `extract_date_strings(texts)` | `list[str]` | Finds calendar-date text and preserves each occurrence |
| `parse_date_strings(texts, *, date_range=None, date_order='auto')` | `list[ParsedDate]` | Parses dates and uses inclusive bounds to infer missing years |

These functions require a month and day. They preserve the source text and
duplicates. A `ParsedDate` has a `.date` value only when one interpretation
remains; unresolved occurrences stay in the list. See the
[calendar-date guide](calendar-dates.md) for range selection and numeric order.

## Classification and relative expressions

| Function | Returns | Behavior |
|---|---|---|
| `parse_dates(text)` | `ParseResult` | Combines explicit date classifications and relative references |
| `extract_explicit_dates(text)` | `dict[str, str]` | Maps explicit date expressions to classification names |
| `parse_time_references(text)` | `list[RelativeTime]` | Extracts relative expressions |
| `extract_relative_times(text)` | `list[RelativeTime]` | Performs the same extraction as `parse_time_references` |
| `parse_dates_with_type(text, date_type=None)` | `dict[str, str]` | Filters explicit dates by a classification name |
| `extract_full_dates_only(text)` | `dict[str, str]` | Selects the `FULL_EXPLICIT_DATE` classification |
| `extract_ambiguous_dates(text)` | `dict[str, str]` | Selects the `DAY_MONTH_AMBIGUOUS` classification |
| `extract_past_references(text)` | `list[RelativeTime]` | Selects references with past tense |
| `extract_future_references(text)` | `list[RelativeTime]` | Selects references with future tense |
| `has_temporal_info(text)` | `bool` | Reports whether `parse_dates` found a match |

An explicit classification describes the expression's form. It does not select
a calendar interpretation. For example, `04/08/2024` receives
`FULL_EXPLICIT_DATE` even though its numeric order is ambiguous. These functions
can also recognize expressions such as `March 2024` and `in 2019` that lack a
month or day. Dictionary results collapse repeated keys and can normalize the
matched text.

## Resolving relative expressions

| Function | Returns | Behavior |
|---|---|---|
| `resolve_to_datetime(text, reference=None)` | `list[datetime]` | Applies each relative offset to a reference time |
| `resolve_to_timedelta(text)` | `list[timedelta]` | Returns signed offsets |
| `parse_and_resolve(text, reference=None)` | `dict` | Returns explicit strings under `explicit` and resolved datetimes under `resolved` |
| `get_date_range(text)` | `tuple[datetime, datetime]` or `None` | Resolves exactly two relative references against the current time and sorts them |

`reference` defaults to `datetime.now()`. Month and year offsets use fixed
durations of 30 and 365 days. Named weekdays are normalized against the local
date during extraction, before the reference is applied.

`get_date_range` works with relative references. The `date_range` argument to
`parse_date_strings` supplies calendar bounds for year inference. They serve
different inputs.

## Results and examples

[Result types](types.md) describes `ParsedDate`, `ExplicitDate`, `RelativeTime`,
`ParseResult`, and `DateType`. [Function examples](functions.md) includes
signatures and executable examples for the public functions.

The legacy `extract_numeric_dates(input_text)` function and
`ExplicitTimeExtractor` class remain available. Use `extract_explicit_dates`
when you need the broader set of explicit date classifications.
