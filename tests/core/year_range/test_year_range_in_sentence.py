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

class TestCompatDatefinder(unittest.TestCase):
    """Compatibility tests matching original datefinder behaviour from issue #24."""

    def test_year_in_sentence_2004(self):
        """'...title in 2004.' — primary compat case."""
        result = extract_explicit_dates('...title in 2004.')
        self.assertIn('2004', result)

    def test_year_in_sentence_2004_type(self):
        result = extract_explicit_dates('...title in 2004.')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_year_in_sentence_2008(self):
        """'...traumatized on the sets in 2008.' — second compat case."""
        result = extract_explicit_dates('...traumatized on the sets in 2008.')
        self.assertIn('2008', result)

    def test_year_in_sentence_2008_type(self):
        result = extract_explicit_dates('...traumatized on the sets in 2008.')
        self.assertEqual(result.get('2008'), 'YEAR_ONLY')

    def test_year_range_compat(self):
        """YEAR_RANGE compatibility: 2014-2015."""
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')


# ============================================================================
# Extended coverage — misc multi-prep and combined scenarios
# ============================================================================

class TestProseYearMultiPrep(unittest.TestCase):
    """Multiple prepositions / years in single input."""

    def test_in_and_since(self):
        result = extract_explicit_dates('opened in 2000 and has been running since 2005')
        self.assertIn('2000', result)
        self.assertIn('2005', result)

    def test_before_and_after(self):
        result = extract_explicit_dates('projects before 2010 and after 2015')
        self.assertIn('2010', result)
        self.assertIn('2015', result)

    def test_until_and_from(self):
        result = extract_explicit_dates('from 2010 until 2020')
        self.assertIn('2010', result)
        self.assertIn('2020', result)

    def test_during_and_since(self):
        result = extract_explicit_dates('during 2020 and since 2021')
        self.assertIn('2020', result)
        self.assertIn('2021', result)

    def test_circa_and_around(self):
        result = extract_explicit_dates('circa 2000 or around 2010')
        self.assertIn('2000', result)
        self.assertIn('2010', result)

    def test_by_and_before(self):
        result = extract_explicit_dates('by 2025 before 2030')
        self.assertIn('2025', result)
        self.assertIn('2030', result)

    def test_prior_to_and_after(self):
        result = extract_explicit_dates('prior to 2010 or after 2015')
        self.assertIn('2010', result)
        self.assertIn('2015', result)

    def test_back_to_and_in(self):
        result = extract_explicit_dates('dating back to 1998 and in 2004')
        self.assertIn('1998', result)
        self.assertIn('2004', result)

    def test_as_of_and_until(self):
        result = extract_explicit_dates('as of 2020 until 2025')
        self.assertIn('2020', result)
        self.assertIn('2025', result)

    def test_all_types_same_year(self):
        """Same year appearing twice with different prepositions — key appears once."""
        result = extract_explicit_dates('in 2004 and after 2004')
        self.assertIn('2004', result)
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')


# ============================================================================
# Additional single-preposition variety tests to reach 250+
# ============================================================================

class TestProseYearAdditional(unittest.TestCase):
    """Additional coverage for diverse year values and sentence positions."""

    def test_in_start_of_sentence(self):
        self.assertTrue(_year_only('In 2004, the company launched.'))

    def test_in_end_of_sentence(self):
        self.assertTrue(_year_only('The company launched in 2004.'))

    def test_in_middle_of_sentence(self):
        self.assertTrue(_year_only('The event, set in 2004, changed everything.'))

    def test_since_start(self):
        self.assertTrue(_year_only('Since 2010, everything changed.'))

    def test_since_end(self):
        self.assertTrue(_year_only('Changes were noted since 2010.'))

    def test_by_with_comma(self):
        self.assertTrue(_year_only('By 2025, all goals should be met.'))

    def test_until_with_comma(self):
        self.assertTrue(_year_only('Until 2030, operations continue.'))

    def test_before_mid_sentence(self):
        self.assertTrue(_year_only('Policies established before 2000 still apply.'))

    def test_after_mid_sentence(self):
        self.assertTrue(_year_only('Methods introduced after 2010 are preferred.'))

    def test_during_with_punctuation(self):
        self.assertTrue(_year_only('Work done during 2020, despite challenges.'))

    def test_circa_literary(self):
        self.assertTrue(_year_only('The document, circa 1980, tells the story.'))

    def test_around_informal(self):
        self.assertTrue(_year_only('It happened around 2012 or so.'))

    def test_through_range_end(self):
        self.assertTrue(_year_only('The program continued through 2022.'))

    def test_as_of_formal(self):
        self.assertTrue(_year_only('As of 2023 these rules are in effect.'))

    def test_back_to_narrative(self):
        self.assertTrue(_year_only('The story goes back to 1975.'))

    def test_prior_to_legal(self):
        self.assertTrue(_year_only('Prior to 2015 the law was different.'))

    def test_in_2001(self):
        self.assertTrue(_year_only('in 2001'))

    def test_in_2002(self):
        self.assertTrue(_year_only('in 2002'))

    def test_in_2003(self):
        self.assertTrue(_year_only('in 2003'))

    def test_in_2005(self):
        self.assertTrue(_year_only('in 2005'))

    def test_in_2006(self):
        self.assertTrue(_year_only('in 2006'))

    def test_in_2007(self):
        self.assertTrue(_year_only('in 2007'))

    def test_in_2009(self):
        self.assertTrue(_year_only('in 2009'))

    def test_in_2011(self):
        self.assertTrue(_year_only('in 2011'))

    def test_in_2012(self):
        self.assertTrue(_year_only('in 2012'))

    def test_in_2013(self):
        self.assertTrue(_year_only('in 2013'))

    def test_in_2014(self):
        self.assertTrue(_year_only('in 2014'))

    def test_in_2016(self):
        self.assertTrue(_year_only('in 2016'))

    def test_in_2017(self):
        self.assertTrue(_year_only('in 2017'))

    def test_in_2018(self):
        self.assertTrue(_year_only('in 2018'))

    def test_during_2019(self):
        self.assertTrue(_year_only('during 2019'))

    def test_after_2022(self):
        self.assertTrue(_year_only('after 2022'))

    def test_from_2020(self):
        result = extract_explicit_dates('from 2020')
        self.assertTrue(result)

    def test_before_1960(self):
        self.assertTrue(_year_only('before 1960'))

    def test_since_1950(self):
        self.assertTrue(_year_only('since 1950'))

    def test_until_1980(self):
        self.assertTrue(_year_only('until 1980'))

    def test_through_2010(self):
        self.assertTrue(_year_only('through 2010'))

    def test_year_range_from_2015_to_2018(self):
        self.assertTrue(_year_range('from 2015 to 2018'))

    def test_year_range_between_2012_and_2016(self):
        self.assertTrue(_year_range('between 2012 and 2016'))

    def test_hyphen_year_range_1995_2005(self):
        self.assertTrue(_year_range('1995-2005'))

    def test_hyphen_year_range_2001_2009(self):
        self.assertTrue(_year_range('2001-2009'))

    def test_from_back_to_basics(self):
        self.assertTrue(extract_explicit_dates('from 2004'))

    def test_between_basic(self):
        self.assertTrue(_year_range('between 2010 and 2022'))


if __name__ == '__main__':
    unittest.main()
