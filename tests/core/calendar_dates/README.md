# Batch calendar dates

Regression coverage for [issue #73](https://github.com/craigtrim/fast-parse-time/issues/73).
The suite contains 9,795 collected cases. All are ordinary passing assertions,
with no skips or expected failures.

- 4,386 full-date cases: every day of 2011 and 2024 in six formats, including
  numeric date orders, written months, ordinals, and varied prose wrappers.
- 1,464 yearless-date cases: all 366 possible month/day pairs in four forms.
- 1,830 range cases: each month/day against term, cross-year, leap-year,
  multiple-year, and single-day ranges. The oracle walks the actual calendar
  with `timedelta`, independently of the production inference algorithm.
- Additional contract, invalid-date, numeric ambiguity, Unicode delimiter,
  whitespace, casing, ordinal, punctuation, and integration cases.

Run this suite with `python -m pytest tests/core/calendar_dates -q`.
Use `python -m pytest tests/core/calendar_dates --collect-only -q` for the exact
collected case count. Test IDs identify dates, formats, and ranges for failures.
