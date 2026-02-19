# ISO 8601 Tests

These tests verify extraction of ISO 8601 datetime strings such as "2017-02-03T09:04:08Z" including UTC offsets, milliseconds, and timezone variants. This format was identified as a gap in [Issue #23](https://github.com/craigtrim/fast-parse-time/issues/23). Tests cover UTC zero, positive, and negative offsets, fractional seconds, Z-suffix forms, and dates embedded within longer sentences.
