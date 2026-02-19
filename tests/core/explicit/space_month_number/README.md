# Space-Delimited Month+Number Tests

These tests verify classification of space-delimited patterns where a written month name is followed by a two-digit number, such as "Oct 23" or "March 15". This pattern was identified as a gap in [Issue #38](https://github.com/craigtrim/fast-parse-time/issues/38) and must be distinguished from non-date strings that share the same surface form.
