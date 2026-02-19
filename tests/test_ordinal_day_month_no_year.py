# -*- coding: utf-8 -*-
"""
Test ordinal day-of-month expressions without year component.

Related GitHub Issue:
    #63 - False positive: '19th day of May' (no year) returns DAY_MONTH, should return empty
    https://github.com/craigtrim/fast-parse-time/issues/63

Ordinal expressions like '19th day of May' without a year should return empty {}.
Ordinal expressions WITH a year like '19th day of May, 2015' should return FULL_EXPLICIT_DATE.
"""

import pytest
from fast_parse_time import extract_explicit_dates


class TestOrdinalDayMonthNoYear:
    """Ordinal + month without year must return empty dict."""

    # Core pattern: "Nth day of Month" without year
    def test_1st_day_of_january(self):
        assert extract_explicit_dates('1st day of January') == {}

    def test_2nd_day_of_february(self):
        assert extract_explicit_dates('2nd day of February') == {}

    def test_3rd_day_of_march(self):
        assert extract_explicit_dates('3rd day of March') == {}

    def test_4th_day_of_april(self):
        assert extract_explicit_dates('4th day of April') == {}

    def test_5th_day_of_may(self):
        assert extract_explicit_dates('5th day of May') == {}

    def test_6th_day_of_june(self):
        assert extract_explicit_dates('6th day of June') == {}

    def test_7th_day_of_july(self):
        assert extract_explicit_dates('7th day of July') == {}

    def test_8th_day_of_august(self):
        assert extract_explicit_dates('8th day of August') == {}

    def test_9th_day_of_september(self):
        assert extract_explicit_dates('9th day of September') == {}

    def test_10th_day_of_october(self):
        assert extract_explicit_dates('10th day of October') == {}

    def test_11th_day_of_november(self):
        assert extract_explicit_dates('11th day of November') == {}

    def test_12th_day_of_december(self):
        assert extract_explicit_dates('12th day of December') == {}

    # All ordinals 13-31 for January (representative month)
    def test_13th_day_of_january(self):
        assert extract_explicit_dates('13th day of January') == {}

    def test_14th_day_of_january(self):
        assert extract_explicit_dates('14th day of January') == {}

    def test_15th_day_of_january(self):
        assert extract_explicit_dates('15th day of January') == {}

    def test_16th_day_of_january(self):
        assert extract_explicit_dates('16th day of January') == {}

    def test_17th_day_of_january(self):
        assert extract_explicit_dates('17th day of January') == {}

    def test_18th_day_of_january(self):
        assert extract_explicit_dates('18th day of January') == {}

    def test_19th_day_of_january(self):
        assert extract_explicit_dates('19th day of January') == {}

    def test_20th_day_of_january(self):
        assert extract_explicit_dates('20th day of January') == {}

    def test_21st_day_of_january(self):
        assert extract_explicit_dates('21st day of January') == {}

    def test_22nd_day_of_january(self):
        assert extract_explicit_dates('22nd day of January') == {}

    def test_23rd_day_of_january(self):
        assert extract_explicit_dates('23rd day of January') == {}

    def test_24th_day_of_january(self):
        assert extract_explicit_dates('24th day of January') == {}

    def test_25th_day_of_january(self):
        assert extract_explicit_dates('25th day of January') == {}

    def test_26th_day_of_january(self):
        assert extract_explicit_dates('26th day of January') == {}

    def test_27th_day_of_january(self):
        assert extract_explicit_dates('27th day of January') == {}

    def test_28th_day_of_january(self):
        assert extract_explicit_dates('28th day of January') == {}

    def test_29th_day_of_january(self):
        assert extract_explicit_dates('29th day of January') == {}

    def test_30th_day_of_january(self):
        assert extract_explicit_dates('30th day of January') == {}

    def test_31st_day_of_january(self):
        assert extract_explicit_dates('31st day of January') == {}

    # All ordinals 1-31 for May (the original compat test case)
    def test_1st_day_of_may(self):
        assert extract_explicit_dates('1st day of May') == {}

    def test_2nd_day_of_may(self):
        assert extract_explicit_dates('2nd day of May') == {}

    def test_3rd_day_of_may(self):
        assert extract_explicit_dates('3rd day of May') == {}

    def test_4th_day_of_may(self):
        assert extract_explicit_dates('4th day of May') == {}

    # 5th already covered above
    def test_6th_day_of_may(self):
        assert extract_explicit_dates('6th day of May') == {}

    def test_7th_day_of_may(self):
        assert extract_explicit_dates('7th day of May') == {}

    def test_8th_day_of_may(self):
        assert extract_explicit_dates('8th day of May') == {}

    def test_9th_day_of_may(self):
        assert extract_explicit_dates('9th day of May') == {}

    def test_10th_day_of_may(self):
        assert extract_explicit_dates('10th day of May') == {}

    def test_11th_day_of_may(self):
        assert extract_explicit_dates('11th day of May') == {}

    def test_12th_day_of_may(self):
        assert extract_explicit_dates('12th day of May') == {}

    def test_13th_day_of_may(self):
        assert extract_explicit_dates('13th day of May') == {}

    def test_14th_day_of_may(self):
        assert extract_explicit_dates('14th day of May') == {}

    def test_15th_day_of_may(self):
        assert extract_explicit_dates('15th day of May') == {}

    def test_16th_day_of_may(self):
        assert extract_explicit_dates('16th day of May') == {}

    def test_17th_day_of_may(self):
        assert extract_explicit_dates('17th day of May') == {}

    def test_18th_day_of_may(self):
        assert extract_explicit_dates('18th day of May') == {}

    def test_19th_day_of_may(self):
        """The original failing compat test case."""
        assert extract_explicit_dates('19th day of May') == {}

    def test_20th_day_of_may(self):
        assert extract_explicit_dates('20th day of May') == {}

    def test_21st_day_of_may(self):
        assert extract_explicit_dates('21st day of May') == {}

    def test_22nd_day_of_may(self):
        assert extract_explicit_dates('22nd day of May') == {}

    def test_23rd_day_of_may(self):
        assert extract_explicit_dates('23rd day of May') == {}

    def test_24th_day_of_may(self):
        assert extract_explicit_dates('24th day of May') == {}

    def test_25th_day_of_may(self):
        assert extract_explicit_dates('25th day of May') == {}

    def test_26th_day_of_may(self):
        assert extract_explicit_dates('26th day of May') == {}

    def test_27th_day_of_may(self):
        assert extract_explicit_dates('27th day of May') == {}

    def test_28th_day_of_may(self):
        assert extract_explicit_dates('28th day of May') == {}

    def test_29th_day_of_may(self):
        assert extract_explicit_dates('29th day of May') == {}

    def test_30th_day_of_may(self):
        assert extract_explicit_dates('30th day of May') == {}

    def test_31st_day_of_may(self):
        assert extract_explicit_dates('31st day of May') == {}

    # Abbreviated months
    def test_19th_day_of_jan(self):
        assert extract_explicit_dates('19th day of Jan') == {}

    def test_5th_day_of_feb(self):
        assert extract_explicit_dates('5th day of Feb') == {}

    def test_15th_day_of_mar(self):
        assert extract_explicit_dates('15th day of Mar') == {}

    def test_22nd_day_of_apr(self):
        assert extract_explicit_dates('22nd day of Apr') == {}

    def test_8th_day_of_jun(self):
        assert extract_explicit_dates('8th day of Jun') == {}

    def test_12th_day_of_jul(self):
        assert extract_explicit_dates('12th day of Jul') == {}

    def test_30th_day_of_aug(self):
        assert extract_explicit_dates('30th day of Aug') == {}

    def test_17th_day_of_sep(self):
        assert extract_explicit_dates('17th day of Sep') == {}

    def test_5th_day_of_oct(self):
        assert extract_explicit_dates('5th day of Oct') == {}

    def test_11th_day_of_nov(self):
        assert extract_explicit_dates('11th day of Nov') == {}

    def test_25th_day_of_dec(self):
        assert extract_explicit_dates('25th day of Dec') == {}

    # Sentence embedding
    def test_scheduled_for_3rd_day_of_april(self):
        assert extract_explicit_dates('scheduled for the 3rd day of April') == {}

    def test_on_10th_day_of_june(self):
        assert extract_explicit_dates('on the 10th day of June') == {}

    def test_meeting_on_1st_day_of_september(self):
        assert extract_explicit_dates('Meeting on 1st day of September') == {}

    def test_due_by_15th_day_of_march(self):
        assert extract_explicit_dates('Due by 15th day of March') == {}

    def test_event_starts_on_20th_day_of_july(self):
        assert extract_explicit_dates('Event starts on the 20th day of July') == {}

    # With day-of-week prefix
    def test_monday_15th_day_of_march(self):
        assert extract_explicit_dates('Monday, 15th day of March') == {}

    def test_friday_20th_day_of_august(self):
        assert extract_explicit_dates('Friday, 20th day of August') == {}

    def test_wednesday_5th_day_of_november(self):
        assert extract_explicit_dates('Wednesday, 5th day of November') == {}


class TestOrdinalDayMonthWithYear:
    """Ordinal + month WITH year must still return FULL_EXPLICIT_DATE."""

    # Original compat test case with year
    def test_19th_day_of_may_2015(self):
        result = extract_explicit_dates('19th day of May, 2015')
        assert len(result) == 1
        assert '19th day of May, 2015' in result
        assert result['19th day of May, 2015'] == 'FULL_EXPLICIT_DATE'

    # Variations with comma
    def test_1st_day_of_january_2020(self):
        result = extract_explicit_dates('1st day of January, 2020')
        assert len(result) == 1
        assert result.get('1st day of January, 2020') == 'FULL_EXPLICIT_DATE'

    def test_3rd_day_of_march_1999(self):
        result = extract_explicit_dates('3rd day of March, 1999')
        assert len(result) == 1
        assert result.get('3rd day of March, 1999') == 'FULL_EXPLICIT_DATE'

    def test_15th_day_of_august_2010(self):
        result = extract_explicit_dates('15th day of August, 2010')
        assert len(result) == 1
        assert result.get('15th day of August, 2010') == 'FULL_EXPLICIT_DATE'

    def test_31st_day_of_december_1999(self):
        result = extract_explicit_dates('31st day of December, 1999')
        assert len(result) == 1
        assert result.get('31st day of December, 1999') == 'FULL_EXPLICIT_DATE'

    # Variations without comma
    def test_10th_day_of_june_2018(self):
        result = extract_explicit_dates('10th day of June 2018')
        assert len(result) == 1
        # Could be with or without comma in the key
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_25th_day_of_november_2022(self):
        result = extract_explicit_dates('25th day of November 2022')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    # Multiple months and years
    def test_2nd_day_of_february_2021(self):
        result = extract_explicit_dates('2nd day of February, 2021')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_4th_day_of_april_2019(self):
        result = extract_explicit_dates('4th day of April, 2019')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_7th_day_of_july_2017(self):
        result = extract_explicit_dates('7th day of July, 2017')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_9th_day_of_september_2016(self):
        result = extract_explicit_dates('9th day of September, 2016')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_12th_day_of_october_2014(self):
        result = extract_explicit_dates('12th day of October, 2014')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    # Abbreviated months with year
    def test_5th_day_of_jan_2020(self):
        result = extract_explicit_dates('5th day of Jan, 2020')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_15th_day_of_mar_2018(self):
        result = extract_explicit_dates('15th day of Mar, 2018')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_20th_day_of_oct_2019(self):
        result = extract_explicit_dates('20th day of Oct, 2019')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())


class TestRelatedMonthDayFormats:
    """
    Related: plain 'Month Day' without year.

    Document expected behavior for simpler formats like 'May 19' without year.
    Current behavior likely returns MONTH_DAY - decide if this is acceptable or should also be suppressed.
    """

    def test_may_19_without_year(self):
        """'May 19' without year - currently may return MONTH_DAY."""
        result = extract_explicit_dates('May 19')
        # Document current behavior - this test documents what happens, not what should happen
        # If we decide to suppress these too, update the assertion
        # For now, just verify it doesn't crash and returns something
        assert isinstance(result, dict)

    def test_19_may_without_year(self):
        """'19 May' without year - European format."""
        result = extract_explicit_dates('19 May')
        assert isinstance(result, dict)

    def test_january_15_without_year(self):
        """'January 15' without year."""
        result = extract_explicit_dates('January 15')
        assert isinstance(result, dict)

    def test_15_january_without_year(self):
        """'15 January' without year."""
        result = extract_explicit_dates('15 January')
        assert isinstance(result, dict)


class TestNegativeCasesStillWork:
    """Negative cases: formats WITH year that should NOT change."""

    # Standard Month Day, Year format
    def test_may_19_2015(self):
        result = extract_explicit_dates('May 19, 2015')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_january_1_2020(self):
        result = extract_explicit_dates('January 1, 2020')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_december_31_1999(self):
        result = extract_explicit_dates('December 31, 1999')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    # European Day Month Year format
    def test_19_may_2015(self):
        result = extract_explicit_dates('19 May 2015')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_1_january_2020(self):
        result = extract_explicit_dates('1 January 2020')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_31_december_1999(self):
        result = extract_explicit_dates('31 December 1999')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    # With ordinals
    def test_19th_may_2015(self):
        result = extract_explicit_dates('19th May 2015')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_1st_january_2020(self):
        result = extract_explicit_dates('1st January 2020')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_31st_december_1999(self):
        result = extract_explicit_dates('31st December 1999')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    # With ordinals and comma
    def test_15th_march_2018(self):
        result = extract_explicit_dates('15th March, 2018')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_22nd_april_2019(self):
        result = extract_explicit_dates('22nd April, 2019')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())

    def test_3rd_july_2020(self):
        result = extract_explicit_dates('3rd July, 2020')
        assert len(result) == 1
        assert any('FULL_EXPLICIT_DATE' in str(v) for v in result.values())


class TestEdgeCasesOrdinalNoYear:
    """Additional edge cases for ordinal patterns without year."""

    # Case variations
    def test_uppercase_month(self):
        assert extract_explicit_dates('5th day of MARCH') == {}

    def test_lowercase_month(self):
        assert extract_explicit_dates('5th day of march') == {}

    def test_mixed_case_month(self):
        assert extract_explicit_dates('5th day of MaRcH') == {}

    # Extra whitespace
    def test_extra_spaces(self):
        assert extract_explicit_dates('5th  day  of  March') == {}

    def test_leading_whitespace(self):
        assert extract_explicit_dates('  5th day of March') == {}

    def test_trailing_whitespace(self):
        assert extract_explicit_dates('5th day of March  ') == {}

    # In longer text
    def test_embedded_in_sentence_start(self):
        assert extract_explicit_dates('The 15th day of March was important') == {}

    def test_embedded_in_sentence_middle(self):
        assert extract_explicit_dates('We met on the 10th day of June for dinner') == {}

    def test_embedded_in_sentence_end(self):
        assert extract_explicit_dates('The event was scheduled for the 20th day of August') == {}

    # Multiple ordinals in same text (all without year)
    def test_multiple_ordinals_no_year(self):
        result = extract_explicit_dates('The 5th day of March and 10th day of April')
        # Both should be suppressed since neither has a year
        assert result == {}

    # Ordinal with full month names vs abbreviations
    def test_all_full_month_names_sample(self):
        """Sample from all 12 full month names."""
        for month in ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']:
            assert extract_explicit_dates(f'10th day of {month}') == {}

    def test_all_abbreviated_month_names_sample(self):
        """Sample from all 12 abbreviated month names."""
        for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            assert extract_explicit_dates(f'10th day of {month}') == {}


class TestAllOrdinalsFebruary:
    """All ordinals 1-29 for February (shorter month)."""

    def test_1st_day_of_february(self):
        assert extract_explicit_dates('1st day of February') == {}

    def test_2nd_day_of_february(self):
        assert extract_explicit_dates('2nd day of February') == {}

    def test_3rd_day_of_february(self):
        assert extract_explicit_dates('3rd day of February') == {}

    def test_4th_day_of_february(self):
        assert extract_explicit_dates('4th day of February') == {}

    def test_5th_day_of_february(self):
        assert extract_explicit_dates('5th day of February') == {}

    def test_6th_day_of_february(self):
        assert extract_explicit_dates('6th day of February') == {}

    def test_7th_day_of_february(self):
        assert extract_explicit_dates('7th day of February') == {}

    def test_8th_day_of_february(self):
        assert extract_explicit_dates('8th day of February') == {}

    def test_9th_day_of_february(self):
        assert extract_explicit_dates('9th day of February') == {}

    def test_10th_day_of_february(self):
        assert extract_explicit_dates('10th day of February') == {}

    def test_11th_day_of_february(self):
        assert extract_explicit_dates('11th day of February') == {}

    def test_12th_day_of_february(self):
        assert extract_explicit_dates('12th day of February') == {}

    def test_13th_day_of_february(self):
        assert extract_explicit_dates('13th day of February') == {}

    def test_14th_day_of_february(self):
        assert extract_explicit_dates('14th day of February') == {}

    def test_15th_day_of_february(self):
        assert extract_explicit_dates('15th day of February') == {}

    def test_16th_day_of_february(self):
        assert extract_explicit_dates('16th day of February') == {}

    def test_17th_day_of_february(self):
        assert extract_explicit_dates('17th day of February') == {}

    def test_18th_day_of_february(self):
        assert extract_explicit_dates('18th day of February') == {}

    def test_19th_day_of_february(self):
        assert extract_explicit_dates('19th day of February') == {}

    def test_20th_day_of_february(self):
        assert extract_explicit_dates('20th day of February') == {}

    def test_21st_day_of_february(self):
        assert extract_explicit_dates('21st day of February') == {}

    def test_22nd_day_of_february(self):
        assert extract_explicit_dates('22nd day of February') == {}

    def test_23rd_day_of_february(self):
        assert extract_explicit_dates('23rd day of February') == {}

    def test_24th_day_of_february(self):
        assert extract_explicit_dates('24th day of February') == {}

    def test_25th_day_of_february(self):
        assert extract_explicit_dates('25th day of February') == {}

    def test_26th_day_of_february(self):
        assert extract_explicit_dates('26th day of February') == {}

    def test_27th_day_of_february(self):
        assert extract_explicit_dates('27th day of February') == {}

    def test_28th_day_of_february(self):
        assert extract_explicit_dates('28th day of February') == {}

    def test_29th_day_of_february(self):
        assert extract_explicit_dates('29th day of February') == {}


class TestAllOrdinalsJune:
    """All ordinals 1-30 for June."""

    def test_1st_day_of_june(self):
        assert extract_explicit_dates('1st day of June') == {}

    def test_2nd_day_of_june(self):
        assert extract_explicit_dates('2nd day of June') == {}

    def test_3rd_day_of_june(self):
        assert extract_explicit_dates('3rd day of June') == {}

    def test_4th_day_of_june(self):
        assert extract_explicit_dates('4th day of June') == {}

    def test_5th_day_of_june(self):
        assert extract_explicit_dates('5th day of June') == {}

    def test_6th_day_of_june(self):
        assert extract_explicit_dates('6th day of June') == {}

    def test_7th_day_of_june(self):
        assert extract_explicit_dates('7th day of June') == {}

    def test_8th_day_of_june(self):
        assert extract_explicit_dates('8th day of June') == {}

    def test_9th_day_of_june(self):
        assert extract_explicit_dates('9th day of June') == {}

    def test_10th_day_of_june(self):
        assert extract_explicit_dates('10th day of June') == {}

    def test_11th_day_of_june(self):
        assert extract_explicit_dates('11th day of June') == {}

    def test_12th_day_of_june(self):
        assert extract_explicit_dates('12th day of June') == {}

    def test_13th_day_of_june(self):
        assert extract_explicit_dates('13th day of June') == {}

    def test_14th_day_of_june(self):
        assert extract_explicit_dates('14th day of June') == {}

    def test_15th_day_of_june(self):
        assert extract_explicit_dates('15th day of June') == {}

    def test_16th_day_of_june(self):
        assert extract_explicit_dates('16th day of June') == {}

    def test_17th_day_of_june(self):
        assert extract_explicit_dates('17th day of June') == {}

    def test_18th_day_of_june(self):
        assert extract_explicit_dates('18th day of June') == {}

    def test_19th_day_of_june(self):
        assert extract_explicit_dates('19th day of June') == {}

    def test_20th_day_of_june(self):
        assert extract_explicit_dates('20th day of June') == {}

    def test_21st_day_of_june(self):
        assert extract_explicit_dates('21st day of June') == {}

    def test_22nd_day_of_june(self):
        assert extract_explicit_dates('22nd day of June') == {}

    def test_23rd_day_of_june(self):
        assert extract_explicit_dates('23rd day of June') == {}

    def test_24th_day_of_june(self):
        assert extract_explicit_dates('24th day of June') == {}

    def test_25th_day_of_june(self):
        assert extract_explicit_dates('25th day of June') == {}

    def test_26th_day_of_june(self):
        assert extract_explicit_dates('26th day of June') == {}

    def test_27th_day_of_june(self):
        assert extract_explicit_dates('27th day of June') == {}

    def test_28th_day_of_june(self):
        assert extract_explicit_dates('28th day of June') == {}

    def test_29th_day_of_june(self):
        assert extract_explicit_dates('29th day of June') == {}

    def test_30th_day_of_june(self):
        assert extract_explicit_dates('30th day of June') == {}


class TestAllOrdinalsSeptember:
    """All ordinals 1-30 for September."""

    def test_1st_day_of_september(self):
        assert extract_explicit_dates('1st day of September') == {}

    def test_2nd_day_of_september(self):
        assert extract_explicit_dates('2nd day of September') == {}

    def test_3rd_day_of_september(self):
        assert extract_explicit_dates('3rd day of September') == {}

    def test_4th_day_of_september(self):
        assert extract_explicit_dates('4th day of September') == {}

    def test_5th_day_of_september(self):
        assert extract_explicit_dates('5th day of September') == {}

    def test_6th_day_of_september(self):
        assert extract_explicit_dates('6th day of September') == {}

    def test_7th_day_of_september(self):
        assert extract_explicit_dates('7th day of September') == {}

    def test_8th_day_of_september(self):
        assert extract_explicit_dates('8th day of September') == {}

    def test_9th_day_of_september(self):
        assert extract_explicit_dates('9th day of September') == {}

    def test_10th_day_of_september(self):
        assert extract_explicit_dates('10th day of September') == {}

    def test_11th_day_of_september(self):
        assert extract_explicit_dates('11th day of September') == {}

    def test_12th_day_of_september(self):
        assert extract_explicit_dates('12th day of September') == {}

    def test_13th_day_of_september(self):
        assert extract_explicit_dates('13th day of September') == {}

    def test_14th_day_of_september(self):
        assert extract_explicit_dates('14th day of September') == {}

    def test_15th_day_of_september(self):
        assert extract_explicit_dates('15th day of September') == {}

    def test_16th_day_of_september(self):
        assert extract_explicit_dates('16th day of September') == {}

    def test_17th_day_of_september(self):
        assert extract_explicit_dates('17th day of September') == {}

    def test_18th_day_of_september(self):
        assert extract_explicit_dates('18th day of September') == {}

    def test_19th_day_of_september(self):
        assert extract_explicit_dates('19th day of September') == {}

    def test_20th_day_of_september(self):
        assert extract_explicit_dates('20th day of September') == {}

    def test_21st_day_of_september(self):
        assert extract_explicit_dates('21st day of September') == {}

    def test_22nd_day_of_september(self):
        assert extract_explicit_dates('22nd day of September') == {}

    def test_23rd_day_of_september(self):
        assert extract_explicit_dates('23rd day of September') == {}

    def test_24th_day_of_september(self):
        assert extract_explicit_dates('24th day of September') == {}

    def test_25th_day_of_september(self):
        assert extract_explicit_dates('25th day of September') == {}

    def test_26th_day_of_september(self):
        assert extract_explicit_dates('26th day of September') == {}

    def test_27th_day_of_september(self):
        assert extract_explicit_dates('27th day of September') == {}

    def test_28th_day_of_september(self):
        assert extract_explicit_dates('28th day of September') == {}

    def test_29th_day_of_september(self):
        assert extract_explicit_dates('29th day of September') == {}

    def test_30th_day_of_september(self):
        assert extract_explicit_dates('30th day of September') == {}


class TestAllOrdinalsDecember:
    """All ordinals 1-31 for December."""

    def test_1st_day_of_december(self):
        assert extract_explicit_dates('1st day of December') == {}

    def test_2nd_day_of_december(self):
        assert extract_explicit_dates('2nd day of December') == {}

    def test_3rd_day_of_december(self):
        assert extract_explicit_dates('3rd day of December') == {}

    def test_4th_day_of_december(self):
        assert extract_explicit_dates('4th day of December') == {}

    def test_5th_day_of_december(self):
        assert extract_explicit_dates('5th day of December') == {}

    def test_6th_day_of_december(self):
        assert extract_explicit_dates('6th day of December') == {}

    def test_7th_day_of_december(self):
        assert extract_explicit_dates('7th day of December') == {}

    def test_8th_day_of_december(self):
        assert extract_explicit_dates('8th day of December') == {}

    def test_9th_day_of_december(self):
        assert extract_explicit_dates('9th day of December') == {}

    def test_10th_day_of_december(self):
        assert extract_explicit_dates('10th day of December') == {}

    def test_11th_day_of_december(self):
        assert extract_explicit_dates('11th day of December') == {}

    def test_12th_day_of_december(self):
        assert extract_explicit_dates('12th day of December') == {}

    def test_13th_day_of_december(self):
        assert extract_explicit_dates('13th day of December') == {}

    def test_14th_day_of_december(self):
        assert extract_explicit_dates('14th day of December') == {}

    def test_15th_day_of_december(self):
        assert extract_explicit_dates('15th day of December') == {}

    def test_16th_day_of_december(self):
        assert extract_explicit_dates('16th day of December') == {}

    def test_17th_day_of_december(self):
        assert extract_explicit_dates('17th day of December') == {}

    def test_18th_day_of_december(self):
        assert extract_explicit_dates('18th day of December') == {}

    def test_19th_day_of_december(self):
        assert extract_explicit_dates('19th day of December') == {}

    def test_20th_day_of_december(self):
        assert extract_explicit_dates('20th day of December') == {}

    def test_21st_day_of_december(self):
        assert extract_explicit_dates('21st day of December') == {}

    def test_22nd_day_of_december(self):
        assert extract_explicit_dates('22nd day of December') == {}

    def test_23rd_day_of_december(self):
        assert extract_explicit_dates('23rd day of December') == {}

    def test_24th_day_of_december(self):
        assert extract_explicit_dates('24th day of December') == {}

    def test_25th_day_of_december(self):
        assert extract_explicit_dates('25th day of December') == {}

    def test_26th_day_of_december(self):
        assert extract_explicit_dates('26th day of December') == {}

    def test_27th_day_of_december(self):
        assert extract_explicit_dates('27th day of December') == {}

    def test_28th_day_of_december(self):
        assert extract_explicit_dates('28th day of December') == {}

    def test_29th_day_of_december(self):
        assert extract_explicit_dates('29th day of December') == {}

    def test_30th_day_of_december(self):
        assert extract_explicit_dates('30th day of December') == {}

    def test_31st_day_of_december(self):
        assert extract_explicit_dates('31st day of December') == {}
