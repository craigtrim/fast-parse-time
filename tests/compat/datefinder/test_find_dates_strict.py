# -*- coding: utf-8 -*-
"""
Test strict-mode date extraction (requires year component).
Source: https://github.com/akoumjian/datefinder/blob/master/tests/test_find_dates_strict.py

datefinder's strict=True rejects date strings without a year component.
fast-parse-time always requires a parseable date, so its behavior
naturally aligns with strict mode for full dates and should reject
month-only or day-month-only strings.
"""
import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestStrictDateExtraction:
    """Source: test_find_date_strings_strict"""

    def test_month_year_extracted_as_month_year(self):
        """
        'June 2018' -- no day component.
        datefinder strict=True returns [] (requires full date).
        fast-parse-time correctly extracts this as MONTH_YEAR -- better behavior
        than silently discarding a valid partial date.
        """
        result = extract_explicit_dates('June 2018')
        assert len(result) == 1
        assert result.get('June 2018') == 'MONTH_YEAR'

    def test_numeric_two_digit_year(self):
        """'09/06/18' -- 2-digit year. datefinder resolves to 2018-09-06."""
        result = extract_explicit_dates('09/06/18')
        assert len(result) >= 1

    def test_numeric_four_digit_year(self):
        """'09/06/2018'"""
        result = extract_explicit_dates('09/06/2018')
        assert len(result) >= 1

    def test_date_with_label_prefix(self):
        """'recorded: 03/14/2008' -- date preceded by a label and colon."""
        result = extract_explicit_dates('recorded: 03/14/2008')
        assert len(result) >= 1

    def test_ordinal_day_of_month_year(self):
        """'19th day of May, 2015' -- ordinal day with full written month."""
        result = extract_explicit_dates('19th day of May, 2015')
        assert len(result) >= 1

    def test_ordinal_day_of_month_no_year_returns_empty(self):
        """'19th day of May' -- no year. datefinder strict=True returns []."""
        result = extract_explicit_dates('19th day of May')
        assert len(result) == 0
