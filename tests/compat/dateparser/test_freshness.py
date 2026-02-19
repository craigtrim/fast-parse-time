# -*- coding: utf-8 -*-
"""
Test freshness / relative time parsing.
Source: https://github.com/scrapinghub/dateparser/blob/master/tests/test_freshness_date_parser.py
English-language cases only.
"""
import pytest
from fast_parse_time import parse_time_references

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestYesterdayAndToday:
    """Source: test_freshness_date_parser -- basic anchors"""

    def test_yesterday(self):
        result = parse_time_references('yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_today(self):
        result = parse_time_references('today')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'

    def test_the_day_before_yesterday(self):
        """dateparser resolves 'the day before yesterday' to 2 days ago."""
        result = parse_time_references('the day before yesterday')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_till_date(self):
        """'till date' is an idiom for 'up to today' -- treated as present."""
        result = parse_time_references('till date')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].frame == 'day'
        assert result[0].tense == 'present'

    def test_just_now(self):
        """'just now' is a present-moment anchor."""
        result = parse_time_references('just now')
        assert len(result) == 1
        assert result[0].cardinality == 0
        assert result[0].tense == 'present'


class TestHoursAgo:
    """Source: test_freshness_date_parser -- hour-based past offsets"""

    def test_an_hour_ago(self):
        result = parse_time_references('an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_an_hour_ago(self):
        """dateparser supports hedged expressions like 'about an hour ago'."""
        result = parse_time_references('about an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_2_hours_ago(self):
        result = parse_time_references('2 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_about_23_hours_ago(self):
        """Hedged expression with large cardinality."""
        result = parse_time_references('about 23 hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 23
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_nine_hours_ago(self):
        """Word-number cardinality."""
        result = parse_time_references('nine hours ago')
        assert len(result) == 1
        assert result[0].cardinality == 9
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hr(self):
        """Abbreviated unit 'hr' without explicit 'ago' -- dateparser defaults to past."""
        result = parse_time_references('15 hr')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_15_hrs(self):
        """Abbreviated unit 'hrs'."""
        result = parse_time_references('15 hrs')
        assert len(result) == 1
        assert result[0].cardinality == 15
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'


class TestDaysAgo:
    """Source: test_freshness_date_parser -- day-based past offsets"""

    def test_a_day_ago(self):
        result = parse_time_references('a day ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_1d_ago(self):
        """Letter-abbreviated unit: '1d ago'."""
        result = parse_time_references('1d ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_4_days_before(self):
        """'N days before' without 'now' -- dateparser treats as past."""
        result = parse_time_references('4 days before')
        assert len(result) == 1
        assert result[0].cardinality == 4
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'

    def test_six_days_ago(self):
        """Word-number cardinality."""
        result = parse_time_references('six days ago')
        assert len(result) == 1
        assert result[0].cardinality == 6
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestWeeksAgo:
    """Source: test_freshness_date_parser -- week-based past offsets"""

    def test_a_week_ago(self):
        result = parse_time_references('a week ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'

    def test_three_week_ago(self):
        """Word-number + singular 'week' (not 'weeks')."""
        result = parse_time_references('three week ago')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'week'
        assert result[0].tense == 'past'


class TestMinutesAndSeconds:
    """Source: test_freshness_date_parser -- minutes and seconds"""

    def test_2_min(self):
        """Abbreviated unit 'min' without 'ago'."""
        result = parse_time_references('2 min')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_2_mins(self):
        """Abbreviated unit 'mins'."""
        result = parse_time_references('2 mins')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_3_sec(self):
        """Abbreviated unit 'sec'."""
        result = parse_time_references('3 sec')
        assert len(result) == 1
        assert result[0].cardinality == 3
        assert result[0].frame == 'second'
        assert result[0].tense == 'past'


class TestMonthsAndYears:
    """Source: test_freshness_date_parser -- month and year offsets"""

    def test_eight_months_ago(self):
        """Word-number cardinality."""
        result = parse_time_references('eight months ago')
        assert len(result) == 1
        assert result[0].cardinality == 8
        assert result[0].frame == 'month'
        assert result[0].tense == 'past'

    def test_five_years_ago(self):
        """Word-number cardinality."""
        result = parse_time_references('five years ago')
        assert len(result) == 1
        assert result[0].cardinality == 5
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_2y_ago(self):
        """Letter-abbreviated unit: '2y ago'."""
        result = parse_time_references('2y ago')
        assert len(result) == 1
        assert result[0].cardinality == 2
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1000_years_ago(self):
        """Very large cardinality."""
        result = parse_time_references('1000 years ago')
        assert len(result) == 1
        assert result[0].cardinality == 1000
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestDecades:
    """
    Source: test_freshness_date_parser -- decade expressions.
    dateparser resolves 'decade' as 10 years.
    """

    def test_a_decade_ago(self):
        result = parse_time_references('a decade ago')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_last_decade(self):
        result = parse_time_references('last decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'

    def test_1_decade(self):
        """'1 decade' without 'ago' -- dateparser defaults to past."""
        result = parse_time_references('1 decade')
        assert len(result) == 1
        assert result[0].cardinality == 10
        assert result[0].frame == 'year'
        assert result[0].tense == 'past'


class TestFloatCardinalities:
    """
    Source: test_freshness_date_parser -- fractional time expressions.
    dateparser supports '2.5 hours', '10.75 minutes', '1.5 days'.
    """

    def test_2_point_5_hours(self):
        result = parse_time_references('2.5 hours')
        assert len(result) == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'

    def test_10_point_75_minutes(self):
        result = parse_time_references('10.75 minutes')
        assert len(result) == 1
        assert result[0].frame == 'minute'
        assert result[0].tense == 'past'

    def test_1_point_5_days(self):
        result = parse_time_references('1.5 days')
        assert len(result) == 1
        assert result[0].frame == 'day'
        assert result[0].tense == 'past'


class TestCompoundExpressions:
    """
    Source: test_freshness_date_parser -- multi-unit compound expressions.
    dateparser parses '1 year 2 months' as a compound offset.
    fast-parse-time handles one unit per expression; these test compound support.
    """

    def test_1_year_2_months(self):
        """'1 year 2 months' -- compound past offset."""
        result = parse_time_references('1 year 2 months')
        assert len(result) >= 1

    def test_1_year_1_month_1_week_1_day_1_hour_and_1_minute_ago(self):
        """Full compound expression from dateparser test suite."""
        result = parse_time_references(
            '1 year, 1 month, 1 week, 1 day, 1 hour and 1 minute ago'
        )
        assert len(result) >= 1
