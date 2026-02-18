# datefinder Compatibility Tests

Test cases sourced from the [datefinder](https://github.com/akoumjian/datefinder) test suite.

**Source repo:** https://github.com/akoumjian/datefinder
**License:** MIT
**Last release:** July 2022 (v0.7.3)
**Monthly downloads:** ~3.5M
**Status:** Stalled

## Purpose

datefinder is the closest competitor for the explicit-date-in-document extraction use case.
It uses regex to scan free-form text for all date-like patterns and returns `datetime` objects.
It does NOT handle relative time expressions.

These tests measure fast-parse-time's coverage of explicit date extraction from text.
fast-parse-time uses `extract_explicit_dates()` which returns `{date_string: date_type}` dicts
rather than `datetime` objects. Assertions check for presence and count, not resolved datetime values.

## Source Files Mapped

| File here | Source in datefinder |
|---|---|
| test_find_dates.py | tests/test_find_dates.py |
| test_find_dates_strict.py | tests/test_find_dates_strict.py |
| test_extract_date_strings.py | tests/test_extract_date_strings.py |

## What Was Changed

`datefinder.find_dates(text)` returns a generator of `datetime` objects.
`extract_explicit_dates(text)` returns a `dict[str, str]` mapping date strings to type classifications.
Assertions were adapted to check for date presence and count rather than exact datetime values.
Input strings are unchanged from the originals.
