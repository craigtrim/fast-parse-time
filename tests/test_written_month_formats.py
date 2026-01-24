#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for written month name formats in explicit dates."""

import pytest
from fast_parse_time import extract_explicit_dates


class TestWrittenMonthFormats:
    """Tests for basic written month formats."""

    def test_month_day_year(self):
        """'March 15, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('March 15, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_day_month_year(self):
        """'15 March 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('15 March 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_abbreviated_month(self):
        """'Mar 15, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('Mar 15, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_ordinal_day(self):
        """'January 1st, 2024' should be parsed as explicit date."""
        result = extract_explicit_dates('January 1st, 2024')
        assert result is not None
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()


class TestOrdinalVariations:
    """Tests for different ordinal suffix variations."""

    def test_ordinal_1st(self):
        """'January 1st, 2024' should be parsed."""
        result = extract_explicit_dates('January 1st, 2024')
        assert len(result) == 1

    def test_ordinal_2nd(self):
        """'February 2nd, 2024' should be parsed."""
        result = extract_explicit_dates('February 2nd, 2024')
        assert len(result) == 1

    def test_ordinal_3rd(self):
        """'March 3rd, 2024' should be parsed."""
        result = extract_explicit_dates('March 3rd, 2024')
        assert len(result) == 1

    def test_ordinal_4th(self):
        """'April 4th, 2024' should be parsed."""
        result = extract_explicit_dates('April 4th, 2024')
        assert len(result) == 1


class TestAbbreviatedMonths:
    """Tests for abbreviated month names."""

    def test_jan(self):
        """'Jan 15, 2024' should be parsed."""
        result = extract_explicit_dates('Jan 15, 2024')
        assert len(result) == 1

    def test_feb(self):
        """'Feb 15, 2024' should be parsed."""
        result = extract_explicit_dates('Feb 15, 2024')
        assert len(result) == 1

    def test_sept(self):
        """'Sept 15, 2024' should be parsed (alternative abbreviation)."""
        result = extract_explicit_dates('Sept 15, 2024')
        assert len(result) == 1

    def test_dec(self):
        """'Dec 25, 2024' should be parsed."""
        result = extract_explicit_dates('Dec 25, 2024')
        assert len(result) == 1


class TestCapitalizationVariations:
    """Tests for capitalization variations."""

    def test_uppercase(self):
        """'MARCH 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('MARCH 15, 2024')
        assert len(result) == 1

    def test_lowercase(self):
        """'march 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('march 15, 2024')
        assert len(result) == 1

    def test_mixed_case(self):
        """'mArCh 15, 2024' should be parsed (case-insensitive)."""
        result = extract_explicit_dates('mArCh 15, 2024')
        assert len(result) == 1


class TestSentenceContext:
    """Tests for written dates within sentences."""

    def test_date_in_sentence(self):
        """Date in a sentence should be extracted."""
        result = extract_explicit_dates('The meeting is on March 15, 2024')
        assert len(result) == 1

    def test_date_at_end(self):
        """Date at end of sentence should be extracted."""
        result = extract_explicit_dates('Event scheduled for December 25, 2024')
        assert len(result) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
