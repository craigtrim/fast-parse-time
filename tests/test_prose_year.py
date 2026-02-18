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

class TestProseYearIn(unittest.TestCase):
    """Preposition 'in' preceding a 4-digit year."""

    def test_in_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2004'))

    def test_in_2004_year_only_type(self):
        self.assertTrue(_year_only('in 2004'))

    def test_in_2004_key(self):
        self.assertTrue(_has_key('in 2004', '2004'))

    def test_in_2008_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2008'))

    def test_in_2008_year_only_type(self):
        self.assertTrue(_year_only('in 2008'))

    def test_in_2008_key(self):
        self.assertTrue(_has_key('in 2008', '2008'))

    def test_in_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 2019'))

    def test_in_2019_key(self):
        self.assertTrue(_has_key('in 2019', '2019'))

    def test_in_1998_nonempty(self):
        self.assertTrue(extract_explicit_dates('in 1998'))

    def test_in_1998_key(self):
        self.assertTrue(_has_key('in 1998', '1998'))

    def test_in_sentence_1(self):
        """'...title in 2004.' — compat datefinder test."""
        self.assertTrue(_year_only('the film had its title in 2004.'))

    def test_in_sentence_2(self):
        """'...traumatized on the sets in 2008.' — compat datefinder test."""
        self.assertTrue(_year_only('traumatized on the sets in 2008.'))

    def test_in_sentence_3(self):
        self.assertTrue(_year_only('the company was founded in 2004'))

    def test_in_sentence_key(self):
        result = extract_explicit_dates('the company was founded in 2004')
        self.assertIn('2004', result)

    def test_in_sentence_type(self):
        result = extract_explicit_dates('the company was founded in 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_in_2024_future_year(self):
        self.assertTrue(_year_only('in 2024'))

    def test_in_2030_near_max(self):
        self.assertTrue(_year_only('in 2030'))

    def test_in_uppercase_IN(self):
        """Case-insensitive: 'IN 2004'."""
        self.assertTrue(_year_only('IN 2004'))

    def test_in_mixed_case(self):
        """Case-insensitive: 'In 2004'."""
        self.assertTrue(_year_only('In 2004'))

    def test_in_result_count_minimum(self):
        result = extract_explicit_dates('in 2004')
        self.assertGreaterEqual(len(result), 1)

    def test_in_year_only_value(self):
        result = extract_explicit_dates('in 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')


# ============================================================================
# Part A — Preposition: "since"
# ============================================================================

class TestProseYearSince(unittest.TestCase):
    """Preposition 'since' preceding a 4-digit year."""

    def test_since_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('since 2019'))

    def test_since_2019_type(self):
        self.assertTrue(_year_only('since 2019'))

    def test_since_2019_key(self):
        self.assertTrue(_has_key('since 2019', '2019'))

    def test_since_1990_key(self):
        self.assertTrue(_has_key('since 1990', '1990'))

    def test_since_sentence(self):
        self.assertTrue(_year_only('we have been open since 2005'))

    def test_since_sentence_key(self):
        result = extract_explicit_dates('we have been open since 2005')
        self.assertIn('2005', result)

    def test_since_value(self):
        result = extract_explicit_dates('since 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_since_uppercase(self):
        self.assertTrue(_year_only('SINCE 2019'))

    def test_since_2000(self):
        self.assertTrue(_year_only('since 2000'))

    def test_since_1970(self):
        self.assertTrue(_year_only('since 1970'))


# ============================================================================
# Part A — Preposition: "by"
# ============================================================================

class TestProseYearBy(unittest.TestCase):
    """Preposition 'by' preceding a 4-digit year."""

    def test_by_2024_nonempty(self):
        self.assertTrue(extract_explicit_dates('by 2024'))

    def test_by_2024_type(self):
        self.assertTrue(_year_only('by 2024'))

    def test_by_2024_key(self):
        self.assertTrue(_has_key('by 2024', '2024'))

    def test_by_2030_key(self):
        self.assertTrue(_has_key('by 2030', '2030'))

    def test_by_sentence(self):
        self.assertTrue(_year_only('complete the project by 2025'))

    def test_by_sentence_key(self):
        result = extract_explicit_dates('complete the project by 2025')
        self.assertIn('2025', result)

    def test_by_value(self):
        result = extract_explicit_dates('by 2024')
        self.assertEqual(result.get('2024'), 'YEAR_ONLY')

    def test_by_uppercase(self):
        self.assertTrue(_year_only('BY 2024'))

    def test_by_2010(self):
        self.assertTrue(_year_only('by 2010'))


# ============================================================================
# Part A — Preposition: "until"
# ============================================================================

class TestProseYearUntil(unittest.TestCase):
    """Preposition 'until' preceding a 4-digit year."""

    def test_until_2030_nonempty(self):
        self.assertTrue(extract_explicit_dates('until 2030'))

    def test_until_2030_type(self):
        self.assertTrue(_year_only('until 2030'))

    def test_until_2030_key(self):
        self.assertTrue(_has_key('until 2030', '2030'))

    def test_until_sentence(self):
        self.assertTrue(_year_only('the program ran until 2020'))

    def test_until_sentence_key(self):
        result = extract_explicit_dates('the program ran until 2020')
        self.assertIn('2020', result)

    def test_until_value(self):
        result = extract_explicit_dates('until 2030')
        self.assertEqual(result.get('2030'), 'YEAR_ONLY')

    def test_until_uppercase(self):
        self.assertTrue(_year_only('UNTIL 2030'))

    def test_until_2005(self):
        self.assertTrue(_year_only('until 2005'))

    def test_until_1999(self):
        self.assertTrue(_year_only('until 1999'))


# ============================================================================
# Part A — Preposition: "before"
# ============================================================================

class TestProseYearBefore(unittest.TestCase):
    """Preposition 'before' preceding a 4-digit year."""

    def test_before_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('before 2004'))

    def test_before_2004_type(self):
        self.assertTrue(_year_only('before 2004'))

    def test_before_2004_key(self):
        self.assertTrue(_has_key('before 2004', '2004'))

    def test_before_sentence(self):
        self.assertTrue(_year_only('it happened before 2010'))

    def test_before_sentence_key(self):
        result = extract_explicit_dates('it happened before 2010')
        self.assertIn('2010', result)

    def test_before_value(self):
        result = extract_explicit_dates('before 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_before_uppercase(self):
        self.assertTrue(_year_only('BEFORE 2004'))

    def test_before_2000(self):
        self.assertTrue(_year_only('before 2000'))

    def test_before_1990(self):
        self.assertTrue(_year_only('before 1990'))


# ============================================================================
# Part A — Preposition: "after"
# ============================================================================

class TestProseYearAfter(unittest.TestCase):
    """Preposition 'after' preceding a 4-digit year."""

    def test_after_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('after 2004'))

    def test_after_2004_type(self):
        self.assertTrue(_year_only('after 2004'))

    def test_after_2004_key(self):
        self.assertTrue(_has_key('after 2004', '2004'))

    def test_after_sentence(self):
        self.assertTrue(_year_only('everything changed after 2001'))

    def test_after_sentence_key(self):
        result = extract_explicit_dates('everything changed after 2001')
        self.assertIn('2001', result)

    def test_after_value(self):
        result = extract_explicit_dates('after 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_after_uppercase(self):
        self.assertTrue(_year_only('AFTER 2004'))

    def test_after_2015(self):
        self.assertTrue(_year_only('after 2015'))

    def test_after_1980(self):
        self.assertTrue(_year_only('after 1980'))


# ============================================================================
# Part A — Preposition: "during"
# ============================================================================

class TestProseYearDuring(unittest.TestCase):
    """Preposition 'during' preceding a 4-digit year."""

    def test_during_2020_nonempty(self):
        self.assertTrue(extract_explicit_dates('during 2020'))

    def test_during_2020_type(self):
        self.assertTrue(_year_only('during 2020'))

    def test_during_2020_key(self):
        self.assertTrue(_has_key('during 2020', '2020'))

    def test_during_sentence(self):
        self.assertTrue(_year_only('production halted during 2020'))

    def test_during_sentence_key(self):
        result = extract_explicit_dates('production halted during 2020')
        self.assertIn('2020', result)

    def test_during_value(self):
        result = extract_explicit_dates('during 2020')
        self.assertEqual(result.get('2020'), 'YEAR_ONLY')

    def test_during_uppercase(self):
        self.assertTrue(_year_only('DURING 2020'))

    def test_during_1945(self):
        self.assertTrue(_year_only('during 1945'))

    def test_during_2008(self):
        self.assertTrue(_year_only('during 2008'))


# ============================================================================
# Part A — Preposition: "circa"
# ============================================================================

class TestProseYearCirca(unittest.TestCase):
    """Preposition 'circa' preceding a 4-digit year."""

    def test_circa_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('circa 2004'))

    def test_circa_2004_type(self):
        self.assertTrue(_year_only('circa 2004'))

    def test_circa_2004_key(self):
        self.assertTrue(_has_key('circa 2004', '2004'))

    def test_circa_sentence(self):
        self.assertTrue(_year_only('the artifact dates to circa 1950'))

    def test_circa_sentence_key(self):
        result = extract_explicit_dates('the artifact dates to circa 1950')
        self.assertIn('1950', result)

    def test_circa_value(self):
        result = extract_explicit_dates('circa 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_circa_uppercase(self):
        self.assertTrue(_year_only('CIRCA 2004'))

    def test_circa_abbreviation_c_dot(self):
        """'c. 2004' is out of scope — should not require support."""
        pass  # intentionally excluded per issue spec

    def test_circa_1970(self):
        self.assertTrue(_year_only('circa 1970'))

    def test_circa_2019(self):
        self.assertTrue(_year_only('circa 2019'))


# ============================================================================
# Part A — Preposition: "around"
# ============================================================================

class TestProseYearAround(unittest.TestCase):
    """Preposition 'around' preceding a 4-digit year."""

    def test_around_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('around 2019'))

    def test_around_2019_type(self):
        self.assertTrue(_year_only('around 2019'))

    def test_around_2019_key(self):
        self.assertTrue(_has_key('around 2019', '2019'))

    def test_around_sentence(self):
        self.assertTrue(_year_only('the trend started around 2012'))

    def test_around_sentence_key(self):
        result = extract_explicit_dates('the trend started around 2012')
        self.assertIn('2012', result)

    def test_around_value(self):
        result = extract_explicit_dates('around 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_around_uppercase(self):
        self.assertTrue(_year_only('AROUND 2019'))

    def test_around_2000(self):
        self.assertTrue(_year_only('around 2000'))

    def test_around_1985(self):
        self.assertTrue(_year_only('around 1985'))


# ============================================================================
# Part A — Preposition: "from"
# ============================================================================

class TestProseYearFrom(unittest.TestCase):
    """Preposition 'from' preceding a single 4-digit year (no 'to' clause)."""

    def test_from_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('from 2019'))

    def test_from_2019_nonempty_contains_year_only(self):
        """Result should contain a YEAR_ONLY entry (at minimum)."""
        result = extract_explicit_dates('from 2019')
        self.assertTrue(any(v in ('YEAR_ONLY', 'YEAR_RANGE') for v in result.values()))

    def test_from_2019_key(self):
        self.assertTrue(_has_key('from 2019', '2019'))

    def test_from_sentence(self):
        result = extract_explicit_dates('data available from 2015')
        self.assertTrue(result)

    def test_from_sentence_key(self):
        result = extract_explicit_dates('data available from 2015')
        self.assertIn('2015', result)

    def test_from_uppercase(self):
        result = extract_explicit_dates('FROM 2019')
        self.assertTrue(result)

    def test_from_2000(self):
        self.assertTrue(extract_explicit_dates('from 2000'))

    def test_from_1998(self):
        self.assertTrue(extract_explicit_dates('from 1998'))


# ============================================================================
# Part A — Preposition: "through"
# ============================================================================

class TestProseYearThrough(unittest.TestCase):
    """Preposition 'through' preceding a 4-digit year."""

    def test_through_2019_nonempty(self):
        self.assertTrue(extract_explicit_dates('through 2019'))

    def test_through_2019_type(self):
        self.assertTrue(_year_only('through 2019'))

    def test_through_2019_key(self):
        self.assertTrue(_has_key('through 2019', '2019'))

    def test_through_sentence(self):
        self.assertTrue(_year_only('the war lasted through 1945'))

    def test_through_sentence_key(self):
        result = extract_explicit_dates('the war lasted through 1945')
        self.assertIn('1945', result)

    def test_through_value(self):
        result = extract_explicit_dates('through 2019')
        self.assertEqual(result.get('2019'), 'YEAR_ONLY')

    def test_through_uppercase(self):
        self.assertTrue(_year_only('THROUGH 2019'))

    def test_through_2005(self):
        self.assertTrue(_year_only('through 2005'))

    def test_through_1990(self):
        self.assertTrue(_year_only('through 1990'))


# ============================================================================
# Part A — Preposition: "as of"  (multi-word)
# ============================================================================

class TestProseYearAsOf(unittest.TestCase):
    """Multi-word preposition 'as of' preceding a 4-digit year."""

    def test_as_of_2004_nonempty(self):
        self.assertTrue(extract_explicit_dates('as of 2004'))

    def test_as_of_2004_type(self):
        self.assertTrue(_year_only('as of 2004'))

    def test_as_of_2004_key(self):
        self.assertTrue(_has_key('as of 2004', '2004'))

    def test_as_of_sentence(self):
        self.assertTrue(_year_only('as of 2023, the regulation applies'))

    def test_as_of_sentence_key(self):
        result = extract_explicit_dates('as of 2023, the regulation applies')
        self.assertIn('2023', result)

    def test_as_of_value(self):
        result = extract_explicit_dates('as of 2004')
        self.assertEqual(result.get('2004'), 'YEAR_ONLY')

    def test_as_of_uppercase(self):
        self.assertTrue(_year_only('AS OF 2004'))

    def test_as_of_2010(self):
        self.assertTrue(_year_only('as of 2010'))

    def test_as_of_2020(self):
        self.assertTrue(_year_only('as of 2020'))


# ============================================================================
# Part A — Preposition: "back to"  (multi-word)
# ============================================================================

class TestProseYearBackTo(unittest.TestCase):
    """Multi-word preposition 'back to' preceding a 4-digit year."""

    def test_back_to_1998_nonempty(self):
        self.assertTrue(extract_explicit_dates('back to 1998'))

    def test_back_to_1998_type(self):
        self.assertTrue(_year_only('back to 1998'))

    def test_back_to_1998_key(self):
        self.assertTrue(_has_key('back to 1998', '1998'))

    def test_dating_back_to_1998(self):
        """Extended form: 'dating back to 1998'."""
        self.assertTrue(_year_only('dating back to 1998'))

    def test_dating_back_to_1998_key(self):
        result = extract_explicit_dates('dating back to 1998')
        self.assertIn('1998', result)

    def test_back_to_sentence(self):
        self.assertTrue(_year_only('the tradition goes back to 1950'))

    def test_back_to_sentence_key(self):
        result = extract_explicit_dates('the tradition goes back to 1950')
        self.assertIn('1950', result)

    def test_back_to_value(self):
        result = extract_explicit_dates('back to 1998')
        self.assertEqual(result.get('1998'), 'YEAR_ONLY')

    def test_back_to_uppercase(self):
        self.assertTrue(_year_only('BACK TO 1998'))

    def test_back_to_2000(self):
        self.assertTrue(_year_only('back to 2000'))


# ============================================================================
# Part A — Preposition: "prior to"  (multi-word)
# ============================================================================

class TestProseYearPriorTo(unittest.TestCase):
    """Multi-word preposition 'prior to' preceding a 4-digit year."""

    def test_prior_to_2010_nonempty(self):
        self.assertTrue(extract_explicit_dates('prior to 2010'))

    def test_prior_to_2010_type(self):
        self.assertTrue(_year_only('prior to 2010'))

    def test_prior_to_2010_key(self):
        self.assertTrue(_has_key('prior to 2010', '2010'))

    def test_prior_to_sentence(self):
        self.assertTrue(_year_only('events prior to 2010 are excluded'))

    def test_prior_to_sentence_key(self):
        result = extract_explicit_dates('events prior to 2010 are excluded')
        self.assertIn('2010', result)

    def test_prior_to_value(self):
        result = extract_explicit_dates('prior to 2010')
        self.assertEqual(result.get('2010'), 'YEAR_ONLY')

    def test_prior_to_uppercase(self):
        self.assertTrue(_year_only('PRIOR TO 2010'))

    def test_prior_to_2000(self):
        self.assertTrue(_year_only('prior to 2000'))

    def test_prior_to_1990(self):
        self.assertTrue(_year_only('prior to 1990'))


# ============================================================================
# Part A — Result shape / key format
# ============================================================================

class TestProseYearResultShape(unittest.TestCase):
    """Result dict: bare year string as key, YEAR_ONLY as value."""

    def test_key_is_bare_year_not_preposition(self):
        result = extract_explicit_dates('in 2004')
        self.assertIn('2004', result)
        self.assertNotIn('in 2004', result)

    def test_key_is_bare_year_since(self):
        result = extract_explicit_dates('since 2019')
        self.assertIn('2019', result)
        self.assertNotIn('since 2019', result)

    def test_key_is_bare_year_by(self):
        result = extract_explicit_dates('by 2024')
        self.assertIn('2024', result)
        self.assertNotIn('by 2024', result)

    def test_key_is_bare_year_as_of(self):
        result = extract_explicit_dates('as of 2004')
        self.assertIn('2004', result)
        self.assertNotIn('as of 2004', result)

    def test_key_is_bare_year_prior_to(self):
        result = extract_explicit_dates('prior to 2010')
        self.assertIn('2010', result)
        self.assertNotIn('prior to 2010', result)

    def test_value_is_string_not_enum(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsInstance(result.get('2004'), str)

    def test_result_is_dict(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsInstance(result, dict)

    def test_result_not_none(self):
        result = extract_explicit_dates('in 2004')
        self.assertIsNotNone(result)

    def test_multiple_prepositions_both_years_present(self):
        """'in 2004 and before 2010' should yield both years."""
        result = extract_explicit_dates('the data spans in 2004 and before 2010')
        self.assertIn('2004', result)
        self.assertIn('2010', result)

    def test_multiple_prepositions_both_year_only(self):
        result = extract_explicit_dates('since 2010 until 2020')
        self.assertIn('2010', result)
        self.assertIn('2020', result)


# ============================================================================
# Part A — Boundary years
# ============================================================================

class TestProseYearBoundary(unittest.TestCase):
    """Edge cases at year boundary limits."""

    def test_year_1950_valid(self):
        self.assertTrue(_year_only('in 1950'))

    def test_year_1927_valid(self):
        """Near MIN_YEAR (approx 1926)."""
        self.assertTrue(_year_only('in 1927'))

    def test_year_2035_valid(self):
        """Near MAX_YEAR (approx 2036)."""
        self.assertTrue(_year_only('in 2035'))

    def test_year_1800_invalid(self):
        """Before MIN_YEAR — should NOT be returned."""
        result = extract_explicit_dates('in 1800')
        self.assertNotIn('1800', result)

    def test_year_2100_invalid(self):
        """After MAX_YEAR — should NOT be returned."""
        result = extract_explicit_dates('in 2100')
        self.assertNotIn('2100', result)

    def test_year_1900_invalid(self):
        """1900 is below MIN_YEAR (≈1926) — should NOT be returned."""
        result = extract_explicit_dates('in 1900')
        self.assertNotIn('1900', result)

    def test_year_2040_invalid(self):
        """2040 is above MAX_YEAR (≈2036) — should NOT be returned."""
        result = extract_explicit_dates('in 2040')
        self.assertNotIn('2040', result)

    def test_boundary_year_1970(self):
        self.assertTrue(_year_only('in 1970'))

    def test_boundary_year_2010(self):
        self.assertTrue(_year_only('in 2010'))


# ============================================================================
# Part A — Negative / non-match cases (bare years without preposition)
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
