# API Reference

Extract dates and times from text. Fast, deterministic, zero cost.

## Quick Reference

| Function | Returns | Use when |
|---|---|---|
| `parse_dates(text)` | `ParseResult` | You want everything - explicit dates and relative times |
| `parse_time_references(text)` | `List[RelativeTime]` | You only care about relative time expressions |
| `extract_explicit_dates(text)` | `Dict[str, str]` | You only care about numeric or written dates |
| `extract_date_strings(texts)` | `list[str]` | Original calendar-date strings from prose or a list |
| `parse_date_strings(texts, *, date_range=None, date_order='auto')` | `list[ParsedDate]` | Parsed dates with missing years inferred from an inclusive range |
| `extract_relative_times(text)` | `List[RelativeTime]` | Low-level relative time extraction |
| `parse_dates_with_type(text, type)` | `Dict[str, str]` | Dates filtered to a specific `DateType` |
| `resolve_to_datetime(text)` | `List[datetime]` | Relative times as absolute datetimes |
| `resolve_to_timedelta(text)` | `List[timedelta]` | Relative times as duration offsets |
| `extract_past_references(text)` | `List[RelativeTime]` | Past-only time references |
| `extract_future_references(text)` | `List[RelativeTime]` | Future-only time references |
| `extract_full_dates_only(text)` | `Dict[str, str]` | Complete dates (year + month + day) only |
| `extract_ambiguous_dates(text)` | `Dict[str, str]` | Dates that need clarification (e.g., `4/8`) |
| `has_temporal_info(text)` | `bool` | Quick yes/no check |
| `parse_and_resolve(text)` | `Dict` | All temporal info with relatives resolved to datetimes |
| `get_date_range(text)` | `Optional[Tuple]` | A start/end range from two relative references |

## Docs

- [Calendar dates and year inference](calendar-dates.md) - Batch parsing, explicit ranges, and unresolved dates
- [functions.md](https://github.com/craigtrim/fast-parse-time/blob/master/docs/functions.md) - All functions with signatures, parameters, and examples
- [types.md](https://github.com/craigtrim/fast-parse-time/blob/master/docs/types.md) - Data classes, `DateType` enum, supported time frames and delimiters
- [BOUNDARIES.md](https://github.com/craigtrim/fast-parse-time/blob/master/BOUNDARIES.md) - Known limitations and design decisions
