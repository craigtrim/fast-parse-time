# fast-parse-time

[![PyPI version](https://img.shields.io/pypi/v/fast-parse-time.svg)](https://pypi.org/project/fast-parse-time/)
[![Python Version](https://img.shields.io/pypi/pyversions/fast-parse-time.svg)](https://pypi.org/project/fast-parse-time/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/craigtrim/fast-parse-time/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/craigtrim/fast-parse-time/actions)

Natural Language Processing (NLP) library for extracting dates and times from text.

## Features

- **Explicit Date Extraction**: Parse numeric dates in multiple formats (`04/08/2024`, `3/24`, `06-05-2016`)
- **Implicit Time References**: Extract relative time expressions (`5 days ago`, `last couple of weeks`, `30 minutes ago`)
- **Multiple Delimiters**: Supports `/`, `-`, and `.` separators
- **Ambiguity Detection**: Identifies ambiguous date formats (e.g., `4/8` could be April 8th or August 4th)
- **Temporal Analysis**: Extracts cardinality, time frame, and tense from natural language

## Installation

```bash
pip install fast-parse-time
```

## Quick Start

### Extract Numeric Dates

```python
from fast_parse_time import extract_numeric_dates

# Extract explicit dates from text
result = extract_numeric_dates("The event is scheduled for 04/08/2024")
# Returns: {'04/08/2024': 'FULL_EXPLICIT_DATE'}

result = extract_numeric_dates("Meeting on 3/24")
# Returns: {'3/24': 'MONTH_DAY'}
```

### Analyze Time References

```python
from fast_parse_time.implicit.svc import AnalyzeTimeReferences

analyzer = AnalyzeTimeReferences()

# Extract relative time references
result = analyzer.process("show me all history from 5 days ago")
# Returns: {'result': [{'Cardinality': 5, 'Frame': 'day', 'Tense': 'past'}]}

result = analyzer.process("the explosion happened 5 minutes ago")
# Returns: {'result': [{'Cardinality': 5, 'Frame': 'minute', 'Tense': 'past'}]}

result = analyzer.process("show me records from the last couple of weeks")
# Returns: {'result': [{'Cardinality': 2, 'Frame': 'week', 'Tense': 'past'}]}
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/craigtrim/fast-parse-time.git
cd fast-parse-time

# Install dependencies
pip install -r requirements.txt
# or with poetry
poetry install
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_extract_numeric_dates_01.py
```

### Pre-commit Hooks

This project uses pre-commit hooks for code quality:

```bash
pre-commit install
pre-commit run --all-files
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues

Report bugs and feature requests at the [issue tracker](https://github.com/craigtrim/fast-parse-time/issues).

## Author

**Craig Trim** - [craigtrim@gmail.com](mailto:craigtrim@gmail.com)
