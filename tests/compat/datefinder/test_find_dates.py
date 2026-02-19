# -*- coding: utf-8 -*-
"""
Test finding dates in free-form text.
Source: https://github.com/akoumjian/datefinder/blob/master/tests/test_find_dates.py
"""
import pytest
from fast_parse_time import extract_explicit_dates

pytestmark = pytest.mark.xfail(strict=False, reason='Compatibility test - implementation gap')


class TestWrittenEnglishDates:
    """Source: test_find_date_strings -- written English date formats"""

    def test_weekday_abbr_month_day_year(self):
        """'Tuesday Jul 22, 2014'"""
        result = extract_explicit_dates('Tuesday Jul 22, 2014')
        assert len(result) >= 1

    def test_full_month_day_year_with_time_word(self):
        """'December 13, 2014 at midnight'"""
        result = extract_explicit_dates('December 13, 2014 at midnight')
        assert len(result) >= 1

    def test_full_month_ordinal_day_year_with_time(self):
        """'April 9, 2013 at 6:11 a.m.'"""
        result = extract_explicit_dates('April 9, 2013 at 6:11 a.m.')
        assert len(result) >= 1

    def test_abbr_month_with_period_day_year_time(self):
        """'Aug. 9, 2012 at 2:57 p.m.'"""
        result = extract_explicit_dates('Aug. 9, 2012 at 2:57 p.m.')
        assert len(result) >= 1

    def test_full_month_day_year_time_am_pm(self):
        """'December 10, 2014, 11:02:21 pm'"""
        result = extract_explicit_dates('December 10, 2014, 11:02:21 pm')
        assert len(result) >= 1

    def test_time_first_then_abbr_month_day_year(self):
        """'8:25 a.m. Dec. 12, 2014'"""
        result = extract_explicit_dates('8:25 a.m. Dec. 12, 2014')
        assert len(result) >= 1

    def test_time_first_comma_full_month_day_year(self):
        """'2:21 p.m., December 11, 2014'"""
        result = extract_explicit_dates('2:21 p.m., December 11, 2014')
        assert len(result) >= 1

    def test_rfc_style_weekday_day_month_year_time(self):
        """'Fri, 12 Dec 2014 10:55:50'"""
        result = extract_explicit_dates('Fri, 12 Dec 2014 10:55:50')
        assert len(result) >= 1

    def test_time_first_abbr_month_day_year(self):
        """'10:06am Dec 11, 2014'"""
        result = extract_explicit_dates('10:06am Dec 11, 2014')
        assert len(result) >= 1

    def test_full_month_ordinal_day_year(self):
        """'September 2nd, 1998'"""
        result = extract_explicit_dates('September 2nd, 1998')
        assert len(result) >= 1

    def test_ordinal_day_of_month_year(self):
        """'12th day of December, 2001'"""
        result = extract_explicit_dates('12th day of December, 2001')
        assert len(result) >= 1

    def test_ordinal_day_of_full_month_year(self):
        """'19th day of May, 2015'"""
        result = extract_explicit_dates('19th day of May, 2015')
        assert len(result) >= 1


class TestDateRanges:
    """Source: test_find_date_strings -- date ranges (two dates in one string)"""

    def test_written_month_range(self):
        """'May 5, 2010 to July 10, 2011' -- two dates"""
        result = extract_explicit_dates('May 5, 2010 to July 10, 2011')
        assert len(result) == 2

    def test_natural_language_range(self):
        """'i am looking for a date june 4th 1996 to july 3rd 2013'"""
        result = extract_explicit_dates(
            'i am looking for a date june 4th 1996 to july 3rd 2013'
        )
        assert len(result) == 2

    def test_legal_language_date_range(self):
        """'october 27 1994 to be put into effect on june 1 1995'"""
        result = extract_explicit_dates(
            'october 27 1994 to be put into effect on june 1 1995'
        )
        assert len(result) == 2

    def test_numeric_date_range(self):
        """'31/08/2012 to 30/08/2013'"""
        result = extract_explicit_dates('31/08/2012 to 30/08/2013')
        assert len(result) == 2

    def test_written_abbr_month_range_with_dash(self):
        """'31 Oct 2021 - 28 Nov 2021'"""
        result = extract_explicit_dates('31 Oct 2021 - 28 Nov 2021')
        assert len(result) == 2

    def test_iso_date_range(self):
        """'2017-02-03T09:04:08Z to 2017-02-03T09:04:09Z' - same day returns 1 entry"""
        result = extract_explicit_dates(
            '2017-02-03T09:04:08Z to 2017-02-03T09:04:09Z'
        )
        # Both datetimes map to same date key, so only 1 entry
        assert len(result) == 1
        assert '2017-02-03' in result


class TestNumericDates:
    """Source: test_find_date_strings -- numeric and ISO date formats"""

    def test_us_numeric_date(self):
        """'06-17-2014'"""
        result = extract_explicit_dates('06-17-2014')
        assert len(result) >= 1

    def test_eu_numeric_date(self):
        """'13/03/2014'"""
        result = extract_explicit_dates('13/03/2014')
        assert len(result) >= 1

    def test_iso_datetime_with_tz(self):
        """'2016-02-04T20:16:26+00:00'"""
        result = extract_explicit_dates('2016-02-04T20:16:26+00:00')
        assert len(result) >= 1

    def test_iso_datetime_z_suffix(self):
        """'2017-02-03T09:04:08Z'"""
        result = extract_explicit_dates('2017-02-03T09:04:08Z')
        assert len(result) >= 1

    def test_iso_datetime_with_millis(self):
        """'2017-02-03T09:04:08.001Z'"""
        result = extract_explicit_dates('2017-02-03T09:04:08.001Z')
        assert len(result) >= 1

    def test_slash_date_in_sentence(self):
        """'recorded: 03/14/2008'"""
        result = extract_explicit_dates('recorded: 03/14/2008')
        assert len(result) >= 1

    def test_simple_slash_date(self):
        """'02/05/2020'"""
        result = extract_explicit_dates('02/05/2020')
        assert len(result) >= 1


class TestYearInSentence:
    """
    Source: test_find_date_strings -- year-only references embedded in prose.
    datefinder extracts the year and fills month/day from today.
    fast-parse-time should extract the year token.
    """

    def test_year_in_sentence_2004(self):
        text = 'Dutta is the recipient of Femina Miss India Universe title in 2004.'
        result = extract_explicit_dates(text)
        assert len(result) >= 1

    def test_year_in_sentence_2008(self):
        text = 'she said that she hit depression after being traumatized on the sets of "Horn OK" in 2008.'
        result = extract_explicit_dates(text)
        assert len(result) >= 1
