#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Tests for parse_dates integration with ISO 8601 datetime strings.

Related GitHub Issue:
    #23 - Gap: ISO 8601 datetime strings not extracted
    https://github.com/craigtrim/fast-parse-time/issues/23
"""

import pytest
from fast_parse_time import parse_dates, ExplicitDate


class TestIso8601ParseDates:
    """parse_dates correctly processes ISO 8601 datetime strings."""

    # --- has_dates ---

    def test_z_suffix_has_dates(self):
        result = parse_dates('2017-02-03T09:04:08Z')
        assert result.has_dates is True

    def test_plus_zero_has_dates(self):
        result = parse_dates('2016-02-04T20:16:26+00:00')
        assert result.has_dates is True

    def test_plus_offset_has_dates(self):
        result = parse_dates('2022-04-15T10:30:00+05:30')
        assert result.has_dates is True

    def test_minus_offset_has_dates(self):
        result = parse_dates('2022-03-15T09:30:00-05:00')
        assert result.has_dates is True

    def test_dot_millis_has_dates(self):
        result = parse_dates('2017-02-03T09:04:08.001Z')
        assert result.has_dates is True

    def test_comma_millis_has_dates(self):
        result = parse_dates('2017-02-03T09:04:08,00123Z')
        assert result.has_dates is True

    # --- explicit_dates list ---

    def test_z_suffix_explicit_dates_one_entry(self):
        result = parse_dates('2017-02-03T09:04:08Z')
        assert len(result.explicit_dates) == 1

    def test_plus_zero_explicit_dates_one_entry(self):
        result = parse_dates('2016-02-04T20:16:26+00:00')
        assert len(result.explicit_dates) == 1

    def test_z_suffix_explicit_date_text(self):
        result = parse_dates('2017-02-03T09:04:08Z')
        assert result.explicit_dates[0].text == '2017-02-03'

    def test_plus_zero_explicit_date_text(self):
        result = parse_dates('2016-02-04T20:16:26+00:00')
        assert result.explicit_dates[0].text == '2016-02-04'

    def test_plus_offset_explicit_date_text(self):
        result = parse_dates('2022-04-15T10:30:00+05:30')
        assert result.explicit_dates[0].text == '2022-04-15'

    def test_minus_offset_explicit_date_text(self):
        result = parse_dates('2022-03-15T09:30:00-05:00')
        assert result.explicit_dates[0].text == '2022-03-15'

    def test_z_suffix_explicit_date_type(self):
        result = parse_dates('2017-02-03T09:04:08Z')
        assert result.explicit_dates[0].date_type == 'FULL_EXPLICIT_DATE'

    def test_plus_zero_explicit_date_type(self):
        result = parse_dates('2016-02-04T20:16:26+00:00')
        assert result.explicit_dates[0].date_type == 'FULL_EXPLICIT_DATE'

    # --- ExplicitDate instance check ---

    def test_z_suffix_is_explicit_date_instance(self):
        result = parse_dates('2017-02-03T09:04:08Z')
        assert isinstance(result.explicit_dates[0], ExplicitDate)

    # --- sentence context ---

    def test_sentence_z_has_dates(self):
        result = parse_dates('Logged at 2021-06-15T09:00:00Z')
        assert result.has_dates is True

    def test_sentence_plus_offset_has_dates(self):
        result = parse_dates('Created at 2022-04-15T10:30:00+05:30')
        assert result.has_dates is True

    def test_sentence_z_explicit_dates_one(self):
        result = parse_dates('Logged at 2021-06-15T09:00:00Z')
        assert len(result.explicit_dates) == 1

    def test_sentence_z_date_text_correct(self):
        result = parse_dates('Logged at 2021-06-15T09:00:00Z')
        assert result.explicit_dates[0].text == '2021-06-15'

    # --- with milliseconds ---

    def test_dot_millis_explicit_dates_one(self):
        result = parse_dates('2017-02-03T09:04:08.001Z')
        assert len(result.explicit_dates) == 1

    def test_dot_millis_date_text(self):
        result = parse_dates('2017-02-03T09:04:08.001Z')
        assert result.explicit_dates[0].text == '2017-02-03'

    def test_comma_millis_explicit_dates_one(self):
        result = parse_dates('2017-02-03T09:04:08,00123Z')
        assert len(result.explicit_dates) == 1

    def test_comma_millis_date_text(self):
        result = parse_dates('2017-02-03T09:04:08,00123Z')
        assert result.explicit_dates[0].text == '2017-02-03'

    # --- no false positives ---

    def test_plain_text_has_dates_false(self):
        result = parse_dates('hello world')
        assert result.has_dates is False

    def test_plain_text_explicit_dates_empty(self):
        result = parse_dates('hello world')
        assert len(result.explicit_dates) == 0
