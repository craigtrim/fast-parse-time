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


class TestAllFullMonthNames:
    """Tests for all twelve full month names."""

    def test_april(self):
        """'April 10, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('April 10, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_may(self):
        """'May 20, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('May 20, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_june(self):
        """'June 5, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('June 5, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_july(self):
        """'July 4, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('July 4, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_august(self):
        """'August 15, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('August 15, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_september(self):
        """'September 1, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('September 1, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_october(self):
        """'October 31, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('October 31, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_november(self):
        """'November 11, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('November 11, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()

    def test_december(self):
        """'December 25, 2024' should be parsed as an explicit date."""
        result = extract_explicit_dates('December 25, 2024')
        assert len(result) == 1
        assert 'FULL_EXPLICIT_DATE' in result.values()


class TestDateAtStartOfSentence:
    """Tests for dates appearing at the very start of a sentence."""

    def test_date_at_start(self):
        """Date at the start of a sentence should be extracted."""
        result = extract_explicit_dates('March 15, 2024 is the deadline')
        assert len(result) == 1

    def test_abbreviated_month_at_start(self):
        """Abbreviated month at the start of a sentence should be extracted."""
        result = extract_explicit_dates('Apr 10, 2024 kicks off the project')
        assert len(result) == 1


class TestDateWithoutComma:
    """Tests for dates with no comma between month+day and year."""

    def test_no_comma_month_day_year(self):
        """Date without comma between day and year should still parse."""
        result = extract_explicit_dates('March 15 2024')
        assert len(result) == 1

    def test_no_comma_abbreviated(self):
        """Abbreviated month date without comma should still parse."""
        result = extract_explicit_dates('Jan 1 2024')
        assert len(result) == 1


class TestAdditionalOrdinals:
    """Tests for additional ordinal day suffixes."""

    def test_ordinal_5th(self):
        """'March 5th, 2024' should be parsed."""
        result = extract_explicit_dates('March 5th, 2024')
        assert len(result) == 1

    def test_ordinal_11th(self):
        """'July 11th, 2024' should be parsed."""
        result = extract_explicit_dates('July 11th, 2024')
        assert len(result) == 1

    def test_ordinal_12th(self):
        """'August 12th, 2024' should be parsed."""
        result = extract_explicit_dates('August 12th, 2024')
        assert len(result) == 1

    def test_ordinal_21st(self):
        """'October 21st, 2024' should be parsed."""
        result = extract_explicit_dates('October 21st, 2024')
        assert len(result) == 1

    def test_ordinal_22nd(self):
        """'November 22nd, 2024' should be parsed."""
        result = extract_explicit_dates('November 22nd, 2024')
        assert len(result) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
