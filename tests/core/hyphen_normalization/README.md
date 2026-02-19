# Hyphen Normalization Tests

These tests verify that non-ASCII dash characters are normalized to a standard ASCII hyphen before parsing, so that patterns like year ranges and hyphen-delimited dates work regardless of which dash variant appears in the input. This preprocessing layer was introduced in [Issue #44](https://github.com/craigtrim/fast-parse-time/issues/44). Tests cover en-dash, em-dash, soft hyphens, space-padded hyphens, chained dashes, and mixed dash types.
