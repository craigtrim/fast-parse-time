#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Regression tests: existing formats that must continue to work after issue #22.

These patterns already work and must NOT be broken by the new ordinal extraction.

Related GitHub Issue:
    #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
    https://github.com/craigtrim/fast-parse-time/issues/22
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalRegression:
    """Existing patterns that must remain unaffected."""

    # ── full dates with ordinal + year (already working) ─────────────────────

    def test_march_15_2024(self):
        result = extract_explicit_dates('March 15, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_september_2nd_1998(self):
        result = extract_explicit_dates('September 2nd, 1998')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_may_19th_2023(self):
        result = extract_explicit_dates('May 19th 2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_15th_march_2024(self):
        result = extract_explicit_dates('15th March 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_january_1st_2024(self):
        result = extract_explicit_dates('January 1st, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_february_2nd_2024(self):
        result = extract_explicit_dates('February 2nd, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_march_3rd_2024(self):
        result = extract_explicit_dates('March 3rd, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_april_4th_2024(self):
        result = extract_explicit_dates('April 4th, 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_15th_march_2024_no_comma(self):
        result = extract_explicit_dates('15th March 2024')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── numeric date formats (must be unaffected) ─────────────────────────────

    def test_numeric_slash_full(self):
        result = extract_explicit_dates('03/19/2023')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_numeric_dash_full(self):
        result = extract_explicit_dates('2023-03-19')
        assert result

    def test_numeric_partial(self):
        result = extract_explicit_dates('3/15')
        assert result

    # ── ISO 8601 (must be unaffected) ─────────────────────────────────────────

    def test_iso8601_z_suffix(self):
        result = extract_explicit_dates('2024-01-15T09:30:00Z')
        assert result
        assert 'FULL_EXPLICIT_DATE' in result.values()

    # ── month-year forms (must be unaffected) ─────────────────────────────────

    def test_month_year_written(self):
        result = extract_explicit_dates('March 2024')
        assert result
        assert 'MONTH_YEAR' in result.values()

    def test_month_year_hyphen(self):
        result = extract_explicit_dates('Oct-23')
        assert result
        assert 'MONTH_YEAR' in result.values()

    # ── prose year forms (must be unaffected) ────────────────────────────────

    def test_prose_year_in(self):
        result = extract_explicit_dates('in 2004')
        assert result
        assert 'YEAR_ONLY' in result.values()

    # ── no date → empty ───────────────────────────────────────────────────────

    def test_no_date_plain_text(self):
        result = extract_explicit_dates('hello world')
        assert not result

    def test_no_date_number_only(self):
        result = extract_explicit_dates('42')
        assert not result
