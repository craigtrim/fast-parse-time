# fast-parse-time

[![PyPI version](https://img.shields.io/pypi/v/fast-parse-time.svg)](https://pypi.org/project/fast-parse-time/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://pypi.org/project/fast-parse-time/)
[![Downloads](https://pepy.tech/badge/fast-parse-time)](https://pepy.tech/project/fast-parse-time)
[![Downloads](https://pepy.tech/badge/fast-parse-time/month)](https://pepy.tech/project/fast-parse-time)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-8560-brightgreen.svg)](https://github.com/craigtrim/fast-parse-time/tree/master/tests)

Extract dates and times from text. Fast, deterministic, zero cost.

## Why?

LLMs can parse dates, but they're slow, expensive, and non-deterministic. This library gives you:

- **Sub-millisecond performance** - Process thousands of documents per second
- **Zero API costs** - No per-request charges
- **Deterministic results** - Same input always produces same output
- **Simple API** - One function call, everything extracted

## Install

```bash
pip install fast-parse-time
```

## Usage

```python
from fast_parse_time import parse_dates

text = "Meeting on 04/08/2024 to discuss issues from 5 days ago"
result = parse_dates(text)

# Explicit dates found in text
print(result.explicit_dates)
# [ExplicitDate(text='04/08/2024', date_type='FULL_EXPLICIT_DATE')]

# Relative time expressions
print(result.relative_times)
# [RelativeTime(cardinality=5, frame='day', tense='past')]

# Convert to Python datetime
for time_ref in result.relative_times:
    print(time_ref.to_datetime())
    # datetime.datetime(2025, 11, 14, ...)
```

## What It Extracts

**Explicit dates:**
```python
"Event on 04/08/2024"          → 04/08/2024 (full date)
"Meeting scheduled for 3/24"   → 3/24 (month/day)
"Copyright 2024"               → 2024 (year only)
"Ambiguous: 4/8"               → 4/8 (flagged as ambiguous)
"Published March 15, 2024"     → March 15, 2024 (written month)
"Filed in 2024"                → 2024 (year in prose)
```

**Year ranges:**
```python
"Active 2014-2015"             → 2014-2015 (year range)
"From 2010 to 2020"           → From 2010 to 2020 (year range)
"Revenue grew 2019–2023"      → 2019-2023 (en/em dash normalized)
"Contract 2023-24"            → 2023-24 (abbreviated)
```

**Relative times:**
```python
"5 days ago"                   → 5 days (past)
"last couple of weeks"         → 2 weeks (past)
"30 minutes ago"               → 30 minutes (past)
"half an hour ago"             → 1 hour (past)
"a few days ago"               → 3 days (past)
```

## Examples

### Parse everything at once

```python
result = parse_dates("Report from 04/08/2024 covering issues from last week")

result.explicit_dates  # ['04/08/2024']
result.relative_times  # [RelativeTime(cardinality=1, frame='week', tense='past')]
```

### Just get dates

```python
from fast_parse_time import extract_explicit_dates

dates = extract_explicit_dates("Event on 04/08/2024 or maybe 3/24")
# {'04/08/2024': 'FULL_EXPLICIT_DATE', '3/24': 'MONTH_DAY'}
```

### Convert to datetime objects

```python
from fast_parse_time import resolve_to_datetime

datetimes = resolve_to_datetime("Show me data from 5 days ago")
# [datetime.datetime(2025, 11, 14, ...)]
```

## Features

- Multiple date formats: `04/08/2024`, `3/24`, `2024-06-05`, `March 15, 2024`
- Multiple delimiters: `/`, `-`, `.`
- Year ranges: `2014-2015`, `2010 to 2020`, `from 2018 through 2022`, `2023-24`
- Unicode normalization: en dash, em dash, and other hyphen variants accepted automatically
- Written months: `March 15, 2024`, `Mar 15, 2024`, `15 March 2024`
- Year-only in prose: `Copyright 2024`, `filed in 2019`
- Relative time expressions: "5 days ago", "last week", "couple of months ago"
- Informal expressions: "half an hour ago", "a few days ago", "several weeks ago"
- Named day and time-of-day references: "last Monday", "this morning", "yesterday"
- Ambiguity detection: Flags dates like `4/8` that could be April 8 or August 4
- Time frame support: seconds, minutes, hours, days, weeks, months, years

## Documentation

- [API Reference](https://github.com/craigtrim/fast-parse-time/blob/master/docs/API.md)
- [Functions](https://github.com/craigtrim/fast-parse-time/blob/master/docs/functions.md) - All functions with examples
- [Types](https://github.com/craigtrim/fast-parse-time/blob/master/docs/types.md) - Data classes and DateType enum
- [System Boundaries](https://github.com/craigtrim/fast-parse-time/blob/master/BOUNDARIES.md) - Design decisions and limitations

## Performance

Typical extraction takes < 1ms per document. No network calls, no model inference, pure Python.

## License

MIT - See [LICENSE](LICENSE) for details.

## Author

**Craig Trim** - [craigtrim@gmail.com](mailto:craigtrim@gmail.com)

---

[Report Issues](https://github.com/craigtrim/fast-parse-time/issues) | [API Docs](https://github.com/craigtrim/fast-parse-time/blob/master/docs/API.md) | [PyPI](https://pypi.org/project/fast-parse-time/)
