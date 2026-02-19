#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for space-delimited MonthName+2-digit-number patterns.

Covers:
  - NN > 31 → unambiguously a year → MONTH_YEAR
  - Preposition 'in' → MONTH_YEAR
  - Preposition 'on' → DAY_MONTH
  - No context, NN ≤ 31 → DAY_MONTH_AMBIGUOUS
  - All 12 abbreviated month names (Jan, Feb, Mar, Apr, May, Jun,
                                    Jul, Aug, Sep, Sept, Oct, Nov, Dec)
  - All 12 full month names (January, February, ..., December)
  - Case variations (upper, lower, title, mixed)
  - Sentence context (embedded in prose)
  - Edge cases (NN = 00, NN = 01, NN = 31, NN = 32, NN = 99)
  - Negative cases (should NOT match)

Related GitHub Issue:
    #38 - Gap: space-delimited MonthName+2-digit-number not classified
    https://github.com/craigtrim/fast-parse-time/issues/38
"""

import pytest
from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MONTH_YEAR = 'MONTH_YEAR'
DAY_MONTH = 'DAY_MONTH'
DAY_MONTH_AMBIGUOUS = 'DAY_MONTH_AMBIGUOUS'

ABBREV_MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

FULL_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

ALL_MONTHS = ABBREV_MONTHS + FULL_MONTHS


# ===========================================================================
# Section 1: NN > 31 → MONTH_YEAR (unambiguous year, all abbreviated months)
# ===========================================================================

class TestAbbrevMonthNNAbove31Year:
    """Abbreviated months with NN > 31 → unambiguous year → MONTH_YEAR."""

    def test_jan_32(self):
        result = extract_explicit_dates('Jan 32')
        assert result and result.get('Jan 32') == MONTH_YEAR

    def test_jan_50(self):
        result = extract_explicit_dates('Jan 50')
        assert result and result.get('Jan 50') == MONTH_YEAR

    def test_jan_99(self):
        result = extract_explicit_dates('Jan 99')
        assert result and result.get('Jan 99') == MONTH_YEAR

    def test_feb_32(self):
        result = extract_explicit_dates('Feb 32')
        assert result and result.get('Feb 32') == MONTH_YEAR

    def test_feb_65(self):
        result = extract_explicit_dates('Feb 65')
        assert result and result.get('Feb 65') == MONTH_YEAR

    def test_feb_99(self):
        result = extract_explicit_dates('Feb 99')
        assert result and result.get('Feb 99') == MONTH_YEAR

    def test_mar_32(self):
        result = extract_explicit_dates('Mar 32')
        assert result and result.get('Mar 32') == MONTH_YEAR

    def test_mar_75(self):
        result = extract_explicit_dates('Mar 75')
        assert result and result.get('Mar 75') == MONTH_YEAR

    def test_mar_99(self):
        result = extract_explicit_dates('Mar 99')
        assert result and result.get('Mar 99') == MONTH_YEAR

    def test_apr_32(self):
        result = extract_explicit_dates('Apr 32')
        assert result and result.get('Apr 32') == MONTH_YEAR

    def test_apr_55(self):
        result = extract_explicit_dates('Apr 55')
        assert result and result.get('Apr 55') == MONTH_YEAR

    def test_apr_99(self):
        result = extract_explicit_dates('Apr 99')
        assert result and result.get('Apr 99') == MONTH_YEAR

    def test_may_32(self):
        result = extract_explicit_dates('May 32')
        assert result and result.get('May 32') == MONTH_YEAR

    def test_may_80(self):
        result = extract_explicit_dates('May 80')
        assert result and result.get('May 80') == MONTH_YEAR

    def test_may_99(self):
        result = extract_explicit_dates('May 99')
        assert result and result.get('May 99') == MONTH_YEAR

    def test_jun_32(self):
        result = extract_explicit_dates('Jun 32')
        assert result and result.get('Jun 32') == MONTH_YEAR

    def test_jun_45(self):
        result = extract_explicit_dates('Jun 45')
        assert result and result.get('Jun 45') == MONTH_YEAR

    def test_jun_99(self):
        result = extract_explicit_dates('Jun 99')
        assert result and result.get('Jun 99') == MONTH_YEAR

    def test_jul_32(self):
        result = extract_explicit_dates('Jul 32')
        assert result and result.get('Jul 32') == MONTH_YEAR

    def test_jul_60(self):
        result = extract_explicit_dates('Jul 60')
        assert result and result.get('Jul 60') == MONTH_YEAR

    def test_jul_99(self):
        result = extract_explicit_dates('Jul 99')
        assert result and result.get('Jul 99') == MONTH_YEAR

    def test_aug_32(self):
        result = extract_explicit_dates('Aug 32')
        assert result and result.get('Aug 32') == MONTH_YEAR

    def test_aug_70(self):
        result = extract_explicit_dates('Aug 70')
        assert result and result.get('Aug 70') == MONTH_YEAR

    def test_aug_99(self):
        result = extract_explicit_dates('Aug 99')
        assert result and result.get('Aug 99') == MONTH_YEAR

    def test_sep_32(self):
        result = extract_explicit_dates('Sep 32')
        assert result and result.get('Sep 32') == MONTH_YEAR

    def test_sep_85(self):
        result = extract_explicit_dates('Sep 85')
        assert result and result.get('Sep 85') == MONTH_YEAR

    def test_sep_99(self):
        result = extract_explicit_dates('Sep 99')
        assert result and result.get('Sep 99') == MONTH_YEAR

    def test_sept_32(self):
        result = extract_explicit_dates('Sept 32')
        assert result and result.get('Sept 32') == MONTH_YEAR

    def test_sept_88(self):
        result = extract_explicit_dates('Sept 88')
        assert result and result.get('Sept 88') == MONTH_YEAR

    def test_sept_99(self):
        result = extract_explicit_dates('Sept 99')
        assert result and result.get('Sept 99') == MONTH_YEAR

    def test_oct_32(self):
        result = extract_explicit_dates('Oct 32')
        assert result and result.get('Oct 32') == MONTH_YEAR

    def test_oct_50(self):
        result = extract_explicit_dates('Oct 50')
        assert result and result.get('Oct 50') == MONTH_YEAR

    def test_oct_99(self):
        result = extract_explicit_dates('Oct 99')
        assert result and result.get('Oct 99') == MONTH_YEAR

    def test_nov_32(self):
        result = extract_explicit_dates('Nov 32')
        assert result and result.get('Nov 32') == MONTH_YEAR

    def test_nov_55(self):
        result = extract_explicit_dates('Nov 55')
        assert result and result.get('Nov 55') == MONTH_YEAR

    def test_nov_99(self):
        result = extract_explicit_dates('Nov 99')
        assert result and result.get('Nov 99') == MONTH_YEAR

    def test_dec_32(self):
        result = extract_explicit_dates('Dec 32')
        assert result and result.get('Dec 32') == MONTH_YEAR

    def test_dec_65(self):
        result = extract_explicit_dates('Dec 65')
        assert result and result.get('Dec 65') == MONTH_YEAR

    def test_dec_99(self):
        result = extract_explicit_dates('Dec 99')
        assert result and result.get('Dec 99') == MONTH_YEAR


# ===========================================================================
# Section 2: NN > 31 → MONTH_YEAR (full month names)
# ===========================================================================

class TestFullMonthNNAbove31Year:
    """Full month names with NN > 31 → unambiguous year → MONTH_YEAR."""

    def test_january_99(self):
        result = extract_explicit_dates('January 99')
        assert result and result.get('January 99') == MONTH_YEAR

    def test_february_32(self):
        result = extract_explicit_dates('February 32')
        assert result and result.get('February 32') == MONTH_YEAR

    def test_february_99(self):
        result = extract_explicit_dates('February 99')
        assert result and result.get('February 99') == MONTH_YEAR

    def test_march_32(self):
        result = extract_explicit_dates('March 32')
        assert result and result.get('March 32') == MONTH_YEAR

    def test_march_99(self):
        result = extract_explicit_dates('March 99')
        assert result and result.get('March 99') == MONTH_YEAR

    def test_april_32(self):
        result = extract_explicit_dates('April 32')
        assert result and result.get('April 32') == MONTH_YEAR

    def test_april_99(self):
        result = extract_explicit_dates('April 99')
        assert result and result.get('April 99') == MONTH_YEAR

    def test_may_full_32(self):
        result = extract_explicit_dates('May 32')
        assert result and result.get('May 32') == MONTH_YEAR

    def test_june_32(self):
        result = extract_explicit_dates('June 32')
        assert result and result.get('June 32') == MONTH_YEAR

    def test_june_99(self):
        result = extract_explicit_dates('June 99')
        assert result and result.get('June 99') == MONTH_YEAR

    def test_july_32(self):
        result = extract_explicit_dates('July 32')
        assert result and result.get('July 32') == MONTH_YEAR

    def test_july_99(self):
        result = extract_explicit_dates('July 99')
        assert result and result.get('July 99') == MONTH_YEAR

    def test_august_32(self):
        result = extract_explicit_dates('August 32')
        assert result and result.get('August 32') == MONTH_YEAR

    def test_august_99(self):
        result = extract_explicit_dates('August 99')
        assert result and result.get('August 99') == MONTH_YEAR

    def test_september_32(self):
        result = extract_explicit_dates('September 32')
        assert result and result.get('September 32') == MONTH_YEAR

    def test_september_99(self):
        result = extract_explicit_dates('September 99')
        assert result and result.get('September 99') == MONTH_YEAR

    def test_october_32(self):
        result = extract_explicit_dates('October 32')
        assert result and result.get('October 32') == MONTH_YEAR

    def test_october_99(self):
        result = extract_explicit_dates('October 99')
        assert result and result.get('October 99') == MONTH_YEAR

    def test_november_32(self):
        result = extract_explicit_dates('November 32')
        assert result and result.get('November 32') == MONTH_YEAR

    def test_november_99(self):
        result = extract_explicit_dates('November 99')
        assert result and result.get('November 99') == MONTH_YEAR

    def test_december_32(self):
        result = extract_explicit_dates('December 32')
        assert result and result.get('December 32') == MONTH_YEAR

    def test_december_99(self):
        result = extract_explicit_dates('December 99')
        assert result and result.get('December 99') == MONTH_YEAR


# ===========================================================================
# Section 3: "in MonthAbbr NN" → MONTH_YEAR (preposition context)
# ===========================================================================

class TestInPrepAbbrevMonth:
    """'in MonthAbbr NN' → MONTH_YEAR for all abbreviated months."""

    def test_in_jan_23(self):
        result = extract_explicit_dates('in Jan 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_feb_23(self):
        result = extract_explicit_dates('in Feb 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_mar_23(self):
        result = extract_explicit_dates('in Mar 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_apr_23(self):
        result = extract_explicit_dates('in Apr 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_may_23(self):
        result = extract_explicit_dates('in May 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_jun_23(self):
        result = extract_explicit_dates('in Jun 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_jul_23(self):
        result = extract_explicit_dates('in Jul 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_aug_23(self):
        result = extract_explicit_dates('in Aug 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_sep_23(self):
        result = extract_explicit_dates('in Sep 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_sept_23(self):
        result = extract_explicit_dates('in Sept 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_oct_23(self):
        result = extract_explicit_dates('in Oct 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_nov_23(self):
        result = extract_explicit_dates('in Nov 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_dec_23(self):
        result = extract_explicit_dates('in Dec 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_jan_15(self):
        result = extract_explicit_dates('in Jan 15')
        assert result and MONTH_YEAR in result.values()

    def test_in_oct_05(self):
        result = extract_explicit_dates('in Oct 05')
        assert result and MONTH_YEAR in result.values()

    def test_in_dec_01(self):
        result = extract_explicit_dates('in Dec 01')
        assert result and MONTH_YEAR in result.values()


# ===========================================================================
# Section 4: "in FullMonth NN" → MONTH_YEAR
# ===========================================================================

class TestInPrepFullMonth:
    """'in FullMonth NN' → MONTH_YEAR for all full month names."""

    def test_in_january_23(self):
        result = extract_explicit_dates('in January 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_february_23(self):
        result = extract_explicit_dates('in February 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_march_23(self):
        result = extract_explicit_dates('in March 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_april_23(self):
        result = extract_explicit_dates('in April 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_may_23(self):
        result = extract_explicit_dates('in May 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_june_23(self):
        result = extract_explicit_dates('in June 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_july_23(self):
        result = extract_explicit_dates('in July 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_august_23(self):
        result = extract_explicit_dates('in August 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_september_23(self):
        result = extract_explicit_dates('in September 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_october_23(self):
        result = extract_explicit_dates('in October 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_november_23(self):
        result = extract_explicit_dates('in November 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_december_23(self):
        result = extract_explicit_dates('in December 23')
        assert result and MONTH_YEAR in result.values()

    def test_in_march_15(self):
        result = extract_explicit_dates('in March 15')
        assert result and MONTH_YEAR in result.values()

    def test_in_october_07(self):
        result = extract_explicit_dates('in October 07')
        assert result and MONTH_YEAR in result.values()


# ===========================================================================
# Section 5: "on MonthAbbr NN" → DAY_MONTH
# ===========================================================================

class TestOnPrepAbbrevMonth:
    """'on MonthAbbr NN' → DAY_MONTH for all abbreviated months (NN ≤ 31)."""

    def test_on_jan_15(self):
        result = extract_explicit_dates('on Jan 15')
        assert result and DAY_MONTH in result.values()

    def test_on_feb_28(self):
        result = extract_explicit_dates('on Feb 28')
        assert result and DAY_MONTH in result.values()

    def test_on_mar_10(self):
        result = extract_explicit_dates('on Mar 10')
        assert result and DAY_MONTH in result.values()

    def test_on_apr_01(self):
        result = extract_explicit_dates('on Apr 01')
        assert result and DAY_MONTH in result.values()

    def test_on_may_05(self):
        result = extract_explicit_dates('on May 05')
        assert result and DAY_MONTH in result.values()

    def test_on_jun_21(self):
        result = extract_explicit_dates('on Jun 21')
        assert result and DAY_MONTH in result.values()

    def test_on_jul_04(self):
        result = extract_explicit_dates('on Jul 04')
        assert result and DAY_MONTH in result.values()

    def test_on_aug_31(self):
        result = extract_explicit_dates('on Aug 31')
        assert result and DAY_MONTH in result.values()

    def test_on_sep_15(self):
        result = extract_explicit_dates('on Sep 15')
        assert result and DAY_MONTH in result.values()

    def test_on_sept_15(self):
        result = extract_explicit_dates('on Sept 15')
        assert result and DAY_MONTH in result.values()

    def test_on_oct_23(self):
        result = extract_explicit_dates('on Oct 23')
        assert result and DAY_MONTH in result.values()

    def test_on_nov_11(self):
        result = extract_explicit_dates('on Nov 11')
        assert result and DAY_MONTH in result.values()

    def test_on_dec_25(self):
        result = extract_explicit_dates('on Dec 25')
        assert result and DAY_MONTH in result.values()

    def test_on_jan_01(self):
        result = extract_explicit_dates('on Jan 01')
        assert result and DAY_MONTH in result.values()

    def test_on_oct_31(self):
        result = extract_explicit_dates('on Oct 31')
        assert result and DAY_MONTH in result.values()


# ===========================================================================
# Section 6: "on FullMonth NN" → DAY_MONTH
# ===========================================================================

class TestOnPrepFullMonth:
    """'on FullMonth NN' → DAY_MONTH for all full month names (NN ≤ 31)."""

    def test_on_january_15(self):
        result = extract_explicit_dates('on January 15')
        assert result and DAY_MONTH in result.values()

    def test_on_february_14(self):
        result = extract_explicit_dates('on February 14')
        assert result and DAY_MONTH in result.values()

    def test_on_march_15(self):
        result = extract_explicit_dates('on March 15')
        assert result and DAY_MONTH in result.values()

    def test_on_april_01(self):
        result = extract_explicit_dates('on April 01')
        assert result and DAY_MONTH in result.values()

    def test_on_may_10(self):
        result = extract_explicit_dates('on May 10')
        assert result and DAY_MONTH in result.values()

    def test_on_june_21(self):
        result = extract_explicit_dates('on June 21')
        assert result and DAY_MONTH in result.values()

    def test_on_july_04(self):
        result = extract_explicit_dates('on July 04')
        assert result and DAY_MONTH in result.values()

    def test_on_august_31(self):
        result = extract_explicit_dates('on August 31')
        assert result and DAY_MONTH in result.values()

    def test_on_september_22(self):
        result = extract_explicit_dates('on September 22')
        assert result and DAY_MONTH in result.values()

    def test_on_october_23(self):
        result = extract_explicit_dates('on October 23')
        assert result and DAY_MONTH in result.values()

    def test_on_november_11(self):
        result = extract_explicit_dates('on November 11')
        assert result and DAY_MONTH in result.values()

    def test_on_december_25(self):
        result = extract_explicit_dates('on December 25')
        assert result and DAY_MONTH in result.values()


# ===========================================================================
# Section 7: No context, NN ≤ 31 → DAY_MONTH_AMBIGUOUS (abbreviated months)
# ===========================================================================

class TestAmbiguousAbbrevMonth:
    """Bare 'MonthAbbr NN' with NN ≤ 31, no preposition → DAY_MONTH_AMBIGUOUS."""

    def test_oct_23(self):
        result = extract_explicit_dates('Oct 23')
        assert result and result.get('Oct 23') == DAY_MONTH_AMBIGUOUS

    def test_mar_15(self):
        result = extract_explicit_dates('Mar 15')
        assert result and result.get('Mar 15') == DAY_MONTH_AMBIGUOUS

    def test_jan_01(self):
        result = extract_explicit_dates('Jan 01')
        assert result and result.get('Jan 01') == DAY_MONTH_AMBIGUOUS

    def test_feb_28(self):
        result = extract_explicit_dates('Feb 28')
        assert result and result.get('Feb 28') == DAY_MONTH_AMBIGUOUS

    def test_apr_15(self):
        result = extract_explicit_dates('Apr 15')
        assert result and result.get('Apr 15') == DAY_MONTH_AMBIGUOUS

    def test_may_20(self):
        result = extract_explicit_dates('May 20')
        assert result and result.get('May 20') == DAY_MONTH_AMBIGUOUS

    def test_jun_10(self):
        result = extract_explicit_dates('Jun 10')
        assert result and result.get('Jun 10') == DAY_MONTH_AMBIGUOUS

    def test_jul_04(self):
        result = extract_explicit_dates('Jul 04')
        assert result and result.get('Jul 04') == DAY_MONTH_AMBIGUOUS

    def test_aug_31(self):
        result = extract_explicit_dates('Aug 31')
        assert result and result.get('Aug 31') == DAY_MONTH_AMBIGUOUS

    def test_sep_07(self):
        result = extract_explicit_dates('Sep 07')
        assert result and result.get('Sep 07') == DAY_MONTH_AMBIGUOUS

    def test_sept_07(self):
        result = extract_explicit_dates('Sept 07')
        assert result and result.get('Sept 07') == DAY_MONTH_AMBIGUOUS

    def test_nov_11(self):
        result = extract_explicit_dates('Nov 11')
        assert result and result.get('Nov 11') == DAY_MONTH_AMBIGUOUS

    def test_dec_25(self):
        result = extract_explicit_dates('Dec 25')
        assert result and result.get('Dec 25') == DAY_MONTH_AMBIGUOUS

    def test_jan_31(self):
        result = extract_explicit_dates('Jan 31')
        assert result and result.get('Jan 31') == DAY_MONTH_AMBIGUOUS

    def test_oct_01(self):
        result = extract_explicit_dates('Oct 01')
        assert result and result.get('Oct 01') == DAY_MONTH_AMBIGUOUS

    def test_oct_05(self):
        result = extract_explicit_dates('Oct 05')
        assert result and result.get('Oct 05') == DAY_MONTH_AMBIGUOUS

    def test_oct_10(self):
        result = extract_explicit_dates('Oct 10')
        assert result and result.get('Oct 10') == DAY_MONTH_AMBIGUOUS

    def test_oct_15(self):
        result = extract_explicit_dates('Oct 15')
        assert result and result.get('Oct 15') == DAY_MONTH_AMBIGUOUS

    def test_oct_20(self):
        result = extract_explicit_dates('Oct 20')
        assert result and result.get('Oct 20') == DAY_MONTH_AMBIGUOUS

    def test_oct_25(self):
        result = extract_explicit_dates('Oct 25')
        assert result and result.get('Oct 25') == DAY_MONTH_AMBIGUOUS

    def test_oct_30(self):
        result = extract_explicit_dates('Oct 30')
        assert result and result.get('Oct 30') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 8: No context, NN ≤ 31 → DAY_MONTH_AMBIGUOUS (full month names)
# ===========================================================================

class TestAmbiguousFullMonth:
    """Bare 'FullMonth NN' with NN ≤ 31, no preposition → DAY_MONTH_AMBIGUOUS."""

    def test_october_23(self):
        result = extract_explicit_dates('October 23')
        assert result and result.get('October 23') == DAY_MONTH_AMBIGUOUS

    def test_march_15(self):
        result = extract_explicit_dates('March 15')
        assert result and result.get('March 15') == DAY_MONTH_AMBIGUOUS

    def test_january_01(self):
        result = extract_explicit_dates('January 01')
        assert result and result.get('January 01') == DAY_MONTH_AMBIGUOUS

    def test_february_28(self):
        result = extract_explicit_dates('February 28')
        assert result and result.get('February 28') == DAY_MONTH_AMBIGUOUS

    def test_april_15(self):
        result = extract_explicit_dates('April 15')
        assert result and result.get('April 15') == DAY_MONTH_AMBIGUOUS

    def test_may_20(self):
        result = extract_explicit_dates('May 20')
        assert result and result.get('May 20') == DAY_MONTH_AMBIGUOUS

    def test_june_10(self):
        result = extract_explicit_dates('June 10')
        assert result and result.get('June 10') == DAY_MONTH_AMBIGUOUS

    def test_july_04(self):
        result = extract_explicit_dates('July 04')
        assert result and result.get('July 04') == DAY_MONTH_AMBIGUOUS

    def test_august_31(self):
        result = extract_explicit_dates('August 31')
        assert result and result.get('August 31') == DAY_MONTH_AMBIGUOUS

    def test_september_22(self):
        result = extract_explicit_dates('September 22')
        assert result and result.get('September 22') == DAY_MONTH_AMBIGUOUS

    def test_november_11(self):
        result = extract_explicit_dates('November 11')
        assert result and result.get('November 11') == DAY_MONTH_AMBIGUOUS

    def test_december_25(self):
        result = extract_explicit_dates('December 25')
        assert result and result.get('December 25') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 9: Case variations
# ===========================================================================

class TestCaseVariations:
    """Case-insensitive matching for month names."""

    # UPPERCASE abbreviated
    def test_upper_oct_23_ambiguous(self):
        result = extract_explicit_dates('OCT 23')
        assert result and result.get('OCT 23') == DAY_MONTH_AMBIGUOUS

    def test_upper_jan_99_year(self):
        result = extract_explicit_dates('JAN 99')
        assert result and result.get('JAN 99') == MONTH_YEAR

    def test_upper_in_oct_23_year(self):
        result = extract_explicit_dates('in OCT 23')
        assert result and MONTH_YEAR in result.values()

    def test_upper_on_oct_23_day(self):
        result = extract_explicit_dates('on OCT 23')
        assert result and DAY_MONTH in result.values()

    # lowercase abbreviated
    def test_lower_oct_23_ambiguous(self):
        result = extract_explicit_dates('oct 23')
        assert result and result.get('oct 23') == DAY_MONTH_AMBIGUOUS

    def test_lower_jan_99_year(self):
        result = extract_explicit_dates('jan 99')
        assert result and result.get('jan 99') == MONTH_YEAR

    def test_lower_in_oct_23_year(self):
        result = extract_explicit_dates('in oct 23')
        assert result and MONTH_YEAR in result.values()

    def test_lower_on_oct_23_day(self):
        result = extract_explicit_dates('on oct 23')
        assert result and DAY_MONTH in result.values()

    # UPPERCASE full
    def test_upper_october_23_ambiguous(self):
        result = extract_explicit_dates('OCTOBER 23')
        assert result and result.get('OCTOBER 23') == DAY_MONTH_AMBIGUOUS

    def test_upper_october_99_year(self):
        result = extract_explicit_dates('OCTOBER 99')
        assert result and result.get('OCTOBER 99') == MONTH_YEAR

    # lowercase full
    def test_lower_october_23_ambiguous(self):
        result = extract_explicit_dates('october 23')
        assert result and result.get('october 23') == DAY_MONTH_AMBIGUOUS

    def test_lower_october_99_year(self):
        result = extract_explicit_dates('october 99')
        assert result and result.get('october 99') == MONTH_YEAR

    def test_lower_in_march_15_year(self):
        result = extract_explicit_dates('in march 15')
        assert result and MONTH_YEAR in result.values()

    def test_lower_on_march_15_day(self):
        result = extract_explicit_dates('on march 15')
        assert result and DAY_MONTH in result.values()

    # Mixed case prepositions
    def test_in_upper_oct_23(self):
        result = extract_explicit_dates('IN OCT 23')
        assert result and MONTH_YEAR in result.values()

    def test_on_upper_oct_23(self):
        result = extract_explicit_dates('ON OCT 23')
        assert result and DAY_MONTH in result.values()


# ===========================================================================
# Section 10: Sentence context (embedded in prose)
# ===========================================================================

class TestSentenceContext:
    """Pattern embedded in longer text still returns correct classification."""

    def test_sentence_in_oct_23(self):
        result = extract_explicit_dates('The report was filed in Oct 23 and approved.')
        assert result and MONTH_YEAR in result.values()

    def test_sentence_on_oct_23(self):
        result = extract_explicit_dates('The event happened on Oct 23 at noon.')
        assert result and DAY_MONTH in result.values()

    def test_sentence_bare_oct_23(self):
        result = extract_explicit_dates('The deadline is Oct 23.')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()

    def test_sentence_in_march_15(self):
        result = extract_explicit_dates('The contract was signed in March 15.')
        assert result and MONTH_YEAR in result.values()

    def test_sentence_on_march_15(self):
        result = extract_explicit_dates('I was born on March 15.')
        assert result and DAY_MONTH in result.values()

    def test_sentence_bare_march_15(self):
        result = extract_explicit_dates('The conference starts March 15.')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()

    def test_sentence_oct_99_year(self):
        result = extract_explicit_dates('The old record from Oct 99 shows this.')
        assert result and MONTH_YEAR in result.values()

    def test_sentence_jan_32_year(self):
        result = extract_explicit_dates('Projected figures for Jan 32 are speculative.')
        assert result and MONTH_YEAR in result.values()

    def test_sentence_multiple_dates(self):
        result = extract_explicit_dates('Between in Oct 23 and on Dec 25 we need to act.')
        assert result and MONTH_YEAR in result.values()
        assert result and DAY_MONTH in result.values()

    def test_sentence_in_jan_23_prose(self):
        result = extract_explicit_dates('Revenues grew sharply in Jan 23.')
        assert result and MONTH_YEAR in result.values()

    def test_sentence_on_dec_25_prose(self):
        result = extract_explicit_dates('Gifts are opened on Dec 25 every year.')
        assert result and DAY_MONTH in result.values()

    def test_sentence_bare_feb_28_prose(self):
        result = extract_explicit_dates('The festival is Feb 28 this year.')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()

    def test_comma_after_pattern(self):
        result = extract_explicit_dates('Starting Oct 23, we begin shipping.')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()

    def test_period_after_pattern(self):
        result = extract_explicit_dates('The meeting is scheduled for Oct 23.')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()

    def test_question_after_pattern(self):
        result = extract_explicit_dates('Is the deadline Oct 23?')
        assert result and DAY_MONTH_AMBIGUOUS in result.values()


# ===========================================================================
# Section 11: Edge values (NN = 01, 02, 31, 32, 00)
# ===========================================================================

class TestEdgeValues:
    """Boundary NN values."""

    def test_nn_01_ambiguous(self):
        result = extract_explicit_dates('Oct 01')
        assert result and result.get('Oct 01') == DAY_MONTH_AMBIGUOUS

    def test_nn_02_ambiguous(self):
        result = extract_explicit_dates('Oct 02')
        assert result and result.get('Oct 02') == DAY_MONTH_AMBIGUOUS

    def test_nn_31_ambiguous(self):
        result = extract_explicit_dates('Oct 31')
        assert result and result.get('Oct 31') == DAY_MONTH_AMBIGUOUS

    def test_nn_32_year(self):
        result = extract_explicit_dates('Oct 32')
        assert result and result.get('Oct 32') == MONTH_YEAR

    def test_nn_99_year(self):
        result = extract_explicit_dates('Oct 99')
        assert result and result.get('Oct 99') == MONTH_YEAR

    def test_nn_50_year(self):
        result = extract_explicit_dates('Oct 50')
        assert result and result.get('Oct 50') == MONTH_YEAR

    def test_nn_01_in_prep(self):
        result = extract_explicit_dates('in Oct 01')
        assert result and MONTH_YEAR in result.values()

    def test_nn_31_in_prep(self):
        result = extract_explicit_dates('in Oct 31')
        assert result and MONTH_YEAR in result.values()

    def test_nn_01_on_prep(self):
        result = extract_explicit_dates('on Oct 01')
        assert result and DAY_MONTH in result.values()

    def test_nn_31_on_prep(self):
        result = extract_explicit_dates('on Oct 31')
        assert result and DAY_MONTH in result.values()

    def test_nn_32_in_prep(self):
        # 32 > 31 so always MONTH_YEAR regardless of preposition
        result = extract_explicit_dates('in Oct 32')
        assert result and MONTH_YEAR in result.values()

    def test_nn_32_on_prep(self):
        # 32 > 31 so always MONTH_YEAR regardless of preposition
        result = extract_explicit_dates('on Oct 32')
        assert result and MONTH_YEAR in result.values()

    def test_single_digit_not_matched(self):
        # Single-digit numbers should not match (must be 2-digit NN)
        result = extract_explicit_dates('Oct 5')
        # Either no result or existing logic handles it — must NOT be our new type incorrectly
        if result:
            assert result.get('Oct 5') not in (DAY_MONTH_AMBIGUOUS, MONTH_YEAR)


# ===========================================================================
# Section 12: Regression — existing patterns must still work
# ===========================================================================

class TestRegressionExistingPatterns:
    """Verify already-working patterns are not broken by new method."""

    def test_oct_2023_month_year(self):
        result = extract_explicit_dates('Oct 2023')
        assert result and result.get('Oct 2023') == MONTH_YEAR

    def test_october_2023_month_year(self):
        result = extract_explicit_dates('October 2023')
        assert result and result.get('October 2023') == MONTH_YEAR

    def test_march_2024_month_year(self):
        result = extract_explicit_dates('March 2024')
        assert result and result.get('March 2024') == MONTH_YEAR

    def test_oct_hyphen_23_month_year(self):
        result = extract_explicit_dates('Oct-23')
        assert result and result.get('Oct-23') == MONTH_YEAR

    def test_march_15_2024_full_date(self):
        result = extract_explicit_dates('March 15, 2024')
        assert result

    def test_jan_15_2024_full_date(self):
        result = extract_explicit_dates('Jan 15, 2024')
        assert result

    def test_numeric_slash_date(self):
        result = extract_explicit_dates('03/15/2024')
        assert result

    def test_iso_date(self):
        result = extract_explicit_dates('2024-03-15')
        assert result


# ===========================================================================
# Section 13: Non-matching / negative cases
# ===========================================================================

class TestNegativeCases:
    """Inputs that should NOT be matched by the new pattern."""

    def test_bare_month_name_only(self):
        # No number following
        result = extract_explicit_dates('October')
        assert not result or 'October' not in result

    def test_month_with_4digit_year(self):
        # 4-digit already handled by existing pipeline — don't double-count
        result = extract_explicit_dates('Oct 2023')
        # Should exist but as MONTH_YEAR from the existing pipeline
        assert result and result.get('Oct 2023') == MONTH_YEAR

    def test_number_only(self):
        result = extract_explicit_dates('23')
        assert not result or '23' not in result

    def test_non_month_word_number(self):
        # "Foo 23" should not match
        result = extract_explicit_dates('Foo 23')
        assert not result or 'Foo 23' not in result

    def test_three_digit_number(self):
        # "Oct 123" — 3 digits, out of scope for this pattern
        result = extract_explicit_dates('Oct 123')
        assert not result or result.get('Oct 123') not in (DAY_MONTH_AMBIGUOUS, MONTH_YEAR)

    def test_year_before_month(self):
        # "23 Oct" reversed order — not in scope for this issue
        result = extract_explicit_dates('23 Oct')
        # Should not be classified by the new method (may be handled elsewhere or not at all)
        if result:
            assert result.get('23 Oct') != DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 14: Additional abbreviated month coverage (all months, NN=23)
# ===========================================================================

class TestAllAbbrevMonthsNN23Ambiguous:
    """All 13 abbreviated forms with NN=23 (≤31, no preposition) → AMBIGUOUS."""

    def test_jan_23_ambiguous(self):
        result = extract_explicit_dates('Jan 23')
        assert result and result.get('Jan 23') == DAY_MONTH_AMBIGUOUS

    def test_feb_23_ambiguous(self):
        result = extract_explicit_dates('Feb 23')
        assert result and result.get('Feb 23') == DAY_MONTH_AMBIGUOUS

    def test_mar_23_ambiguous(self):
        result = extract_explicit_dates('Mar 23')
        assert result and result.get('Mar 23') == DAY_MONTH_AMBIGUOUS

    def test_apr_23_ambiguous(self):
        result = extract_explicit_dates('Apr 23')
        assert result and result.get('Apr 23') == DAY_MONTH_AMBIGUOUS

    def test_may_23_ambiguous(self):
        result = extract_explicit_dates('May 23')
        assert result and result.get('May 23') == DAY_MONTH_AMBIGUOUS

    def test_jun_23_ambiguous(self):
        result = extract_explicit_dates('Jun 23')
        assert result and result.get('Jun 23') == DAY_MONTH_AMBIGUOUS

    def test_jul_23_ambiguous(self):
        result = extract_explicit_dates('Jul 23')
        assert result and result.get('Jul 23') == DAY_MONTH_AMBIGUOUS

    def test_aug_23_ambiguous(self):
        result = extract_explicit_dates('Aug 23')
        assert result and result.get('Aug 23') == DAY_MONTH_AMBIGUOUS

    def test_sep_23_ambiguous(self):
        result = extract_explicit_dates('Sep 23')
        assert result and result.get('Sep 23') == DAY_MONTH_AMBIGUOUS

    def test_sept_23_ambiguous(self):
        result = extract_explicit_dates('Sept 23')
        assert result and result.get('Sept 23') == DAY_MONTH_AMBIGUOUS

    def test_oct_23_ambiguous(self):
        result = extract_explicit_dates('Oct 23')
        assert result and result.get('Oct 23') == DAY_MONTH_AMBIGUOUS

    def test_nov_23_ambiguous(self):
        result = extract_explicit_dates('Nov 23')
        assert result and result.get('Nov 23') == DAY_MONTH_AMBIGUOUS

    def test_dec_23_ambiguous(self):
        result = extract_explicit_dates('Dec 23')
        assert result and result.get('Dec 23') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 15: All full month names, NN=23 → AMBIGUOUS
# ===========================================================================

class TestAllFullMonthsNN23Ambiguous:
    """All 12 full month names with NN=23 (≤31, no preposition) → AMBIGUOUS."""

    def test_january_23(self):
        result = extract_explicit_dates('January 23')
        assert result and result.get('January 23') == DAY_MONTH_AMBIGUOUS

    def test_february_23(self):
        result = extract_explicit_dates('February 23')
        assert result and result.get('February 23') == DAY_MONTH_AMBIGUOUS

    def test_march_23(self):
        result = extract_explicit_dates('March 23')
        assert result and result.get('March 23') == DAY_MONTH_AMBIGUOUS

    def test_april_23(self):
        result = extract_explicit_dates('April 23')
        assert result and result.get('April 23') == DAY_MONTH_AMBIGUOUS

    def test_may_23(self):
        result = extract_explicit_dates('May 23')
        assert result and result.get('May 23') == DAY_MONTH_AMBIGUOUS

    def test_june_23(self):
        result = extract_explicit_dates('June 23')
        assert result and result.get('June 23') == DAY_MONTH_AMBIGUOUS

    def test_july_23(self):
        result = extract_explicit_dates('July 23')
        assert result and result.get('July 23') == DAY_MONTH_AMBIGUOUS

    def test_august_23(self):
        result = extract_explicit_dates('August 23')
        assert result and result.get('August 23') == DAY_MONTH_AMBIGUOUS

    def test_september_23(self):
        result = extract_explicit_dates('September 23')
        assert result and result.get('September 23') == DAY_MONTH_AMBIGUOUS

    def test_october_23(self):
        result = extract_explicit_dates('October 23')
        assert result and result.get('October 23') == DAY_MONTH_AMBIGUOUS

    def test_november_23(self):
        result = extract_explicit_dates('November 23')
        assert result and result.get('November 23') == DAY_MONTH_AMBIGUOUS

    def test_december_23(self):
        result = extract_explicit_dates('December 23')
        assert result and result.get('December 23') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 16: All full month names, NN=99 → MONTH_YEAR
# ===========================================================================

class TestAllFullMonthsNN99Year:
    """All 12 full month names with NN=99 (>31) → MONTH_YEAR."""

    def test_january_99(self):
        result = extract_explicit_dates('January 99')
        assert result and result.get('January 99') == MONTH_YEAR

    def test_february_99(self):
        result = extract_explicit_dates('February 99')
        assert result and result.get('February 99') == MONTH_YEAR

    def test_march_99(self):
        result = extract_explicit_dates('March 99')
        assert result and result.get('March 99') == MONTH_YEAR

    def test_april_99(self):
        result = extract_explicit_dates('April 99')
        assert result and result.get('April 99') == MONTH_YEAR

    def test_may_99(self):
        result = extract_explicit_dates('May 99')
        assert result and result.get('May 99') == MONTH_YEAR

    def test_june_99(self):
        result = extract_explicit_dates('June 99')
        assert result and result.get('June 99') == MONTH_YEAR

    def test_july_99(self):
        result = extract_explicit_dates('July 99')
        assert result and result.get('July 99') == MONTH_YEAR

    def test_august_99(self):
        result = extract_explicit_dates('August 99')
        assert result and result.get('August 99') == MONTH_YEAR

    def test_september_99(self):
        result = extract_explicit_dates('September 99')
        assert result and result.get('September 99') == MONTH_YEAR

    def test_october_99(self):
        result = extract_explicit_dates('October 99')
        assert result and result.get('October 99') == MONTH_YEAR

    def test_november_99(self):
        result = extract_explicit_dates('November 99')
        assert result and result.get('November 99') == MONTH_YEAR

    def test_december_99(self):
        result = extract_explicit_dates('December 99')
        assert result and result.get('December 99') == MONTH_YEAR


# ===========================================================================
# Section 17: "in" preposition — all months NN=15 → MONTH_YEAR
# ===========================================================================

class TestInPrepAllMonthsNN15:
    """'in <all-months> 15' → MONTH_YEAR."""

    def test_in_jan_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Jan 15') or {}).values()
    def test_in_feb_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Feb 15') or {}).values()
    def test_in_mar_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Mar 15') or {}).values()
    def test_in_apr_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Apr 15') or {}).values()
    def test_in_may_15(self): assert MONTH_YEAR in (extract_explicit_dates('in May 15') or {}).values()
    def test_in_jun_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Jun 15') or {}).values()
    def test_in_jul_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Jul 15') or {}).values()
    def test_in_aug_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Aug 15') or {}).values()
    def test_in_sep_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Sep 15') or {}).values()
    def test_in_sept_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Sept 15') or {}).values()
    def test_in_oct_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Oct 15') or {}).values()
    def test_in_nov_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Nov 15') or {}).values()
    def test_in_dec_15(self): assert MONTH_YEAR in (extract_explicit_dates('in Dec 15') or {}).values()
    def test_in_january_15(self): assert MONTH_YEAR in (extract_explicit_dates('in January 15') or {}).values()
    def test_in_february_15(self): assert MONTH_YEAR in (extract_explicit_dates('in February 15') or {}).values()
    def test_in_march_15(self): assert MONTH_YEAR in (extract_explicit_dates('in March 15') or {}).values()
    def test_in_april_15(self): assert MONTH_YEAR in (extract_explicit_dates('in April 15') or {}).values()
    def test_in_june_15(self): assert MONTH_YEAR in (extract_explicit_dates('in June 15') or {}).values()
    def test_in_july_15(self): assert MONTH_YEAR in (extract_explicit_dates('in July 15') or {}).values()
    def test_in_august_15(self): assert MONTH_YEAR in (extract_explicit_dates('in August 15') or {}).values()
    def test_in_september_15(self): assert MONTH_YEAR in (extract_explicit_dates('in September 15') or {}).values()
    def test_in_october_15(self): assert MONTH_YEAR in (extract_explicit_dates('in October 15') or {}).values()
    def test_in_november_15(self): assert MONTH_YEAR in (extract_explicit_dates('in November 15') or {}).values()
    def test_in_december_15(self): assert MONTH_YEAR in (extract_explicit_dates('in December 15') or {}).values()


# ===========================================================================
# Section 18: "on" preposition — all months NN=15 → DAY_MONTH
# ===========================================================================

class TestOnPrepAllMonthsNN15:
    """'on <all-months> 15' → DAY_MONTH."""

    def test_on_jan_15(self): assert DAY_MONTH in (extract_explicit_dates('on Jan 15') or {}).values()
    def test_on_feb_15(self): assert DAY_MONTH in (extract_explicit_dates('on Feb 15') or {}).values()
    def test_on_mar_15(self): assert DAY_MONTH in (extract_explicit_dates('on Mar 15') or {}).values()
    def test_on_apr_15(self): assert DAY_MONTH in (extract_explicit_dates('on Apr 15') or {}).values()
    def test_on_may_15(self): assert DAY_MONTH in (extract_explicit_dates('on May 15') or {}).values()
    def test_on_jun_15(self): assert DAY_MONTH in (extract_explicit_dates('on Jun 15') or {}).values()
    def test_on_jul_15(self): assert DAY_MONTH in (extract_explicit_dates('on Jul 15') or {}).values()
    def test_on_aug_15(self): assert DAY_MONTH in (extract_explicit_dates('on Aug 15') or {}).values()
    def test_on_sep_15(self): assert DAY_MONTH in (extract_explicit_dates('on Sep 15') or {}).values()
    def test_on_sept_15(self): assert DAY_MONTH in (extract_explicit_dates('on Sept 15') or {}).values()
    def test_on_oct_15(self): assert DAY_MONTH in (extract_explicit_dates('on Oct 15') or {}).values()
    def test_on_nov_15(self): assert DAY_MONTH in (extract_explicit_dates('on Nov 15') or {}).values()
    def test_on_dec_15(self): assert DAY_MONTH in (extract_explicit_dates('on Dec 15') or {}).values()
    def test_on_january_15(self): assert DAY_MONTH in (extract_explicit_dates('on January 15') or {}).values()
    def test_on_february_15(self): assert DAY_MONTH in (extract_explicit_dates('on February 15') or {}).values()
    def test_on_march_15(self): assert DAY_MONTH in (extract_explicit_dates('on March 15') or {}).values()
    def test_on_april_15(self): assert DAY_MONTH in (extract_explicit_dates('on April 15') or {}).values()
    def test_on_june_15(self): assert DAY_MONTH in (extract_explicit_dates('on June 15') or {}).values()
    def test_on_july_15(self): assert DAY_MONTH in (extract_explicit_dates('on July 15') or {}).values()
    def test_on_august_15(self): assert DAY_MONTH in (extract_explicit_dates('on August 15') or {}).values()
    def test_on_september_15(self): assert DAY_MONTH in (extract_explicit_dates('on September 15') or {}).values()
    def test_on_october_15(self): assert DAY_MONTH in (extract_explicit_dates('on October 15') or {}).values()
    def test_on_november_15(self): assert DAY_MONTH in (extract_explicit_dates('on November 15') or {}).values()
    def test_on_december_15(self): assert DAY_MONTH in (extract_explicit_dates('on December 15') or {}).values()


# ===========================================================================
# Section 19: "on" prep — all abbreviated months NN=23 → DAY_MONTH
# ===========================================================================

class TestOnPrepAllAbbrevMonthsNN23:
    """'on <abbrev-month> 23' → DAY_MONTH (23 ≤ 31, so preposition decides)."""

    def test_on_jan_23(self): assert DAY_MONTH in (extract_explicit_dates('on Jan 23') or {}).values()
    def test_on_feb_23(self): assert DAY_MONTH in (extract_explicit_dates('on Feb 23') or {}).values()
    def test_on_mar_23(self): assert DAY_MONTH in (extract_explicit_dates('on Mar 23') or {}).values()
    def test_on_apr_23(self): assert DAY_MONTH in (extract_explicit_dates('on Apr 23') or {}).values()
    def test_on_may_23(self): assert DAY_MONTH in (extract_explicit_dates('on May 23') or {}).values()
    def test_on_jun_23(self): assert DAY_MONTH in (extract_explicit_dates('on Jun 23') or {}).values()
    def test_on_jul_23(self): assert DAY_MONTH in (extract_explicit_dates('on Jul 23') or {}).values()
    def test_on_aug_23(self): assert DAY_MONTH in (extract_explicit_dates('on Aug 23') or {}).values()
    def test_on_sep_23(self): assert DAY_MONTH in (extract_explicit_dates('on Sep 23') or {}).values()
    def test_on_sept_23(self): assert DAY_MONTH in (extract_explicit_dates('on Sept 23') or {}).values()
    def test_on_oct_23(self): assert DAY_MONTH in (extract_explicit_dates('on Oct 23') or {}).values()
    def test_on_nov_23(self): assert DAY_MONTH in (extract_explicit_dates('on Nov 23') or {}).values()
    def test_on_dec_23(self): assert DAY_MONTH in (extract_explicit_dates('on Dec 23') or {}).values()


# ===========================================================================
# Section 20: "in" prep — all abbreviated months NN=23 → MONTH_YEAR
# ===========================================================================

class TestInPrepAllAbbrevMonthsNN23:
    """'in <abbrev-month> 23' → MONTH_YEAR (preposition decides for NN ≤ 31)."""

    def test_in_jan_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Jan 23') or {}).values()
    def test_in_feb_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Feb 23') or {}).values()
    def test_in_mar_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Mar 23') or {}).values()
    def test_in_apr_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Apr 23') or {}).values()
    def test_in_may_23(self): assert MONTH_YEAR in (extract_explicit_dates('in May 23') or {}).values()
    def test_in_jun_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Jun 23') or {}).values()
    def test_in_jul_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Jul 23') or {}).values()
    def test_in_aug_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Aug 23') or {}).values()
    def test_in_sep_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Sep 23') or {}).values()
    def test_in_sept_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Sept 23') or {}).values()
    def test_in_oct_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Oct 23') or {}).values()
    def test_in_nov_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Nov 23') or {}).values()
    def test_in_dec_23(self): assert MONTH_YEAR in (extract_explicit_dates('in Dec 23') or {}).values()


# ===========================================================================
# Section 21: Bare abbreviated months NN=07 → DAY_MONTH_AMBIGUOUS
# ===========================================================================

class TestBareAbbrevMonthsNN07:
    """'<abbrev-month> 07' (no preposition, NN ≤ 31) → DAY_MONTH_AMBIGUOUS."""

    def test_jan_07(self): assert (extract_explicit_dates('Jan 07') or {}).get('Jan 07') == DAY_MONTH_AMBIGUOUS
    def test_feb_07(self): assert (extract_explicit_dates('Feb 07') or {}).get('Feb 07') == DAY_MONTH_AMBIGUOUS
    def test_mar_07(self): assert (extract_explicit_dates('Mar 07') or {}).get('Mar 07') == DAY_MONTH_AMBIGUOUS
    def test_apr_07(self): assert (extract_explicit_dates('Apr 07') or {}).get('Apr 07') == DAY_MONTH_AMBIGUOUS
    def test_may_07(self): assert (extract_explicit_dates('May 07') or {}).get('May 07') == DAY_MONTH_AMBIGUOUS
    def test_jun_07(self): assert (extract_explicit_dates('Jun 07') or {}).get('Jun 07') == DAY_MONTH_AMBIGUOUS
    def test_jul_07(self): assert (extract_explicit_dates('Jul 07') or {}).get('Jul 07') == DAY_MONTH_AMBIGUOUS
    def test_aug_07(self): assert (extract_explicit_dates('Aug 07') or {}).get('Aug 07') == DAY_MONTH_AMBIGUOUS
    def test_sep_07(self): assert (extract_explicit_dates('Sep 07') or {}).get('Sep 07') == DAY_MONTH_AMBIGUOUS
    def test_sept_07(self): assert (extract_explicit_dates('Sept 07') or {}).get('Sept 07') == DAY_MONTH_AMBIGUOUS
    def test_oct_07(self): assert (extract_explicit_dates('Oct 07') or {}).get('Oct 07') == DAY_MONTH_AMBIGUOUS
    def test_nov_07(self): assert (extract_explicit_dates('Nov 07') or {}).get('Nov 07') == DAY_MONTH_AMBIGUOUS
    def test_dec_07(self): assert (extract_explicit_dates('Dec 07') or {}).get('Dec 07') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 22: Bare full months NN=07 → DAY_MONTH_AMBIGUOUS
# ===========================================================================

class TestBareFullMonthsNN07:
    """'<full-month> 07' (no preposition, NN ≤ 31) → DAY_MONTH_AMBIGUOUS."""

    def test_january_07(self): assert (extract_explicit_dates('January 07') or {}).get('January 07') == DAY_MONTH_AMBIGUOUS
    def test_february_07(self): assert (extract_explicit_dates('February 07') or {}).get('February 07') == DAY_MONTH_AMBIGUOUS
    def test_march_07(self): assert (extract_explicit_dates('March 07') or {}).get('March 07') == DAY_MONTH_AMBIGUOUS
    def test_april_07(self): assert (extract_explicit_dates('April 07') or {}).get('April 07') == DAY_MONTH_AMBIGUOUS
    def test_may_07(self): assert (extract_explicit_dates('May 07') or {}).get('May 07') == DAY_MONTH_AMBIGUOUS
    def test_june_07(self): assert (extract_explicit_dates('June 07') or {}).get('June 07') == DAY_MONTH_AMBIGUOUS
    def test_july_07(self): assert (extract_explicit_dates('July 07') or {}).get('July 07') == DAY_MONTH_AMBIGUOUS
    def test_august_07(self): assert (extract_explicit_dates('August 07') or {}).get('August 07') == DAY_MONTH_AMBIGUOUS
    def test_september_07(self): assert (extract_explicit_dates('September 07') or {}).get('September 07') == DAY_MONTH_AMBIGUOUS
    def test_october_07(self): assert (extract_explicit_dates('October 07') or {}).get('October 07') == DAY_MONTH_AMBIGUOUS
    def test_november_07(self): assert (extract_explicit_dates('November 07') or {}).get('November 07') == DAY_MONTH_AMBIGUOUS
    def test_december_07(self): assert (extract_explicit_dates('December 07') or {}).get('December 07') == DAY_MONTH_AMBIGUOUS


# ===========================================================================
# Section 23: "on" prep — all full months NN=23 → DAY_MONTH
# ===========================================================================

class TestOnPrepAllFullMonthsNN23:
    """'on <full-month> 23' → DAY_MONTH (preposition decides)."""

    def test_on_january_23(self): assert DAY_MONTH in (extract_explicit_dates('on January 23') or {}).values()
    def test_on_february_23(self): assert DAY_MONTH in (extract_explicit_dates('on February 23') or {}).values()
    def test_on_march_23(self): assert DAY_MONTH in (extract_explicit_dates('on March 23') or {}).values()
    def test_on_april_23(self): assert DAY_MONTH in (extract_explicit_dates('on April 23') or {}).values()
    def test_on_may_23(self): assert DAY_MONTH in (extract_explicit_dates('on May 23') or {}).values()
    def test_on_june_23(self): assert DAY_MONTH in (extract_explicit_dates('on June 23') or {}).values()
    def test_on_july_23(self): assert DAY_MONTH in (extract_explicit_dates('on July 23') or {}).values()
    def test_on_august_23(self): assert DAY_MONTH in (extract_explicit_dates('on August 23') or {}).values()
    def test_on_september_23(self): assert DAY_MONTH in (extract_explicit_dates('on September 23') or {}).values()
    def test_on_october_23(self): assert DAY_MONTH in (extract_explicit_dates('on October 23') or {}).values()
    def test_on_november_23(self): assert DAY_MONTH in (extract_explicit_dates('on November 23') or {}).values()
    def test_on_december_23(self): assert DAY_MONTH in (extract_explicit_dates('on December 23') or {}).values()


# ===========================================================================
# Section 24: "in" prep — all full months NN=23 → MONTH_YEAR
# ===========================================================================

class TestInPrepAllFullMonthsNN23:
    """'in <full-month> 23' → MONTH_YEAR (preposition decides)."""

    def test_in_january_23(self): assert MONTH_YEAR in (extract_explicit_dates('in January 23') or {}).values()
    def test_in_february_23(self): assert MONTH_YEAR in (extract_explicit_dates('in February 23') or {}).values()
    def test_in_march_23(self): assert MONTH_YEAR in (extract_explicit_dates('in March 23') or {}).values()
    def test_in_april_23(self): assert MONTH_YEAR in (extract_explicit_dates('in April 23') or {}).values()
    def test_in_may_23(self): assert MONTH_YEAR in (extract_explicit_dates('in May 23') or {}).values()
    def test_in_june_23(self): assert MONTH_YEAR in (extract_explicit_dates('in June 23') or {}).values()
    def test_in_july_23(self): assert MONTH_YEAR in (extract_explicit_dates('in July 23') or {}).values()
    def test_in_august_23(self): assert MONTH_YEAR in (extract_explicit_dates('in August 23') or {}).values()
    def test_in_september_23(self): assert MONTH_YEAR in (extract_explicit_dates('in September 23') or {}).values()
    def test_in_october_23(self): assert MONTH_YEAR in (extract_explicit_dates('in October 23') or {}).values()
    def test_in_november_23(self): assert MONTH_YEAR in (extract_explicit_dates('in November 23') or {}).values()
    def test_in_december_23(self): assert MONTH_YEAR in (extract_explicit_dates('in December 23') or {}).values()
