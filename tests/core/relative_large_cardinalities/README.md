# Large Cardinality Tests

These tests verify that relative time expressions with large numeric cardinalities are parsed and resolved correctly, such as "34 hours ago" or "100 days from now". This capability was introduced in [Issue #14](https://github.com/craigtrim/fast-parse-time/issues/14), which identified that cardinalities above roughly 31 were not being recognized. Tests cover every time frame at large values and verify both parse results and resolved timedelta accuracy.
