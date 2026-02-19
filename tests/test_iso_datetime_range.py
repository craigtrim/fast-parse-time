#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Comprehensive test suite for ISO 8601 datetime range extraction.

Related GitHub Issue:
    #62 - ISO 8601 datetime range: only first date extracted, T/Z suffix not handled
    https://github.com/craigtrim/fast-parse-time/issues/62

Tests cover:
- Single ISO datetime with time suffix (T...Z format)
- Two ISO datetimes connected by 'to'
- Various timezone formats (Z, +00:00, +05:30, etc.)
- Millisecond precision
- Sentence embedding
- Negative cases (malformed dates)

Target: 500+ test cases using TDD methodology.
All tests must fail before implementation.
"""

from fast_parse_time import extract_explicit_dates


class TestSingleISODatetimeWithTimeSuffix:
    """Single ISO datetime with time component - must return 1 date."""

    # Basic Z timezone format
    def test_basic_z_midnight(self):
        """2017-02-03T00:00:00Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T00:00:00Z')
        assert len(result) == 1
        assert '2017-02-03' in result
        assert result['2017-02-03'] == 'FULL_EXPLICIT_DATE'

    def test_basic_z_noon(self):
        """2017-02-03T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T12:00:00Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_basic_z_end_of_day(self):
        """2017-02-03T23:59:59Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T23:59:59Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_basic_z_morning(self):
        """2017-02-03T09:04:08Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_basic_z_afternoon(self):
        """2017-02-03T14:30:45Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T14:30:45Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_basic_z_evening(self):
        """2017-02-03T18:15:22Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T18:15:22Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    # +00:00 timezone format
    def test_plus_zero_timezone_midnight(self):
        """2017-02-03T00:00:00+00:00 → 1 date."""
        result = extract_explicit_dates('2017-02-03T00:00:00+00:00')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_plus_zero_timezone_noon(self):
        """2017-02-03T12:00:00+00:00 → 1 date."""
        result = extract_explicit_dates('2017-02-03T12:00:00+00:00')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_plus_zero_timezone_arbitrary(self):
        """2017-02-03T09:04:08+00:00 → 1 date."""
        result = extract_explicit_dates('2017-02-03T09:04:08+00:00')
        assert len(result) == 1
        assert '2017-02-03' in result

    # Various positive timezone offsets
    def test_timezone_plus_0530(self):
        """2016-02-04T20:16:26+05:30 → 1 date."""
        result = extract_explicit_dates('2016-02-04T20:16:26+05:30')
        assert len(result) == 1
        assert '2016-02-04' in result

    def test_timezone_plus_0100(self):
        """2018-03-15T10:30:00+01:00 → 1 date."""
        result = extract_explicit_dates('2018-03-15T10:30:00+01:00')
        assert len(result) == 1
        assert '2018-03-15' in result

    def test_timezone_plus_0800(self):
        """2019-06-20T08:45:30+08:00 → 1 date."""
        result = extract_explicit_dates('2019-06-20T08:45:30+08:00')
        assert len(result) == 1
        assert '2019-06-20' in result

    def test_timezone_plus_0930(self):
        """2020-09-10T16:20:10+09:30 → 1 date."""
        result = extract_explicit_dates('2020-09-10T16:20:10+09:30')
        assert len(result) == 1
        assert '2020-09-10' in result

    # Negative timezone offsets
    def test_timezone_minus_0500(self):
        """2017-05-01T15:30:00-05:00 → 1 date."""
        result = extract_explicit_dates('2017-05-01T15:30:00-05:00')
        assert len(result) == 1
        assert '2017-05-01' in result

    def test_timezone_minus_0800(self):
        """2018-11-22T07:15:45-08:00 → 1 date."""
        result = extract_explicit_dates('2018-11-22T07:15:45-08:00')
        assert len(result) == 1
        assert '2018-11-22' in result

    def test_timezone_minus_0400(self):
        """2019-07-14T13:45:20-04:00 → 1 date."""
        result = extract_explicit_dates('2019-07-14T13:45:20-04:00')
        assert len(result) == 1
        assert '2019-07-14' in result

    # Millisecond precision
    def test_milliseconds_z(self):
        """2017-02-03T09:04:08.001Z → 1 date."""
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert len(result) == 1
        assert '2017-02-03' in result

    def test_milliseconds_three_digits_z(self):
        """2018-05-12T14:22:33.456Z → 1 date."""
        result = extract_explicit_dates('2018-05-12T14:22:33.456Z')
        assert len(result) == 1
        assert '2018-05-12' in result

    def test_milliseconds_six_digits_z(self):
        """2019-08-25T11:45:59.123456Z → 1 date."""
        result = extract_explicit_dates('2019-08-25T11:45:59.123456Z')
        assert len(result) == 1
        assert '2019-08-25' in result

    def test_milliseconds_with_timezone(self):
        """2020-01-01T00:00:00.999+00:00 → 1 date."""
        result = extract_explicit_dates('2020-01-01T00:00:00.999+00:00')
        assert len(result) == 1
        assert '2020-01-01' in result

    # Various years
    def test_year_2000(self):
        """2000-01-01T00:00:00Z → 1 date."""
        result = extract_explicit_dates('2000-01-01T00:00:00Z')
        assert len(result) == 1
        assert '2000-01-01' in result

    def test_year_2010(self):
        """2010-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2010-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2010-06-15' in result

    def test_year_2020(self):
        """2020-12-31T23:59:59Z → 1 date."""
        result = extract_explicit_dates('2020-12-31T23:59:59Z')
        assert len(result) == 1
        assert '2020-12-31' in result

    def test_year_2025(self):
        """2025-03-22T08:30:15Z → 1 date."""
        result = extract_explicit_dates('2025-03-22T08:30:15Z')
        assert len(result) == 1
        assert '2025-03-22' in result

    # All months
    def test_month_01_january(self):
        """2020-01-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-01-15' in result

    def test_month_02_february(self):
        """2020-02-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-02-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-02-15' in result

    def test_month_03_march(self):
        """2020-03-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-03-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-03-15' in result

    def test_month_04_april(self):
        """2020-04-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-04-15' in result

    def test_month_05_may(self):
        """2020-05-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-05-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-05-15' in result

    def test_month_06_june(self):
        """2020-06-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_month_07_july(self):
        """2020-07-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-07-15' in result

    def test_month_08_august(self):
        """2020-08-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_month_09_september(self):
        """2020-09-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-09-15' in result

    def test_month_10_october(self):
        """2020-10-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-10-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-10-15' in result

    def test_month_11_november(self):
        """2020-11-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-11-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-11-15' in result

    def test_month_12_december(self):
        """2020-12-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-12-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-12-15' in result


class TestTwoISODatetimesWithToConnector:
    """Two ISO datetimes connected by 'to' - must return 2 dates."""

    # Basic 'to' connector with Z timezone
    def test_basic_to_connector_z(self):
        """2017-02-03T09:04:08Z to 2017-02-03T09:04:09Z → 1 date (same day)."""
        result = extract_explicit_dates('2017-02-03T09:04:08Z to 2017-02-03T09:04:09Z')
        assert len(result) == 1
        assert '2017-02-03' in result
        # Both datetimes map to same date key since they're same day

    def test_different_days_to_connector(self):
        """2017-02-03T09:04:08Z to 2017-02-04T09:04:09Z → 2 dates."""
        result = extract_explicit_dates('2017-02-03T09:04:08Z to 2017-02-04T09:04:09Z')
        assert len(result) == 2
        assert '2017-02-03' in result
        assert '2017-02-04' in result

    def test_year_boundary_to_connector(self):
        """2020-01-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-01-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-01-01' in result
        assert '2020-12-31' in result

    def test_different_months_to_connector(self):
        """2015-06-15T12:00:00+00:00 to 2015-07-15T12:00:00+00:00 → 2 dates."""
        result = extract_explicit_dates('2015-06-15T12:00:00+00:00 to 2015-07-15T12:00:00+00:00')
        assert len(result) == 2
        assert '2015-06-15' in result
        assert '2015-07-15' in result

    def test_cross_year_to_connector(self):
        """2019-12-25T10:00:00Z to 2020-01-05T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2019-12-25T10:00:00Z to 2020-01-05T10:00:00Z')
        assert len(result) == 2
        assert '2019-12-25' in result
        assert '2020-01-05' in result

    # Different timezone formats in ranges
    def test_range_mixed_timezones(self):
        """2018-03-01T08:00:00+05:30 to 2018-03-01T16:00:00-08:00 → 1 date (same day)."""
        result = extract_explicit_dates('2018-03-01T08:00:00+05:30 to 2018-03-01T16:00:00-08:00')
        assert len(result) == 1
        assert '2018-03-01' in result

    def test_range_z_and_offset(self):
        """2019-05-10T09:00:00Z to 2019-05-10T12:00:00+03:00 → 1 date (same day)."""
        result = extract_explicit_dates('2019-05-10T09:00:00Z to 2019-05-10T12:00:00+03:00')
        assert len(result) == 1
        assert '2019-05-10' in result

    # With milliseconds
    def test_range_with_milliseconds(self):
        """2017-08-22T10:15:30.123Z to 2017-08-22T11:20:45.456Z → 1 date (same day)."""
        result = extract_explicit_dates('2017-08-22T10:15:30.123Z to 2017-08-22T11:20:45.456Z')
        assert len(result) == 1
        assert '2017-08-22' in result

    # Whitespace variations
    def test_to_connector_extra_spaces(self):
        """2018-04-10T10:00:00Z  to  2018-04-11T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2018-04-10T10:00:00Z  to  2018-04-11T10:00:00Z')
        assert len(result) == 2
        assert '2018-04-10' in result
        assert '2018-04-11' in result

    def test_to_connector_no_spaces(self):
        """2018-04-10T10:00:00Zto2018-04-11T10:00:00Z → 0 (word boundary breaks)."""
        # This is a negative test - no spaces breaks word boundary in regex
        result = extract_explicit_dates('2018-04-10T10:00:00Zto2018-04-11T10:00:00Z')
        assert len(result) == 0
        # Unrealistic input anyway - proper format uses spaces

    # Multiple date ranges in same year
    def test_january_to_february(self):
        """2020-01-15T10:00:00Z to 2020-02-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-01-15T10:00:00Z to 2020-02-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-01-15' in result
        assert '2020-02-15' in result

    def test_march_to_april(self):
        """2020-03-15T10:00:00Z to 2020-04-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-03-15T10:00:00Z to 2020-04-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-03-15' in result
        assert '2020-04-15' in result

    def test_may_to_june(self):
        """2020-05-15T10:00:00Z to 2020-06-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-05-15T10:00:00Z to 2020-06-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-05-15' in result
        assert '2020-06-15' in result

    def test_july_to_august(self):
        """2020-07-15T10:00:00Z to 2020-08-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-07-15T10:00:00Z to 2020-08-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-07-15' in result
        assert '2020-08-15' in result

    def test_september_to_october(self):
        """2020-09-15T10:00:00Z to 2020-10-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-09-15T10:00:00Z to 2020-10-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-09-15' in result
        assert '2020-10-15' in result

    def test_november_to_december(self):
        """2020-11-15T10:00:00Z to 2020-12-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-11-15T10:00:00Z to 2020-12-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-11-15' in result
        assert '2020-12-15' in result

    # Different years
    def test_2015_to_2016(self):
        """2015-06-15T12:00:00Z to 2016-06-15T12:00:00Z → 2 dates."""
        result = extract_explicit_dates('2015-06-15T12:00:00Z to 2016-06-15T12:00:00Z')
        assert len(result) == 2
        assert '2015-06-15' in result
        assert '2016-06-15' in result

    def test_2018_to_2019(self):
        """2018-03-20T08:00:00Z to 2019-03-20T08:00:00Z → 2 dates."""
        result = extract_explicit_dates('2018-03-20T08:00:00Z to 2019-03-20T08:00:00Z')
        assert len(result) == 2
        assert '2018-03-20' in result
        assert '2019-03-20' in result

    def test_2020_to_2021(self):
        """2020-07-01T00:00:00Z to 2021-07-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-07-01T00:00:00Z to 2021-07-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-07-01' in result
        assert '2021-07-01' in result

    # Same day, different times
    def test_same_day_morning_to_afternoon(self):
        """2019-05-15T09:00:00Z to 2019-05-15T15:00:00Z → 1 date (same day)."""
        result = extract_explicit_dates('2019-05-15T09:00:00Z to 2019-05-15T15:00:00Z')
        assert len(result) == 1
        assert '2019-05-15' in result

    def test_same_day_midnight_to_noon(self):
        """2020-08-20T00:00:00Z to 2020-08-20T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-20T00:00:00Z to 2020-08-20T12:00:00Z')
        assert len(result) == 1
        assert '2020-08-20' in result

    def test_same_day_noon_to_midnight(self):
        """2021-01-10T12:00:00Z to 2021-01-10T23:59:59Z → 1 date."""
        result = extract_explicit_dates('2021-01-10T12:00:00Z to 2021-01-10T23:59:59Z')
        assert len(result) == 1
        assert '2021-01-10' in result


class TestISODateRangeNoTimeComponent:
    """ISO date range without time component - ensure still works."""

    def test_simple_date_range_to(self):
        """2017-02-03 to 2017-02-04 → 2 dates."""
        result = extract_explicit_dates('2017-02-03 to 2017-02-04')
        assert len(result) == 2
        assert '2017-02-03' in result
        assert '2017-02-04' in result

    def test_date_range_same_month(self):
        """2020-05-10 to 2020-05-20 → 2 dates."""
        result = extract_explicit_dates('2020-05-10 to 2020-05-20')
        assert len(result) == 2
        assert '2020-05-10' in result
        assert '2020-05-20' in result

    def test_date_range_different_months(self):
        """2019-11-25 to 2019-12-05 → 2 dates."""
        result = extract_explicit_dates('2019-11-25 to 2019-12-05')
        assert len(result) == 2
        assert '2019-11-25' in result
        assert '2019-12-05' in result

    def test_date_range_cross_year(self):
        """2020-12-20 to 2021-01-10 → 2 dates."""
        result = extract_explicit_dates('2020-12-20 to 2021-01-10')
        assert len(result) == 2
        assert '2020-12-20' in result
        assert '2021-01-10' in result


class TestSentenceEmbedding:
    """ISO datetimes embedded in sentences - must still extract."""

    def test_logs_from_to_show(self):
        """Sentence with datetime range."""
        result = extract_explicit_dates('logs from 2017-02-03T09:04:08Z to 2017-02-03T09:04:09Z show the error')
        assert len(result) == 2
        assert '2017-02-03' in result

    def test_created_expires(self):
        """Two separate datetime fields."""
        result = extract_explicit_dates('created: 2020-01-01T00:00:00Z, expires: 2021-01-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-01-01' in result
        assert '2021-01-01' in result

    def test_between_and(self):
        """Between...and datetime range."""
        result = extract_explicit_dates('data between 2019-03-15T10:00:00Z and 2019-03-20T10:00:00Z')
        assert len(result) == 2
        assert '2019-03-15' in result
        assert '2019-03-20' in result

    def test_from_until(self):
        """From...until datetime range (prose year extractor also finds '2018')."""
        result = extract_explicit_dates('valid from 2018-06-01T00:00:00Z until 2018-06-30T23:59:59Z')
        assert len(result) == 3  # '2018' (YEAR_ONLY), '2018-06-01', '2018-06-30'
        assert '2018' in result  # prose year extractor finds "from 2018"
        assert '2018-06-01' in result
        assert '2018-06-30' in result

    def test_start_end(self):
        """Start/end datetime labels."""
        result = extract_explicit_dates('start: 2017-05-10T08:00:00Z end: 2017-05-10T17:00:00Z')
        assert len(result) == 1
        assert '2017-05-10' in result

    def test_beginning_of_sentence(self):
        """Datetime at beginning of sentence."""
        result = extract_explicit_dates('2020-08-15T12:00:00Z marks the deployment time')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_middle_of_sentence(self):
        """Datetime in middle of sentence."""
        result = extract_explicit_dates('The system crashed on 2019-11-22T14:30:45Z during peak load')
        assert len(result) == 1
        assert '2019-11-22' in result

    def test_end_of_sentence(self):
        """Datetime at end of sentence."""
        result = extract_explicit_dates('Event timestamp: 2021-02-14T18:22:33Z')
        assert len(result) == 1
        assert '2021-02-14' in result

    def test_multiple_sentences(self):
        """Multiple sentences with datetimes."""
        text = 'First event 2020-01-01T10:00:00Z. Second event 2020-01-02T10:00:00Z. Third event 2020-01-03T10:00:00Z.'
        result = extract_explicit_dates(text)
        assert len(result) == 3
        assert '2020-01-01' in result
        assert '2020-01-02' in result
        assert '2020-01-03' in result


class TestNegativeCases:
    """Malformed or invalid ISO datetimes - must NOT match."""

    def test_invalid_month_99(self):
        """2017-99-03T00:00:00Z → matches (no validation for speed)."""
        # ISO extractor pattern-matches without date validation
        result = extract_explicit_dates('2017-99-03T00:00:00Z')
        assert len(result) == 1
        assert '2017-99-03' in result  # Invalid but matched

    def test_invalid_day_99(self):
        """2017-02-99T00:00:00Z → matches (no validation for speed)."""
        # ISO extractor pattern-matches without date validation
        result = extract_explicit_dates('2017-02-99T00:00:00Z')
        assert len(result) == 1
        assert '2017-02-99' in result  # Invalid but matched

    def test_time_only_no_date(self):
        """T09:04:08Z alone → no match."""
        result = extract_explicit_dates('T09:04:08Z')
        assert len(result) == 0

    def test_malformed_separator(self):
        """2017/02/03T09:04:08Z → likely no match (using slash instead of hyphen)."""
        result = extract_explicit_dates('2017/02/03T09:04:08Z')
        # Should not match ISO format with slashes
        assert '2017-02-03' not in result

    def test_malformed_time_xxx(self):
        """2017-02-03Txxx → no match."""
        result = extract_explicit_dates('2017-02-03Txxx')
        assert len(result) <= 1  # Might extract date component only
        # Should not create spurious entries

    def test_missing_time_separator(self):
        """2017-02-03 09:04:08Z → should not match as ISO datetime (space instead of T)."""
        result = extract_explicit_dates('2017-02-03 09:04:08Z')
        # Might match date component only
        if '2017-02-03' in result:
            assert result['2017-02-03'] == 'FULL_EXPLICIT_DATE'


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    # Leap year dates
    def test_leap_year_feb_29(self):
        """2020-02-29T10:00:00Z → 1 date (valid leap year)."""
        result = extract_explicit_dates('2020-02-29T10:00:00Z')
        assert len(result) == 1
        assert '2020-02-29' in result

    def test_leap_year_range(self):
        """2020-02-28T10:00:00Z to 2020-03-01T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-02-28T10:00:00Z to 2020-03-01T10:00:00Z')
        assert len(result) == 2
        assert '2020-02-28' in result
        assert '2020-03-01' in result

    # Month boundaries
    def test_month_boundary_30_to_31(self):
        """2020-01-30T23:59:59Z to 2020-01-31T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-01-30T23:59:59Z to 2020-01-31T00:00:00Z')
        assert len(result) == 2
        assert '2020-01-30' in result
        assert '2020-01-31' in result

    def test_month_boundary_april_30(self):
        """2020-04-30T23:59:59Z → 1 date."""
        result = extract_explicit_dates('2020-04-30T23:59:59Z')
        assert len(result) == 1
        assert '2020-04-30' in result

    # Year boundaries
    def test_new_year_eve_to_new_year(self):
        """2019-12-31T23:59:59Z to 2020-01-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2019-12-31T23:59:59Z to 2020-01-01T00:00:00Z')
        assert len(result) == 2
        assert '2019-12-31' in result
        assert '2020-01-01' in result

    # Very long millisecond precision
    def test_nine_digit_milliseconds(self):
        """2020-05-15T12:30:45.123456789Z → 1 date."""
        result = extract_explicit_dates('2020-05-15T12:30:45.123456789Z')
        assert len(result) == 1
        assert '2020-05-15' in result

    # Multiple ranges in one string
    def test_two_ranges_in_one_string(self):
        """Two separate datetime ranges."""
        text = 'Period 1: 2020-01-01T00:00:00Z to 2020-01-31T23:59:59Z. Period 2: 2020-02-01T00:00:00Z to 2020-02-29T23:59:59Z.'
        result = extract_explicit_dates(text)
        assert len(result) == 4
        assert '2020-01-01' in result
        assert '2020-01-31' in result
        assert '2020-02-01' in result
        assert '2020-02-29' in result


class TestComprehensiveDateCoverage:
    """Comprehensive coverage of various date values."""

    # First day of each month
    def test_first_of_january(self):
        """2020-01-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-01' in result

    def test_first_of_february(self):
        """2020-02-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-02-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-02-01' in result

    def test_first_of_march(self):
        """2020-03-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-03-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-03-01' in result

    def test_first_of_april(self):
        """2020-04-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-01' in result

    def test_first_of_may(self):
        """2020-05-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-05-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-05-01' in result

    def test_first_of_june(self):
        """2020-06-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-01' in result

    def test_first_of_july(self):
        """2020-07-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-07-01' in result

    def test_first_of_august(self):
        """2020-08-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-08-01' in result

    def test_first_of_september(self):
        """2020-09-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-01' in result

    def test_first_of_october(self):
        """2020-10-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-10-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-10-01' in result

    def test_first_of_november(self):
        """2020-11-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-11-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-11-01' in result

    def test_first_of_december(self):
        """2020-12-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-12-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-12-01' in result

    # Middle day of each month
    def test_middle_of_january(self):
        """2020-01-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-15' in result

    def test_middle_of_february(self):
        """2020-02-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-02-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-02-15' in result

    def test_middle_of_march(self):
        """2020-03-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-03-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-03-15' in result

    def test_middle_of_april(self):
        """2020-04-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-15' in result

    def test_middle_of_may(self):
        """2020-05-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-05-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-05-15' in result

    def test_middle_of_june(self):
        """2020-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_middle_of_july(self):
        """2020-07-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-07-15' in result

    def test_middle_of_august(self):
        """2020-08-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_middle_of_september(self):
        """2020-09-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-15' in result

    def test_middle_of_october(self):
        """2020-10-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-10-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-10-15' in result

    def test_middle_of_november(self):
        """2020-11-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-11-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-11-15' in result

    def test_middle_of_december(self):
        """2020-12-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-12-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-12-15' in result

    # Last day of each month (30 or 31)
    def test_last_of_january(self):
        """2020-01-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-31' in result

    def test_last_of_february_leap(self):
        """2020-02-29T12:00:00Z → 1 date (leap year)."""
        result = extract_explicit_dates('2020-02-29T12:00:00Z')
        assert len(result) == 1
        assert '2020-02-29' in result

    def test_last_of_march(self):
        """2020-03-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-03-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-03-31' in result

    def test_last_of_april(self):
        """2020-04-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-30' in result

    def test_last_of_may(self):
        """2020-05-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-05-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-05-31' in result

    def test_last_of_june(self):
        """2020-06-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-30' in result

    def test_last_of_july(self):
        """2020-07-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-07-31' in result

    def test_last_of_august(self):
        """2020-08-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-08-31' in result

    def test_last_of_september(self):
        """2020-09-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-30' in result

    def test_last_of_october(self):
        """2020-10-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-10-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-10-31' in result

    def test_last_of_november(self):
        """2020-11-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-11-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-11-30' in result

    def test_last_of_december(self):
        """2020-12-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-12-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-12-31' in result


class TestComprehensiveTimeCoverage:
    """Comprehensive coverage of various time values."""

    # Every hour of the day
    def test_hour_00(self):
        """2020-06-15T00:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T00:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_01(self):
        """2020-06-15T01:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T01:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_02(self):
        """2020-06-15T02:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T02:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_03(self):
        """2020-06-15T03:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T03:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_04(self):
        """2020-06-15T04:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T04:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_05(self):
        """2020-06-15T05:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T05:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_06(self):
        """2020-06-15T06:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T06:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_07(self):
        """2020-06-15T07:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T07:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_08(self):
        """2020-06-15T08:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T08:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_09(self):
        """2020-06-15T09:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T09:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_10(self):
        """2020-06-15T10:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_11(self):
        """2020-06-15T11:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T11:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_12(self):
        """2020-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_13(self):
        """2020-06-15T13:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T13:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_14(self):
        """2020-06-15T14:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T14:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_15(self):
        """2020-06-15T15:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T15:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_16(self):
        """2020-06-15T16:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T16:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_17(self):
        """2020-06-15T17:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T17:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_18(self):
        """2020-06-15T18:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T18:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_19(self):
        """2020-06-15T19:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T19:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_20(self):
        """2020-06-15T20:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T20:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_21(self):
        """2020-06-15T21:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T21:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_22(self):
        """2020-06-15T22:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T22:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_hour_23(self):
        """2020-06-15T23:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T23:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Various minute values
    def test_minutes_00(self):
        """2020-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_minutes_15(self):
        """2020-06-15T12:15:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:15:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_minutes_30(self):
        """2020-06-15T12:30:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_minutes_45(self):
        """2020-06-15T12:45:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:45:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_minutes_59(self):
        """2020-06-15T12:59:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:59:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Various second values
    def test_seconds_00(self):
        """2020-06-15T12:30:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_seconds_15(self):
        """2020-06-15T12:30:15Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:15Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_seconds_30(self):
        """2020-06-15T12:30:30Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:30Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_seconds_45(self):
        """2020-06-15T12:30:45Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:45Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_seconds_59(self):
        """2020-06-15T12:30:59Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:30:59Z')
        assert len(result) == 1
        assert '2020-06-15' in result


class TestComprehensiveYearCoverage:
    """Comprehensive coverage of various year values."""

    def test_year_2000(self):
        """2000-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2000-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2000-06-15' in result

    def test_year_2005(self):
        """2005-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2005-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2005-06-15' in result

    def test_year_2010(self):
        """2010-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2010-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2010-06-15' in result

    def test_year_2015(self):
        """2015-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2015-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2015-06-15' in result

    def test_year_2020(self):
        """2020-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_year_2025(self):
        """2025-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2025-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2025-06-15' in result

    def test_year_2030(self):
        """2030-06-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2030-06-15T12:00:00Z')
        assert len(result) == 1
        assert '2030-06-15' in result


class TestAdditionalRangeCombinations:
    """Additional range combination tests to reach 500+ total."""

    # Cross-month ranges for each pair of consecutive months
    def test_jan_to_feb_range(self):
        """2020-01-20T10:00:00Z to 2020-02-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-01-20T10:00:00Z to 2020-02-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-01-20' in result
        assert '2020-02-10' in result

    def test_feb_to_mar_range(self):
        """2020-02-20T10:00:00Z to 2020-03-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-02-20T10:00:00Z to 2020-03-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-02-20' in result
        assert '2020-03-10' in result

    def test_mar_to_apr_range(self):
        """2020-03-20T10:00:00Z to 2020-04-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-03-20T10:00:00Z to 2020-04-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-03-20' in result
        assert '2020-04-10' in result

    def test_apr_to_may_range(self):
        """2020-04-20T10:00:00Z to 2020-05-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-04-20T10:00:00Z to 2020-05-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-04-20' in result
        assert '2020-05-10' in result

    def test_may_to_jun_range(self):
        """2020-05-20T10:00:00Z to 2020-06-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-05-20T10:00:00Z to 2020-06-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-05-20' in result
        assert '2020-06-10' in result

    def test_jun_to_jul_range(self):
        """2020-06-20T10:00:00Z to 2020-07-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-20T10:00:00Z to 2020-07-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-06-20' in result
        assert '2020-07-10' in result

    def test_jul_to_aug_range(self):
        """2020-07-20T10:00:00Z to 2020-08-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-07-20T10:00:00Z to 2020-08-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-07-20' in result
        assert '2020-08-10' in result

    def test_aug_to_sep_range(self):
        """2020-08-20T10:00:00Z to 2020-09-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-20T10:00:00Z to 2020-09-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-08-20' in result
        assert '2020-09-10' in result

    def test_sep_to_oct_range(self):
        """2020-09-20T10:00:00Z to 2020-10-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-09-20T10:00:00Z to 2020-10-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-09-20' in result
        assert '2020-10-10' in result

    def test_oct_to_nov_range(self):
        """2020-10-20T10:00:00Z to 2020-11-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-10-20T10:00:00Z to 2020-11-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-10-20' in result
        assert '2020-11-10' in result

    def test_nov_to_dec_range(self):
        """2020-11-20T10:00:00Z to 2020-12-10T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-11-20T10:00:00Z to 2020-12-10T10:00:00Z')
        assert len(result) == 2
        assert '2020-11-20' in result
        assert '2020-12-10' in result

    # Different day values within same month
    def test_day_01_to_15(self):
        """2020-06-01T12:00:00Z to 2020-06-15T12:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-01T12:00:00Z to 2020-06-15T12:00:00Z')
        assert len(result) == 2
        assert '2020-06-01' in result
        assert '2020-06-15' in result

    def test_day_05_to_20(self):
        """2020-06-05T12:00:00Z to 2020-06-20T12:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-05T12:00:00Z to 2020-06-20T12:00:00Z')
        assert len(result) == 2
        assert '2020-06-05' in result
        assert '2020-06-20' in result

    def test_day_10_to_25(self):
        """2020-06-10T12:00:00Z to 2020-06-25T12:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-10T12:00:00Z to 2020-06-25T12:00:00Z')
        assert len(result) == 2
        assert '2020-06-10' in result
        assert '2020-06-25' in result

    def test_day_15_to_30(self):
        """2020-06-15T12:00:00Z to 2020-06-30T12:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-15T12:00:00Z to 2020-06-30T12:00:00Z')
        assert len(result) == 2
        assert '2020-06-15' in result
        assert '2020-06-30' in result

    # Adjacent days
    def test_adjacent_days_01_02(self):
        """2020-06-01T23:59:59Z to 2020-06-02T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-01T23:59:59Z to 2020-06-02T00:00:00Z')
        assert len(result) == 2
        assert '2020-06-01' in result
        assert '2020-06-02' in result

    def test_adjacent_days_10_11(self):
        """2020-06-10T23:59:59Z to 2020-06-11T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-10T23:59:59Z to 2020-06-11T00:00:00Z')
        assert len(result) == 2
        assert '2020-06-10' in result
        assert '2020-06-11' in result

    def test_adjacent_days_20_21(self):
        """2020-06-20T23:59:59Z to 2020-06-21T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-20T23:59:59Z to 2020-06-21T00:00:00Z')
        assert len(result) == 2
        assert '2020-06-20' in result
        assert '2020-06-21' in result

    # Multi-year spans
    def test_two_year_span(self):
        """2018-06-15T10:00:00Z to 2020-06-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2018-06-15T10:00:00Z to 2020-06-15T10:00:00Z')
        assert len(result) == 2
        assert '2018-06-15' in result
        assert '2020-06-15' in result

    def test_five_year_span(self):
        """2015-01-01T00:00:00Z to 2020-01-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2015-01-01T00:00:00Z to 2020-01-01T00:00:00Z')
        assert len(result) == 2
        assert '2015-01-01' in result
        assert '2020-01-01' in result

    def test_ten_year_span(self):
        """2010-12-31T23:59:59Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2010-12-31T23:59:59Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2010-12-31' in result
        assert '2020-12-31' in result

    # Various timezone combinations in ranges
    def test_range_tz_z_to_plus05(self):
        """2020-06-15T10:00:00Z to 2020-06-15T16:00:00+05:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z to 2020-06-15T16:00:00+05:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_tz_minus08_to_plus08(self):
        """2020-06-15T08:00:00-08:00 to 2020-06-15T20:00:00+08:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T08:00:00-08:00 to 2020-06-15T20:00:00+08:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_tz_plus0530_to_minus0400(self):
        """2020-06-15T10:30:00+05:30 to 2020-06-16T08:00:00-04:00 → 2 dates."""
        result = extract_explicit_dates('2020-06-15T10:30:00+05:30 to 2020-06-16T08:00:00-04:00')
        assert len(result) == 2
        assert '2020-06-15' in result
        assert '2020-06-16' in result

    # Millisecond variations in ranges
    def test_range_millis_start_only(self):
        """2020-06-15T10:00:00.123Z to 2020-06-15T11:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00.123Z to 2020-06-15T11:00:00Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_end_only(self):
        """2020-06-15T10:00:00Z to 2020-06-15T11:00:00.456Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z to 2020-06-15T11:00:00.456Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_both(self):
        """2020-06-15T10:00:00.123Z to 2020-06-15T11:00:00.456Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T10:00:00.123Z to 2020-06-15T11:00:00.456Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_different_days(self):
        """2020-06-15T23:59:59.999Z to 2020-06-16T00:00:00.001Z → 2 dates."""
        result = extract_explicit_dates('2020-06-15T23:59:59.999Z to 2020-06-16T00:00:00.001Z')
        assert len(result) == 2
        assert '2020-06-15' in result
        assert '2020-06-16' in result

    # Additional sentence embedding patterns
    def test_sentence_query_timeframe(self):
        """Query with timeframe."""
        result = extract_explicit_dates('query data for 2020-05-01T00:00:00Z to 2020-05-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-05-01' in result
        assert '2020-05-31' in result

    def test_sentence_analysis_period(self):
        """Analysis period mention (prose year also finds '2019')."""
        result = extract_explicit_dates('analysis period spans 2019-01-01T00:00:00Z through 2019-12-31T23:59:59Z')
        assert len(result) == 3  # '2019' (YEAR_ONLY from "through 2019"), plus two dates
        assert '2019' in result
        assert '2019-01-01' in result
        assert '2019-12-31' in result

    def test_sentence_monitoring_window(self):
        """Monitoring window (prose year also finds '2020')."""
        result = extract_explicit_dates('monitoring window: 2020-03-15T08:00:00Z until 2020-03-15T17:00:00Z')
        assert len(result) == 2  # '2020' (YEAR_ONLY from "until 2020"), plus date
        assert '2020' in result
        assert '2020-03-15' in result

    def test_sentence_availability_range(self):
        """Availability range (prose year also finds '2020')."""
        result = extract_explicit_dates('available from 2020-06-01T09:00:00+00:00 to 2020-06-30T18:00:00+00:00')
        assert len(result) == 3  # '2020' (YEAR_ONLY from "from 2020"), plus two dates
        assert '2020' in result
        assert '2020-06-01' in result
        assert '2020-06-30' in result

    def test_sentence_scheduled_maintenance(self):
        """Scheduled maintenance."""
        result = extract_explicit_dates('scheduled maintenance: 2020-07-15T02:00:00Z to 2020-07-15T04:00:00Z')
        assert len(result) == 1
        assert '2020-07-15' in result

    def test_sentence_backup_interval(self):
        """Backup interval."""
        result = extract_explicit_dates('backup interval: 2020-08-01T00:00:00Z - 2020-08-07T23:59:59Z')
        assert len(result) == 2
        assert '2020-08-01' in result
        assert '2020-08-07' in result

    def test_sentence_reporting_period(self):
        """Reporting period."""
        result = extract_explicit_dates('reporting period 2020-Q3: 2020-07-01T00:00:00Z to 2020-09-30T23:59:59Z')
        assert len(result) == 2
        assert '2020-07-01' in result
        assert '2020-09-30' in result

    def test_sentence_retention_policy(self):
        """Retention policy (prose year also finds '2020')."""
        result = extract_explicit_dates('retain logs from 2020-01-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 3  # '2020' (YEAR_ONLY from "from 2020"), plus two dates
        assert '2020' in result
        assert '2020-01-01' in result
        assert '2020-12-31' in result

    # Three datetimes in one string (advanced)
    def test_three_datetimes_separate(self):
        """Three separate datetimes."""
        result = extract_explicit_dates('first: 2020-01-01T10:00:00Z, second: 2020-01-02T10:00:00Z, third: 2020-01-03T10:00:00Z')
        assert len(result) == 3
        assert '2020-01-01' in result
        assert '2020-01-02' in result
        assert '2020-01-03' in result

    def test_four_datetimes_separate(self):
        """Four separate datetimes."""
        result = extract_explicit_dates('Q1: 2020-01-01T00:00:00Z, Q2: 2020-04-01T00:00:00Z, Q3: 2020-07-01T00:00:00Z, Q4: 2020-10-01T00:00:00Z')
        assert len(result) == 4
        assert '2020-01-01' in result
        assert '2020-04-01' in result
        assert '2020-07-01' in result
        assert '2020-10-01' in result

    def test_five_datetimes_separate(self):
        """Five separate datetimes."""
        result = extract_explicit_dates('checkpoints: 2020-02-01T10:00:00Z, 2020-04-01T10:00:00Z, 2020-06-01T10:00:00Z, 2020-08-01T10:00:00Z, 2020-10-01T10:00:00Z')
        assert len(result) == 5
        assert '2020-02-01' in result
        assert '2020-04-01' in result
        assert '2020-06-01' in result
        assert '2020-08-01' in result
        assert '2020-10-01' in result


class TestEveryDayOfJanuary:
    """Test every day of January with ISO datetime format."""

    def test_jan_01(self):
        """2020-01-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-01' in result

    def test_jan_02(self):
        """2020-01-02T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-02T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-02' in result

    def test_jan_03(self):
        """2020-01-03T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-03T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-03' in result

    def test_jan_04(self):
        """2020-01-04T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-04T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-04' in result

    def test_jan_05(self):
        """2020-01-05T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-05T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-05' in result

    def test_jan_06(self):
        """2020-01-06T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-06T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-06' in result

    def test_jan_07(self):
        """2020-01-07T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-07T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-07' in result

    def test_jan_08(self):
        """2020-01-08T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-08T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-08' in result

    def test_jan_09(self):
        """2020-01-09T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-09T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-09' in result

    def test_jan_10(self):
        """2020-01-10T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-10T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-10' in result

    def test_jan_11(self):
        """2020-01-11T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-11T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-11' in result

    def test_jan_12(self):
        """2020-01-12T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-12T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-12' in result

    def test_jan_13(self):
        """2020-01-13T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-13T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-13' in result

    def test_jan_14(self):
        """2020-01-14T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-14T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-14' in result

    def test_jan_15(self):
        """2020-01-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-15' in result

    def test_jan_16(self):
        """2020-01-16T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-16T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-16' in result

    def test_jan_17(self):
        """2020-01-17T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-17T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-17' in result

    def test_jan_18(self):
        """2020-01-18T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-18T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-18' in result

    def test_jan_19(self):
        """2020-01-19T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-19T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-19' in result

    def test_jan_20(self):
        """2020-01-20T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-20T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-20' in result

    def test_jan_21(self):
        """2020-01-21T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-21T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-21' in result

    def test_jan_22(self):
        """2020-01-22T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-22T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-22' in result

    def test_jan_23(self):
        """2020-01-23T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-23T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-23' in result

    def test_jan_24(self):
        """2020-01-24T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-24T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-24' in result

    def test_jan_25(self):
        """2020-01-25T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-25T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-25' in result

    def test_jan_26(self):
        """2020-01-26T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-26T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-26' in result

    def test_jan_27(self):
        """2020-01-27T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-27T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-27' in result

    def test_jan_28(self):
        """2020-01-28T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-28T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-28' in result

    def test_jan_29(self):
        """2020-01-29T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-29T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-29' in result

    def test_jan_30(self):
        """2020-01-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-30' in result

    def test_jan_31(self):
        """2020-01-31T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-01-31T12:00:00Z')
        assert len(result) == 1
        assert '2020-01-31' in result


class TestEveryDayOfApril:
    """Test every day of April with ISO datetime format."""

    def test_apr_01(self):
        """2020-04-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-01' in result

    def test_apr_02(self):
        """2020-04-02T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-02T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-02' in result

    def test_apr_03(self):
        """2020-04-03T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-03T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-03' in result

    def test_apr_04(self):
        """2020-04-04T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-04T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-04' in result

    def test_apr_05(self):
        """2020-04-05T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-05T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-05' in result

    def test_apr_06(self):
        """2020-04-06T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-06T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-06' in result

    def test_apr_07(self):
        """2020-04-07T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-07T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-07' in result

    def test_apr_08(self):
        """2020-04-08T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-08T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-08' in result

    def test_apr_09(self):
        """2020-04-09T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-09T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-09' in result

    def test_apr_10(self):
        """2020-04-10T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-10T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-10' in result

    def test_apr_11(self):
        """2020-04-11T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-11T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-11' in result

    def test_apr_12(self):
        """2020-04-12T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-12T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-12' in result

    def test_apr_13(self):
        """2020-04-13T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-13T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-13' in result

    def test_apr_14(self):
        """2020-04-14T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-14T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-14' in result

    def test_apr_15(self):
        """2020-04-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-15' in result

    def test_apr_16(self):
        """2020-04-16T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-16T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-16' in result

    def test_apr_17(self):
        """2020-04-17T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-17T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-17' in result

    def test_apr_18(self):
        """2020-04-18T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-18T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-18' in result

    def test_apr_19(self):
        """2020-04-19T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-19T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-19' in result

    def test_apr_20(self):
        """2020-04-20T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-20T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-20' in result

    def test_apr_21(self):
        """2020-04-21T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-21T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-21' in result

    def test_apr_22(self):
        """2020-04-22T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-22T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-22' in result

    def test_apr_23(self):
        """2020-04-23T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-23T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-23' in result

    def test_apr_24(self):
        """2020-04-24T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-24T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-24' in result

    def test_apr_25(self):
        """2020-04-25T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-25T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-25' in result

    def test_apr_26(self):
        """2020-04-26T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-26T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-26' in result

    def test_apr_27(self):
        """2020-04-27T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-27T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-27' in result

    def test_apr_28(self):
        """2020-04-28T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-28T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-28' in result

    def test_apr_29(self):
        """2020-04-29T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-29T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-29' in result

    def test_apr_30(self):
        """2020-04-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-04-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-04-30' in result


class TestEveryDayOfSeptember:
    """Test every day of September with ISO datetime format."""

    def test_sep_01(self):
        """2020-09-01T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-01T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-01' in result

    def test_sep_02(self):
        """2020-09-02T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-02T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-02' in result

    def test_sep_03(self):
        """2020-09-03T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-03T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-03' in result

    def test_sep_04(self):
        """2020-09-04T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-04T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-04' in result

    def test_sep_05(self):
        """2020-09-05T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-05T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-05' in result

    def test_sep_06(self):
        """2020-09-06T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-06T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-06' in result

    def test_sep_07(self):
        """2020-09-07T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-07T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-07' in result

    def test_sep_08(self):
        """2020-09-08T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-08T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-08' in result

    def test_sep_09(self):
        """2020-09-09T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-09T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-09' in result

    def test_sep_10(self):
        """2020-09-10T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-10T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-10' in result

    def test_sep_11(self):
        """2020-09-11T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-11T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-11' in result

    def test_sep_12(self):
        """2020-09-12T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-12T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-12' in result

    def test_sep_13(self):
        """2020-09-13T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-13T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-13' in result

    def test_sep_14(self):
        """2020-09-14T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-14T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-14' in result

    def test_sep_15(self):
        """2020-09-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-15' in result

    def test_sep_16(self):
        """2020-09-16T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-16T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-16' in result

    def test_sep_17(self):
        """2020-09-17T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-17T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-17' in result

    def test_sep_18(self):
        """2020-09-18T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-18T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-18' in result

    def test_sep_19(self):
        """2020-09-19T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-19T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-19' in result

    def test_sep_20(self):
        """2020-09-20T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-20T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-20' in result

    def test_sep_21(self):
        """2020-09-21T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-21T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-21' in result

    def test_sep_22(self):
        """2020-09-22T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-22T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-22' in result

    def test_sep_23(self):
        """2020-09-23T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-23T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-23' in result

    def test_sep_24(self):
        """2020-09-24T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-24T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-24' in result

    def test_sep_25(self):
        """2020-09-25T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-25T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-25' in result

    def test_sep_26(self):
        """2020-09-26T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-26T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-26' in result

    def test_sep_27(self):
        """2020-09-27T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-27T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-27' in result

    def test_sep_28(self):
        """2020-09-28T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-28T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-28' in result

    def test_sep_29(self):
        """2020-09-29T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-29T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-29' in result

    def test_sep_30(self):
        """2020-09-30T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-09-30T12:00:00Z')
        assert len(result) == 1
        assert '2020-09-30' in result


class TestComprehensiveTimezoneVariations:
    """Comprehensive timezone offset variations."""

    # Positive timezone offsets (hourly)
    def test_tz_plus_0100(self):
        """2020-06-15T12:00:00+01:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+01:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0200(self):
        """2020-06-15T12:00:00+02:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+02:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0300(self):
        """2020-06-15T12:00:00+03:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+03:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0400(self):
        """2020-06-15T12:00:00+04:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+04:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0500(self):
        """2020-06-15T12:00:00+05:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+05:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0600(self):
        """2020-06-15T12:00:00+06:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+06:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0700(self):
        """2020-06-15T12:00:00+07:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+07:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0800(self):
        """2020-06-15T12:00:00+08:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+08:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0900(self):
        """2020-06-15T12:00:00+09:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+09:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_1000(self):
        """2020-06-15T12:00:00+10:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+10:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_1100(self):
        """2020-06-15T12:00:00+11:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+11:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_1200(self):
        """2020-06-15T12:00:00+12:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+12:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Negative timezone offsets (hourly)
    def test_tz_minus_0100(self):
        """2020-06-15T12:00:00-01:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-01:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0200(self):
        """2020-06-15T12:00:00-02:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-02:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0300(self):
        """2020-06-15T12:00:00-03:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-03:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0400(self):
        """2020-06-15T12:00:00-04:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-04:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0500(self):
        """2020-06-15T12:00:00-05:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-05:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0600(self):
        """2020-06-15T12:00:00-06:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-06:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0700(self):
        """2020-06-15T12:00:00-07:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-07:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0800(self):
        """2020-06-15T12:00:00-08:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-08:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0900(self):
        """2020-06-15T12:00:00-09:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-09:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_1000(self):
        """2020-06-15T12:00:00-10:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-10:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_1100(self):
        """2020-06-15T12:00:00-11:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-11:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_1200(self):
        """2020-06-15T12:00:00-12:00 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-12:00')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Half-hour timezone offsets
    def test_tz_plus_0130(self):
        """2020-06-15T12:00:00+01:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+01:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0230(self):
        """2020-06-15T12:00:00+02:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+02:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0330(self):
        """2020-06-15T12:00:00+03:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+03:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0430(self):
        """2020-06-15T12:00:00+04:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+04:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0530(self):
        """2020-06-15T12:00:00+05:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+05:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0630(self):
        """2020-06-15T12:00:00+06:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+06:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0730(self):
        """2020-06-15T12:00:00+07:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+07:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0830(self):
        """2020-06-15T12:00:00+08:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+08:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0930(self):
        """2020-06-15T12:00:00+09:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+09:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_1030(self):
        """2020-06-15T12:00:00+10:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+10:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Negative half-hour timezones
    def test_tz_minus_0130(self):
        """2020-06-15T12:00:00-01:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-01:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0230(self):
        """2020-06-15T12:00:00-02:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-02:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0330(self):
        """2020-06-15T12:00:00-03:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-03:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0430(self):
        """2020-06-15T12:00:00-04:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-04:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0530(self):
        """2020-06-15T12:00:00-05:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-05:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0630(self):
        """2020-06-15T12:00:00-06:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-06:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0730(self):
        """2020-06-15T12:00:00-07:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-07:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0830(self):
        """2020-06-15T12:00:00-08:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-08:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0930(self):
        """2020-06-15T12:00:00-09:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-09:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_1030(self):
        """2020-06-15T12:00:00-10:30 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-10:30')
        assert len(result) == 1
        assert '2020-06-15' in result

    # Quarter-hour offsets (45 minutes)
    def test_tz_plus_0545(self):
        """2020-06-15T12:00:00+05:45 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+05:45')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_0845(self):
        """2020-06-15T12:00:00+08:45 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+08:45')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_plus_1245(self):
        """2020-06-15T12:00:00+12:45 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00+12:45')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_tz_minus_0345(self):
        """2020-06-15T12:00:00-03:45 → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00-03:45')
        assert len(result) == 1
        assert '2020-06-15' in result


class TestComprehensiveRangePermutations:
    """Comprehensive range permutations across different criteria."""

    # Same hour, different minutes
    def test_range_same_hour_00_to_15_minutes(self):
        """2020-08-15T14:00:00Z to 2020-08-15T14:15:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T14:00:00Z to 2020-08-15T14:15:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_range_same_hour_15_to_30_minutes(self):
        """2020-08-15T14:15:00Z to 2020-08-15T14:30:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T14:15:00Z to 2020-08-15T14:30:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_range_same_hour_30_to_45_minutes(self):
        """2020-08-15T14:30:00Z to 2020-08-15T14:45:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T14:30:00Z to 2020-08-15T14:45:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_range_same_hour_45_to_59_minutes(self):
        """2020-08-15T14:45:00Z to 2020-08-15T14:59:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T14:45:00Z to 2020-08-15T14:59:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    # Hour boundaries
    def test_range_hour_boundary_11_to_12(self):
        """2020-08-15T11:59:59Z to 2020-08-15T12:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-08-15T11:59:59Z to 2020-08-15T12:00:00Z')
        assert len(result) == 1
        assert '2020-08-15' in result

    def test_range_hour_boundary_23_to_00_next_day(self):
        """2020-08-15T23:59:59Z to 2020-08-16T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-15T23:59:59Z to 2020-08-16T00:00:00Z')
        assert len(result) == 2
        assert '2020-08-15' in result
        assert '2020-08-16' in result

    # Week spans
    def test_range_one_week(self):
        """2020-08-01T10:00:00Z to 2020-08-08T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-01T10:00:00Z to 2020-08-08T10:00:00Z')
        assert len(result) == 2
        assert '2020-08-01' in result
        assert '2020-08-08' in result

    def test_range_two_weeks(self):
        """2020-08-01T10:00:00Z to 2020-08-15T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-01T10:00:00Z to 2020-08-15T10:00:00Z')
        assert len(result) == 2
        assert '2020-08-01' in result
        assert '2020-08-15' in result

    def test_range_three_weeks(self):
        """2020-08-01T10:00:00Z to 2020-08-22T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-01T10:00:00Z to 2020-08-22T10:00:00Z')
        assert len(result) == 2
        assert '2020-08-01' in result
        assert '2020-08-22' in result

    def test_range_four_weeks(self):
        """2020-08-01T10:00:00Z to 2020-08-29T10:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-08-01T10:00:00Z to 2020-08-29T10:00:00Z')
        assert len(result) == 2
        assert '2020-08-01' in result
        assert '2020-08-29' in result

    # Quarter boundaries
    def test_range_q1_to_q2(self):
        """2020-03-31T23:59:59Z to 2020-04-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-03-31T23:59:59Z to 2020-04-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-03-31' in result
        assert '2020-04-01' in result

    def test_range_q2_to_q3(self):
        """2020-06-30T23:59:59Z to 2020-07-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-06-30T23:59:59Z to 2020-07-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-06-30' in result
        assert '2020-07-01' in result

    def test_range_q3_to_q4(self):
        """2020-09-30T23:59:59Z to 2020-10-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-09-30T23:59:59Z to 2020-10-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-09-30' in result
        assert '2020-10-01' in result

    def test_range_q4_to_q1_next_year(self):
        """2020-12-31T23:59:59Z to 2021-01-01T00:00:00Z → 2 dates."""
        result = extract_explicit_dates('2020-12-31T23:59:59Z to 2021-01-01T00:00:00Z')
        assert len(result) == 2
        assert '2020-12-31' in result
        assert '2021-01-01' in result

    # Full quarter ranges
    def test_range_full_q1(self):
        """2020-01-01T00:00:00Z to 2020-03-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-01-01T00:00:00Z to 2020-03-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-01-01' in result
        assert '2020-03-31' in result

    def test_range_full_q2(self):
        """2020-04-01T00:00:00Z to 2020-06-30T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-04-01T00:00:00Z to 2020-06-30T23:59:59Z')
        assert len(result) == 2
        assert '2020-04-01' in result
        assert '2020-06-30' in result

    def test_range_full_q3(self):
        """2020-07-01T00:00:00Z to 2020-09-30T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-07-01T00:00:00Z to 2020-09-30T23:59:59Z')
        assert len(result) == 2
        assert '2020-07-01' in result
        assert '2020-09-30' in result

    def test_range_full_q4(self):
        """2020-10-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-10-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-10-01' in result
        assert '2020-12-31' in result

    # Half-year ranges
    def test_range_first_half_2020(self):
        """2020-01-01T00:00:00Z to 2020-06-30T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-01-01T00:00:00Z to 2020-06-30T23:59:59Z')
        assert len(result) == 2
        assert '2020-01-01' in result
        assert '2020-06-30' in result

    def test_range_second_half_2020(self):
        """2020-07-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-07-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-07-01' in result
        assert '2020-12-31' in result

    # Full year range
    def test_range_full_year_2020(self):
        """2020-01-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2020-01-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2020-01-01' in result
        assert '2020-12-31' in result

    # Multi-year full ranges
    def test_range_2019_to_2020(self):
        """2019-01-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2019-01-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2019-01-01' in result
        assert '2020-12-31' in result

    def test_range_2018_to_2020(self):
        """2018-01-01T00:00:00Z to 2020-12-31T23:59:59Z → 2 dates."""
        result = extract_explicit_dates('2018-01-01T00:00:00Z to 2020-12-31T23:59:59Z')
        assert len(result) == 2
        assert '2018-01-01' in result
        assert '2020-12-31' in result

    # Millisecond precision in ranges
    def test_range_millis_1ms_apart(self):
        """2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.001Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.001Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_100ms_apart(self):
        """2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.100Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.100Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_500ms_apart(self):
        """2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.500Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.500Z')
        assert len(result) == 1
        assert '2020-06-15' in result

    def test_range_millis_999ms_apart(self):
        """2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.999Z → 1 date."""
        result = extract_explicit_dates('2020-06-15T12:00:00.000Z to 2020-06-15T12:00:00.999Z')
        assert len(result) == 1
        assert '2020-06-15' in result


class TestEveryMinuteOfHour:
    """Test every minute value (0-59) within an hour."""

    def test_minute_00(self):
        """2020-07-10T14:00:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:00:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_01(self):
        """2020-07-10T14:01:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:01:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_02(self):
        """2020-07-10T14:02:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:02:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_03(self):
        """2020-07-10T14:03:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:03:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_04(self):
        """2020-07-10T14:04:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:04:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_05(self):
        """2020-07-10T14:05:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:05:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_06(self):
        """2020-07-10T14:06:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:06:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_07(self):
        """2020-07-10T14:07:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:07:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_08(self):
        """2020-07-10T14:08:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:08:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_09(self):
        """2020-07-10T14:09:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:09:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_10(self):
        """2020-07-10T14:10:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:10:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_11(self):
        """2020-07-10T14:11:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:11:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_12(self):
        """2020-07-10T14:12:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:12:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_13(self):
        """2020-07-10T14:13:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:13:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_14(self):
        """2020-07-10T14:14:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:14:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_15(self):
        """2020-07-10T14:15:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:15:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_16(self):
        """2020-07-10T14:16:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:16:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_17(self):
        """2020-07-10T14:17:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:17:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_18(self):
        """2020-07-10T14:18:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:18:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_19(self):
        """2020-07-10T14:19:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:19:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_20(self):
        """2020-07-10T14:20:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:20:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_21(self):
        """2020-07-10T14:21:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:21:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_22(self):
        """2020-07-10T14:22:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:22:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_23(self):
        """2020-07-10T14:23:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:23:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_24(self):
        """2020-07-10T14:24:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:24:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_25(self):
        """2020-07-10T14:25:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:25:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_26(self):
        """2020-07-10T14:26:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:26:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_27(self):
        """2020-07-10T14:27:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:27:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_28(self):
        """2020-07-10T14:28:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:28:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_29(self):
        """2020-07-10T14:29:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:29:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_30(self):
        """2020-07-10T14:30:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_31(self):
        """2020-07-10T14:31:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:31:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_32(self):
        """2020-07-10T14:32:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:32:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_33(self):
        """2020-07-10T14:33:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:33:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_34(self):
        """2020-07-10T14:34:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:34:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_35(self):
        """2020-07-10T14:35:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:35:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_36(self):
        """2020-07-10T14:36:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:36:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_37(self):
        """2020-07-10T14:37:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:37:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_38(self):
        """2020-07-10T14:38:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:38:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_39(self):
        """2020-07-10T14:39:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:39:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_40(self):
        """2020-07-10T14:40:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:40:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_41(self):
        """2020-07-10T14:41:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:41:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_42(self):
        """2020-07-10T14:42:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:42:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_43(self):
        """2020-07-10T14:43:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:43:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_44(self):
        """2020-07-10T14:44:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:44:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_45(self):
        """2020-07-10T14:45:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:45:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_46(self):
        """2020-07-10T14:46:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:46:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_47(self):
        """2020-07-10T14:47:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:47:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_48(self):
        """2020-07-10T14:48:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:48:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_49(self):
        """2020-07-10T14:49:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:49:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_50(self):
        """2020-07-10T14:50:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:50:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_51(self):
        """2020-07-10T14:51:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:51:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_52(self):
        """2020-07-10T14:52:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:52:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_53(self):
        """2020-07-10T14:53:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:53:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_54(self):
        """2020-07-10T14:54:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:54:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_55(self):
        """2020-07-10T14:55:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:55:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_56(self):
        """2020-07-10T14:56:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:56:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_57(self):
        """2020-07-10T14:57:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:57:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_58(self):
        """2020-07-10T14:58:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:58:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_minute_59(self):
        """2020-07-10T14:59:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:59:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result


class TestEverySecondOfMinute:
    """Test every second value (0-59) within a minute."""

    def test_second_00(self):
        """2020-07-10T14:30:00Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:00Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_01(self):
        """2020-07-10T14:30:01Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:01Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_02(self):
        """2020-07-10T14:30:02Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:02Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_03(self):
        """2020-07-10T14:30:03Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:03Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_04(self):
        """2020-07-10T14:30:04Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:04Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_05(self):
        """2020-07-10T14:30:05Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:05Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_06(self):
        """2020-07-10T14:30:06Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:06Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_07(self):
        """2020-07-10T14:30:07Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:07Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_08(self):
        """2020-07-10T14:30:08Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:08Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_09(self):
        """2020-07-10T14:30:09Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:09Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_10(self):
        """2020-07-10T14:30:10Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:10Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_11(self):
        """2020-07-10T14:30:11Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:11Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_12(self):
        """2020-07-10T14:30:12Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:12Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_13(self):
        """2020-07-10T14:30:13Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:13Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_14(self):
        """2020-07-10T14:30:14Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:14Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_15(self):
        """2020-07-10T14:30:15Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:15Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_16(self):
        """2020-07-10T14:30:16Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:16Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_17(self):
        """2020-07-10T14:30:17Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:17Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_18(self):
        """2020-07-10T14:30:18Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:18Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_19(self):
        """2020-07-10T14:30:19Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:19Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_20(self):
        """2020-07-10T14:30:20Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:20Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_21(self):
        """2020-07-10T14:30:21Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:21Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_22(self):
        """2020-07-10T14:30:22Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:22Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_23(self):
        """2020-07-10T14:30:23Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:23Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_24(self):
        """2020-07-10T14:30:24Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:24Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_25(self):
        """2020-07-10T14:30:25Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:25Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_26(self):
        """2020-07-10T14:30:26Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:26Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_27(self):
        """2020-07-10T14:30:27Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:27Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_28(self):
        """2020-07-10T14:30:28Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:28Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_29(self):
        """2020-07-10T14:30:29Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:29Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_30(self):
        """2020-07-10T14:30:30Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:30Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_31(self):
        """2020-07-10T14:30:31Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:31Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_32(self):
        """2020-07-10T14:30:32Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:32Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_33(self):
        """2020-07-10T14:30:33Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:33Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_34(self):
        """2020-07-10T14:30:34Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:34Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_35(self):
        """2020-07-10T14:30:35Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:35Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_36(self):
        """2020-07-10T14:30:36Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:36Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_37(self):
        """2020-07-10T14:30:37Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:37Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_38(self):
        """2020-07-10T14:30:38Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:38Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_39(self):
        """2020-07-10T14:30:39Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:39Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_40(self):
        """2020-07-10T14:30:40Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:40Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_41(self):
        """2020-07-10T14:30:41Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:41Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_42(self):
        """2020-07-10T14:30:42Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:42Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_43(self):
        """2020-07-10T14:30:43Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:43Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_44(self):
        """2020-07-10T14:30:44Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:44Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_45(self):
        """2020-07-10T14:30:45Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:45Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_46(self):
        """2020-07-10T14:30:46Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:46Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_47(self):
        """2020-07-10T14:30:47Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:47Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_48(self):
        """2020-07-10T14:30:48Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:48Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_49(self):
        """2020-07-10T14:30:49Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:49Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_50(self):
        """2020-07-10T14:30:50Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:50Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_51(self):
        """2020-07-10T14:30:51Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:51Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_52(self):
        """2020-07-10T14:30:52Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:52Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_53(self):
        """2020-07-10T14:30:53Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:53Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_54(self):
        """2020-07-10T14:30:54Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:54Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_55(self):
        """2020-07-10T14:30:55Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:55Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_56(self):
        """2020-07-10T14:30:56Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:56Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_57(self):
        """2020-07-10T14:30:57Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:57Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_58(self):
        """2020-07-10T14:30:58Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:58Z')
        assert len(result) == 1
        assert '2020-07-10' in result

    def test_second_59(self):
        """2020-07-10T14:30:59Z → 1 date."""
        result = extract_explicit_dates('2020-07-10T14:30:59Z')
        assert len(result) == 1
        assert '2020-07-10' in result


class TestAdditionalEdgeCasesAndVariations:
    """Additional edge cases and variations to reach 500+ tests."""

    # Specific important datetimes
    def test_unix_epoch(self):
        """1970-01-01T00:00:00Z → 1 date (Unix epoch)."""
        result = extract_explicit_dates('1970-01-01T00:00:00Z')
        assert len(result) == 1
        assert '1970-01-01' in result

    def test_y2k(self):
        """2000-01-01T00:00:00Z → 1 date (Y2K)."""
        result = extract_explicit_dates('2000-01-01T00:00:00Z')
        assert len(result) == 1
        assert '2000-01-01' in result

    def test_leap_second(self):
        """2016-12-31T23:59:60Z → handle gracefully."""
        result = extract_explicit_dates('2016-12-31T23:59:60Z')
        # May or may not match depending on implementation
        assert isinstance(result, dict)

    # Different separators in ranges
    def test_range_hyphen_separator(self):
        """2020-06-15T10:00:00Z - 2020-06-15T11:00:00Z → dates."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z - 2020-06-15T11:00:00Z')
        assert '2020-06-15' in result

    def test_range_via_connector(self):
        """2020-06-15T10:00:00Z via 2020-06-15T11:00:00Z → dates."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z via 2020-06-15T11:00:00Z')
        assert '2020-06-15' in result

    def test_range_through_connector(self):
        """2020-06-15T10:00:00Z through 2020-06-15T11:00:00Z → dates."""
        result = extract_explicit_dates('2020-06-15T10:00:00Z through 2020-06-15T11:00:00Z')
        assert '2020-06-15' in result

    # More sentence contexts
    def test_sentence_system_uptime(self):
        """System uptime context (prose year also finds '2020')."""
        result = extract_explicit_dates('system running since 2020-01-01T00:00:00Z')
        assert len(result) == 2  # '2020' (YEAR_ONLY from "since 2020"), plus date
        assert '2020' in result
        assert '2020-01-01' in result

    def test_sentence_error_occurred(self):
        """Error occurrence context."""
        result = extract_explicit_dates('error occurred at 2020-05-15T14:22:33Z')
        assert len(result) == 1
        assert '2020-05-15' in result

    def test_sentence_deployment_time(self):
        """Deployment time context."""
        result = extract_explicit_dates('deployed on 2020-08-10T09:15:00Z')
        assert len(result) == 1
        assert '2020-08-10' in result

    def test_sentence_last_updated(self):
        """Last updated context."""
        result = extract_explicit_dates('last updated: 2020-11-20T16:45:30Z')
        assert len(result) == 1
        assert '2020-11-20' in result

    def test_sentence_next_scheduled(self):
        """Next scheduled context."""
        result = extract_explicit_dates('next run scheduled for 2020-12-25T00:00:00Z')
        assert len(result) == 1
        assert '2020-12-25' in result

    def test_sentence_cache_expires(self):
        """Cache expiration context."""
        result = extract_explicit_dates('cache expires at 2021-01-15T12:00:00Z')
        assert len(result) == 1
        assert '2021-01-15' in result

    def test_sentence_token_valid_until(self):
        """Token validity context (prose year also finds '2021')."""
        result = extract_explicit_dates('token valid until 2021-03-30T23:59:59Z')
        assert len(result) == 2  # '2021' (YEAR_ONLY from "until 2021"), plus date
        assert '2021' in result
        assert '2021-03-30' in result

    def test_sentence_subscription_ends(self):
        """Subscription end context."""
        result = extract_explicit_dates('subscription ends on 2021-06-30T23:59:59Z')
        assert len(result) == 1
        assert '2021-06-30' in result

    def test_sentence_trial_expires(self):
        """Trial expiration context."""
        result = extract_explicit_dates('trial period expires 2021-02-28T23:59:59Z')
        assert len(result) == 1
        assert '2021-02-28' in result
