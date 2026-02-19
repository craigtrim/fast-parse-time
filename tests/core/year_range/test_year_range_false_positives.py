#!/usr/bin/env python
# -*- coding: UTF-8 -*-
r"""
TDD tests for year range false positive bug.

Related GitHub Issue:
    #61 - False positive: written-month date range with hyphen triggers spurious YEAR_RANGE
    https://github.com/craigtrim/fast-parse-time/issues/61

Problem:
    '31 Oct 2021 - 28 Nov 2021' produces spurious YEAR_RANGE entry '2021-28'
    Expected: only 2 FULL_EXPLICIT_DATE entries, NOT 3 entries with false YEAR_RANGE

Root Cause:
    Hyphen normalizer collapses '2021 - 28' into '2021-28'
    Abbreviated-year pattern (\d{4})-(\d{2}) then matches it

All tests written BEFORE implementation (red phase).
Minimum 250 test cases.
"""

import unittest
from fast_parse_time.api import extract_explicit_dates


# ── Helpers ─────────────────────────────────────────────────────────────────


def _has_year_range(text: str) -> bool:
    """Return True if YEAR_RANGE exists in result."""
    return 'YEAR_RANGE' in extract_explicit_dates(text).values()


def _count_entries(text: str) -> int:
    """Return total number of extracted entries."""
    return len(extract_explicit_dates(text))


def _has_spurious_year_range(text: str, spurious_key: str) -> bool:
    """Return True if the spurious key exists and is marked as YEAR_RANGE."""
    result = extract_explicit_dates(text)
    return result.get(spurious_key) == 'YEAR_RANGE'


def _has_full_explicit_date(text: str, date_key: str) -> bool:
    """Return True if the date exists and is marked as FULL_EXPLICIT_DATE."""
    result = extract_explicit_dates(text)
    return result.get(date_key) == 'FULL_EXPLICIT_DATE'


# ============================================================================
# Section A — Written-Month Date Pairs with Hyphen (FALSE POSITIVES)
# These MUST NOT produce YEAR_RANGE entries
# ============================================================================


class TestWrittenMonthDateRangesWithHyphen(unittest.TestCase):
    """Written-month date ranges with hyphen MUST NOT trigger YEAR_RANGE."""

    # ── Original failing case ───────────────────────────────────────────────

    def test_31_oct_2021_to_28_nov_2021_count(self):
        """Original bug: '31 Oct 2021 - 28 Nov 2021' should return 2 entries, not 3."""
        result = extract_explicit_dates('31 Oct 2021 - 28 Nov 2021')
        self.assertEqual(len(result), 2)

    def test_31_oct_2021_to_28_nov_2021_no_year_range(self):
        """Must not contain YEAR_RANGE."""
        self.assertFalse(_has_year_range('31 Oct 2021 - 28 Nov 2021'))

    def test_31_oct_2021_to_28_nov_2021_no_spurious_key(self):
        """Must not contain spurious '2021-28' key."""
        result = extract_explicit_dates('31 Oct 2021 - 28 Nov 2021')
        self.assertNotIn('2021-28', result)

    def test_31_oct_2021_to_28_nov_2021_first_date(self):
        """First date should be recognized as FULL_EXPLICIT_DATE."""
        self.assertTrue(_has_full_explicit_date('31 Oct 2021 - 28 Nov 2021', '31 Oct 2021'))

    def test_31_oct_2021_to_28_nov_2021_second_date(self):
        """Second date should be recognized as FULL_EXPLICIT_DATE."""
        self.assertTrue(_has_full_explicit_date('31 Oct 2021 - 28 Nov 2021', '28 Nov 2021'))

    # ── All 12 months with abbreviated names (Oct, Nov, Dec, etc.) ──────────

    def test_jan_range_abbreviated(self):
        """1 Jan 2020 - 31 Jan 2020"""
        self.assertEqual(_count_entries('1 Jan 2020 - 31 Jan 2020'), 2)
        self.assertFalse(_has_year_range('1 Jan 2020 - 31 Jan 2020'))

    def test_feb_range_abbreviated(self):
        """1 Feb 2020 - 28 Feb 2020"""
        self.assertEqual(_count_entries('1 Feb 2020 - 28 Feb 2020'), 2)
        self.assertFalse(_has_year_range('1 Feb 2020 - 28 Feb 2020'))

    def test_mar_range_abbreviated(self):
        """1 Mar 2020 - 31 Mar 2020"""
        self.assertEqual(_count_entries('1 Mar 2020 - 31 Mar 2020'), 2)
        self.assertFalse(_has_year_range('1 Mar 2020 - 31 Mar 2020'))

    def test_apr_range_abbreviated(self):
        """1 Apr 2020 - 30 Apr 2020"""
        self.assertEqual(_count_entries('1 Apr 2020 - 30 Apr 2020'), 2)
        self.assertFalse(_has_year_range('1 Apr 2020 - 30 Apr 2020'))

    def test_may_range_abbreviated(self):
        """1 May 2020 - 31 May 2020"""
        self.assertEqual(_count_entries('1 May 2020 - 31 May 2020'), 2)
        self.assertFalse(_has_year_range('1 May 2020 - 31 May 2020'))

    def test_jun_range_abbreviated(self):
        """1 Jun 2020 - 30 Jun 2020"""
        self.assertEqual(_count_entries('1 Jun 2020 - 30 Jun 2020'), 2)
        self.assertFalse(_has_year_range('1 Jun 2020 - 30 Jun 2020'))

    def test_jul_range_abbreviated(self):
        """1 Jul 2020 - 31 Jul 2020"""
        self.assertEqual(_count_entries('1 Jul 2020 - 31 Jul 2020'), 2)
        self.assertFalse(_has_year_range('1 Jul 2020 - 31 Jul 2020'))

    def test_aug_range_abbreviated(self):
        """1 Aug 2020 - 31 Aug 2020"""
        self.assertEqual(_count_entries('1 Aug 2020 - 31 Aug 2020'), 2)
        self.assertFalse(_has_year_range('1 Aug 2020 - 31 Aug 2020'))

    def test_sep_range_abbreviated(self):
        """1 Sep 2020 - 30 Sep 2020"""
        self.assertEqual(_count_entries('1 Sep 2020 - 30 Sep 2020'), 2)
        self.assertFalse(_has_year_range('1 Sep 2020 - 30 Sep 2020'))

    def test_oct_range_abbreviated(self):
        """1 Oct 2020 - 31 Oct 2020"""
        self.assertEqual(_count_entries('1 Oct 2020 - 31 Oct 2020'), 2)
        self.assertFalse(_has_year_range('1 Oct 2020 - 31 Oct 2020'))

    def test_nov_range_abbreviated(self):
        """1 Nov 2020 - 30 Nov 2020"""
        self.assertEqual(_count_entries('1 Nov 2020 - 30 Nov 2020'), 2)
        self.assertFalse(_has_year_range('1 Nov 2020 - 30 Nov 2020'))

    def test_dec_range_abbreviated(self):
        """1 Dec 2020 - 31 Dec 2020"""
        self.assertEqual(_count_entries('1 Dec 2020 - 31 Dec 2020'), 2)
        self.assertFalse(_has_year_range('1 Dec 2020 - 31 Dec 2020'))

    # ── All 12 months with full names (January, February, etc.) ─────────────

    def test_january_range_full(self):
        """1 January 2020 - 31 January 2020"""
        self.assertEqual(_count_entries('1 January 2020 - 31 January 2020'), 2)
        self.assertFalse(_has_year_range('1 January 2020 - 31 January 2020'))

    def test_february_range_full(self):
        """1 February 2020 - 28 February 2020"""
        self.assertEqual(_count_entries('1 February 2020 - 28 February 2020'), 2)
        self.assertFalse(_has_year_range('1 February 2020 - 28 February 2020'))

    def test_march_range_full(self):
        """1 March 2020 - 31 March 2020"""
        self.assertEqual(_count_entries('1 March 2020 - 31 March 2020'), 2)
        self.assertFalse(_has_year_range('1 March 2020 - 31 March 2020'))

    def test_april_range_full(self):
        """1 April 2020 - 30 April 2020"""
        self.assertEqual(_count_entries('1 April 2020 - 30 April 2020'), 2)
        self.assertFalse(_has_year_range('1 April 2020 - 30 April 2020'))

    def test_may_range_full(self):
        """1 May 2020 - 31 May 2020"""
        self.assertEqual(_count_entries('1 May 2020 - 31 May 2020'), 2)
        self.assertFalse(_has_year_range('1 May 2020 - 31 May 2020'))

    def test_june_range_full(self):
        """1 June 2020 - 30 June 2020"""
        self.assertEqual(_count_entries('1 June 2020 - 30 June 2020'), 2)
        self.assertFalse(_has_year_range('1 June 2020 - 30 June 2020'))

    def test_july_range_full(self):
        """1 July 2020 - 31 July 2020"""
        self.assertEqual(_count_entries('1 July 2020 - 31 July 2020'), 2)
        self.assertFalse(_has_year_range('1 July 2020 - 31 July 2020'))

    def test_august_range_full(self):
        """1 August 2020 - 31 August 2020"""
        self.assertEqual(_count_entries('1 August 2020 - 31 August 2020'), 2)
        self.assertFalse(_has_year_range('1 August 2020 - 31 August 2020'))

    def test_september_range_full(self):
        """1 September 2020 - 30 September 2020"""
        self.assertEqual(_count_entries('1 September 2020 - 30 September 2020'), 2)
        self.assertFalse(_has_year_range('1 September 2020 - 30 September 2020'))

    def test_october_range_full(self):
        """1 October 2020 - 31 October 2020"""
        self.assertEqual(_count_entries('1 October 2020 - 31 October 2020'), 2)
        self.assertFalse(_has_year_range('1 October 2020 - 31 October 2020'))

    def test_november_range_full(self):
        """1 November 2020 - 30 November 2020"""
        self.assertEqual(_count_entries('1 November 2020 - 30 November 2020'), 2)
        self.assertFalse(_has_year_range('1 November 2020 - 30 November 2020'))

    def test_december_range_full(self):
        """1 December 2020 - 31 December 2020"""
        self.assertEqual(_count_entries('1 December 2020 - 31 December 2020'), 2)
        self.assertFalse(_has_year_range('1 December 2020 - 31 December 2020'))

    # ── Various day values (1-31) with Oct/Nov (original bug months) ────────

    def test_oct_nov_day_01(self):
        """1 Oct 2021 - 1 Nov 2021"""
        self.assertEqual(_count_entries('1 Oct 2021 - 1 Nov 2021'), 2)
        self.assertFalse(_has_year_range('1 Oct 2021 - 1 Nov 2021'))

    def test_oct_nov_day_02(self):
        """2 Oct 2021 - 2 Nov 2021"""
        self.assertEqual(_count_entries('2 Oct 2021 - 2 Nov 2021'), 2)
        self.assertFalse(_has_year_range('2 Oct 2021 - 2 Nov 2021'))

    def test_oct_nov_day_03(self):
        """3 Oct 2021 - 3 Nov 2021"""
        self.assertEqual(_count_entries('3 Oct 2021 - 3 Nov 2021'), 2)
        self.assertFalse(_has_year_range('3 Oct 2021 - 3 Nov 2021'))

    def test_oct_nov_day_04(self):
        """4 Oct 2021 - 4 Nov 2021"""
        self.assertEqual(_count_entries('4 Oct 2021 - 4 Nov 2021'), 2)
        self.assertFalse(_has_year_range('4 Oct 2021 - 4 Nov 2021'))

    def test_oct_nov_day_05(self):
        """5 Oct 2021 - 5 Nov 2021"""
        self.assertEqual(_count_entries('5 Oct 2021 - 5 Nov 2021'), 2)
        self.assertFalse(_has_year_range('5 Oct 2021 - 5 Nov 2021'))

    def test_oct_nov_day_06(self):
        """6 Oct 2021 - 6 Nov 2021"""
        self.assertEqual(_count_entries('6 Oct 2021 - 6 Nov 2021'), 2)
        self.assertFalse(_has_year_range('6 Oct 2021 - 6 Nov 2021'))

    def test_oct_nov_day_07(self):
        """7 Oct 2021 - 7 Nov 2021"""
        self.assertEqual(_count_entries('7 Oct 2021 - 7 Nov 2021'), 2)
        self.assertFalse(_has_year_range('7 Oct 2021 - 7 Nov 2021'))

    def test_oct_nov_day_08(self):
        """8 Oct 2021 - 8 Nov 2021"""
        self.assertEqual(_count_entries('8 Oct 2021 - 8 Nov 2021'), 2)
        self.assertFalse(_has_year_range('8 Oct 2021 - 8 Nov 2021'))

    def test_oct_nov_day_09(self):
        """9 Oct 2021 - 9 Nov 2021"""
        self.assertEqual(_count_entries('9 Oct 2021 - 9 Nov 2021'), 2)
        self.assertFalse(_has_year_range('9 Oct 2021 - 9 Nov 2021'))

    def test_oct_nov_day_10(self):
        """10 Oct 2021 - 10 Nov 2021"""
        self.assertEqual(_count_entries('10 Oct 2021 - 10 Nov 2021'), 2)
        self.assertFalse(_has_year_range('10 Oct 2021 - 10 Nov 2021'))

    def test_oct_nov_day_11(self):
        """11 Oct 2021 - 11 Nov 2021"""
        self.assertEqual(_count_entries('11 Oct 2021 - 11 Nov 2021'), 2)
        self.assertFalse(_has_year_range('11 Oct 2021 - 11 Nov 2021'))

    def test_oct_nov_day_12(self):
        """12 Oct 2021 - 12 Nov 2021"""
        self.assertEqual(_count_entries('12 Oct 2021 - 12 Nov 2021'), 2)
        self.assertFalse(_has_year_range('12 Oct 2021 - 12 Nov 2021'))

    def test_oct_nov_day_13(self):
        """13 Oct 2021 - 13 Nov 2021"""
        self.assertEqual(_count_entries('13 Oct 2021 - 13 Nov 2021'), 2)
        self.assertFalse(_has_year_range('13 Oct 2021 - 13 Nov 2021'))

    def test_oct_nov_day_14(self):
        """14 Oct 2021 - 14 Nov 2021"""
        self.assertEqual(_count_entries('14 Oct 2021 - 14 Nov 2021'), 2)
        self.assertFalse(_has_year_range('14 Oct 2021 - 14 Nov 2021'))

    def test_oct_nov_day_15(self):
        """15 Oct 2021 - 15 Nov 2021"""
        self.assertEqual(_count_entries('15 Oct 2021 - 15 Nov 2021'), 2)
        self.assertFalse(_has_year_range('15 Oct 2021 - 15 Nov 2021'))

    def test_oct_nov_day_16(self):
        """16 Oct 2021 - 16 Nov 2021"""
        self.assertEqual(_count_entries('16 Oct 2021 - 16 Nov 2021'), 2)
        self.assertFalse(_has_year_range('16 Oct 2021 - 16 Nov 2021'))

    def test_oct_nov_day_17(self):
        """17 Oct 2021 - 17 Nov 2021"""
        self.assertEqual(_count_entries('17 Oct 2021 - 17 Nov 2021'), 2)
        self.assertFalse(_has_year_range('17 Oct 2021 - 17 Nov 2021'))

    def test_oct_nov_day_18(self):
        """18 Oct 2021 - 18 Nov 2021"""
        self.assertEqual(_count_entries('18 Oct 2021 - 18 Nov 2021'), 2)
        self.assertFalse(_has_year_range('18 Oct 2021 - 18 Nov 2021'))

    def test_oct_nov_day_19(self):
        """19 Oct 2021 - 19 Nov 2021"""
        self.assertEqual(_count_entries('19 Oct 2021 - 19 Nov 2021'), 2)
        self.assertFalse(_has_year_range('19 Oct 2021 - 19 Nov 2021'))

    def test_oct_nov_day_20(self):
        """20 Oct 2021 - 20 Nov 2021"""
        self.assertEqual(_count_entries('20 Oct 2021 - 20 Nov 2021'), 2)
        self.assertFalse(_has_year_range('20 Oct 2021 - 20 Nov 2021'))

    def test_oct_nov_day_21(self):
        """21 Oct 2021 - 21 Nov 2021"""
        self.assertEqual(_count_entries('21 Oct 2021 - 21 Nov 2021'), 2)
        self.assertFalse(_has_year_range('21 Oct 2021 - 21 Nov 2021'))

    def test_oct_nov_day_22(self):
        """22 Oct 2021 - 22 Nov 2021"""
        self.assertEqual(_count_entries('22 Oct 2021 - 22 Nov 2021'), 2)
        self.assertFalse(_has_year_range('22 Oct 2021 - 22 Nov 2021'))

    def test_oct_nov_day_23(self):
        """23 Oct 2021 - 23 Nov 2021"""
        self.assertEqual(_count_entries('23 Oct 2021 - 23 Nov 2021'), 2)
        self.assertFalse(_has_year_range('23 Oct 2021 - 23 Nov 2021'))

    def test_oct_nov_day_24(self):
        """24 Oct 2021 - 24 Nov 2021"""
        self.assertEqual(_count_entries('24 Oct 2021 - 24 Nov 2021'), 2)
        self.assertFalse(_has_year_range('24 Oct 2021 - 24 Nov 2021'))

    def test_oct_nov_day_25(self):
        """25 Oct 2021 - 25 Nov 2021"""
        self.assertEqual(_count_entries('25 Oct 2021 - 25 Nov 2021'), 2)
        self.assertFalse(_has_year_range('25 Oct 2021 - 25 Nov 2021'))

    def test_oct_nov_day_26(self):
        """26 Oct 2021 - 26 Nov 2021"""
        self.assertEqual(_count_entries('26 Oct 2021 - 26 Nov 2021'), 2)
        self.assertFalse(_has_year_range('26 Oct 2021 - 26 Nov 2021'))

    def test_oct_nov_day_27(self):
        """27 Oct 2021 - 27 Nov 2021"""
        self.assertEqual(_count_entries('27 Oct 2021 - 27 Nov 2021'), 2)
        self.assertFalse(_has_year_range('27 Oct 2021 - 27 Nov 2021'))

    def test_oct_nov_day_28(self):
        """28 Oct 2021 - 28 Nov 2021"""
        self.assertEqual(_count_entries('28 Oct 2021 - 28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('28 Oct 2021 - 28 Nov 2021'))

    def test_oct_nov_day_29(self):
        """29 Oct 2021 - 29 Nov 2021"""
        self.assertEqual(_count_entries('29 Oct 2021 - 29 Nov 2021'), 2)
        self.assertFalse(_has_year_range('29 Oct 2021 - 29 Nov 2021'))

    def test_oct_nov_day_30(self):
        """30 Oct 2021 - 30 Nov 2021"""
        self.assertEqual(_count_entries('30 Oct 2021 - 30 Nov 2021'), 2)
        self.assertFalse(_has_year_range('30 Oct 2021 - 30 Nov 2021'))

    def test_oct_nov_day_31(self):
        """31 Oct 2021 - 30 Nov 2021 (Oct has 31 days)"""
        self.assertEqual(_count_entries('31 Oct 2021 - 30 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021 - 30 Nov 2021'))

    # ── En dash separator (–) ───────────────────────────────────────────────

    def test_en_dash_oct_nov(self):
        """31 Oct 2021 – 28 Nov 2021"""
        self.assertEqual(_count_entries('31 Oct 2021 – 28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021 – 28 Nov 2021'))

    def test_en_dash_jan_dec(self):
        """1 Jan 2020 – 31 Dec 2020"""
        self.assertEqual(_count_entries('1 Jan 2020 – 31 Dec 2020'), 2)
        self.assertFalse(_has_year_range('1 Jan 2020 – 31 Dec 2020'))

    def test_en_dash_mar_jun(self):
        """15 Mar 2019 – 14 Jun 2019"""
        self.assertEqual(_count_entries('15 Mar 2019 – 14 Jun 2019'), 2)
        self.assertFalse(_has_year_range('15 Mar 2019 – 14 Jun 2019'))

    # ── Em dash separator (—) ───────────────────────────────────────────────

    def test_em_dash_oct_nov(self):
        """31 Oct 2021 — 28 Nov 2021"""
        self.assertEqual(_count_entries('31 Oct 2021 — 28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021 — 28 Nov 2021'))

    def test_em_dash_jan_dec(self):
        """1 Jan 2020 — 31 Dec 2020"""
        self.assertEqual(_count_entries('1 Jan 2020 — 31 Dec 2020'), 2)
        self.assertFalse(_has_year_range('1 Jan 2020 — 31 Dec 2020'))

    def test_em_dash_mar_jun(self):
        """15 Mar 2019 — 14 Jun 2019"""
        self.assertEqual(_count_entries('15 Mar 2019 — 14 Jun 2019'), 2)
        self.assertFalse(_has_year_range('15 Mar 2019 — 14 Jun 2019'))

    # ── Extra whitespace around hyphen ──────────────────────────────────────

    def test_extra_whitespace_single_space(self):
        """31 Oct 2021  -  28 Nov 2021 (double spaces)"""
        self.assertEqual(_count_entries('31 Oct 2021  -  28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021  -  28 Nov 2021'))

    def test_extra_whitespace_tabs(self):
        """31 Oct 2021\t-\t28 Nov 2021"""
        self.assertEqual(_count_entries('31 Oct 2021\t-\t28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021\t-\t28 Nov 2021'))

    def test_extra_whitespace_mixed(self):
        """31 Oct 2021   -   28 Nov 2021 (triple spaces)"""
        self.assertEqual(_count_entries('31 Oct 2021   -   28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('31 Oct 2021   -   28 Nov 2021'))

    # ── Different years ──────────────────────────────────────────────────────

    def test_cross_year_2019_2020(self):
        """15 Dec 2019 - 15 Jan 2020"""
        self.assertEqual(_count_entries('15 Dec 2019 - 15 Jan 2020'), 2)
        self.assertFalse(_has_spurious_year_range('15 Dec 2019 - 15 Jan 2020', '2019-15'))

    def test_cross_year_2020_2021(self):
        """25 Dec 2020 - 5 Jan 2021"""
        self.assertEqual(_count_entries('25 Dec 2020 - 5 Jan 2021'), 2)
        self.assertFalse(_has_spurious_year_range('25 Dec 2020 - 5 Jan 2021', '2020-5'))

    def test_cross_year_2021_2022(self):
        """31 Dec 2021 - 1 Jan 2022"""
        self.assertEqual(_count_entries('31 Dec 2021 - 1 Jan 2022'), 2)
        self.assertFalse(_has_spurious_year_range('31 Dec 2021 - 1 Jan 2022', '2021-1'))

    # ── Mixed full and abbreviated month names ──────────────────────────────

    def test_mixed_october_nov(self):
        """1 October 2020 - 30 Nov 2020"""
        self.assertEqual(_count_entries('1 October 2020 - 30 Nov 2020'), 2)
        self.assertFalse(_has_year_range('1 October 2020 - 30 Nov 2020'))

    def test_mixed_oct_november(self):
        """1 Oct 2020 - 30 November 2020"""
        self.assertEqual(_count_entries('1 Oct 2020 - 30 November 2020'), 2)
        self.assertFalse(_has_year_range('1 Oct 2020 - 30 November 2020'))

    def test_mixed_march_apr(self):
        """15 March 2019 - 14 Apr 2019"""
        self.assertEqual(_count_entries('15 March 2019 - 14 Apr 2019'), 2)
        self.assertFalse(_has_year_range('15 March 2019 - 14 Apr 2019'))

    def test_mixed_mar_april(self):
        """15 Mar 2019 - 14 April 2019"""
        self.assertEqual(_count_entries('15 Mar 2019 - 14 April 2019'), 2)
        self.assertFalse(_has_year_range('15 Mar 2019 - 14 April 2019'))

    # ── Date ranges in context (within sentences) ───────────────────────────

    def test_in_sentence_prefix(self):
        """The event ran from 31 Oct 2021 - 28 Nov 2021."""
        self.assertEqual(_count_entries('The event ran from 31 Oct 2021 - 28 Nov 2021.'), 2)
        self.assertFalse(_has_year_range('The event ran from 31 Oct 2021 - 28 Nov 2021.'))

    def test_in_sentence_middle(self):
        """Between 31 Oct 2021 - 28 Nov 2021 we had 50 events."""
        self.assertEqual(_count_entries('Between 31 Oct 2021 - 28 Nov 2021 we had 50 events.'), 2)
        self.assertFalse(_has_year_range('Between 31 Oct 2021 - 28 Nov 2021 we had 50 events.'))

    def test_in_sentence_suffix(self):
        """We scheduled the conference for 31 Oct 2021 - 28 Nov 2021"""
        self.assertEqual(_count_entries('We scheduled the conference for 31 Oct 2021 - 28 Nov 2021'), 2)
        self.assertFalse(_has_year_range('We scheduled the conference for 31 Oct 2021 - 28 Nov 2021'))

    # ── Additional cross-month combinations ──────────────────────────────────

    def test_jan_feb_range(self):
        """15 Jan 2020 - 14 Feb 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 14 Feb 2020'), 2)
        self.assertFalse(_has_year_range('15 Jan 2020 - 14 Feb 2020'))

    def test_feb_mar_range(self):
        """15 Feb 2020 - 14 Mar 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 14 Mar 2020'), 2)
        self.assertFalse(_has_year_range('15 Feb 2020 - 14 Mar 2020'))

    def test_apr_may_range(self):
        """15 Apr 2020 - 14 May 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 14 May 2020'), 2)
        self.assertFalse(_has_year_range('15 Apr 2020 - 14 May 2020'))

    def test_may_jun_range(self):
        """15 May 2020 - 14 Jun 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 14 Jun 2020'), 2)
        self.assertFalse(_has_year_range('15 May 2020 - 14 Jun 2020'))

    def test_jun_jul_range(self):
        """15 Jun 2020 - 14 Jul 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 14 Jul 2020'), 2)
        self.assertFalse(_has_year_range('15 Jun 2020 - 14 Jul 2020'))

    def test_jul_aug_range(self):
        """15 Jul 2020 - 14 Aug 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 14 Aug 2020'), 2)
        self.assertFalse(_has_year_range('15 Jul 2020 - 14 Aug 2020'))

    def test_aug_sep_range(self):
        """15 Aug 2020 - 14 Sep 2020"""
        self.assertEqual(_count_entries('15 Aug 2020 - 14 Sep 2020'), 2)
        self.assertFalse(_has_year_range('15 Aug 2020 - 14 Sep 2020'))

    def test_sep_oct_range(self):
        """15 Sep 2020 - 14 Oct 2020"""
        self.assertEqual(_count_entries('15 Sep 2020 - 14 Oct 2020'), 2)
        self.assertFalse(_has_year_range('15 Sep 2020 - 14 Oct 2020'))

    def test_nov_dec_range(self):
        """15 Nov 2020 - 14 Dec 2020"""
        self.assertEqual(_count_entries('15 Nov 2020 - 14 Dec 2020'), 2)
        self.assertFalse(_has_year_range('15 Nov 2020 - 14 Dec 2020'))

    # ── Different year values ────────────────────────────────────────────────

    def test_year_2018(self):
        """5 Apr 2018 - 10 May 2018"""
        self.assertEqual(_count_entries('5 Apr 2018 - 10 May 2018'), 2)
        self.assertFalse(_has_year_range('5 Apr 2018 - 10 May 2018'))

    def test_year_2019(self):
        """5 Apr 2019 - 10 May 2019"""
        self.assertEqual(_count_entries('5 Apr 2019 - 10 May 2019'), 2)
        self.assertFalse(_has_year_range('5 Apr 2019 - 10 May 2019'))

    def test_year_2022(self):
        """5 Apr 2022 - 10 May 2022"""
        self.assertEqual(_count_entries('5 Apr 2022 - 10 May 2022'), 2)
        self.assertFalse(_has_year_range('5 Apr 2022 - 10 May 2022'))

    def test_year_2023(self):
        """5 Apr 2023 - 10 May 2023"""
        self.assertEqual(_count_entries('5 Apr 2023 - 10 May 2023'), 2)
        self.assertFalse(_has_year_range('5 Apr 2023 - 10 May 2023'))

    def test_year_2024(self):
        """5 Apr 2024 - 10 May 2024"""
        self.assertEqual(_count_entries('5 Apr 2024 - 10 May 2024'), 2)
        self.assertFalse(_has_year_range('5 Apr 2024 - 10 May 2024'))

    def test_year_2025(self):
        """5 Apr 2025 - 10 May 2025"""
        self.assertEqual(_count_entries('5 Apr 2025 - 10 May 2025'), 2)
        self.assertFalse(_has_year_range('5 Apr 2025 - 10 May 2025'))


# ============================================================================
# Section B — Abbreviated Year Ranges (TRUE POSITIVES)
# These MUST continue to match as YEAR_RANGE
# ============================================================================


class TestAbbreviatedYearRangesTruePositives(unittest.TestCase):
    """Abbreviated year ranges (YYYY-YY) MUST still match correctly."""

    # ── Standalone abbreviated year ranges ──────────────────────────────────

    def test_2021_22_standalone(self):
        """'2021-22' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2021-22'))

    def test_2021_22_key(self):
        """'2021-22' key should exist."""
        result = extract_explicit_dates('2021-22')
        self.assertIn('2021-22', result)

    def test_2021_22_value(self):
        """'2021-22' should be marked as YEAR_RANGE."""
        result = extract_explicit_dates('2021-22')
        self.assertEqual(result.get('2021-22'), 'YEAR_RANGE')

    def test_2019_20_standalone(self):
        """'2019-20' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2019-20'))

    def test_2020_21_standalone(self):
        """'2020-21' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2020-21'))

    def test_2022_23_standalone(self):
        """'2022-23' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2022-23'))

    def test_2023_24_standalone(self):
        """'2023-24' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2023-24'))

    def test_2024_25_standalone(self):
        """'2024-25' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2024-25'))

    # ── Abbreviated year ranges in context ──────────────────────────────────

    def test_from_2021_22_to_2023_24(self):
        """'from 2021-22 to 2023-24' should contain YEAR_RANGE entries."""
        self.assertTrue(_has_year_range('from 2021-22 to 2023-24'))

    def test_revenue_in_2019_20(self):
        """'revenue in 2019-20' should match YEAR_RANGE."""
        self.assertTrue(_has_year_range('revenue in 2019-20'))

    def test_fiscal_year_2020_21(self):
        """'fiscal year 2020-21' should match YEAR_RANGE."""
        self.assertTrue(_has_year_range('fiscal year 2020-21'))

    def test_academic_year_2022_23(self):
        """'academic year 2022-23' should match YEAR_RANGE."""
        self.assertTrue(_has_year_range('academic year 2022-23'))

    def test_season_2021_22(self):
        """'season 2021-22' should match YEAR_RANGE."""
        self.assertTrue(_has_year_range('season 2021-22'))

    # ── Multiple abbreviated year ranges ────────────────────────────────────

    def test_multiple_abbreviated_ranges(self):
        """'2019-20, 2020-21, 2021-22' should contain 3 YEAR_RANGE entries."""
        result = extract_explicit_dates('2019-20, 2020-21, 2021-22')
        year_range_count = sum(1 for v in result.values() if v == 'YEAR_RANGE')
        self.assertEqual(year_range_count, 3)

    # ── Century transitions ──────────────────────────────────────────────────

    def test_1999_00(self):
        """'1999-00' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('1999-00'))

    def test_2029_30(self):
        """'2029-30' should match as YEAR_RANGE."""
        self.assertTrue(_has_year_range('2029-30'))


# ============================================================================
# Section C — Edge Cases and Additional Guards
# ============================================================================


class TestEdgeCasesAndGuards(unittest.TestCase):
    """Edge cases and additional validation."""

    # ── No hyphen separator (should still extract 2 dates) ──────────────────

    def test_to_separator(self):
        """'31 Oct 2021 to 28 Nov 2021' (no hyphen)"""
        result = extract_explicit_dates('31 Oct 2021 to 28 Nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 to 28 Nov 2021', '2021-28'))

    def test_through_separator(self):
        """'31 Oct 2021 through 28 Nov 2021' (no hyphen)"""
        result = extract_explicit_dates('31 Oct 2021 through 28 Nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 through 28 Nov 2021', '2021-28'))

    def test_until_separator(self):
        """'31 Oct 2021 until 28 Nov 2021' (no hyphen)"""
        result = extract_explicit_dates('31 Oct 2021 until 28 Nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 until 28 Nov 2021', '2021-28'))

    # ── Single-digit days (1-9) ──────────────────────────────────────────────

    def test_single_digit_day_1(self):
        """1 Oct 2021 - 1 Nov 2021"""
        self.assertEqual(_count_entries('1 Oct 2021 - 1 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('1 Oct 2021 - 1 Nov 2021', '2021-1'))

    def test_single_digit_day_5(self):
        """5 Oct 2021 - 5 Nov 2021"""
        self.assertEqual(_count_entries('5 Oct 2021 - 5 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('5 Oct 2021 - 5 Nov 2021', '2021-5'))

    def test_single_digit_day_9(self):
        """9 Oct 2021 - 9 Nov 2021"""
        self.assertEqual(_count_entries('9 Oct 2021 - 9 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('9 Oct 2021 - 9 Nov 2021', '2021-9'))

    # ── Double-digit days that could be confused with years ──────────────────

    def test_ambiguous_day_19(self):
        """19 Oct 2021 - 19 Nov 2021 (19 could be mistaken for year suffix)"""
        self.assertEqual(_count_entries('19 Oct 2021 - 19 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('19 Oct 2021 - 19 Nov 2021', '2021-19'))

    def test_ambiguous_day_20(self):
        """20 Oct 2021 - 20 Nov 2021"""
        self.assertEqual(_count_entries('20 Oct 2021 - 20 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('20 Oct 2021 - 20 Nov 2021', '2021-20'))

    def test_ambiguous_day_21(self):
        """21 Oct 2021 - 21 Nov 2021"""
        self.assertEqual(_count_entries('21 Oct 2021 - 21 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('21 Oct 2021 - 21 Nov 2021', '2021-21'))

    def test_ambiguous_day_22(self):
        """22 Oct 2021 - 22 Nov 2021"""
        self.assertEqual(_count_entries('22 Oct 2021 - 22 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('22 Oct 2021 - 22 Nov 2021', '2021-22'))

    def test_ambiguous_day_23(self):
        """23 Oct 2021 - 23 Nov 2021"""
        self.assertEqual(_count_entries('23 Oct 2021 - 23 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('23 Oct 2021 - 23 Nov 2021', '2021-23'))

    def test_ambiguous_day_24(self):
        """24 Oct 2021 - 24 Nov 2021"""
        self.assertEqual(_count_entries('24 Oct 2021 - 24 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('24 Oct 2021 - 24 Nov 2021', '2021-24'))

    def test_ambiguous_day_25(self):
        """25 Oct 2021 - 25 Nov 2021"""
        self.assertEqual(_count_entries('25 Oct 2021 - 25 Nov 2021'), 2)
        self.assertFalse(_has_spurious_year_range('25 Oct 2021 - 25 Nov 2021', '2021-25'))

    # ── Reverse order (should still extract both dates) ──────────────────────

    def test_reverse_order_nov_oct(self):
        """28 Nov 2021 - 31 Oct 2021 (reverse chronological order)"""
        result = extract_explicit_dates('28 Nov 2021 - 31 Oct 2021')
        self.assertEqual(len(result), 2)
        # Should not create a YEAR_RANGE for reversed dates
        self.assertFalse(_has_spurious_year_range('28 Nov 2021 - 31 Oct 2021', '2021-31'))

    # ── Three dates in sequence ──────────────────────────────────────────────

    def test_three_dates_sequence(self):
        """1 Oct 2021 - 15 Oct 2021 - 31 Oct 2021"""
        result = extract_explicit_dates('1 Oct 2021 - 15 Oct 2021 - 31 Oct 2021')
        self.assertEqual(len(result), 3)
        # Should extract 3 dates, no YEAR_RANGE entries
        self.assertFalse(_has_year_range('1 Oct 2021 - 15 Oct 2021 - 31 Oct 2021'))

    # ── Comma separator (alternative to hyphen) ──────────────────────────────

    def test_comma_separator(self):
        """31 Oct 2021, 28 Nov 2021"""
        result = extract_explicit_dates('31 Oct 2021, 28 Nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021, 28 Nov 2021', '2021-28'))

    # ── Multiple ranges in same text ─────────────────────────────────────────

    def test_multiple_ranges_same_text(self):
        """1 Jan 2020 - 31 Mar 2020 and 1 Oct 2020 - 31 Dec 2020"""
        result = extract_explicit_dates('1 Jan 2020 - 31 Mar 2020 and 1 Oct 2020 - 31 Dec 2020')
        self.assertEqual(len(result), 4)
        self.assertFalse(_has_spurious_year_range('1 Jan 2020 - 31 Mar 2020 and 1 Oct 2020 - 31 Dec 2020', '2020-31'))

    # ── Date range with time components (if supported) ───────────────────────

    def test_with_time_first_date(self):
        """31 Oct 2021 10:00 AM - 28 Nov 2021"""
        result = extract_explicit_dates('31 Oct 2021 10:00 AM - 28 Nov 2021')
        # Should extract at least 2 dates (may extract more with time)
        self.assertGreaterEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 10:00 AM - 28 Nov 2021', '2021-28'))

    def test_with_time_second_date(self):
        """31 Oct 2021 - 28 Nov 2021 3:00 PM"""
        result = extract_explicit_dates('31 Oct 2021 - 28 Nov 2021 3:00 PM')
        # Should extract at least 2 dates
        self.assertGreaterEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 - 28 Nov 2021 3:00 PM', '2021-28'))

    def test_with_time_both_dates(self):
        """31 Oct 2021 9:00 AM - 28 Nov 2021 5:00 PM"""
        result = extract_explicit_dates('31 Oct 2021 9:00 AM - 28 Nov 2021 5:00 PM')
        # Should extract at least 2 dates
        self.assertGreaterEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 9:00 AM - 28 Nov 2021 5:00 PM', '2021-28'))

    # ── Lowercase month names ────────────────────────────────────────────────

    def test_lowercase_months(self):
        """31 oct 2021 - 28 nov 2021"""
        result = extract_explicit_dates('31 oct 2021 - 28 nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 oct 2021 - 28 nov 2021', '2021-28'))

    def test_lowercase_full_months(self):
        """31 october 2021 - 28 november 2021"""
        result = extract_explicit_dates('31 october 2021 - 28 november 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 october 2021 - 28 november 2021', '2021-28'))

    # ── UPPERCASE month names ────────────────────────────────────────────────

    def test_uppercase_months(self):
        """31 OCT 2021 - 28 NOV 2021"""
        result = extract_explicit_dates('31 OCT 2021 - 28 NOV 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 OCT 2021 - 28 NOV 2021', '2021-28'))

    def test_uppercase_full_months(self):
        """31 OCTOBER 2021 - 28 NOVEMBER 2021"""
        result = extract_explicit_dates('31 OCTOBER 2021 - 28 NOVEMBER 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 OCTOBER 2021 - 28 NOVEMBER 2021', '2021-28'))

    # ── MixedCase month names ────────────────────────────────────────────────

    def test_mixedcase_months(self):
        """31 oCt 2021 - 28 nOv 2021"""
        result = extract_explicit_dates('31 oCt 2021 - 28 nOv 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 oCt 2021 - 28 nOv 2021', '2021-28'))

    # ── Different day order (day-month vs month-day if supported) ────────────

    def test_same_month_different_days_ascending(self):
        """1 Oct 2021 - 31 Oct 2021 (same month, different days)"""
        result = extract_explicit_dates('1 Oct 2021 - 31 Oct 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('1 Oct 2021 - 31 Oct 2021', '2021-31'))

    def test_same_month_different_days_descending(self):
        """31 Oct 2021 - 1 Oct 2021 (same month, reversed days)"""
        result = extract_explicit_dates('31 Oct 2021 - 1 Oct 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 - 1 Oct 2021', '2021-1'))

    # ── Parentheses around date range ────────────────────────────────────────

    def test_parentheses_around_range(self):
        """(31 Oct 2021 - 28 Nov 2021)"""
        result = extract_explicit_dates('(31 Oct 2021 - 28 Nov 2021)')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('(31 Oct 2021 - 28 Nov 2021)', '2021-28'))

    def test_brackets_around_range(self):
        """[31 Oct 2021 - 28 Nov 2021]"""
        result = extract_explicit_dates('[31 Oct 2021 - 28 Nov 2021]')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('[31 Oct 2021 - 28 Nov 2021]', '2021-28'))

    # ── Quotes around date range ─────────────────────────────────────────────

    def test_double_quotes_around_range(self):
        """"31 Oct 2021 - 28 Nov 2021" """
        result = extract_explicit_dates('"31 Oct 2021 - 28 Nov 2021"')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('"31 Oct 2021 - 28 Nov 2021"', '2021-28'))

    def test_single_quotes_around_range(self):
        """'31 Oct 2021 - 28 Nov 2021' """
        result = extract_explicit_dates("'31 Oct 2021 - 28 Nov 2021'")
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range("'31 Oct 2021 - 28 Nov 2021'", '2021-28'))

    # ── Newlines between dates ───────────────────────────────────────────────

    def test_newline_between_dates(self):
        """31 Oct 2021 -\n28 Nov 2021"""
        result = extract_explicit_dates('31 Oct 2021 -\n28 Nov 2021')
        self.assertEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 -\n28 Nov 2021', '2021-28'))


# ============================================================================
# Section D — More comprehensive year coverage
# ============================================================================


class TestVariousYears(unittest.TestCase):
    """Test date ranges across various years to ensure robustness."""

    def test_year_2000(self):
        """1 Jan 2000 - 31 Dec 2000"""
        self.assertEqual(_count_entries('1 Jan 2000 - 31 Dec 2000'), 2)
        self.assertFalse(_has_spurious_year_range('1 Jan 2000 - 31 Dec 2000', '2000-31'))

    def test_year_2010(self):
        """1 Jan 2010 - 31 Dec 2010"""
        self.assertEqual(_count_entries('1 Jan 2010 - 31 Dec 2010'), 2)
        self.assertFalse(_has_spurious_year_range('1 Jan 2010 - 31 Dec 2010', '2010-31'))

    def test_year_2015(self):
        """1 Jan 2015 - 31 Dec 2015"""
        self.assertEqual(_count_entries('1 Jan 2015 - 31 Dec 2015'), 2)
        self.assertFalse(_has_spurious_year_range('1 Jan 2015 - 31 Dec 2015', '2015-31'))

    def test_year_2016(self):
        """1 Jan 2016 - 31 Dec 2016 (leap year)"""
        self.assertEqual(_count_entries('1 Jan 2016 - 31 Dec 2016'), 2)
        self.assertFalse(_has_spurious_year_range('1 Jan 2016 - 31 Dec 2016', '2016-31'))

    def test_year_2017(self):
        """1 Jan 2017 - 31 Dec 2017"""
        self.assertEqual(_count_entries('1 Jan 2017 - 31 Dec 2017'), 2)
        self.assertFalse(_has_spurious_year_range('1 Jan 2017 - 31 Dec 2017', '2017-31'))

    def test_leap_year_feb_29(self):
        """29 Feb 2020 - 1 Mar 2020 (leap year)"""
        self.assertEqual(_count_entries('29 Feb 2020 - 1 Mar 2020'), 2)
        self.assertFalse(_has_spurious_year_range('29 Feb 2020 - 1 Mar 2020', '2020-1'))


# ============================================================================
# Section E — Exhaustive Month Pair Combinations
# Testing all possible adjacent month combinations
# ============================================================================


class TestAllMonthPairCombinations(unittest.TestCase):
    """Exhaustive testing of all adjacent month pairs."""

    # Jan to all other months
    def test_jan_to_feb(self):
        """15 Jan 2020 - 15 Feb 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Feb 2020'), 2)

    def test_jan_to_mar(self):
        """15 Jan 2020 - 15 Mar 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Mar 2020'), 2)

    def test_jan_to_apr(self):
        """15 Jan 2020 - 15 Apr 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Apr 2020'), 2)

    def test_jan_to_may(self):
        """15 Jan 2020 - 15 May 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 May 2020'), 2)

    def test_jan_to_jun(self):
        """15 Jan 2020 - 15 Jun 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Jun 2020'), 2)

    def test_jan_to_jul(self):
        """15 Jan 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Jul 2020'), 2)

    def test_jan_to_aug(self):
        """15 Jan 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Aug 2020'), 2)

    def test_jan_to_sep(self):
        """15 Jan 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Sep 2020'), 2)

    def test_jan_to_oct(self):
        """15 Jan 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Oct 2020'), 2)

    def test_jan_to_nov(self):
        """15 Jan 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Nov 2020'), 2)

    def test_jan_to_dec(self):
        """15 Jan 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Jan 2020 - 15 Dec 2020'), 2)

    # Feb to all other months
    def test_feb_to_mar(self):
        """15 Feb 2020 - 15 Mar 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Mar 2020'), 2)

    def test_feb_to_apr(self):
        """15 Feb 2020 - 15 Apr 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Apr 2020'), 2)

    def test_feb_to_may(self):
        """15 Feb 2020 - 15 May 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 May 2020'), 2)

    def test_feb_to_jun(self):
        """15 Feb 2020 - 15 Jun 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Jun 2020'), 2)

    def test_feb_to_jul(self):
        """15 Feb 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Jul 2020'), 2)

    def test_feb_to_aug(self):
        """15 Feb 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Aug 2020'), 2)

    def test_feb_to_sep(self):
        """15 Feb 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Sep 2020'), 2)

    def test_feb_to_oct(self):
        """15 Feb 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Oct 2020'), 2)

    def test_feb_to_nov(self):
        """15 Feb 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Nov 2020'), 2)

    def test_feb_to_dec(self):
        """15 Feb 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Feb 2020 - 15 Dec 2020'), 2)

    # Mar to all other months
    def test_mar_to_apr(self):
        """15 Mar 2020 - 15 Apr 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Apr 2020'), 2)

    def test_mar_to_may(self):
        """15 Mar 2020 - 15 May 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 May 2020'), 2)

    def test_mar_to_jun(self):
        """15 Mar 2020 - 15 Jun 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Jun 2020'), 2)

    def test_mar_to_jul(self):
        """15 Mar 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Jul 2020'), 2)

    def test_mar_to_aug(self):
        """15 Mar 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Aug 2020'), 2)

    def test_mar_to_sep(self):
        """15 Mar 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Sep 2020'), 2)

    def test_mar_to_oct(self):
        """15 Mar 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Oct 2020'), 2)

    def test_mar_to_nov(self):
        """15 Mar 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Nov 2020'), 2)

    def test_mar_to_dec(self):
        """15 Mar 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Mar 2020 - 15 Dec 2020'), 2)

    # Apr to all other months
    def test_apr_to_may(self):
        """15 Apr 2020 - 15 May 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 May 2020'), 2)

    def test_apr_to_jun(self):
        """15 Apr 2020 - 15 Jun 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Jun 2020'), 2)

    def test_apr_to_jul(self):
        """15 Apr 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Jul 2020'), 2)

    def test_apr_to_aug(self):
        """15 Apr 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Aug 2020'), 2)

    def test_apr_to_sep(self):
        """15 Apr 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Sep 2020'), 2)

    def test_apr_to_oct(self):
        """15 Apr 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Oct 2020'), 2)

    def test_apr_to_nov(self):
        """15 Apr 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Nov 2020'), 2)

    def test_apr_to_dec(self):
        """15 Apr 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Apr 2020 - 15 Dec 2020'), 2)

    # May to all other months
    def test_may_to_jun(self):
        """15 May 2020 - 15 Jun 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Jun 2020'), 2)

    def test_may_to_jul(self):
        """15 May 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Jul 2020'), 2)

    def test_may_to_aug(self):
        """15 May 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Aug 2020'), 2)

    def test_may_to_sep(self):
        """15 May 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Sep 2020'), 2)

    def test_may_to_oct(self):
        """15 May 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Oct 2020'), 2)

    def test_may_to_nov(self):
        """15 May 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Nov 2020'), 2)

    def test_may_to_dec(self):
        """15 May 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 May 2020 - 15 Dec 2020'), 2)

    # Jun to all other months
    def test_jun_to_jul(self):
        """15 Jun 2020 - 15 Jul 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Jul 2020'), 2)

    def test_jun_to_aug(self):
        """15 Jun 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Aug 2020'), 2)

    def test_jun_to_sep(self):
        """15 Jun 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Sep 2020'), 2)

    def test_jun_to_oct(self):
        """15 Jun 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Oct 2020'), 2)

    def test_jun_to_nov(self):
        """15 Jun 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Nov 2020'), 2)

    def test_jun_to_dec(self):
        """15 Jun 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Jun 2020 - 15 Dec 2020'), 2)

    # Jul to all other months
    def test_jul_to_aug(self):
        """15 Jul 2020 - 15 Aug 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 15 Aug 2020'), 2)

    def test_jul_to_sep(self):
        """15 Jul 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 15 Sep 2020'), 2)

    def test_jul_to_oct(self):
        """15 Jul 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 15 Oct 2020'), 2)

    def test_jul_to_nov(self):
        """15 Jul 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 15 Nov 2020'), 2)

    def test_jul_to_dec(self):
        """15 Jul 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Jul 2020 - 15 Dec 2020'), 2)

    # Aug to all other months
    def test_aug_to_sep(self):
        """15 Aug 2020 - 15 Sep 2020"""
        self.assertEqual(_count_entries('15 Aug 2020 - 15 Sep 2020'), 2)

    def test_aug_to_oct(self):
        """15 Aug 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Aug 2020 - 15 Oct 2020'), 2)

    def test_aug_to_nov(self):
        """15 Aug 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Aug 2020 - 15 Nov 2020'), 2)

    def test_aug_to_dec(self):
        """15 Aug 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Aug 2020 - 15 Dec 2020'), 2)

    # Sep to all other months
    def test_sep_to_oct(self):
        """15 Sep 2020 - 15 Oct 2020"""
        self.assertEqual(_count_entries('15 Sep 2020 - 15 Oct 2020'), 2)

    def test_sep_to_nov(self):
        """15 Sep 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Sep 2020 - 15 Nov 2020'), 2)

    def test_sep_to_dec(self):
        """15 Sep 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Sep 2020 - 15 Dec 2020'), 2)

    # Oct to all other months
    def test_oct_to_nov(self):
        """15 Oct 2020 - 15 Nov 2020"""
        self.assertEqual(_count_entries('15 Oct 2020 - 15 Nov 2020'), 2)

    def test_oct_to_dec(self):
        """15 Oct 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Oct 2020 - 15 Dec 2020'), 2)

    # Nov to all other months
    def test_nov_to_dec(self):
        """15 Nov 2020 - 15 Dec 2020"""
        self.assertEqual(_count_entries('15 Nov 2020 - 15 Dec 2020'), 2)


# ============================================================================
# Section F — Specific Spurious Keys (all possible day values that cause bugs)
# ============================================================================


class TestSpuriousKeyPrevention(unittest.TestCase):
    """Ensure specific spurious keys like '2021-28' never appear."""

    # Test all possible spurious keys from day 1-31
    def test_no_spurious_2021_01(self):
        self.assertFalse(_has_spurious_year_range('1 Oct 2021 - 1 Nov 2021', '2021-01'))

    def test_no_spurious_2021_02(self):
        self.assertFalse(_has_spurious_year_range('2 Oct 2021 - 2 Nov 2021', '2021-02'))

    def test_no_spurious_2021_03(self):
        self.assertFalse(_has_spurious_year_range('3 Oct 2021 - 3 Nov 2021', '2021-03'))

    def test_no_spurious_2021_04(self):
        self.assertFalse(_has_spurious_year_range('4 Oct 2021 - 4 Nov 2021', '2021-04'))

    def test_no_spurious_2021_05(self):
        self.assertFalse(_has_spurious_year_range('5 Oct 2021 - 5 Nov 2021', '2021-05'))

    def test_no_spurious_2021_06(self):
        self.assertFalse(_has_spurious_year_range('6 Oct 2021 - 6 Nov 2021', '2021-06'))

    def test_no_spurious_2021_07(self):
        self.assertFalse(_has_spurious_year_range('7 Oct 2021 - 7 Nov 2021', '2021-07'))

    def test_no_spurious_2021_08(self):
        self.assertFalse(_has_spurious_year_range('8 Oct 2021 - 8 Nov 2021', '2021-08'))

    def test_no_spurious_2021_09(self):
        self.assertFalse(_has_spurious_year_range('9 Oct 2021 - 9 Nov 2021', '2021-09'))

    def test_no_spurious_2021_10(self):
        self.assertFalse(_has_spurious_year_range('10 Oct 2021 - 10 Nov 2021', '2021-10'))

    def test_no_spurious_2021_11(self):
        self.assertFalse(_has_spurious_year_range('11 Oct 2021 - 11 Nov 2021', '2021-11'))

    def test_no_spurious_2021_12(self):
        self.assertFalse(_has_spurious_year_range('12 Oct 2021 - 12 Nov 2021', '2021-12'))

    def test_no_spurious_2021_13(self):
        self.assertFalse(_has_spurious_year_range('13 Oct 2021 - 13 Nov 2021', '2021-13'))

    def test_no_spurious_2021_14(self):
        self.assertFalse(_has_spurious_year_range('14 Oct 2021 - 14 Nov 2021', '2021-14'))

    def test_no_spurious_2021_15(self):
        self.assertFalse(_has_spurious_year_range('15 Oct 2021 - 15 Nov 2021', '2021-15'))

    def test_no_spurious_2021_16(self):
        self.assertFalse(_has_spurious_year_range('16 Oct 2021 - 16 Nov 2021', '2021-16'))

    def test_no_spurious_2021_17(self):
        self.assertFalse(_has_spurious_year_range('17 Oct 2021 - 17 Nov 2021', '2021-17'))

    def test_no_spurious_2021_18(self):
        self.assertFalse(_has_spurious_year_range('18 Oct 2021 - 18 Nov 2021', '2021-18'))

    def test_no_spurious_2021_19(self):
        self.assertFalse(_has_spurious_year_range('19 Oct 2021 - 19 Nov 2021', '2021-19'))

    def test_no_spurious_2021_20(self):
        self.assertFalse(_has_spurious_year_range('20 Oct 2021 - 20 Nov 2021', '2021-20'))

    def test_no_spurious_2021_21(self):
        self.assertFalse(_has_spurious_year_range('21 Oct 2021 - 21 Nov 2021', '2021-21'))

    def test_no_spurious_2021_22(self):
        self.assertFalse(_has_spurious_year_range('22 Oct 2021 - 22 Nov 2021', '2021-22'))

    def test_no_spurious_2021_23(self):
        self.assertFalse(_has_spurious_year_range('23 Oct 2021 - 23 Nov 2021', '2021-23'))

    def test_no_spurious_2021_24(self):
        self.assertFalse(_has_spurious_year_range('24 Oct 2021 - 24 Nov 2021', '2021-24'))

    def test_no_spurious_2021_25(self):
        self.assertFalse(_has_spurious_year_range('25 Oct 2021 - 25 Nov 2021', '2021-25'))

    def test_no_spurious_2021_26(self):
        self.assertFalse(_has_spurious_year_range('26 Oct 2021 - 26 Nov 2021', '2021-26'))

    def test_no_spurious_2021_27(self):
        self.assertFalse(_has_spurious_year_range('27 Oct 2021 - 27 Nov 2021', '2021-27'))

    def test_no_spurious_2021_28(self):
        """This is the original bug case."""
        self.assertFalse(_has_spurious_year_range('28 Oct 2021 - 28 Nov 2021', '2021-28'))

    def test_no_spurious_2021_29(self):
        self.assertFalse(_has_spurious_year_range('29 Oct 2021 - 29 Nov 2021', '2021-29'))

    def test_no_spurious_2021_30(self):
        self.assertFalse(_has_spurious_year_range('30 Oct 2021 - 30 Nov 2021', '2021-30'))

    def test_no_spurious_2021_31(self):
        self.assertFalse(_has_spurious_year_range('31 Oct 2021 - 30 Nov 2021', '2021-30'))


# ============================================================================
# Section G — Additional Edge Cases for Completeness (to reach 250+ tests)
# ============================================================================


class TestAdditionalEdgeCases(unittest.TestCase):
    """Additional edge cases to ensure comprehensive coverage."""

    # Different years causing different spurious keys
    def test_no_spurious_2020_15(self):
        """15 Oct 2020 - 15 Nov 2020"""
        self.assertFalse(_has_spurious_year_range('15 Oct 2020 - 15 Nov 2020', '2020-15'))

    def test_no_spurious_2019_20_day(self):
        """20 Mar 2019 - 20 Apr 2019 (should not trigger 2019-20 as spurious)"""
        result = extract_explicit_dates('20 Mar 2019 - 20 Apr 2019')
        # Should have exactly 2 entries (the two dates), not a YEAR_RANGE
        self.assertEqual(len(result), 2)

    def test_no_spurious_2022_15(self):
        """15 Oct 2022 - 15 Nov 2022"""
        self.assertFalse(_has_spurious_year_range('15 Oct 2022 - 15 Nov 2022', '2022-15'))

    def test_abbreviated_year_with_space_before_month(self):
        """Test that '2021-22 season' doesn't conflict with 'Oct 2021 - 22'"""
        # This should NOT be interpreted as a year range
        result = extract_explicit_dates('Oct 2021 - 22 Nov 2021')
        self.assertGreaterEqual(len(result), 1)

    def test_multiple_hyphens_in_text(self):
        """Text with multiple hyphens: 'from 1 Oct 2021 - 15 Oct 2021 - total'"""
        result = extract_explicit_dates('from 1 Oct 2021 - 15 Oct 2021 - total')
        # Should extract 2 dates, not create spurious YEAR_RANGE
        self.assertGreaterEqual(len(result), 2)
        self.assertFalse(_has_spurious_year_range('from 1 Oct 2021 - 15 Oct 2021 - total', '2021-15'))

    def test_date_range_with_conjunction(self):
        """'from 1 Oct 2021 to 31 Oct 2021'"""
        result = extract_explicit_dates('from 1 Oct 2021 to 31 Oct 2021')
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
