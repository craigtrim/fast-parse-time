# Red Team Tests

These tests are adversarial, edge-case, and boundary tests for every pattern type the library handles. This is **not** standard regression testing. The goal is to break the parser, confuse it, expose silent failures, and find inputs that should work but don't.

See [GitHub Issue #43](https://github.com/craigtrim/fast-parse-time/issues/43) for the full specification.

## Purpose

Each file targets a specific pattern type and covers three categories of attack:

- **True Positive Attacks** -- inputs that should match and return a result
- **False Positive Attacks** -- inputs that look like dates but should not match
- **Boundary / Edge Cases** -- inputs at the limits of valid ranges, degenerate forms, and malformed input
- **Unicode Attacks** -- homoglyphs, invisible characters, RTL overrides, and digit substitutions

## Test Files

| File | Pattern Type |
|---|---|
| `test_rt_numeric_delimited.py` | `04/08/2024`, `06-05-2016`, `12.31.2023` |
| `test_rt_written_month.py` | `March 15, 2024`, `15 March 2024`, `March 2024` |
| `test_rt_hyphen_month_year.py` | `Oct-23`, `Oct-2023`, `2023-Oct` |
| `test_rt_iso8601.py` | `2017-02-03T09:04:08Z`, timezone offsets, fractional seconds |
| `test_rt_prose_year.py` | `in 2024`, `since 2019`, `circa 2004`, `as of 2004` |
| `test_rt_year_range.py` | `2014-2015`, `from 2004 to 2008`, `between 2010 and 2020` |
| `test_rt_relative_ago_back.py` | `5 days ago`, `10 hours back`, `100 years ago` |
| `test_rt_relative_from_now.py` | `5 days from now`, `in 3 months`, `in 1 year` |
| `test_rt_last_next.py` | `last week`, `next month`, `last 10 days` |
| `test_rt_special_words.py` | `today`, `yesterday`, `tomorrow`, `tonight`, `now` |
| `test_rt_quantifiers.py` | `a few days ago`, `couple of weeks`, `several months ago` |
| `test_rt_eod_eom_eoy.py` | `eod`, `eom`, `eoy` |
| `test_rt_written_cardinals.py` | `twenty-three days ago`, `one hundred and fifty minutes` |
| `test_rt_compound_multi_unit.py` | `1 year 2 months ago`, `in 1 year 2 months` |
| `test_rt_unicode_and_homoglyphs.py` | Cross-cutting unicode attacks across all pattern types |

## xfail Strategy

All tests are marked `xfail` in Phase 1. This allows the full suite to land green from day one regardless of current parser behavior.

- `XFAIL` -- parser does not yet handle this input (expected gap confirmed)
- `XPASS` -- parser already handles this correctly (candidate for promotion to a hard assertion)

Phase 2 promotes `XPASS` tests and clear-cut true/false positive cases to hard assertions, and refines `xfail` reason strings for remaining gaps.

## Running the Suite

```
pytest tests/red_team/ -v
```
