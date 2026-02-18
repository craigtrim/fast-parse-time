# dateparser Compatibility Tests

Test cases sourced from the [dateparser](https://github.com/scrapinghub/dateparser) test suite.

**Source repo:** https://github.com/scrapinghub/dateparser
**License:** BSD
**Last release:** February 2026 (v1.3.0)
**Monthly downloads:** ~33.3M

## Purpose

dateparser is the primary active competitor for English natural language date and time parsing.
These tests measure fast-parse-time's coverage of the input space that dateparser handles.

Only English-language test cases are included. dateparser supports 200+ languages;
fast-parse-time is English-only, so non-English inputs are out of scope.

Tests that currently fail indicate gaps. Tests that pass indicate parity.

## Source Files Mapped

| File here | Source in dateparser |
|---|---|
| test_freshness.py | tests/test_freshness_date_parser.py (English cases only) |
| test_explicit_dates.py | tests/test_clean_api.py + tests/test_search.py (English cases) |

## Note on Directory Naming

This directory is named `compat_dateparser` rather than `dateparser` to avoid shadowing
the installed `dateparser` PyPI package. A local `tests/dateparser/__init__.py` would
be resolved by Python's import system before the installed package, causing
`AttributeError: module 'dateparser' has no attribute 'parse'` in production code.

## What Was Changed

Only the API calls and assertions were adapted. dateparser uses `dateparser.parse(text)` or
`search_dates(text)` which returns `datetime` objects. fast-parse-time uses
`parse_time_references(text)` for relative time (returns `[RelativeTime]`) and
`extract_explicit_dates(text)` for explicit dates (returns `{str: str}`).
Input strings are unchanged from the originals.
