# Temporal Now Tests

These tests verify recognition of "now" and "right now" as present-tense temporal references. This support was introduced in [Issue #16](https://github.com/craigtrim/fast-parse-time/issues/16). Tests confirm correct classification as neither past nor future, that results resolve to a zero timedelta, and that the forms are recognized in isolation, mid-sentence, and at the trailing position.
