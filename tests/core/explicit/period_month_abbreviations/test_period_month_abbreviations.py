#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for period-suffixed month abbreviations (Aug., Dec., etc.)

This test suite verifies recognition of abbreviated month names with trailing
periods, which is standard American newspaper/AP style. All tests should FAIL
before implementation, then pass after the regex update.

Issue: https://github.com/craigtrim/fast-parse-time/issues/60
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestJanPeriodFormats:
    """Test all format variations for 'Jan.'"""

    def test_jan_period_d_comma_yyyy(self):
        """'Jan. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Jan. 9, 2012')
        assert len(result) == 1

    def test_jan_period_dd_comma_yyyy(self):
        """'Jan. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Jan. 09, 2012')
        assert len(result) == 1

    def test_jan_period_d_space_yyyy(self):
        """'Jan. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Jan. 9 2012')
        assert len(result) == 1

    def test_d_jan_period_yyyy(self):
        """'9 Jan. 2012' should be parsed."""
        result = extract_explicit_dates('9 Jan. 2012')
        assert len(result) == 1

    def test_dd_jan_period_yyyy(self):
        """'09 Jan. 2012' should be parsed."""
        result = extract_explicit_dates('09 Jan. 2012')
        assert len(result) == 1

    def test_jan_period_1st_comma_yyyy(self):
        """'Jan. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jan. 1st, 2012')
        assert len(result) == 1

    def test_jan_period_2nd_comma_yyyy(self):
        """'Jan. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jan. 2nd, 2012')
        assert len(result) == 1

    def test_jan_period_3rd_comma_yyyy(self):
        """'Jan. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jan. 3rd, 2012')
        assert len(result) == 1

    def test_jan_period_9th_comma_yyyy(self):
        """'Jan. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jan. 9th, 2012')
        assert len(result) == 1

    def test_jan_period_with_time_suffix(self):
        """'Jan. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Jan. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_jan_period_with_time_suffix_am(self):
        """'Jan. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Jan. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_jan_period(self):
        """'8:25 a.m. Jan. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Jan. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_jan_period_variant(self):
        """'10:06am Jan. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Jan. 11, 2014')
        assert len(result) == 1

    def test_jan_period_in_sentence(self):
        """'filed on Jan. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Jan. 9, 2012 for review')
        assert len(result) == 1

    def test_jan_period_at_start(self):
        """'Jan. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Jan. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_jan_period_at_end(self):
        """'The event occurred on Jan. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Jan. 20, 2012')
        assert len(result) == 1

    def test_jan_period_lowercase(self):
        """'jan. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('jan. 9, 2012')
        assert len(result) == 1

    def test_jan_period_uppercase(self):
        """'JAN. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('JAN. 9, 2012')
        assert len(result) == 1

    def test_jan_period_day_31(self):
        """'Jan. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jan. 31, 2012')
        assert len(result) == 1

    def test_jan_period_day_1(self):
        """'Jan. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jan. 1, 2012')
        assert len(result) == 1


class TestFebPeriodFormats:
    """Test all format variations for 'Feb.'"""

    def test_feb_period_d_comma_yyyy(self):
        """'Feb. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Feb. 9, 2012')
        assert len(result) == 1

    def test_feb_period_dd_comma_yyyy(self):
        """'Feb. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Feb. 09, 2012')
        assert len(result) == 1

    def test_feb_period_d_space_yyyy(self):
        """'Feb. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Feb. 9 2012')
        assert len(result) == 1

    def test_d_feb_period_yyyy(self):
        """'9 Feb. 2012' should be parsed."""
        result = extract_explicit_dates('9 Feb. 2012')
        assert len(result) == 1

    def test_dd_feb_period_yyyy(self):
        """'09 Feb. 2012' should be parsed."""
        result = extract_explicit_dates('09 Feb. 2012')
        assert len(result) == 1

    def test_feb_period_1st_comma_yyyy(self):
        """'Feb. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Feb. 1st, 2012')
        assert len(result) == 1

    def test_feb_period_2nd_comma_yyyy(self):
        """'Feb. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Feb. 2nd, 2012')
        assert len(result) == 1

    def test_feb_period_3rd_comma_yyyy(self):
        """'Feb. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Feb. 3rd, 2012')
        assert len(result) == 1

    def test_feb_period_9th_comma_yyyy(self):
        """'Feb. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Feb. 9th, 2012')
        assert len(result) == 1

    def test_feb_period_with_time_suffix(self):
        """'Feb. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Feb. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_feb_period_with_time_suffix_am(self):
        """'Feb. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Feb. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_feb_period(self):
        """'8:25 a.m. Feb. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Feb. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_feb_period_variant(self):
        """'10:06am Feb. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Feb. 11, 2014')
        assert len(result) == 1

    def test_feb_period_in_sentence(self):
        """'filed on Feb. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Feb. 9, 2012 for review')
        assert len(result) == 1

    def test_feb_period_at_start(self):
        """'Feb. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Feb. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_feb_period_at_end(self):
        """'The event occurred on Feb. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Feb. 20, 2012')
        assert len(result) == 1

    def test_feb_period_lowercase(self):
        """'feb. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('feb. 9, 2012')
        assert len(result) == 1

    def test_feb_period_uppercase(self):
        """'FEB. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('FEB. 9, 2012')
        assert len(result) == 1

    def test_feb_period_day_28(self):
        """'Feb. 28, 2012' should be parsed."""
        result = extract_explicit_dates('Feb. 28, 2012')
        assert len(result) == 1

    def test_feb_period_day_29_leap(self):
        """'Feb. 29, 2012' should be parsed (leap year)."""
        result = extract_explicit_dates('Feb. 29, 2012')
        assert len(result) == 1


class TestMarPeriodFormats:
    """Test all format variations for 'Mar.'"""

    def test_mar_period_d_comma_yyyy(self):
        """'Mar. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Mar. 9, 2012')
        assert len(result) == 1

    def test_mar_period_dd_comma_yyyy(self):
        """'Mar. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Mar. 09, 2012')
        assert len(result) == 1

    def test_mar_period_d_space_yyyy(self):
        """'Mar. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Mar. 9 2012')
        assert len(result) == 1

    def test_d_mar_period_yyyy(self):
        """'9 Mar. 2012' should be parsed."""
        result = extract_explicit_dates('9 Mar. 2012')
        assert len(result) == 1

    def test_dd_mar_period_yyyy(self):
        """'09 Mar. 2012' should be parsed."""
        result = extract_explicit_dates('09 Mar. 2012')
        assert len(result) == 1

    def test_mar_period_1st_comma_yyyy(self):
        """'Mar. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Mar. 1st, 2012')
        assert len(result) == 1

    def test_mar_period_2nd_comma_yyyy(self):
        """'Mar. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Mar. 2nd, 2012')
        assert len(result) == 1

    def test_mar_period_3rd_comma_yyyy(self):
        """'Mar. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Mar. 3rd, 2012')
        assert len(result) == 1

    def test_mar_period_9th_comma_yyyy(self):
        """'Mar. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Mar. 9th, 2012')
        assert len(result) == 1

    def test_mar_period_with_time_suffix(self):
        """'Mar. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Mar. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_mar_period_with_time_suffix_am(self):
        """'Mar. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Mar. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_mar_period(self):
        """'8:25 a.m. Mar. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Mar. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_mar_period_variant(self):
        """'10:06am Mar. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Mar. 11, 2014')
        assert len(result) == 1

    def test_mar_period_in_sentence(self):
        """'filed on Mar. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Mar. 9, 2012 for review')
        assert len(result) == 1

    def test_mar_period_at_start(self):
        """'Mar. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Mar. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_mar_period_at_end(self):
        """'The event occurred on Mar. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Mar. 20, 2012')
        assert len(result) == 1

    def test_mar_period_lowercase(self):
        """'mar. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('mar. 9, 2012')
        assert len(result) == 1

    def test_mar_period_uppercase(self):
        """'MAR. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('MAR. 9, 2012')
        assert len(result) == 1

    def test_mar_period_day_31(self):
        """'Mar. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Mar. 31, 2012')
        assert len(result) == 1

    def test_mar_period_day_1(self):
        """'Mar. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Mar. 1, 2012')
        assert len(result) == 1


class TestAprPeriodFormats:
    """Test all format variations for 'Apr.'"""

    def test_apr_period_d_comma_yyyy(self):
        """'Apr. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Apr. 9, 2012')
        assert len(result) == 1

    def test_apr_period_dd_comma_yyyy(self):
        """'Apr. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Apr. 09, 2012')
        assert len(result) == 1

    def test_apr_period_d_space_yyyy(self):
        """'Apr. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Apr. 9 2012')
        assert len(result) == 1

    def test_d_apr_period_yyyy(self):
        """'9 Apr. 2012' should be parsed."""
        result = extract_explicit_dates('9 Apr. 2012')
        assert len(result) == 1

    def test_dd_apr_period_yyyy(self):
        """'09 Apr. 2012' should be parsed."""
        result = extract_explicit_dates('09 Apr. 2012')
        assert len(result) == 1

    def test_apr_period_1st_comma_yyyy(self):
        """'Apr. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Apr. 1st, 2012')
        assert len(result) == 1

    def test_apr_period_2nd_comma_yyyy(self):
        """'Apr. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Apr. 2nd, 2012')
        assert len(result) == 1

    def test_apr_period_3rd_comma_yyyy(self):
        """'Apr. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Apr. 3rd, 2012')
        assert len(result) == 1

    def test_apr_period_9th_comma_yyyy(self):
        """'Apr. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Apr. 9th, 2012')
        assert len(result) == 1

    def test_apr_period_with_time_suffix(self):
        """'Apr. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Apr. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_apr_period_with_time_suffix_am(self):
        """'Apr. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Apr. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_apr_period(self):
        """'8:25 a.m. Apr. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Apr. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_apr_period_variant(self):
        """'10:06am Apr. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Apr. 11, 2014')
        assert len(result) == 1

    def test_apr_period_in_sentence(self):
        """'filed on Apr. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Apr. 9, 2012 for review')
        assert len(result) == 1

    def test_apr_period_at_start(self):
        """'Apr. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Apr. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_apr_period_at_end(self):
        """'The event occurred on Apr. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Apr. 20, 2012')
        assert len(result) == 1

    def test_apr_period_lowercase(self):
        """'apr. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('apr. 9, 2012')
        assert len(result) == 1

    def test_apr_period_uppercase(self):
        """'APR. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('APR. 9, 2012')
        assert len(result) == 1

    def test_apr_period_day_30(self):
        """'Apr. 30, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Apr. 30, 2012')
        assert len(result) == 1

    def test_apr_period_day_1(self):
        """'Apr. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Apr. 1, 2012')
        assert len(result) == 1


class TestJunPeriodFormats:
    """Test all format variations for 'Jun.'"""

    def test_jun_period_d_comma_yyyy(self):
        """'Jun. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Jun. 9, 2012')
        assert len(result) == 1

    def test_jun_period_dd_comma_yyyy(self):
        """'Jun. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Jun. 09, 2012')
        assert len(result) == 1

    def test_jun_period_d_space_yyyy(self):
        """'Jun. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Jun. 9 2012')
        assert len(result) == 1

    def test_d_jun_period_yyyy(self):
        """'9 Jun. 2012' should be parsed."""
        result = extract_explicit_dates('9 Jun. 2012')
        assert len(result) == 1

    def test_dd_jun_period_yyyy(self):
        """'09 Jun. 2012' should be parsed."""
        result = extract_explicit_dates('09 Jun. 2012')
        assert len(result) == 1

    def test_jun_period_1st_comma_yyyy(self):
        """'Jun. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jun. 1st, 2012')
        assert len(result) == 1

    def test_jun_period_2nd_comma_yyyy(self):
        """'Jun. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jun. 2nd, 2012')
        assert len(result) == 1

    def test_jun_period_3rd_comma_yyyy(self):
        """'Jun. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jun. 3rd, 2012')
        assert len(result) == 1

    def test_jun_period_9th_comma_yyyy(self):
        """'Jun. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jun. 9th, 2012')
        assert len(result) == 1

    def test_jun_period_with_time_suffix(self):
        """'Jun. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Jun. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_jun_period_with_time_suffix_am(self):
        """'Jun. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Jun. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_jun_period(self):
        """'8:25 a.m. Jun. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Jun. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_jun_period_variant(self):
        """'10:06am Jun. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Jun. 11, 2014')
        assert len(result) == 1

    def test_jun_period_in_sentence(self):
        """'filed on Jun. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Jun. 9, 2012 for review')
        assert len(result) == 1

    def test_jun_period_at_start(self):
        """'Jun. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Jun. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_jun_period_at_end(self):
        """'The event occurred on Jun. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Jun. 20, 2012')
        assert len(result) == 1

    def test_jun_period_lowercase(self):
        """'jun. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('jun. 9, 2012')
        assert len(result) == 1

    def test_jun_period_uppercase(self):
        """'JUN. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('JUN. 9, 2012')
        assert len(result) == 1

    def test_jun_period_day_30(self):
        """'Jun. 30, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jun. 30, 2012')
        assert len(result) == 1

    def test_jun_period_day_1(self):
        """'Jun. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jun. 1, 2012')
        assert len(result) == 1


class TestJulPeriodFormats:
    """Test all format variations for 'Jul.'"""

    def test_jul_period_d_comma_yyyy(self):
        """'Jul. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Jul. 9, 2012')
        assert len(result) == 1

    def test_jul_period_dd_comma_yyyy(self):
        """'Jul. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Jul. 09, 2012')
        assert len(result) == 1

    def test_jul_period_d_space_yyyy(self):
        """'Jul. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Jul. 9 2012')
        assert len(result) == 1

    def test_d_jul_period_yyyy(self):
        """'9 Jul. 2012' should be parsed."""
        result = extract_explicit_dates('9 Jul. 2012')
        assert len(result) == 1

    def test_dd_jul_period_yyyy(self):
        """'09 Jul. 2012' should be parsed."""
        result = extract_explicit_dates('09 Jul. 2012')
        assert len(result) == 1

    def test_jul_period_1st_comma_yyyy(self):
        """'Jul. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jul. 1st, 2012')
        assert len(result) == 1

    def test_jul_period_2nd_comma_yyyy(self):
        """'Jul. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jul. 2nd, 2012')
        assert len(result) == 1

    def test_jul_period_3rd_comma_yyyy(self):
        """'Jul. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jul. 3rd, 2012')
        assert len(result) == 1

    def test_jul_period_9th_comma_yyyy(self):
        """'Jul. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jul. 9th, 2012')
        assert len(result) == 1

    def test_jul_period_with_time_suffix(self):
        """'Jul. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Jul. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_jul_period_with_time_suffix_am(self):
        """'Jul. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Jul. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_jul_period(self):
        """'8:25 a.m. Jul. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Jul. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_jul_period_variant(self):
        """'10:06am Jul. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Jul. 11, 2014')
        assert len(result) == 1

    def test_jul_period_in_sentence(self):
        """'filed on Jul. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Jul. 9, 2012 for review')
        assert len(result) == 1

    def test_jul_period_at_start(self):
        """'Jul. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Jul. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_jul_period_at_end(self):
        """'The event occurred on Jul. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Jul. 20, 2012')
        assert len(result) == 1

    def test_jul_period_lowercase(self):
        """'jul. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('jul. 9, 2012')
        assert len(result) == 1

    def test_jul_period_uppercase(self):
        """'JUL. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('JUL. 9, 2012')
        assert len(result) == 1

    def test_jul_period_day_31(self):
        """'Jul. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jul. 31, 2012')
        assert len(result) == 1

    def test_jul_period_day_1(self):
        """'Jul. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Jul. 1, 2012')
        assert len(result) == 1


class TestAugPeriodFormats:
    """Test all format variations for 'Aug.'"""

    def test_aug_period_d_comma_yyyy(self):
        """'Aug. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Aug. 9, 2012')
        assert len(result) == 1

    def test_aug_period_dd_comma_yyyy(self):
        """'Aug. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Aug. 09, 2012')
        assert len(result) == 1

    def test_aug_period_d_space_yyyy(self):
        """'Aug. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Aug. 9 2012')
        assert len(result) == 1

    def test_d_aug_period_yyyy(self):
        """'9 Aug. 2012' should be parsed."""
        result = extract_explicit_dates('9 Aug. 2012')
        assert len(result) == 1

    def test_dd_aug_period_yyyy(self):
        """'09 Aug. 2012' should be parsed."""
        result = extract_explicit_dates('09 Aug. 2012')
        assert len(result) == 1

    def test_aug_period_1st_comma_yyyy(self):
        """'Aug. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Aug. 1st, 2012')
        assert len(result) == 1

    def test_aug_period_2nd_comma_yyyy(self):
        """'Aug. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Aug. 2nd, 2012')
        assert len(result) == 1

    def test_aug_period_3rd_comma_yyyy(self):
        """'Aug. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Aug. 3rd, 2012')
        assert len(result) == 1

    def test_aug_period_9th_comma_yyyy(self):
        """'Aug. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Aug. 9th, 2012')
        assert len(result) == 1

    def test_aug_period_with_time_suffix(self):
        """'Aug. 9, 2012 at 2:57 p.m.' should be parsed (from issue example)."""
        result = extract_explicit_dates('Aug. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_aug_period_with_time_suffix_am(self):
        """'Aug. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Aug. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_aug_period(self):
        """'8:25 a.m. Aug. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Aug. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_aug_period_variant(self):
        """'10:06am Aug. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Aug. 11, 2014')
        assert len(result) == 1

    def test_aug_period_in_sentence(self):
        """'filed on Aug. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Aug. 9, 2012 for review')
        assert len(result) == 1

    def test_aug_period_at_start(self):
        """'Aug. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Aug. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_aug_period_at_end(self):
        """'The event occurred on Aug. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Aug. 20, 2012')
        assert len(result) == 1

    def test_aug_period_lowercase(self):
        """'aug. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('aug. 9, 2012')
        assert len(result) == 1

    def test_aug_period_uppercase(self):
        """'AUG. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('AUG. 9, 2012')
        assert len(result) == 1

    def test_aug_period_day_31(self):
        """'Aug. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Aug. 31, 2012')
        assert len(result) == 1

    def test_aug_period_day_1(self):
        """'Aug. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Aug. 1, 2012')
        assert len(result) == 1


class TestSepPeriodFormats:
    """Test all format variations for 'Sep.'"""

    def test_sep_period_d_comma_yyyy(self):
        """'Sep. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Sep. 9, 2012')
        assert len(result) == 1

    def test_sep_period_dd_comma_yyyy(self):
        """'Sep. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Sep. 09, 2012')
        assert len(result) == 1

    def test_sep_period_d_space_yyyy(self):
        """'Sep. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Sep. 9 2012')
        assert len(result) == 1

    def test_d_sep_period_yyyy(self):
        """'9 Sep. 2012' should be parsed."""
        result = extract_explicit_dates('9 Sep. 2012')
        assert len(result) == 1

    def test_dd_sep_period_yyyy(self):
        """'09 Sep. 2012' should be parsed."""
        result = extract_explicit_dates('09 Sep. 2012')
        assert len(result) == 1

    def test_sep_period_1st_comma_yyyy(self):
        """'Sep. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Sep. 1st, 2012')
        assert len(result) == 1

    def test_sep_period_2nd_comma_yyyy(self):
        """'Sep. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Sep. 2nd, 2012')
        assert len(result) == 1

    def test_sep_period_3rd_comma_yyyy(self):
        """'Sep. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Sep. 3rd, 2012')
        assert len(result) == 1

    def test_sep_period_9th_comma_yyyy(self):
        """'Sep. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Sep. 9th, 2012')
        assert len(result) == 1

    def test_sep_period_with_time_suffix(self):
        """'Sep. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Sep. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_sep_period_with_time_suffix_am(self):
        """'Sep. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Sep. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_sep_period(self):
        """'8:25 a.m. Sep. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Sep. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_sep_period_variant(self):
        """'10:06am Sep. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Sep. 11, 2014')
        assert len(result) == 1

    def test_sep_period_in_sentence(self):
        """'filed on Sep. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Sep. 9, 2012 for review')
        assert len(result) == 1

    def test_sep_period_at_start(self):
        """'Sep. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Sep. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_sep_period_at_end(self):
        """'The event occurred on Sep. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Sep. 20, 2012')
        assert len(result) == 1

    def test_sep_period_lowercase(self):
        """'sep. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('sep. 9, 2012')
        assert len(result) == 1

    def test_sep_period_uppercase(self):
        """'SEP. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('SEP. 9, 2012')
        assert len(result) == 1

    def test_sep_period_day_30(self):
        """'Sep. 30, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Sep. 30, 2012')
        assert len(result) == 1

    def test_sep_period_day_1(self):
        """'Sep. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Sep. 1, 2012')
        assert len(result) == 1


class TestOctPeriodFormats:
    """Test all format variations for 'Oct.'"""

    def test_oct_period_d_comma_yyyy(self):
        """'Oct. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Oct. 9, 2012')
        assert len(result) == 1

    def test_oct_period_dd_comma_yyyy(self):
        """'Oct. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Oct. 09, 2012')
        assert len(result) == 1

    def test_oct_period_d_space_yyyy(self):
        """'Oct. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Oct. 9 2012')
        assert len(result) == 1

    def test_d_oct_period_yyyy(self):
        """'9 Oct. 2012' should be parsed."""
        result = extract_explicit_dates('9 Oct. 2012')
        assert len(result) == 1

    def test_dd_oct_period_yyyy(self):
        """'09 Oct. 2012' should be parsed."""
        result = extract_explicit_dates('09 Oct. 2012')
        assert len(result) == 1

    def test_oct_period_1st_comma_yyyy(self):
        """'Oct. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Oct. 1st, 2012')
        assert len(result) == 1

    def test_oct_period_2nd_comma_yyyy(self):
        """'Oct. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Oct. 2nd, 2012')
        assert len(result) == 1

    def test_oct_period_3rd_comma_yyyy(self):
        """'Oct. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Oct. 3rd, 2012')
        assert len(result) == 1

    def test_oct_period_9th_comma_yyyy(self):
        """'Oct. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Oct. 9th, 2012')
        assert len(result) == 1

    def test_oct_period_with_time_suffix(self):
        """'Oct. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Oct. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_oct_period_with_time_suffix_am(self):
        """'Oct. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Oct. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_oct_period(self):
        """'8:25 a.m. Oct. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Oct. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_oct_period_variant(self):
        """'10:06am Oct. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Oct. 11, 2014')
        assert len(result) == 1

    def test_oct_period_in_sentence(self):
        """'filed on Oct. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Oct. 9, 2012 for review')
        assert len(result) == 1

    def test_oct_period_at_start(self):
        """'Oct. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Oct. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_oct_period_at_end(self):
        """'The event occurred on Oct. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Oct. 20, 2012')
        assert len(result) == 1

    def test_oct_period_lowercase(self):
        """'oct. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('oct. 9, 2012')
        assert len(result) == 1

    def test_oct_period_uppercase(self):
        """'OCT. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('OCT. 9, 2012')
        assert len(result) == 1

    def test_oct_period_day_31(self):
        """'Oct. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Oct. 31, 2012')
        assert len(result) == 1

    def test_oct_period_day_1(self):
        """'Oct. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Oct. 1, 2012')
        assert len(result) == 1


class TestNovPeriodFormats:
    """Test all format variations for 'Nov.'"""

    def test_nov_period_d_comma_yyyy(self):
        """'Nov. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Nov. 9, 2012')
        assert len(result) == 1

    def test_nov_period_dd_comma_yyyy(self):
        """'Nov. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Nov. 09, 2012')
        assert len(result) == 1

    def test_nov_period_d_space_yyyy(self):
        """'Nov. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Nov. 9 2012')
        assert len(result) == 1

    def test_d_nov_period_yyyy(self):
        """'9 Nov. 2012' should be parsed."""
        result = extract_explicit_dates('9 Nov. 2012')
        assert len(result) == 1

    def test_dd_nov_period_yyyy(self):
        """'09 Nov. 2012' should be parsed."""
        result = extract_explicit_dates('09 Nov. 2012')
        assert len(result) == 1

    def test_nov_period_1st_comma_yyyy(self):
        """'Nov. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Nov. 1st, 2012')
        assert len(result) == 1

    def test_nov_period_2nd_comma_yyyy(self):
        """'Nov. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Nov. 2nd, 2012')
        assert len(result) == 1

    def test_nov_period_3rd_comma_yyyy(self):
        """'Nov. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Nov. 3rd, 2012')
        assert len(result) == 1

    def test_nov_period_9th_comma_yyyy(self):
        """'Nov. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Nov. 9th, 2012')
        assert len(result) == 1

    def test_nov_period_with_time_suffix(self):
        """'Nov. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Nov. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_nov_period_with_time_suffix_am(self):
        """'Nov. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Nov. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_nov_period(self):
        """'8:25 a.m. Nov. 12, 2014' should be parsed."""
        result = extract_explicit_dates('8:25 a.m. Nov. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_nov_period_variant(self):
        """'10:06am Nov. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Nov. 11, 2014')
        assert len(result) == 1

    def test_nov_period_in_sentence(self):
        """'filed on Nov. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Nov. 9, 2012 for review')
        assert len(result) == 1

    def test_nov_period_at_start(self):
        """'Nov. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Nov. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_nov_period_at_end(self):
        """'The event occurred on Nov. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Nov. 20, 2012')
        assert len(result) == 1

    def test_nov_period_lowercase(self):
        """'nov. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('nov. 9, 2012')
        assert len(result) == 1

    def test_nov_period_uppercase(self):
        """'NOV. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('NOV. 9, 2012')
        assert len(result) == 1

    def test_nov_period_day_30(self):
        """'Nov. 30, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Nov. 30, 2012')
        assert len(result) == 1

    def test_nov_period_day_1(self):
        """'Nov. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Nov. 1, 2012')
        assert len(result) == 1


class TestDecPeriodFormats:
    """Test all format variations for 'Dec.'"""

    def test_dec_period_d_comma_yyyy(self):
        """'Dec. 9, 2012' should be parsed."""
        result = extract_explicit_dates('Dec. 9, 2012')
        assert len(result) == 1

    def test_dec_period_dd_comma_yyyy(self):
        """'Dec. 09, 2012' should be parsed."""
        result = extract_explicit_dates('Dec. 09, 2012')
        assert len(result) == 1

    def test_dec_period_d_space_yyyy(self):
        """'Dec. 9 2012' should be parsed (no comma)."""
        result = extract_explicit_dates('Dec. 9 2012')
        assert len(result) == 1

    def test_d_dec_period_yyyy(self):
        """'9 Dec. 2012' should be parsed."""
        result = extract_explicit_dates('9 Dec. 2012')
        assert len(result) == 1

    def test_dd_dec_period_yyyy(self):
        """'09 Dec. 2012' should be parsed."""
        result = extract_explicit_dates('09 Dec. 2012')
        assert len(result) == 1

    def test_dec_period_1st_comma_yyyy(self):
        """'Dec. 1st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Dec. 1st, 2012')
        assert len(result) == 1

    def test_dec_period_2nd_comma_yyyy(self):
        """'Dec. 2nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Dec. 2nd, 2012')
        assert len(result) == 1

    def test_dec_period_3rd_comma_yyyy(self):
        """'Dec. 3rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Dec. 3rd, 2012')
        assert len(result) == 1

    def test_dec_period_9th_comma_yyyy(self):
        """'Dec. 9th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Dec. 9th, 2012')
        assert len(result) == 1

    def test_dec_period_with_time_suffix(self):
        """'Dec. 9, 2012 at 2:57 p.m.' should be parsed."""
        result = extract_explicit_dates('Dec. 9, 2012 at 2:57 p.m.')
        assert len(result) == 1

    def test_dec_period_with_time_suffix_am(self):
        """'Dec. 9, 2012 10:30am' should be parsed."""
        result = extract_explicit_dates('Dec. 9, 2012 10:30am')
        assert len(result) == 1

    def test_time_prefix_dec_period(self):
        """'8:25 a.m. Dec. 12, 2014' should be parsed (from issue example)."""
        result = extract_explicit_dates('8:25 a.m. Dec. 12, 2014')
        assert len(result) == 1

    def test_time_prefix_dec_period_variant(self):
        """'10:06am Dec. 11, 2014' should be parsed."""
        result = extract_explicit_dates('10:06am Dec. 11, 2014')
        assert len(result) == 1

    def test_dec_period_in_sentence(self):
        """'filed on Dec. 9, 2012 for review' should be parsed."""
        result = extract_explicit_dates('filed on Dec. 9, 2012 for review')
        assert len(result) == 1

    def test_dec_period_at_start(self):
        """'Dec. 15, 2012 was the deadline' should be parsed."""
        result = extract_explicit_dates('Dec. 15, 2012 was the deadline')
        assert len(result) == 1

    def test_dec_period_at_end(self):
        """'The event occurred on Dec. 20, 2012' should be parsed."""
        result = extract_explicit_dates('The event occurred on Dec. 20, 2012')
        assert len(result) == 1

    def test_dec_period_lowercase(self):
        """'dec. 9, 2012' should be parsed (lowercase)."""
        result = extract_explicit_dates('dec. 9, 2012')
        assert len(result) == 1

    def test_dec_period_uppercase(self):
        """'DEC. 9, 2012' should be parsed (uppercase)."""
        result = extract_explicit_dates('DEC. 9, 2012')
        assert len(result) == 1

    def test_dec_period_day_31(self):
        """'Dec. 31, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Dec. 31, 2012')
        assert len(result) == 1

    def test_dec_period_day_1(self):
        """'Dec. 1, 2012' should be parsed (boundary)."""
        result = extract_explicit_dates('Dec. 1, 2012')
        assert len(result) == 1


class TestNegativeCases:
    """Negative test cases that should NOT match."""

    def test_aug_period_alone(self):
        """'Aug.' alone should not be parsed (no day or year)."""
        result = extract_explicit_dates('Aug.')
        assert len(result) == 0

    def test_aug_period_d_only(self):
        """'Aug. 9' should not be parsed (no year)."""
        result = extract_explicit_dates('Aug. 9')
        assert len(result) == 0

    def test_d_aug_period_only(self):
        """'9 Aug.' should not be parsed (no year)."""
        result = extract_explicit_dates('9 Aug.')
        assert len(result) == 0

    def test_aug_period_invalid_day(self):
        """'Aug. 32, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Aug. 32, 2012')
        assert len(result) == 0

    def test_dec_period_alone(self):
        """'Dec.' alone should not be parsed (no day or year)."""
        result = extract_explicit_dates('Dec.')
        assert len(result) == 0

    def test_dec_period_d_only(self):
        """'Dec. 12' should not be parsed (no year)."""
        result = extract_explicit_dates('Dec. 12')
        assert len(result) == 0

    def test_d_dec_period_only(self):
        """'12 Dec.' should not be parsed (no year)."""
        result = extract_explicit_dates('12 Dec.')
        assert len(result) == 0

    def test_dec_period_invalid_day(self):
        """'Dec. 32, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Dec. 32, 2012')
        assert len(result) == 0

    def test_feb_period_invalid_day(self):
        """'Feb. 30, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Feb. 30, 2012')
        assert len(result) == 0

    def test_apr_period_invalid_day(self):
        """'Apr. 31, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Apr. 31, 2012')
        assert len(result) == 0

    def test_jun_period_invalid_day(self):
        """'Jun. 31, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Jun. 31, 2012')
        assert len(result) == 0

    def test_sep_period_invalid_day(self):
        """'Sep. 31, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Sep. 31, 2012')
        assert len(result) == 0

    def test_nov_period_invalid_day(self):
        """'Nov. 31, 2012' should not be parsed (invalid day)."""
        result = extract_explicit_dates('Nov. 31, 2012')
        assert len(result) == 0


class TestMixedAndAdditionalFormats:
    """Additional edge cases and mixed formats."""

    def test_multiple_periods_in_sentence(self):
        """'Filed on Aug. 9, 2012 and Dec. 12, 2014' should find both."""
        result = extract_explicit_dates('Filed on Aug. 9, 2012 and Dec. 12, 2014')
        assert len(result) == 2

    def test_jan_period_with_year_2000(self):
        """'Jan. 1, 2000' should be parsed."""
        result = extract_explicit_dates('Jan. 1, 2000')
        assert len(result) == 1

    def test_dec_period_with_year_2100(self):
        """'Dec. 31, 2100' should be parsed."""
        result = extract_explicit_dates('Dec. 31, 2100')
        assert len(result) == 1

    def test_mar_period_with_year_1900(self):
        """'Mar. 15, 1900' should be parsed."""
        result = extract_explicit_dates('Mar. 15, 1900')
        assert len(result) == 1

    def test_mixed_period_and_no_period(self):
        """'Aug. 9, 2012 and Aug 10, 2012' should find both."""
        result = extract_explicit_dates('Aug. 9, 2012 and Aug 10, 2012')
        assert len(result) == 2

    def test_sept_period_variant(self):
        """'Sept. 9, 2012' should be parsed (alternative abbreviation)."""
        result = extract_explicit_dates('Sept. 9, 2012')
        assert len(result) == 1

    def test_mixed_case_sentence(self):
        """'The deadline was Aug. 9, 2012 for filing.' should be parsed."""
        result = extract_explicit_dates('The deadline was Aug. 9, 2012 for filing.')
        assert len(result) == 1

    def test_parenthetical_date(self):
        """'(Aug. 9, 2012)' should be parsed."""
        result = extract_explicit_dates('(Aug. 9, 2012)')
        assert len(result) == 1

    def test_quoted_date(self):
        """'"Aug. 9, 2012"' should be parsed."""
        result = extract_explicit_dates('"Aug. 9, 2012"')
        assert len(result) == 1

    def test_hyphenated_context(self):
        """'pre-Aug. 9, 2012 filing' should be parsed."""
        result = extract_explicit_dates('pre-Aug. 9, 2012 filing')
        assert len(result) == 1

    def test_jan_period_21st(self):
        """'Jan. 21st, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jan. 21st, 2012')
        assert len(result) == 1

    def test_feb_period_22nd(self):
        """'Feb. 22nd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Feb. 22nd, 2012')
        assert len(result) == 1

    def test_mar_period_23rd(self):
        """'Mar. 23rd, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Mar. 23rd, 2012')
        assert len(result) == 1

    def test_apr_period_11th(self):
        """'Apr. 11th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Apr. 11th, 2012')
        assert len(result) == 1

    def test_may_no_period(self):
        """'May 9, 2012' should be parsed (May is not abbreviated with period)."""
        result = extract_explicit_dates('May 9, 2012')
        assert len(result) == 1

    def test_jun_period_12th(self):
        """'Jun. 12th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jun. 12th, 2012')
        assert len(result) == 1

    def test_jul_period_13th(self):
        """'Jul. 13th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Jul. 13th, 2012')
        assert len(result) == 1

    def test_aug_period_14th(self):
        """'Aug. 14th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Aug. 14th, 2012')
        assert len(result) == 1

    def test_sep_period_15th(self):
        """'Sep. 15th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Sep. 15th, 2012')
        assert len(result) == 1

    def test_oct_period_20th(self):
        """'Oct. 20th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Oct. 20th, 2012')
        assert len(result) == 1

    def test_nov_period_25th(self):
        """'Nov. 25th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Nov. 25th, 2012')
        assert len(result) == 1

    def test_dec_period_30th(self):
        """'Dec. 30th, 2012' should be parsed (ordinal)."""
        result = extract_explicit_dates('Dec. 30th, 2012')
        assert len(result) == 1
