# parsedatetime Compatibility Tests

Test cases sourced from the [parsedatetime](https://github.com/bear/parsedatetime) test suite.

**Source repo:** https://github.com/bear/parsedatetime
**License:** Apache 2.0
**Last release:** May 2020 (v2.6)

## Purpose

These tests exist to measure fast-parse-time's coverage of the input space that parsedatetime handles.
parsedatetime has ~24M monthly downloads on PyPI but is stalled with no active maintainer.
Its users represent the most reachable audience for fast-parse-time.

Tests that currently fail indicate gaps. Tests that pass indicate parity with parsedatetime on that input.

## Source Files Mapped

| File here | Source in parsedatetime |
|---|---|
| test_simple_offsets.py | tests/TestSimpleOffsets.py |
| test_simple_offsets_hours.py | tests/TestSimpleOffsetsHours.py |
| test_units.py | tests/TestUnits.py |
| test_delta.py | tests/TestDelta.py |
| test_phrases.py | tests/TestPhrases.py |

## What Was Changed

Only the API calls and assertions were adapted. parsedatetime uses `cal.parse(text)` which returns
`(time_struct, pdtContext_flag)` tuples. fast-parse-time uses `parse_time_references(text)` which
returns `[RelativeTime(cardinality, frame, tense)]` objects. The input strings are unchanged.
