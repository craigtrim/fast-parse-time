# fast-parse-time

[![PyPI version](https://img.shields.io/pypi/v/fast-parse-time.svg)](https://pypi.org/project/fast-parse-time/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://pypi.org/project/fast-parse-time/)
[![Downloads](https://pepy.tech/badge/fast-parse-time)](https://pepy.tech/project/fast-parse-time)
[![Downloads](https://pepy.tech/badge/fast-parse-time/month)](https://pepy.tech/project/fast-parse-time)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-21170-brightgreen.svg)](https://github.com/craigtrim/fast-parse-time/tree/master/tests)

`fast-parse-time` extracts calendar dates and relative time expressions from
text. The calendar-date functions also accept a list of strings and can use an
explicit date range to infer missing years. Parsing runs locally without network
calls or a language model.

## Install

Python 3.10 or later is required.

```sh
python -m pip install fast-parse-time
```

## Find dates in a list

`extract_date_strings` returns the date text in the order it appears. Each list
entry can contain a date, a sentence with several dates, or unrelated text.
Matches retain their spelling and internal whitespace. Repeated dates remain in
the result.

```python
from fast_parse_time import extract_date_strings

texts = ['Term: 3/28/2011 to 4/22/2011', 'Mar 28', 'Apr 22', 'No classes']

assert extract_date_strings(texts) == [
    '3/28/2011', '4/22/2011', 'Mar 28', 'Apr 22',
]
```

## Parse dates and infer missing years

`parse_date_strings` returns a record for each date occurrence. When at least
two distinct full dates have unambiguous interpretations, the earliest and
latest define an inclusive range. A date without a year is resolved only when
that range supports a single calendar date.

```python
from datetime import date
from fast_parse_time import parse_date_strings

matches = parse_date_strings(['3/28/2011', '4/22/2011', 'Mar 28', 'Apr 22'])

assert [match.date for match in matches] == [
    date(2011, 3, 28), date(2011, 4, 22),
    date(2011, 3, 28), date(2011, 4, 22),
]
```

The same inference works when the range crosses a year boundary. Both calendar
functions accept a whole string as well as a list.

```python
from datetime import date
from fast_parse_time import parse_date_strings

matches = parse_date_strings(
    'Term runs from 11/28/2025 to 4/14/2026; meetings on Nov 22 and March 13'
)

assert matches[-1].date == date(2026, 3, 13)
assert matches[-2].text == 'Nov 22'
assert matches[-2].year is None
```

March 13 occurs once inside that range, in 2026. November 22 falls outside it in
both years, so its year remains unknown. The parser keeps the occurrence in the
result. It does not substitute the current year.

Use `date_range=(start, end)` to supply your own bounds. If several dates remain
possible, `.date` is `None` and `.candidates` contains the alternatives. The
[calendar-date guide](docs/calendar-dates.md) covers numeric date order, leap
days, and unresolved results.

## Extract explicit dates and relative expressions

`parse_dates` returns explicit date text with classification labels, along with
relative expressions such as `5 days ago`. Use `parse_date_strings` when you need
calendar dates as Python `date` objects.

```python
from datetime import datetime
from fast_parse_time import parse_dates

result = parse_dates('Meeting on 04/08/2024 about issues from 5 days ago')

assert result.explicit_dates[0].text == '04/08/2024'
assert result.explicit_dates[0].date_type == 'FULL_EXPLICIT_DATE'
assert result.relative_times[0].to_datetime(datetime(2026, 1, 1)) == datetime(2025, 12, 27)
```

You can also request relative offsets directly. Past references produce negative
offsets; future references produce positive offsets.

```python
from datetime import timedelta
from fast_parse_time import resolve_to_timedelta

assert resolve_to_timedelta('5 days ago') == [timedelta(days=-5)]
assert resolve_to_timedelta('half an hour ago') == [timedelta(minutes=-30)]
assert resolve_to_timedelta('tomorrow') == [timedelta(days=1)]
```

## Choose a function

| What you need | Function | Result |
|---|---|---|
| Date strings from prose or a list | `extract_date_strings` | `list[str]` |
| Calendar dates with range-based year inference | `parse_date_strings` | `list[ParsedDate]` |
| Explicit date classifications and relative references | `parse_dates` | `ParseResult` |
| Explicit date classifications, including year-only and month/year expressions | `extract_explicit_dates` | `dict[str, str]` |
| Relative expressions as quantities and units | `extract_relative_times` | `list[RelativeTime]` |
| Relative expressions resolved against a reference time | `resolve_to_datetime` | `list[datetime]` |

## Interpreting results

Numeric dates can have more than one interpretation. `parse_date_strings`
preserves that ambiguity by default; use `date_order='mdy'` or `'dmy'` when the
source's convention is known. A classification such as `FULL_EXPLICIT_DATE`
identifies a complete date expression without selecting its month/day order.

Keep unrelated periods in separate batches, or supply explicit bounds. Relative
month and year offsets use 30-day months and 365-day years. Pass a fixed
`reference` when resolving offsets if the result needs to be reproducible.

## Documentation

- [API reference](docs/API.md) lists the public functions and their return values.
- [Calendar dates and year inference](docs/calendar-dates.md) explains batch parsing and ambiguity.
- [Function examples](docs/functions.md) covers extraction, filtering, and resolution.
- [Result types](docs/types.md) describes the fields returned by each API.
- [Development](docs/development.md) covers local tests and distribution builds.

## License and author

The library is available under the [MIT license](LICENSE).
Craig Trim maintains it: [craigtrim@gmail.com](mailto:craigtrim@gmail.com).

[Report an issue](https://github.com/craigtrim/fast-parse-time/issues).
