#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
TDD tests for prose year extraction (preposition-preceded YEAR_ONLY and YEAR_RANGE).

Related GitHub Issue:
    #24 - Gap: year-only references not extracted from prose (in 2004, in 2008)
    https://github.com/craigtrim/fast-parse-time/issues/24

All tests are written BEFORE implementation (red phase).
"""

import unittest
from fast_parse_time.api import extract_explicit_dates


# ── helpers ─────────────────────────────────────────────────────────────────

def _year_only(text: str) -> bool:
    """Return True if at least one YEAR_ONLY entry exists in the result."""
    return 'YEAR_ONLY' in extract_explicit_dates(text).values()


def _year_range(text: str) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    return 'YEAR_RANGE' in extract_explicit_dates(text).values()


def _has_key(text: str, key: str) -> bool:
    return key in extract_explicit_dates(text)


# ============================================================================
# Part A — Preposition: "in"
# ============================================================================


class TestProseYearNegative(unittest.TestCase):
    """
    Bare years without prepositions should NOT be returned as YEAR_ONLY.
    Design choice: no false positives on copyright notices, version strings, etc.
    """

    def test_bare_year_not_year_only(self):
        """Bare '2004' alone should not yield YEAR_ONLY."""
        result = extract_explicit_dates('2004')
        self.assertNotEqual(result.get('2004'), 'YEAR_ONLY')

    def test_copyright_2023_not_year_only(self):
        """'Copyright 2023' should not yield YEAR_ONLY."""
        result = extract_explicit_dates('Copyright 2023')
        self.assertNotIn('YEAR_ONLY', result.values())

    def test_version_2024_not_year_only(self):
        """'version 2024' should not yield YEAR_ONLY."""
        result = extract_explicit_dates('version 2024')
        self.assertNotIn('YEAR_ONLY', result.values())

    def test_rooms_2001_not_year_only(self):
        """'rooms 2001' should not yield YEAR_ONLY."""
        result = extract_explicit_dates('rooms 2001')
        self.assertNotIn('YEAR_ONLY', result.values())

    def test_invalid_too_short(self):
        """3-digit number is not a year."""
        result = extract_explicit_dates('in 200')
        self.assertNotIn('200', result)

    def test_invalid_too_long(self):
        """5-digit number is not a year."""
        result = extract_explicit_dates('in 20004')
        self.assertNotIn('20004', result)

    def test_no_preposition_no_year_only(self):
        """'article published 2018' — no preposition, no YEAR_ONLY."""
        result = extract_explicit_dates('article published 2018')
        self.assertNotIn('YEAR_ONLY', result.values())


# ============================================================================
# Part B — YEAR_RANGE: YYYY-YYYY hyphen form (bug fix)
# ============================================================================

class TestYearRangeHyphen(unittest.TestCase):
    """YYYY-YYYY hyphen form should return YEAR_RANGE (existing bug fix)."""

    def test_2014_2015_nonempty(self):
        self.assertTrue(extract_explicit_dates('2014-2015'))

    def test_2014_2015_type(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_2014_2015_key(self):
        self.assertTrue(_has_key('2014-2015', '2014-2015'))

    def test_2014_2015_value(self):
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_2000_2010_range(self):
        self.assertTrue(_year_range('2000-2010'))

    def test_2000_2010_key(self):
        self.assertTrue(_has_key('2000-2010', '2000-2010'))

    def test_1990_2000_range(self):
        self.assertTrue(_year_range('1990-2000'))

    def test_2010_2020_range(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_2020_2025_range(self):
        self.assertTrue(_year_range('2020-2025'))

    def test_2004_2008_range(self):
        self.assertTrue(_year_range('2004-2008'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('the period 2014-2015 was significant'))

    def test_in_sentence_key(self):
        result = extract_explicit_dates('the period 2014-2015 was significant')
        self.assertIn('2014-2015', result)

    def test_monotonic_required_same_year_not_range(self):
        """2014-2014 is not a valid range (start == end)."""
        result = extract_explicit_dates('2014-2014')
        self.assertNotEqual(result.get('2014-2014'), 'YEAR_RANGE')

    def test_reversed_not_range(self):
        """2015-2014 (end < start) is not a valid range."""
        result = extract_explicit_dates('2015-2014')
        self.assertNotEqual(result.get('2015-2014'), 'YEAR_RANGE')

    def test_out_of_range_years_not_range(self):
        """1800-1900 — both out of MIN_YEAR — should not return YEAR_RANGE."""
        result = extract_explicit_dates('1800-1900')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result, dict)


# ============================================================================
# Part B — YEAR_RANGE: "from YYYY to YYYY"
# ============================================================================

class TestYearRangeFrom(unittest.TestCase):
    """'from YYYY to YYYY' prose form returns YEAR_RANGE."""

    def test_from_2004_to_2008_nonempty(self):
        self.assertTrue(extract_explicit_dates('from 2004 to 2008'))

    def test_from_2004_to_2008_type(self):
        self.assertTrue(_year_range('from 2004 to 2008'))

    def test_from_2004_to_2008_has_range_entry(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_from_2000_to_2010(self):
        self.assertTrue(_year_range('from 2000 to 2010'))

    def test_from_1990_to_2000(self):
        self.assertTrue(_year_range('from 1990 to 2000'))

    def test_from_2010_to_2020(self):
        self.assertTrue(_year_range('from 2010 to 2020'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('he worked there from 2005 to 2015'))

    def test_in_sentence_has_range(self):
        result = extract_explicit_dates('he worked there from 2005 to 2015')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_uppercase_from(self):
        self.assertTrue(_year_range('FROM 2004 TO 2008'))

    def test_from_reversed_not_range(self):
        """'from 2008 to 2004' — inverted, should not be YEAR_RANGE."""
        result = extract_explicit_dates('from 2008 to 2004')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(len(result) >= 1)


# ============================================================================
# Part B — YEAR_RANGE: "between YYYY and YYYY"
# ============================================================================

class TestYearRangeBetween(unittest.TestCase):
    """'between YYYY and YYYY' prose form returns YEAR_RANGE."""

    def test_between_2010_and_2020_nonempty(self):
        self.assertTrue(extract_explicit_dates('between 2010 and 2020'))

    def test_between_2010_and_2020_type(self):
        self.assertTrue(_year_range('between 2010 and 2020'))

    def test_between_2010_and_2020_has_range_entry(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_between_2000_and_2010(self):
        self.assertTrue(_year_range('between 2000 and 2010'))

    def test_between_1990_and_2000(self):
        self.assertTrue(_year_range('between 1990 and 2000'))

    def test_between_2004_and_2008(self):
        self.assertTrue(_year_range('between 2004 and 2008'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('born between 1950 and 1960'))

    def test_in_sentence_has_range(self):
        result = extract_explicit_dates('born between 1950 and 1960')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_uppercase_between(self):
        self.assertTrue(_year_range('BETWEEN 2010 AND 2020'))

    def test_between_reversed_not_range(self):
        """'between 2020 and 2010' — inverted."""
        result = extract_explicit_dates('between 2020 and 2010')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_result_is_dict(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('between 2010 and 2020')
        self.assertTrue(len(result) >= 1)


# ============================================================================
# Part B — YEAR_RANGE boundary and negative
# ============================================================================

class TestYearRangeBoundary(unittest.TestCase):
    """Boundary conditions for YEAR_RANGE."""

    def test_hyphen_range_in_valid_range(self):
        self.assertTrue(_year_range('1960-1970'))

    def test_hyphen_range_at_lower_boundary(self):
        """Years near MIN_YEAR."""
        self.assertTrue(_year_range('1930-1940'))

    def test_hyphen_range_at_upper_boundary(self):
        """Years near MAX_YEAR."""
        self.assertTrue(_year_range('2030-2035'))

    def test_hyphen_range_one_year_out_of_range(self):
        """If start year is out of range — no YEAR_RANGE expected."""
        result = extract_explicit_dates('1800-2010')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_from_range_valid(self):
        self.assertTrue(_year_range('from 1960 to 1970'))

    def test_between_range_valid(self):
        self.assertTrue(_year_range('between 1960 and 1970'))

    def test_large_span_hyphen(self):
        """50-year span."""
        self.assertTrue(_year_range('1970-2020'))

    def test_small_span_hyphen(self):
        """1-year span."""
        self.assertTrue(_year_range('2019-2020'))


# ============================================================================
# Part B — YEAR_RANGE: negative cases
# ============================================================================

class TestYearRangeNegative(unittest.TestCase):
    """Cases that should NOT produce YEAR_RANGE."""

    def test_hyphen_month_year_not_year_range(self):
        """'Oct-2023' should be MONTH_YEAR not YEAR_RANGE (issue #21 handles this)."""
        result = extract_explicit_dates('Oct-2023')
        self.assertNotEqual(result.get('Oct-2023'), 'YEAR_RANGE')

    def test_full_date_not_year_range(self):
        """A full date like '2024-03-15' should not become YEAR_RANGE."""
        result = extract_explicit_dates('2024-03-15')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_plain_text_no_range(self):
        """No years in text — no YEAR_RANGE."""
        result = extract_explicit_dates('hello world')
        self.assertNotIn('YEAR_RANGE', result.values())

    def test_single_year_no_range(self):
        """Single year is not a range."""
        result = extract_explicit_dates('2015')
        self.assertNotIn('YEAR_RANGE', result.values())


# ============================================================================
# Part B — YEAR_RANGE: in sentences
# ============================================================================

class TestYearRangeInSentence(unittest.TestCase):
    """YEAR_RANGE embedded in longer prose."""

    def test_hyphen_in_sentence_1(self):
        self.assertTrue(_year_range('the 2014-2015 season was exceptional'))

    def test_hyphen_in_sentence_2(self):
        self.assertTrue(_year_range('revenue grew from 2010-2015'))

    def test_hyphen_in_sentence_3(self):
        result = extract_explicit_dates('the fiscal year 2019-2020 report')
        self.assertIn('2019-2020', result)

    def test_from_to_in_sentence_1(self):
        self.assertTrue(_year_range('the merger happened from 2003 to 2005'))

    def test_from_to_in_sentence_2(self):
        result = extract_explicit_dates('records from 2001 to 2009')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_between_in_sentence_1(self):
        self.assertTrue(_year_range('growth occurred between 2010 and 2018'))

    def test_between_in_sentence_2(self):
        result = extract_explicit_dates('events between 1999 and 2005 are included')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))

    def test_multiple_ranges_in_sentence(self):
        """Two ranges in one text."""
        result = extract_explicit_dates('2010-2015 and 2018-2020 both show growth')
        self.assertTrue(any(v == 'YEAR_RANGE' for v in result.values()))


# ============================================================================
# Compat: datefinder original test cases
# ============================================================================
