#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""TDD tests for year-range expression extraction.

620 test cases covering:
  - True positives: YYYY-YYYY bare, from/to, between/and forms
  - False positives: same year, reversed, out-of-range, non-year numbers
  - Edge cases: boundary years, punctuation, adjacency, multiple ranges
  - Crazy inputs: None, malformed, Unicode, HTML
  - Currently-unsupported forms (en dash, spaces, abbreviated year, etc.)

Related GitHub Issue:
    #40 - feat: Parse year-range expressions (e.g., 2014-2015)
    https://github.com/craigtrim/fast-parse-time/issues/40
"""

import unittest
import pytest

from fast_parse_time import extract_explicit_dates


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _year_range(text) -> bool:
    """Return True if at least one YEAR_RANGE entry exists in the result."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and 'YEAR_RANGE' in result.values()
    except Exception:
        return False


def _no_year_range(text) -> bool:
    """Return True if no YEAR_RANGE entry exists (valid false-positive check)."""
    try:
        result = extract_explicit_dates(text)
        return result is None or 'YEAR_RANGE' not in result.values()
    except Exception:
        return True


def _range_key(text: str, key: str) -> bool:
    """Return True if the specific key maps to YEAR_RANGE."""
    try:
        result = extract_explicit_dates(text)
        return result is not None and result.get(key) == 'YEAR_RANGE'
    except Exception:
        return False


def _is_dict_or_none(text) -> bool:
    """Result must be a dict or None — never raise."""
    try:
        result = extract_explicit_dates(text)
        return result is None or isinstance(result, dict)
    except Exception:
        return False


# ============================================================================
# Class 1 — TestHyphenBareValidPairs
# 40 tests: valid YYYY-YYYY pairs, bare (no surrounding text)
# ============================================================================

class TestHyphenBareValidPairs(unittest.TestCase):
    """Bare YYYY-YYYY forms with valid in-range, ascending year pairs."""

    def test_2014_2015(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_2000_2010(self):
        self.assertTrue(_year_range('2000-2010'))

    def test_1990_2000(self):
        self.assertTrue(_year_range('1990-2000'))

    def test_2010_2020(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_2004_2008(self):
        self.assertTrue(_year_range('2004-2008'))

    def test_1960_1970(self):
        self.assertTrue(_year_range('1960-1970'))

    def test_1970_1980(self):
        self.assertTrue(_year_range('1970-1980'))

    def test_1980_1990(self):
        self.assertTrue(_year_range('1980-1990'))

    def test_1930_1940(self):
        self.assertTrue(_year_range('1930-1940'))

    def test_1940_1950(self):
        self.assertTrue(_year_range('1940-1950'))

    def test_1950_1960(self):
        self.assertTrue(_year_range('1950-1960'))

    def test_2020_2025(self):
        self.assertTrue(_year_range('2020-2025'))

    def test_2025_2030(self):
        self.assertTrue(_year_range('2025-2030'))

    def test_2030_2035(self):
        self.assertTrue(_year_range('2030-2035'))

    def test_1926_1927(self):
        self.assertTrue(_year_range('1926-1927'))

    def test_1927_1928(self):
        self.assertTrue(_year_range('1927-1928'))

    def test_2001_2002(self):
        self.assertTrue(_year_range('2001-2002'))

    def test_2003_2007(self):
        self.assertTrue(_year_range('2003-2007'))

    def test_2005_2015(self):
        self.assertTrue(_year_range('2005-2015'))

    def test_1955_1965(self):
        self.assertTrue(_year_range('1955-1965'))

    def test_1945_1955(self):
        self.assertTrue(_year_range('1945-1955'))

    def test_1935_1945(self):
        self.assertTrue(_year_range('1935-1945'))

    def test_2009_2011(self):
        self.assertTrue(_year_range('2009-2011'))

    def test_1998_2002(self):
        self.assertTrue(_year_range('1998-2002'))

    def test_2016_2024(self):
        self.assertTrue(_year_range('2016-2024'))

    def test_2024_2026(self):
        self.assertTrue(_year_range('2024-2026'))

    def test_1965_1975(self):
        self.assertTrue(_year_range('1965-1975'))

    def test_1975_1985(self):
        self.assertTrue(_year_range('1975-1985'))

    def test_1985_1995(self):
        self.assertTrue(_year_range('1985-1995'))

    def test_1995_2005(self):
        self.assertTrue(_year_range('1995-2005'))

    def test_2006_2016(self):
        self.assertTrue(_year_range('2006-2016'))

    def test_2007_2017(self):
        self.assertTrue(_year_range('2007-2017'))

    def test_2008_2018(self):
        self.assertTrue(_year_range('2008-2018'))

    def test_2011_2021(self):
        self.assertTrue(_year_range('2011-2021'))

    def test_2012_2022(self):
        self.assertTrue(_year_range('2012-2022'))

    def test_2013_2023(self):
        self.assertTrue(_year_range('2013-2023'))

    def test_2015_2025(self):
        self.assertTrue(_year_range('2015-2025'))

    def test_2017_2027(self):
        self.assertTrue(_year_range('2017-2027'))

    def test_1929_1933(self):
        self.assertTrue(_year_range('1929-1933'))

    def test_1939_1945(self):
        self.assertTrue(_year_range('1939-1945'))


# ============================================================================
# Class 2 — TestHyphenBareConsecutiveYears
# 20 tests: YYYY-YYYY where years differ by exactly 1
# ============================================================================

class TestHyphenBareConsecutiveYears(unittest.TestCase):
    """Consecutive-year pairs: the smallest valid range."""

    def test_2019_2020(self):
        self.assertTrue(_year_range('2019-2020'))

    def test_2020_2021(self):
        self.assertTrue(_year_range('2020-2021'))

    def test_2021_2022(self):
        self.assertTrue(_year_range('2021-2022'))

    def test_2022_2023(self):
        self.assertTrue(_year_range('2022-2023'))

    def test_2023_2024(self):
        self.assertTrue(_year_range('2023-2024'))

    def test_2018_2019(self):
        self.assertTrue(_year_range('2018-2019'))

    def test_2017_2018(self):
        self.assertTrue(_year_range('2017-2018'))

    def test_2016_2017(self):
        self.assertTrue(_year_range('2016-2017'))

    def test_2015_2016(self):
        self.assertTrue(_year_range('2015-2016'))

    def test_2014_2015_consecutive(self):
        self.assertTrue(_year_range('2014-2015'))

    def test_1999_2000(self):
        self.assertTrue(_year_range('1999-2000'))

    def test_1989_1990(self):
        self.assertTrue(_year_range('1989-1990'))

    def test_1979_1980(self):
        self.assertTrue(_year_range('1979-1980'))

    def test_1969_1970(self):
        self.assertTrue(_year_range('1969-1970'))

    def test_1959_1960(self):
        self.assertTrue(_year_range('1959-1960'))

    def test_1949_1950(self):
        self.assertTrue(_year_range('1949-1950'))

    def test_1939_1940(self):
        self.assertTrue(_year_range('1939-1940'))

    def test_1929_1930(self):
        self.assertTrue(_year_range('1929-1930'))

    def test_2035_2036(self):
        self.assertTrue(_year_range('2035-2036'))

    def test_2034_2035(self):
        self.assertTrue(_year_range('2034-2035'))


# ============================================================================
# Class 3 — TestHyphenInSentenceStart
# 15 tests: Year range at the start of a sentence
# ============================================================================

class TestHyphenInSentenceStart(unittest.TestCase):
    """Year range appears at the beginning of a sentence."""

    def test_2014_2015_start(self):
        self.assertTrue(_year_range('2014-2015 was a pivotal period.'))

    def test_2000_2010_start(self):
        self.assertTrue(_year_range('2000-2010 saw dramatic changes.'))

    def test_1990_2000_start(self):
        self.assertTrue(_year_range('1990-2000 was the last decade of the century.'))

    def test_1939_1945_start(self):
        self.assertTrue(_year_range('1939-1945 marked World War II.'))

    def test_2008_2009_start(self):
        self.assertTrue(_year_range('2008-2009 were years of financial crisis.'))

    def test_2020_2021_start(self):
        self.assertTrue(_year_range('2020-2021 brought the global pandemic.'))

    def test_2010_2015_start(self):
        self.assertTrue(_year_range('2010-2015 are the years I want to highlight.'))

    def test_1960_1970_start(self):
        self.assertTrue(_year_range('1960-1970 covered the space race.'))

    def test_2001_2003_start(self):
        self.assertTrue(_year_range('2001-2003 followed the dot-com crash.'))

    def test_1950_1960_start(self):
        self.assertTrue(_year_range('1950-1960 was the postwar boom.'))

    def test_2015_2020_start(self):
        self.assertTrue(_year_range('2015-2020 shaped the modern tech landscape.'))

    def test_2024_2026_start(self):
        self.assertTrue(_year_range('2024-2026 will be years of AI growth.'))

    def test_1926_1936_start(self):
        self.assertTrue(_year_range('1926-1936 saw the Great Depression.'))

    def test_1980_1990_start(self):
        self.assertTrue(_year_range('1980-1990 is often called the decade of excess.'))

    def test_1970_1975_start(self):
        self.assertTrue(_year_range('1970-1975 were challenging economic years.'))


# ============================================================================
# Class 4 — TestHyphenInSentenceMiddle
# 15 tests: Year range embedded in the middle of a sentence
# ============================================================================

class TestHyphenInSentenceMiddle(unittest.TestCase):
    """Year range appears in the middle of a sentence."""

    def test_period_2014_2015(self):
        self.assertTrue(_year_range('The period 2014-2015 was significant.'))

    def test_during_2000_2010(self):
        self.assertTrue(_year_range('Economic growth during 2000-2010 was uneven.'))

    def test_between_wars_1918_1939(self):
        self.assertTrue(_year_range('The interwar period 1918-1939 reshaped Europe. The period 1930-1940 was also critical.'))

    def test_years_1990_2000(self):
        self.assertTrue(_year_range('The years 1990-2000 are sometimes called the long boom.'))

    def test_span_1960_1970(self):
        self.assertTrue(_year_range('The decade span 1960-1970 saw rapid change.'))

    def test_era_2001_2009(self):
        self.assertTrue(_year_range('The era 2001-2009 redefined security.'))

    def test_window_2010_2015(self):
        self.assertTrue(_year_range('This window, 2010-2015, was critical.'))

    def test_from_to_via_hyphen(self):
        self.assertTrue(_year_range('The range 2004-2008 covers four years.'))

    def test_recent_1999_2004(self):
        self.assertTrue(_year_range('In the recent past 1999-2004 we saw innovation.'))

    def test_postwar_1945_1955(self):
        self.assertTrue(_year_range('The postwar era 1945-1955 was remarkable.'))

    def test_employment_2008_2012(self):
        self.assertTrue(_year_range('High unemployment in 2008-2012 hit hard.'))

    def test_comma_before(self):
        self.assertTrue(_year_range('Revenue in, 2015-2020, declined.'))

    def test_colon_before(self):
        self.assertTrue(_year_range('Results: 2010-2018 showed growth.'))

    def test_dash_context(self):
        self.assertTrue(_year_range('The years — 2012-2016 — were transformative.'))

    def test_quote_context(self):
        self.assertTrue(_year_range('"2014-2015" is the period under review.'))


# ============================================================================
# Class 5 — TestHyphenInSentenceEnd
# 15 tests: Year range at the end of a sentence
# ============================================================================

class TestHyphenInSentenceEnd(unittest.TestCase):
    """Year range appears at the end of a sentence."""

    def test_ref_2014_2015(self):
        self.assertTrue(_year_range('See the data for 2014-2015'))

    def test_covers_2000_2010(self):
        self.assertTrue(_year_range('The study covers 2000-2010'))

    def test_relevant_1990_2000(self):
        self.assertTrue(_year_range('Data is most relevant for 1990-2000'))

    def test_analysis_1960_1970(self):
        self.assertTrue(_year_range('The analysis spans 1960-1970'))

    def test_focus_2015_2020(self):
        self.assertTrue(_year_range('The report focuses on 2015-2020'))

    def test_period_2008_2012(self):
        self.assertTrue(_year_range('The crisis period: 2008-2012'))

    def test_refer_1950_1960(self):
        self.assertTrue(_year_range('All figures refer to 1950-1960'))

    def test_war_years_1939_1945(self):
        self.assertTrue(_year_range('These are the war years 1939-1945'))

    def test_boom_1945_1955(self):
        self.assertTrue(_year_range('The boom years were 1945-1955'))

    def test_dot_com_1995_2001(self):
        self.assertTrue(_year_range('Peak dot-com era: 1995-2001'))

    def test_decade_2010_2020(self):
        self.assertTrue(_year_range('The last full decade was 2010-2020'))

    def test_trailing_period(self):
        self.assertTrue(_year_range('Data covers 2014-2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_year_range('Data covers 2014-2015,'))

    def test_trailing_question(self):
        self.assertTrue(_year_range('Does it cover 2014-2015?'))

    def test_trailing_exclamation(self):
        self.assertTrue(_year_range('What a span: 2014-2015!'))


# ============================================================================
# Class 6 — TestHyphenWithSurroundingPunctuation
# 20 tests: Year range surrounded by various punctuation
# ============================================================================

class TestHyphenWithSurroundingPunctuation(unittest.TestCase):
    """Surrounding punctuation should not prevent YEAR_RANGE detection."""

    def test_parens(self):
        self.assertTrue(_year_range('(2014-2015)'))

    def test_brackets(self):
        self.assertTrue(_year_range('[2014-2015]'))

    def test_curly(self):
        self.assertTrue(_year_range('{2014-2015}'))

    def test_quotes_double(self):
        self.assertTrue(_year_range('"2014-2015"'))

    def test_quotes_single(self):
        self.assertTrue(_year_range("'2014-2015'"))

    def test_trailing_period(self):
        self.assertTrue(_year_range('2014-2015.'))

    def test_trailing_comma(self):
        self.assertTrue(_year_range('2014-2015,'))

    def test_trailing_semicolon(self):
        self.assertTrue(_year_range('2014-2015;'))

    def test_trailing_colon(self):
        self.assertTrue(_year_range('2014-2015:'))

    def test_trailing_question(self):
        self.assertTrue(_year_range('2014-2015?'))

    def test_trailing_exclamation(self):
        self.assertTrue(_year_range('2014-2015!'))

    def test_parens_in_sentence(self):
        self.assertTrue(_year_range('The era (2014-2015) was notable.'))

    def test_brackets_in_sentence(self):
        self.assertTrue(_year_range('See [2014-2015] for data.'))

    def test_period_in_sentence(self):
        self.assertTrue(_year_range('We covered 2014-2015. Then 2016 came.'))

    def test_comma_in_sentence(self):
        self.assertTrue(_year_range('The years 2014-2015, were busy.'))

    def test_colon_in_sentence(self):
        self.assertTrue(_year_range('Revenue: 2014-2015, grew quickly.'))

    def test_slash_after(self):
        self.assertTrue(_year_range('Report 2014-2015/annual'))

    def test_angle_brackets(self):
        self.assertTrue(_year_range('<2014-2015>'))

    def test_parens_wrapped_sentence(self):
        self.assertTrue(_year_range('(see: 2014-2015)'))

    def test_mixed_punct(self):
        self.assertTrue(_year_range('[period: 2014-2015]'))


# ============================================================================
# Class 7 — TestHyphenBoundaryYears
# 20 tests: Years near MIN_YEAR (1926) and MAX_YEAR (2036)
# ============================================================================

class TestHyphenBoundaryYears(unittest.TestCase):
    """Test year pairs near the valid MIN_YEAR/MAX_YEAR boundaries."""

    def test_at_min_year_start(self):
        """MIN_YEAR-1927: first valid pair starting at MIN_YEAR."""
        self.assertTrue(_year_range('1926-1927'))

    def test_near_min_year(self):
        self.assertTrue(_year_range('1926-1936'))

    def test_one_above_min(self):
        self.assertTrue(_year_range('1927-1928'))

    def test_two_above_min(self):
        self.assertTrue(_year_range('1928-1930'))

    def test_five_above_min(self):
        self.assertTrue(_year_range('1931-1940'))

    def test_ten_above_min(self):
        self.assertTrue(_year_range('1936-1946'))

    def test_near_max_year_end(self):
        """MAX_YEAR is 2036; 2035-2036 should be valid."""
        self.assertTrue(_year_range('2035-2036'))

    def test_at_max_year(self):
        self.assertTrue(_year_range('2025-2036'))

    def test_one_below_max(self):
        self.assertTrue(_year_range('2034-2035'))

    def test_two_below_max(self):
        self.assertTrue(_year_range('2033-2034'))

    def test_five_below_max(self):
        self.assertTrue(_year_range('2030-2035'))

    def test_ten_below_max(self):
        self.assertTrue(_year_range('2026-2034'))

    def test_cross_min_boundary_invalid(self):
        """1925-1927: 1925 is below MIN_YEAR; no YEAR_RANGE expected."""
        self.assertTrue(_no_year_range('1925-1927'))

    def test_below_min_year_invalid(self):
        """1800-1900: both below MIN_YEAR."""
        self.assertTrue(_no_year_range('1800-1900'))

    def test_above_max_year_invalid(self):
        """2040-2050: both above MAX_YEAR."""
        self.assertTrue(_no_year_range('2040-2050'))

    def test_cross_max_boundary_invalid(self):
        """2035-2040: 2040 above MAX_YEAR; no YEAR_RANGE expected."""
        self.assertTrue(_no_year_range('2035-2040'))

    def test_only_end_out_of_range(self):
        """2025-2099: end year out of range."""
        self.assertTrue(_no_year_range('2025-2099'))

    def test_only_start_out_of_range(self):
        """1899-2010: start year out of range."""
        self.assertTrue(_no_year_range('1899-2010'))

    def test_both_at_valid_boundary(self):
        """1926 to 2036: full span of valid range."""
        self.assertTrue(_year_range('1926-2036'))

    def test_near_boundary_valid(self):
        self.assertTrue(_year_range('1928-1929'))


# ============================================================================
# Class 8 — TestHyphenSameYearNotRange
# 15 tests: Same year on both sides should NOT be a YEAR_RANGE
# ============================================================================

class TestHyphenSameYearNotRange(unittest.TestCase):
    """Same-year hyphenated pairs are not year ranges."""

    def test_2014_2014(self):
        self.assertTrue(_no_year_range('2014-2014'))

    def test_2000_2000(self):
        self.assertTrue(_no_year_range('2000-2000'))

    def test_2020_2020(self):
        self.assertTrue(_no_year_range('2020-2020'))

    def test_1990_1990(self):
        self.assertTrue(_no_year_range('1990-1990'))

    def test_1960_1960(self):
        self.assertTrue(_no_year_range('1960-1960'))

    def test_1950_1950(self):
        self.assertTrue(_no_year_range('1950-1950'))

    def test_1940_1940(self):
        self.assertTrue(_no_year_range('1940-1940'))

    def test_1930_1930(self):
        self.assertTrue(_no_year_range('1930-1930'))

    def test_2010_2010(self):
        self.assertTrue(_no_year_range('2010-2010'))

    def test_2015_2015(self):
        self.assertTrue(_no_year_range('2015-2015'))

    def test_2024_2024(self):
        self.assertTrue(_no_year_range('2024-2024'))

    def test_1926_1926(self):
        self.assertTrue(_no_year_range('1926-1926'))

    def test_2036_2036(self):
        self.assertTrue(_no_year_range('2036-2036'))

    def test_2001_2001(self):
        self.assertTrue(_no_year_range('2001-2001'))

    def test_1975_1975(self):
        self.assertTrue(_no_year_range('1975-1975'))


# ============================================================================
# Class 9 — TestHyphenReversedNotRange
# 15 tests: Reversed (end < start) must not be YEAR_RANGE
# ============================================================================

class TestHyphenReversedNotRange(unittest.TestCase):
    """Reversed year order is not a valid range."""

    def test_2015_2014(self):
        self.assertTrue(_no_year_range('2015-2014'))

    def test_2010_2000(self):
        self.assertTrue(_no_year_range('2010-2000'))

    def test_2000_1990(self):
        self.assertTrue(_no_year_range('2000-1990'))

    def test_1990_1980(self):
        self.assertTrue(_no_year_range('1990-1980'))

    def test_1970_1960(self):
        self.assertTrue(_no_year_range('1970-1960'))

    def test_2020_2019(self):
        self.assertTrue(_no_year_range('2020-2019'))

    def test_2024_2023(self):
        self.assertTrue(_no_year_range('2024-2023'))

    def test_2030_2020(self):
        self.assertTrue(_no_year_range('2030-2020'))

    def test_1960_1950(self):
        self.assertTrue(_no_year_range('1960-1950'))

    def test_1950_1940(self):
        self.assertTrue(_no_year_range('1950-1940'))

    def test_1940_1930(self):
        self.assertTrue(_no_year_range('1940-1930'))

    def test_1980_1970(self):
        self.assertTrue(_no_year_range('1980-1970'))

    def test_2036_2026(self):
        self.assertTrue(_no_year_range('2036-2026'))

    def test_2000_1926(self):
        self.assertTrue(_no_year_range('2000-1926'))

    def test_2015_2014_in_sentence(self):
        self.assertTrue(_no_year_range('The period 2015-2014 is odd.'))


# ============================================================================
# Class 10 — TestHyphenOutOfRangeYears
# 20 tests: Year values outside MIN_YEAR..MAX_YEAR range
# ============================================================================

class TestHyphenOutOfRangeYears(unittest.TestCase):
    """Out-of-range years should not produce YEAR_RANGE."""

    def test_1800_1900(self):
        self.assertTrue(_no_year_range('1800-1900'))

    def test_1700_1800(self):
        self.assertTrue(_no_year_range('1700-1800'))

    def test_1000_1500(self):
        self.assertTrue(_no_year_range('1000-1500'))

    def test_0001_1000(self):
        self.assertTrue(_no_year_range('0001-1000'))

    def test_2040_2050(self):
        self.assertTrue(_no_year_range('2040-2050'))

    def test_2050_2060(self):
        self.assertTrue(_no_year_range('2050-2060'))

    def test_2100_2200(self):
        self.assertTrue(_no_year_range('2100-2200'))

    def test_9000_9999(self):
        self.assertTrue(_no_year_range('9000-9999'))

    def test_1920_1930(self):
        """1920-1930: 1920 is below MIN_YEAR (1926)."""
        self.assertTrue(_no_year_range('1920-1930'))

    def test_1924_1926(self):
        """1924 < MIN_YEAR."""
        self.assertTrue(_no_year_range('1924-1926'))

    def test_1925_1930(self):
        """1925 < MIN_YEAR."""
        self.assertTrue(_no_year_range('1925-1930'))

    def test_2036_2037(self):
        """2037 > MAX_YEAR (2036)."""
        self.assertTrue(_no_year_range('2036-2037'))

    def test_2037_2040(self):
        self.assertTrue(_no_year_range('2037-2040'))

    def test_2038_2050(self):
        self.assertTrue(_no_year_range('2038-2050'))

    def test_1899_1901(self):
        self.assertTrue(_no_year_range('1899-1901'))

    def test_1910_1920(self):
        self.assertTrue(_no_year_range('1910-1920'))

    def test_1900_1910(self):
        self.assertTrue(_no_year_range('1900-1910'))

    def test_1234_1235(self):
        self.assertTrue(_no_year_range('1234-1235'))

    def test_1111_1112(self):
        self.assertTrue(_no_year_range('1111-1112'))

    def test_3000_4000(self):
        self.assertTrue(_no_year_range('3000-4000'))


# ============================================================================
# Class 11 — TestHyphenNonYearNumbers
# 20 tests: 4-digit or other number combos that aren't year ranges
# ============================================================================

class TestHyphenNonYearNumbers(unittest.TestCase):
    """Numbers that look like year ranges but aren't (not in valid range, etc.)."""

    def test_phone_555_1234(self):
        """555-1234: not 4-digit pairs in valid year range."""
        self.assertTrue(_no_year_range('555-1234'))

    def test_page_range_3_10(self):
        self.assertTrue(_no_year_range('pages 3-10'))

    def test_page_range_100_200(self):
        self.assertTrue(_no_year_range('pages 100-200'))

    def test_version_1_2(self):
        self.assertTrue(_no_year_range('version 1-2'))

    def test_score_3_0(self):
        self.assertTrue(_no_year_range('score 3-0'))

    def test_isbn_like(self):
        self.assertTrue(_no_year_range('978-3-16'))

    def test_zip_90210_1234(self):
        """ZIP+4: 90210-1234 — 90210 and 1234 not in year range."""
        self.assertTrue(_no_year_range('90210-1234'))

    def test_small_small(self):
        self.assertTrue(_no_year_range('12-34'))

    def test_large_large(self):
        self.assertTrue(_no_year_range('10000-20000'))

    def test_not_four_digits_each(self):
        self.assertTrue(_no_year_range('20-2015'))

    def test_five_digit_first(self):
        self.assertTrue(_no_year_range('20145-2016'))

    def test_five_digit_second(self):
        self.assertTrue(_no_year_range('2014-20155'))

    def test_zero_range(self):
        self.assertTrue(_no_year_range('0000-0000'))

    def test_all_nines(self):
        self.assertTrue(_no_year_range('9999-9998'))

    def test_ssn_like(self):
        self.assertTrue(_no_year_range('123-45-6789'))

    def test_time_range(self):
        """9-5 job: not year range."""
        self.assertTrue(_no_year_range('9-5 job'))

    def test_channel_range(self):
        self.assertTrue(_no_year_range('channels 100-200'))

    def test_zip_code_like(self):
        self.assertTrue(_no_year_range('12345-6789'))

    def test_product_code(self):
        self.assertTrue(_no_year_range('SKU-1234'))

    def test_mix_alpha_num(self):
        self.assertTrue(_no_year_range('A2014-B2015'))


# ============================================================================
# Class 12 — TestHyphenAdjacentNonBoundary
# 10 tests: Year-like strings that don't have word boundaries
# ============================================================================

class TestHyphenAdjacentNonBoundary(unittest.TestCase):
    """Year ranges abutting alpha chars lack word boundary; should not match."""

    def test_prefix_alpha(self):
        """abc2014-2015: no word boundary before 2014."""
        self.assertTrue(_no_year_range('abc2014-2015'))

    def test_suffix_alpha(self):
        """2014-2015xyz: no word boundary after 2015."""
        self.assertTrue(_no_year_range('2014-2015xyz'))

    def test_both_sides_alpha(self):
        self.assertTrue(_no_year_range('x2014-2015y'))

    def test_prefix_underscore(self):
        """_2014-2015: underscore is a word char, so no boundary before 2014."""
        self.assertTrue(_no_year_range('_2014-2015'))

    def test_suffix_underscore(self):
        self.assertTrue(_no_year_range('2014-2015_suffix'))

    def test_embedded_in_word(self):
        self.assertTrue(_no_year_range('report2014-2015data'))

    def test_camel_case_prefix(self):
        self.assertTrue(_no_year_range('Year2014-2015'))

    def test_camel_case_suffix(self):
        self.assertTrue(_no_year_range('2014-2015Year'))

    def test_digit_prefix(self):
        """32014-2015: 5-digit first token, no match."""
        self.assertTrue(_no_year_range('32014-2015'))

    def test_digit_suffix(self):
        """2014-20153: 5-digit second token, no match."""
        self.assertTrue(_no_year_range('2014-20153'))


# ============================================================================
# Class 13 — TestHyphenResultKeyFormat
# 15 tests: Verify the key in result is exactly "YYYY-YYYY"
# ============================================================================

class TestHyphenResultKeyFormat(unittest.TestCase):
    """The result dict key for YYYY-YYYY should be the 'YYYY-YYYY' string."""

    def test_key_2014_2015(self):
        self.assertTrue(_range_key('2014-2015', '2014-2015'))

    def test_key_2000_2010(self):
        self.assertTrue(_range_key('2000-2010', '2000-2010'))

    def test_key_1990_2000(self):
        self.assertTrue(_range_key('1990-2000', '1990-2000'))

    def test_key_2004_2008(self):
        self.assertTrue(_range_key('2004-2008', '2004-2008'))

    def test_key_1960_1970(self):
        self.assertTrue(_range_key('1960-1970', '1960-1970'))

    def test_key_2019_2020(self):
        self.assertTrue(_range_key('2019-2020', '2019-2020'))

    def test_key_in_sentence(self):
        self.assertTrue(_range_key('The era 2014-2015 passed.', '2014-2015'))

    def test_key_1926_1927(self):
        self.assertTrue(_range_key('1926-1927', '1926-1927'))

    def test_key_2035_2036(self):
        self.assertTrue(_range_key('2035-2036', '2035-2036'))

    def test_key_1939_1945(self):
        self.assertTrue(_range_key('1939-1945', '1939-1945'))

    def test_key_2020_2025(self):
        self.assertTrue(_range_key('2020-2025', '2020-2025'))

    def test_key_not_swapped(self):
        """Key should be 2014-2015, not 2015-2014."""
        result = extract_explicit_dates('2014-2015')
        self.assertIn('2014-2015', result or {})
        self.assertNotIn('2015-2014', result or {})

    def test_key_2010_2020(self):
        self.assertTrue(_range_key('2010-2020', '2010-2020'))

    def test_key_1975_1985(self):
        self.assertTrue(_range_key('1975-1985', '1975-1985'))

    def test_key_with_punctuation(self):
        self.assertTrue(_range_key('(2014-2015)', '2014-2015'))


# ============================================================================
# Class 14 — TestHyphenResultValueFormat
# 15 tests: The dict value must be the string 'YEAR_RANGE'
# ============================================================================

class TestHyphenResultValueFormat(unittest.TestCase):
    """Verify the value in result dict is the string 'YEAR_RANGE'."""

    def test_value_2014_2015(self):
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_2000_2010(self):
        result = extract_explicit_dates('2000-2010')
        self.assertEqual(result.get('2000-2010'), 'YEAR_RANGE')

    def test_value_1990_2000(self):
        result = extract_explicit_dates('1990-2000')
        self.assertEqual(result.get('1990-2000'), 'YEAR_RANGE')

    def test_value_2004_2008(self):
        result = extract_explicit_dates('2004-2008')
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_value_is_string(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result.get('2014-2015'), str)

    def test_value_not_enum(self):
        """Should be string 'YEAR_RANGE', not a DateType enum member."""
        result = extract_explicit_dates('2014-2015')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_exact_case(self):
        result = extract_explicit_dates('2014-2015')
        self.assertNotEqual(result.get('2014-2015'), 'year_range')

    def test_value_not_year_only(self):
        result = extract_explicit_dates('2014-2015')
        self.assertNotEqual(result.get('2014-2015'), 'YEAR_ONLY')

    def test_value_1939_1945(self):
        result = extract_explicit_dates('1939-1945')
        self.assertEqual(result.get('1939-1945'), 'YEAR_RANGE')

    def test_value_2019_2020(self):
        result = extract_explicit_dates('2019-2020')
        self.assertEqual(result.get('2019-2020'), 'YEAR_RANGE')

    def test_value_1926_1927(self):
        result = extract_explicit_dates('1926-1927')
        self.assertEqual(result.get('1926-1927'), 'YEAR_RANGE')

    def test_value_2035_2036(self):
        result = extract_explicit_dates('2035-2036')
        self.assertEqual(result.get('2035-2036'), 'YEAR_RANGE')

    def test_value_in_sentence(self):
        result = extract_explicit_dates('The era 2014-2015 was notable.')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_with_parens(self):
        result = extract_explicit_dates('(2014-2015)')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')

    def test_value_trailing_period(self):
        result = extract_explicit_dates('2014-2015.')
        self.assertEqual(result.get('2014-2015'), 'YEAR_RANGE')


# ============================================================================
# Class 15 — TestHyphenResultIsDict
# 10 tests: Result must always be a dict or None, never raise
# ============================================================================

class TestHyphenResultIsDict(unittest.TestCase):
    """extract_explicit_dates must return dict or None for year-range inputs."""

    def test_valid_returns_dict(self):
        result = extract_explicit_dates('2014-2015')
        self.assertIsInstance(result, dict)

    def test_invalid_returns_dict_or_none(self):
        self.assertTrue(_is_dict_or_none('2015-2014'))

    def test_none_input_safe(self):
        self.assertTrue(_is_dict_or_none(None))

    def test_empty_input_safe(self):
        self.assertTrue(_is_dict_or_none(''))

    def test_out_of_range_safe(self):
        self.assertTrue(_is_dict_or_none('1800-1900'))

    def test_same_year_safe(self):
        self.assertTrue(_is_dict_or_none('2014-2014'))

    def test_random_text_safe(self):
        self.assertTrue(_is_dict_or_none('no dates here'))

    def test_partial_match_safe(self):
        self.assertTrue(_is_dict_or_none('2014'))

    def test_weird_chars_safe(self):
        self.assertTrue(_is_dict_or_none('!!!###$$$'))

    def test_valid_result_nonempty(self):
        result = extract_explicit_dates('2014-2015')
        self.assertGreater(len(result), 0)


# ============================================================================
# Class 16 — TestHyphenMultipleRanges
# 15 tests: Texts with multiple year ranges
# ============================================================================

class TestHyphenMultipleRanges(unittest.TestCase):
    """Multiple year ranges in a single text."""

    def test_two_ranges_both_detected(self):
        result = extract_explicit_dates('The periods 2000-2010 and 2014-2015 both matter.')
        self.assertIn('2000-2010', result or {})
        self.assertIn('2014-2015', result or {})

    def test_two_ranges_year_range_present(self):
        self.assertTrue(_year_range('The periods 2000-2010 and 2014-2015 both matter.'))

    def test_three_ranges(self):
        result = extract_explicit_dates('1990-2000, 2000-2010, and 2010-2020 were all important.')
        values = list((result or {}).values())
        self.assertGreaterEqual(values.count('YEAR_RANGE'), 1)

    def test_adjacent_ranges_no_overlap(self):
        result = extract_explicit_dates('2000-2005 and 2005-2010')
        self.assertIn('2000-2005', result or {})
        self.assertIn('2005-2010', result or {})

    def test_two_ranges_result_size(self):
        result = extract_explicit_dates('2000-2010 and 2014-2015') or {}
        year_range_count = sum(1 for v in result.values() if v == 'YEAR_RANGE')
        self.assertGreaterEqual(year_range_count, 2)

    def test_range_and_year_only(self):
        """One YEAR_RANGE and one YEAR_ONLY in same text."""
        result = extract_explicit_dates('In 2024 the period 2014-2015 was recalled.') or {}
        self.assertIn('YEAR_RANGE', result.values())
        self.assertIn('YEAR_ONLY', result.values())

    def test_two_ranges_different_spans(self):
        self.assertTrue(_year_range('1939-1945 and 2001-2010 are notable.'))

    def test_overlapping_year_ranges(self):
        """2000-2010 and 2005-2015 share 2005-2010."""
        result = extract_explicit_dates('The overlapping spans 2000-2010 and 2005-2015.') or {}
        self.assertIn('2000-2010', result)
        self.assertIn('2005-2015', result)

    def test_range_after_standalone_year(self):
        result = extract_explicit_dates('In 2020, the range 2014-2018 was reviewed.') or {}
        self.assertIn('YEAR_RANGE', result.values())

    def test_range_and_written_date(self):
        self.assertTrue(_year_range('March 2020 and the period 2014-2015.'))

    def test_two_invalid_one_valid(self):
        """1800-1900 invalid, 2014-2015 valid: only second should match."""
        result = extract_explicit_dates('From 1800-1900 and now 2014-2015.') or {}
        self.assertNotIn('1800-1900', result)
        self.assertIn('2014-2015', result)

    def test_same_range_twice(self):
        result = extract_explicit_dates('2014-2015 and again 2014-2015.') or {}
        self.assertIn('2014-2015', result)

    def test_four_ranges(self):
        text = '1960-1970, 1970-1980, 1980-1990, 1990-2000'
        self.assertTrue(_year_range(text))

    def test_range_in_list(self):
        text = '- 2000-2005\n- 2005-2010\n- 2010-2015'
        self.assertTrue(_year_range(text))

    def test_range_in_parenthetical(self):
        self.assertTrue(_year_range('Revenue (2014-2015) and costs (2016-2017) both rose.'))


# ============================================================================
# Class 17 — TestHyphenSpanSizes
# 15 tests: Various span sizes from 1 to 100 years
# ============================================================================

class TestHyphenSpanSizes(unittest.TestCase):
    """Valid ranges of varying year-span sizes."""

    def test_span_1_year(self):
        self.assertTrue(_year_range('2019-2020'))

    def test_span_2_years(self):
        self.assertTrue(_year_range('2018-2020'))

    def test_span_3_years(self):
        self.assertTrue(_year_range('2017-2020'))

    def test_span_4_years(self):
        self.assertTrue(_year_range('2016-2020'))

    def test_span_5_years(self):
        self.assertTrue(_year_range('2015-2020'))

    def test_span_10_years(self):
        self.assertTrue(_year_range('2010-2020'))

    def test_span_15_years(self):
        self.assertTrue(_year_range('2005-2020'))

    def test_span_20_years(self):
        self.assertTrue(_year_range('2000-2020'))

    def test_span_25_years(self):
        self.assertTrue(_year_range('1995-2020'))

    def test_span_30_years(self):
        self.assertTrue(_year_range('1990-2020'))

    def test_span_40_years(self):
        self.assertTrue(_year_range('1980-2020'))

    def test_span_50_years(self):
        self.assertTrue(_year_range('1970-2020'))

    def test_span_60_years(self):
        self.assertTrue(_year_range('1960-2020'))

    def test_span_70_years(self):
        self.assertTrue(_year_range('1950-2020'))

    def test_span_110_years_full_range(self):
        """Span from MIN_YEAR to MAX_YEAR: 1926-2036."""
        self.assertTrue(_year_range('1926-2036'))


# ============================================================================
# Class 18 — TestFromToValidPairs
# 30 tests: "from YYYY to YYYY" valid pairs
# ============================================================================

class TestFromToValidPairs(unittest.TestCase):
    """'from YYYY to YYYY' produces YEAR_RANGE for valid pairs."""

    def test_from_2004_to_2008(self):
        self.assertTrue(_year_range('from 2004 to 2008'))

    def test_from_2000_to_2010(self):
        self.assertTrue(_year_range('from 2000 to 2010'))

    def test_from_1990_to_2000(self):
        self.assertTrue(_year_range('from 1990 to 2000'))

    def test_from_2010_to_2020(self):
        self.assertTrue(_year_range('from 2010 to 2020'))

    def test_from_1960_to_1970(self):
        self.assertTrue(_year_range('from 1960 to 1970'))

    def test_from_1950_to_1960(self):
        self.assertTrue(_year_range('from 1950 to 1960'))

    def test_from_1940_to_1950(self):
        self.assertTrue(_year_range('from 1940 to 1950'))

    def test_from_1930_to_1940(self):
        self.assertTrue(_year_range('from 1930 to 1940'))

    def test_from_1926_to_1936(self):
        self.assertTrue(_year_range('from 1926 to 1936'))

    def test_from_2019_to_2020(self):
        self.assertTrue(_year_range('from 2019 to 2020'))

    def test_from_2014_to_2015(self):
        self.assertTrue(_year_range('from 2014 to 2015'))

    def test_from_2020_to_2025(self):
        self.assertTrue(_year_range('from 2020 to 2025'))

    def test_from_2025_to_2030(self):
        self.assertTrue(_year_range('from 2025 to 2030'))

    def test_from_2030_to_2035(self):
        self.assertTrue(_year_range('from 2030 to 2035'))

    def test_from_2035_to_2036(self):
        self.assertTrue(_year_range('from 2035 to 2036'))

    def test_from_1970_to_2000(self):
        self.assertTrue(_year_range('from 1970 to 2000'))

    def test_from_1939_to_1945(self):
        self.assertTrue(_year_range('from 1939 to 1945'))

    def test_from_1945_to_1955(self):
        self.assertTrue(_year_range('from 1945 to 1955'))

    def test_from_1955_to_1965(self):
        self.assertTrue(_year_range('from 1955 to 1965'))

    def test_from_1965_to_1975(self):
        self.assertTrue(_year_range('from 1965 to 1975'))

    def test_from_1975_to_1985(self):
        self.assertTrue(_year_range('from 1975 to 1985'))

    def test_from_1985_to_1995(self):
        self.assertTrue(_year_range('from 1985 to 1995'))

    def test_from_1995_to_2005(self):
        self.assertTrue(_year_range('from 1995 to 2005'))

    def test_from_2005_to_2015(self):
        self.assertTrue(_year_range('from 2005 to 2015'))

    def test_from_2015_to_2025(self):
        self.assertTrue(_year_range('from 2015 to 2025'))

    def test_from_key_format(self):
        """from-to produces 'YYYY-YYYY' key in result."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)

    def test_from_value_format(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_from_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_from_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertTrue(len(result) >= 1)

    def test_from_1926_to_2036(self):
        """Full valid range."""
        self.assertTrue(_year_range('from 1926 to 2036'))


# ============================================================================
# Class 19 — TestFromToInSentence
# 15 tests: "from YYYY to YYYY" embedded in sentences
# ============================================================================

class TestFromToInSentence(unittest.TestCase):
    """'from YYYY to YYYY' inside longer sentences."""

    def test_he_worked_2005_to_2015(self):
        self.assertTrue(_year_range('He worked there from 2005 to 2015.'))

    def test_the_project_ran(self):
        self.assertTrue(_year_range('The project ran from 2010 to 2015.'))

    def test_the_war_lasted(self):
        self.assertTrue(_year_range('The war lasted from 1939 to 1945.'))

    def test_revenue_grew(self):
        self.assertTrue(_year_range('Revenue grew from 2000 to 2010.'))

    def test_she_studied(self):
        self.assertTrue(_year_range('She studied from 2015 to 2019.'))

    def test_population_tripled(self):
        self.assertTrue(_year_range('Population tripled from 1960 to 1980.'))

    def test_the_policy(self):
        self.assertTrue(_year_range('The policy was in effect from 2004 to 2008.'))

    def test_records_go_back(self):
        self.assertTrue(_year_range('Records go back from 1930 to 1940.'))

    def test_he_led_the_team(self):
        self.assertTrue(_year_range('He led the team from 2014 to 2016.'))

    def test_the_boom(self):
        self.assertTrue(_year_range('The boom period, from 1990 to 2000, was extraordinary.'))

    def test_with_comma(self):
        self.assertTrue(_year_range('From 2004 to 2008, growth was strong.'))

    def test_after_conjunction(self):
        self.assertTrue(_year_range('Profits rose and then from 2010 to 2015 declined.'))

    def test_at_end(self):
        self.assertTrue(_year_range('The project ran from 2010 to 2015'))

    def test_with_quotes(self):
        self.assertTrue(_year_range('"from 2004 to 2008" is the relevant period'))

    def test_with_parens(self):
        self.assertTrue(_year_range('(from 2004 to 2008) is key'))


# ============================================================================
# Class 20 — TestFromToCasing
# 15 tests: Casing variants of "from YYYY to YYYY"
# ============================================================================

class TestFromToCasing(unittest.TestCase):
    """Case insensitivity for 'from YYYY to YYYY'."""

    def test_uppercase_from_to(self):
        self.assertTrue(_year_range('FROM 2004 TO 2008'))

    def test_title_case(self):
        self.assertTrue(_year_range('From 2004 To 2008'))

    def test_from_upper_to_lower(self):
        self.assertTrue(_year_range('FROM 2004 to 2008'))

    def test_from_lower_to_upper(self):
        self.assertTrue(_year_range('from 2004 TO 2008'))

    def test_mixed_case_1(self):
        self.assertTrue(_year_range('FrOm 2004 tO 2008'))

    def test_mixed_case_2(self):
        self.assertTrue(_year_range('fROM 2004 To 2008'))

    def test_all_caps_in_sentence(self):
        self.assertTrue(_year_range('THE PERIOD FROM 2004 TO 2008 WAS KEY.'))

    def test_title_in_sentence(self):
        self.assertTrue(_year_range('The Period From 2004 To 2008 Was Key.'))

    def test_from_lower_in_sentence(self):
        self.assertTrue(_year_range('It ran from 2004 to 2008.'))

    def test_from_upper_in_sentence(self):
        self.assertTrue(_year_range('It ran FROM 2004 TO 2008.'))

    def test_from_title_in_sentence(self):
        self.assertTrue(_year_range('It ran From 2004 To 2008.'))

    def test_random_caps_1(self):
        self.assertTrue(_year_range('FROm 2010 tO 2020'))

    def test_random_caps_2(self):
        self.assertTrue(_year_range('froM 2010 TO 2020'))

    def test_sentence_start_upper(self):
        self.assertTrue(_year_range('From 2014 to 2015 was significant.'))

    def test_sentence_start_lower(self):
        self.assertTrue(_year_range('from 2014 to 2015 was significant.'))


# ============================================================================
# Class 21 — TestFromToWithExtraWhitespace
# 10 tests: Extra spaces in "from YYYY to YYYY"
# MIN_YEAR=1926, MAX_YEAR=2036; valid pairs only
# ============================================================================

class TestFromToWithExtraWhitespace(unittest.TestCase):
    """Extra whitespace between tokens in 'from YYYY to YYYY'."""

    def test_double_space_from(self):
        """'from  2004 to 2008': two spaces after 'from'."""
        self.assertTrue(_year_range('from  2004 to 2008'))

    def test_double_space_to(self):
        """'from 2004 to  2008': two spaces after 'to'."""
        self.assertTrue(_year_range('from 2004 to  2008'))

    def test_double_space_both(self):
        self.assertTrue(_year_range('from  2004  to  2008'))

    def test_tab_after_from(self):
        self.assertTrue(_year_range('from\t2004 to 2008'))

    def test_tab_after_to(self):
        self.assertTrue(_year_range('from 2004 to\t2008'))

    def test_tab_both(self):
        self.assertTrue(_year_range('from\t2004\tto\t2008'))

    def test_newline_after_from(self):
        self.assertTrue(_year_range('from\n2004 to 2008'))

    def test_newline_after_to(self):
        self.assertTrue(_year_range('from 2004 to\n2008'))

    def test_triple_space_from(self):
        self.assertTrue(_year_range('from   2004 to 2008'))

    def test_mixed_whitespace(self):
        self.assertTrue(_year_range('from \t 2004 to \t 2008'))


# ============================================================================
# Class 22 — TestFromToReversedNotRange
# 15 tests: "from YYYY to YYYY" with reversed years not a range
# ============================================================================

class TestFromToReversedNotRange(unittest.TestCase):
    """Reversed from/to pairs should not produce YEAR_RANGE."""

    def test_from_2008_to_2004(self):
        self.assertTrue(_no_year_range('from 2008 to 2004'))

    def test_from_2010_to_2000(self):
        self.assertTrue(_no_year_range('from 2010 to 2000'))

    def test_from_2020_to_2010(self):
        self.assertTrue(_no_year_range('from 2020 to 2010'))

    def test_from_2000_to_1990(self):
        self.assertTrue(_no_year_range('from 2000 to 1990'))

    def test_from_1970_to_1960(self):
        self.assertTrue(_no_year_range('from 1970 to 1960'))

    def test_from_1945_to_1939(self):
        self.assertTrue(_no_year_range('from 1945 to 1939'))

    def test_from_2020_to_2019(self):
        self.assertTrue(_no_year_range('from 2020 to 2019'))

    def test_from_2015_to_2014(self):
        self.assertTrue(_no_year_range('from 2015 to 2014'))

    def test_from_2024_to_2023(self):
        self.assertTrue(_no_year_range('from 2024 to 2023'))

    def test_from_1980_to_1970(self):
        self.assertTrue(_no_year_range('from 1980 to 1970'))

    def test_from_reversed_in_sentence(self):
        self.assertTrue(_no_year_range('He went from 2010 to 2005, backward.'))

    def test_from_2030_to_2020(self):
        self.assertTrue(_no_year_range('from 2030 to 2020'))

    def test_from_2036_to_2026(self):
        self.assertTrue(_no_year_range('from 2036 to 2026'))

    def test_from_1960_to_1950(self):
        self.assertTrue(_no_year_range('from 1960 to 1950'))

    def test_from_1950_to_1940(self):
        self.assertTrue(_no_year_range('from 1950 to 1940'))


# ============================================================================
# Class 23 — TestFromToSameYearNotRange
# 10 tests: "from YYYY to YYYY" with same year not a range
# ============================================================================

class TestFromToSameYearNotRange(unittest.TestCase):
    """Same year in from/to form should not produce YEAR_RANGE."""

    def test_from_2014_to_2014(self):
        self.assertTrue(_no_year_range('from 2014 to 2014'))

    def test_from_2000_to_2000(self):
        self.assertTrue(_no_year_range('from 2000 to 2000'))

    def test_from_1990_to_1990(self):
        self.assertTrue(_no_year_range('from 1990 to 1990'))

    def test_from_1960_to_1960(self):
        self.assertTrue(_no_year_range('from 1960 to 1960'))

    def test_from_2024_to_2024(self):
        self.assertTrue(_no_year_range('from 2024 to 2024'))

    def test_from_2020_to_2020(self):
        self.assertTrue(_no_year_range('from 2020 to 2020'))

    def test_from_1926_to_1926(self):
        self.assertTrue(_no_year_range('from 1926 to 1926'))

    def test_from_2036_to_2036(self):
        self.assertTrue(_no_year_range('from 2036 to 2036'))

    def test_from_1950_to_1950(self):
        self.assertTrue(_no_year_range('from 1950 to 1950'))

    def test_from_1975_to_1975(self):
        self.assertTrue(_no_year_range('from 1975 to 1975'))


# ============================================================================
# Class 24 — TestFromToOutOfRange
# 10 tests: "from YYYY to YYYY" with out-of-range years
# ============================================================================

class TestFromToOutOfRange(unittest.TestCase):
    """Out-of-range years in from/to form should not produce YEAR_RANGE."""

    def test_from_1800_to_1900(self):
        self.assertTrue(_no_year_range('from 1800 to 1900'))

    def test_from_1900_to_1910(self):
        self.assertTrue(_no_year_range('from 1900 to 1910'))

    def test_from_1920_to_1930(self):
        self.assertTrue(_no_year_range('from 1920 to 1930'))

    def test_from_2040_to_2050(self):
        self.assertTrue(_no_year_range('from 2040 to 2050'))

    def test_from_2100_to_2200(self):
        self.assertTrue(_no_year_range('from 2100 to 2200'))

    def test_from_1924_to_1934(self):
        """1924 < MIN_YEAR."""
        self.assertTrue(_no_year_range('from 1924 to 1934'))

    def test_from_2036_to_2046(self):
        """2046 > MAX_YEAR."""
        self.assertTrue(_no_year_range('from 2036 to 2046'))

    def test_from_1234_to_1235(self):
        self.assertTrue(_no_year_range('from 1234 to 1235'))

    def test_from_9000_to_9999(self):
        self.assertTrue(_no_year_range('from 9000 to 9999'))

    def test_from_0001_to_0999(self):
        self.assertTrue(_no_year_range('from 0001 to 0999'))


# ============================================================================
# Class 25 — TestFromToResultShape
# 10 tests: Shape of result for "from YYYY to YYYY"
# ============================================================================

class TestFromToResultShape(unittest.TestCase):
    """Verify result structure for from/to year range expressions."""

    def test_result_is_dict(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertGreater(len(result), 0)

    def test_key_format(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)

    def test_value_is_year_range(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_key_is_string(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        for k in result:
            self.assertIsInstance(k, str)

    def test_value_is_string(self):
        result = extract_explicit_dates('from 2004 to 2008') or {}
        for v in result.values():
            self.assertIsInstance(v, str)

    def test_key_not_full_phrase(self):
        """Key should be '2004-2008', not 'from 2004 to 2008'."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertNotIn('from 2004 to 2008', result)

    def test_key_ascending(self):
        """Key must be start-end, not end-start."""
        result = extract_explicit_dates('from 2004 to 2008') or {}
        self.assertIn('2004-2008', result)
        self.assertNotIn('2008-2004', result)

    def test_result_not_list(self):
        result = extract_explicit_dates('from 2004 to 2008')
        self.assertNotIsInstance(result, list)

    def test_multiple_from_to(self):
        result = extract_explicit_dates('from 2000 to 2005 and from 2010 to 2015') or {}
        self.assertIn('2000-2005', result)
        self.assertIn('2010-2015', result)


# ============================================================================
# Class 26 — TestBetweenAndValidPairs
# 30 tests: "between YYYY and YYYY" valid pairs
# ============================================================================

class TestBetweenAndValidPairs(unittest.TestCase):
    """'between YYYY and YYYY' produces YEAR_RANGE for valid pairs."""

    def test_between_2010_and_2020(self):
        self.assertTrue(_year_range('between 2010 and 2020'))

    def test_between_2000_and_2010(self):
        self.assertTrue(_year_range('between 2000 and 2010'))

    def test_between_1990_and_2000(self):
        self.assertTrue(_year_range('between 1990 and 2000'))

    def test_between_2004_and_2008(self):
        self.assertTrue(_year_range('between 2004 and 2008'))

    def test_between_1960_and_1970(self):
        self.assertTrue(_year_range('between 1960 and 1970'))

    def test_between_1950_and_1960(self):
        self.assertTrue(_year_range('between 1950 and 1960'))

    def test_between_1940_and_1950(self):
        self.assertTrue(_year_range('between 1940 and 1950'))

    def test_between_1930_and_1940(self):
        self.assertTrue(_year_range('between 1930 and 1940'))

    def test_between_1926_and_1936(self):
        self.assertTrue(_year_range('between 1926 and 1936'))

    def test_between_2019_and_2020(self):
        self.assertTrue(_year_range('between 2019 and 2020'))

    def test_between_2014_and_2015(self):
        self.assertTrue(_year_range('between 2014 and 2015'))

    def test_between_2020_and_2025(self):
        self.assertTrue(_year_range('between 2020 and 2025'))

    def test_between_2025_and_2030(self):
        self.assertTrue(_year_range('between 2025 and 2030'))

    def test_between_2030_and_2035(self):
        self.assertTrue(_year_range('between 2030 and 2035'))

    def test_between_2035_and_2036(self):
        self.assertTrue(_year_range('between 2035 and 2036'))

    def test_between_1939_and_1945(self):
        self.assertTrue(_year_range('between 1939 and 1945'))

    def test_between_1970_and_2000(self):
        self.assertTrue(_year_range('between 1970 and 2000'))

    def test_between_1945_and_1955(self):
        self.assertTrue(_year_range('between 1945 and 1955'))

    def test_between_1955_and_1965(self):
        self.assertTrue(_year_range('between 1955 and 1965'))

    def test_between_1965_and_1975(self):
        self.assertTrue(_year_range('between 1965 and 1975'))

    def test_between_1975_and_1985(self):
        self.assertTrue(_year_range('between 1975 and 1985'))

    def test_between_1985_and_1995(self):
        self.assertTrue(_year_range('between 1985 and 1995'))

    def test_between_1995_and_2005(self):
        self.assertTrue(_year_range('between 1995 and 2005'))

    def test_between_2005_and_2015(self):
        self.assertTrue(_year_range('between 2005 and 2015'))

    def test_between_2015_and_2025(self):
        self.assertTrue(_year_range('between 2015 and 2025'))

    def test_between_key_format(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertIn('2004-2008', result)

    def test_between_value_format(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_between_result_is_dict(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertIsInstance(result, dict)

    def test_between_result_nonempty(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertGreater(len(result), 0)

    def test_between_1926_and_2036(self):
        """Full valid range."""
        self.assertTrue(_year_range('between 1926 and 2036'))


# ============================================================================
# Class 27 — TestBetweenAndInSentence
# 15 tests: "between YYYY and YYYY" embedded in sentences
# ============================================================================

class TestBetweenAndInSentence(unittest.TestCase):
    """'between YYYY and YYYY' inside longer sentences."""

    def test_born_between(self):
        self.assertTrue(_year_range('He was born between 1950 and 1960.'))

    def test_happened_between(self):
        self.assertTrue(_year_range('It happened between 2000 and 2010.'))

    def test_built_between(self):
        self.assertTrue(_year_range('The building was built between 1960 and 1970.'))

    def test_income_between(self):
        self.assertTrue(_year_range('Income grew between 1990 and 2000.'))

    def test_she_worked_between(self):
        self.assertTrue(_year_range('She worked there between 2005 and 2015.'))

    def test_war_between(self):
        self.assertTrue(_year_range('The war ended between 1939 and 1945.'))

    def test_period_between(self):
        self.assertTrue(_year_range('The period between 2014 and 2020 saw growth.'))

    def test_data_between(self):
        self.assertTrue(_year_range('Data collected between 2008 and 2012.'))

    def test_sentence_start(self):
        self.assertTrue(_year_range('Between 2010 and 2020, revenues doubled.'))

    def test_with_comma(self):
        self.assertTrue(_year_range('Between 2010 and 2020, revenues doubled.'))

    def test_mid_sentence_comma(self):
        self.assertTrue(_year_range('The gap, between 2004 and 2008, was notable.'))

    def test_at_end(self):
        self.assertTrue(_year_range('Prices rose between 2000 and 2010'))

    def test_with_quotes(self):
        self.assertTrue(_year_range('"between 2004 and 2008" is the range'))

    def test_after_conjunction(self):
        self.assertTrue(_year_range('I lived there and then between 2010 and 2015.'))

    def test_multiple_between(self):
        self.assertTrue(_year_range('Events between 1960 and 1970 and also between 2000 and 2010.'))


# ============================================================================
# Class 28 — TestBetweenAndCasing
# 15 tests: Casing variants of "between YYYY and YYYY"
# ============================================================================

class TestBetweenAndCasing(unittest.TestCase):
    """Case insensitivity for 'between YYYY and YYYY'."""

    def test_uppercase(self):
        self.assertTrue(_year_range('BETWEEN 2010 AND 2020'))

    def test_title_case(self):
        self.assertTrue(_year_range('Between 2010 And 2020'))

    def test_between_upper_and_lower(self):
        self.assertTrue(_year_range('BETWEEN 2010 and 2020'))

    def test_between_lower_and_upper(self):
        self.assertTrue(_year_range('between 2010 AND 2020'))

    def test_mixed_case_1(self):
        self.assertTrue(_year_range('BeTwEeN 2010 AnD 2020'))

    def test_mixed_case_2(self):
        self.assertTrue(_year_range('bEtWeEn 2010 aND 2020'))

    def test_all_caps_in_sentence(self):
        self.assertTrue(_year_range('BORN BETWEEN 2010 AND 2020.'))

    def test_title_in_sentence(self):
        self.assertTrue(_year_range('Born Between 2010 And 2020.'))

    def test_lower_in_sentence(self):
        self.assertTrue(_year_range('born between 2010 and 2020.'))

    def test_upper_in_sentence(self):
        self.assertTrue(_year_range('born BETWEEN 2010 AND 2020.'))

    def test_random_caps_1(self):
        self.assertTrue(_year_range('BETween 2004 aNd 2008'))

    def test_random_caps_2(self):
        self.assertTrue(_year_range('betWEEN 2004 AND 2008'))

    def test_sentence_start_upper(self):
        self.assertTrue(_year_range('Between 2014 and 2015 was notable.'))

    def test_sentence_start_lower(self):
        self.assertTrue(_year_range('between 2014 and 2015 was notable.'))

    def test_sentence_start_all_caps(self):
        self.assertTrue(_year_range('BETWEEN 2014 AND 2015 was notable.'))


# ============================================================================
# Class 29 — TestBetweenAndReversedNotRange
# 15 tests: Reversed years in between/and form
# ============================================================================

class TestBetweenAndReversedNotRange(unittest.TestCase):
    """Reversed year order in between/and form is not a YEAR_RANGE."""

    def test_between_2020_and_2010(self):
        self.assertTrue(_no_year_range('between 2020 and 2010'))

    def test_between_2010_and_2000(self):
        self.assertTrue(_no_year_range('between 2010 and 2000'))

    def test_between_2000_and_1990(self):
        self.assertTrue(_no_year_range('between 2000 and 1990'))

    def test_between_1970_and_1960(self):
        self.assertTrue(_no_year_range('between 1970 and 1960'))

    def test_between_1945_and_1939(self):
        self.assertTrue(_no_year_range('between 1945 and 1939'))

    def test_between_2020_and_2019(self):
        self.assertTrue(_no_year_range('between 2020 and 2019'))

    def test_between_2015_and_2014(self):
        self.assertTrue(_no_year_range('between 2015 and 2014'))

    def test_between_2024_and_2023(self):
        self.assertTrue(_no_year_range('between 2024 and 2023'))

    def test_between_1980_and_1970(self):
        self.assertTrue(_no_year_range('between 1980 and 1970'))

    def test_between_reversed_in_sentence(self):
        self.assertTrue(_no_year_range('He lived between 2010 and 2005.'))

    def test_between_2030_and_2020(self):
        self.assertTrue(_no_year_range('between 2030 and 2020'))

    def test_between_1960_and_1950(self):
        self.assertTrue(_no_year_range('between 1960 and 1950'))

    def test_between_1950_and_1940(self):
        self.assertTrue(_no_year_range('between 1950 and 1940'))

    def test_between_1940_and_1930(self):
        self.assertTrue(_no_year_range('between 1940 and 1930'))

    def test_between_2036_and_2026(self):
        self.assertTrue(_no_year_range('between 2036 and 2026'))


# ============================================================================
# Class 30 — TestBetweenAndSameYear
# 10 tests: Same year in between/and form
# ============================================================================

class TestBetweenAndSameYear(unittest.TestCase):
    """Same year in between/and form should not be YEAR_RANGE."""

    def test_between_2014_and_2014(self):
        self.assertTrue(_no_year_range('between 2014 and 2014'))

    def test_between_2000_and_2000(self):
        self.assertTrue(_no_year_range('between 2000 and 2000'))

    def test_between_1990_and_1990(self):
        self.assertTrue(_no_year_range('between 1990 and 1990'))

    def test_between_2024_and_2024(self):
        self.assertTrue(_no_year_range('between 2024 and 2024'))

    def test_between_2020_and_2020(self):
        self.assertTrue(_no_year_range('between 2020 and 2020'))

    def test_between_1926_and_1926(self):
        self.assertTrue(_no_year_range('between 1926 and 1926'))

    def test_between_2036_and_2036(self):
        self.assertTrue(_no_year_range('between 2036 and 2036'))

    def test_between_1950_and_1950(self):
        self.assertTrue(_no_year_range('between 1950 and 1950'))

    def test_between_1975_and_1975(self):
        self.assertTrue(_no_year_range('between 1975 and 1975'))

    def test_between_2010_and_2010(self):
        self.assertTrue(_no_year_range('between 2010 and 2010'))


# ============================================================================
# Class 31 — TestBetweenAndOutOfRange
# 10 tests: Out-of-range years in between/and form
# ============================================================================

class TestBetweenAndOutOfRange(unittest.TestCase):
    """Out-of-range years in between/and form."""

    def test_between_1800_and_1900(self):
        self.assertTrue(_no_year_range('between 1800 and 1900'))

    def test_between_1900_and_1910(self):
        self.assertTrue(_no_year_range('between 1900 and 1910'))

    def test_between_2040_and_2050(self):
        self.assertTrue(_no_year_range('between 2040 and 2050'))

    def test_between_1920_and_1930(self):
        self.assertTrue(_no_year_range('between 1920 and 1930'))

    def test_between_2100_and_2200(self):
        self.assertTrue(_no_year_range('between 2100 and 2200'))

    def test_between_1924_and_1934(self):
        self.assertTrue(_no_year_range('between 1924 and 1934'))

    def test_between_2037_and_2047(self):
        self.assertTrue(_no_year_range('between 2037 and 2047'))

    def test_between_1234_and_1235(self):
        self.assertTrue(_no_year_range('between 1234 and 1235'))

    def test_between_9000_and_9999(self):
        self.assertTrue(_no_year_range('between 9000 and 9999'))

    def test_between_0001_and_0999(self):
        self.assertTrue(_no_year_range('between 0001 and 0999'))


# ============================================================================
# Class 32 — TestBetweenAndResultShape
# 10 tests: Shape of result for "between YYYY and YYYY"
# ============================================================================

class TestBetweenAndResultShape(unittest.TestCase):
    """Verify result structure for between/and year range expressions."""

    def test_result_is_dict(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertIsInstance(result, dict)

    def test_result_nonempty(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertGreater(len(result), 0)

    def test_key_format(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertIn('2004-2008', result)

    def test_value_is_year_range(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertEqual(result.get('2004-2008'), 'YEAR_RANGE')

    def test_key_is_string(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        for k in result:
            self.assertIsInstance(k, str)

    def test_key_not_full_phrase(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertNotIn('between 2004 and 2008', result)

    def test_key_ascending(self):
        result = extract_explicit_dates('between 2004 and 2008') or {}
        self.assertIn('2004-2008', result)
        self.assertNotIn('2008-2004', result)

    def test_result_not_list(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertNotIsInstance(result, list)

    def test_result_not_none(self):
        result = extract_explicit_dates('between 2004 and 2008')
        self.assertIsNotNone(result)

    def test_multiple_between_and(self):
        result = extract_explicit_dates('between 2000 and 2005 and between 2010 and 2015') or {}
        self.assertIn('2000-2005', result)
        self.assertIn('2010-2015', result)


# ============================================================================
# Class 33 — TestMalformedInput
# 25 tests: None, empty, non-string inputs
# ============================================================================

class TestMalformedInput(unittest.TestCase):
    """Malformed or unusual inputs must not crash and must return dict or None."""

    def test_none_input(self):
        self.assertTrue(_is_dict_or_none(None))

    def test_empty_string(self):
        self.assertTrue(_is_dict_or_none(''))

    def test_whitespace_only(self):
        self.assertTrue(_is_dict_or_none('   '))

    def test_single_space(self):
        self.assertTrue(_is_dict_or_none(' '))

    def test_tab_only(self):
        self.assertTrue(_is_dict_or_none('\t'))

    def test_newline_only(self):
        self.assertTrue(_is_dict_or_none('\n'))

    def test_integer_input(self):
        self.assertTrue(_is_dict_or_none(2014))

    def test_float_input(self):
        self.assertTrue(_is_dict_or_none(2014.5))

    def test_list_input(self):
        self.assertTrue(_is_dict_or_none(['2014-2015']))

    def test_dict_input(self):
        self.assertTrue(_is_dict_or_none({'year': '2014-2015'}))

    def test_bool_true(self):
        self.assertTrue(_is_dict_or_none(True))

    def test_bool_false(self):
        self.assertTrue(_is_dict_or_none(False))

    def test_bytes_input(self):
        self.assertTrue(_is_dict_or_none(b'2014-2015'))

    def test_tuple_input(self):
        self.assertTrue(_is_dict_or_none(('2014', '2015')))

    def test_none_no_year_range(self):
        self.assertTrue(_no_year_range(None))

    def test_empty_no_year_range(self):
        self.assertTrue(_no_year_range(''))

    def test_whitespace_no_year_range(self):
        self.assertTrue(_no_year_range('   '))

    def test_int_no_year_range(self):
        self.assertTrue(_no_year_range(42))

    def test_only_letters(self):
        self.assertTrue(_no_year_range('abcdefghijk'))

    def test_single_number(self):
        """A standalone 4-digit year is YEAR_ONLY if valid, not YEAR_RANGE."""
        self.assertTrue(_no_year_range('2014'))

    def test_three_digit_number(self):
        self.assertTrue(_no_year_range('201'))

    def test_five_digit_number(self):
        self.assertTrue(_no_year_range('20145'))

    def test_special_chars_only(self):
        self.assertTrue(_is_dict_or_none('!@#$%^&*()'))

    def test_zero_string(self):
        self.assertTrue(_no_year_range('0'))

    def test_hyphen_only(self):
        self.assertTrue(_no_year_range('-'))


# ============================================================================
# Class 34 — TestCrazyInputs
# 20 tests: Unicode, HTML, emoji, pathological strings
# ============================================================================

class TestCrazyInputs(unittest.TestCase):
    """Unusual, unexpected, or pathological inputs."""

    def test_emoji_only(self):
        self.assertTrue(_is_dict_or_none('🎉🎂🎊'))

    def test_emoji_with_years(self):
        self.assertTrue(_is_dict_or_none('🎉 2014-2015 🎂'))

    def test_html_entity(self):
        self.assertTrue(_is_dict_or_none('2014&ndash;2015'))

    def test_html_tag(self):
        self.assertTrue(_is_dict_or_none('<b>2014-2015</b>'))

    def test_html_year_range(self):
        """HTML-wrapped year range should still be detected."""
        self.assertTrue(_year_range('<b>2014-2015</b>'))

    def test_unicode_quotes(self):
        self.assertTrue(_is_dict_or_none('\u20182014-2015\u2019'))

    def test_very_long_string(self):
        text = 'lorem ipsum ' * 1000 + '2014-2015' + ' dolor sit amet' * 1000
        self.assertTrue(_year_range(text))

    def test_null_bytes(self):
        self.assertTrue(_is_dict_or_none('2014\x002015'))

    def test_escaped_chars(self):
        self.assertTrue(_is_dict_or_none('2014\\n2015'))

    def test_carriage_return(self):
        self.assertTrue(_is_dict_or_none('2014\r2015'))

    def test_sql_injection_like(self):
        self.assertTrue(_is_dict_or_none("'; DROP TABLE years; --"))

    def test_json_like(self):
        self.assertTrue(_is_dict_or_none('{"year": "2014-2015"}'))

    def test_json_range_detected(self):
        self.assertTrue(_year_range('{"year": "2014-2015"}'))

    def test_xml_like(self):
        self.assertTrue(_is_dict_or_none('<year>2014-2015</year>'))

    def test_markdown_like(self):
        self.assertTrue(_year_range('**The period 2014-2015** was notable.'))

    def test_repeated_range(self):
        text = '2014-2015 ' * 100
        self.assertTrue(_year_range(text))

    def test_alternating_valid_invalid(self):
        text = '2014-2015 abc 1800-1900 xyz 2000-2010'
        result = extract_explicit_dates(text) or {}
        self.assertIn('2014-2015', result)
        self.assertIn('2000-2010', result)
        self.assertNotIn('1800-1900', result)

    def test_url_like(self):
        self.assertTrue(_is_dict_or_none('https://example.com/report/2014-2015'))

    def test_path_like(self):
        self.assertTrue(_is_dict_or_none('/usr/local/data/2014-2015/report.csv'))

    def test_decade_as_range(self):
        """The 2010s could loosely suggest a range but isn't YYYY-YYYY."""
        self.assertTrue(_is_dict_or_none('the 2010s'))


# ============================================================================
# Class 35 — TestEnDashForm (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY–YYYY" using en dash (U+2013)
# ============================================================================

class TestEnDashForm(unittest.TestCase):
    """En dash (–) year ranges. Support TBD — may require xfail."""

    def test_en_dash_2014_2015(self):
        """2014\u20132015 — en dash."""
        self.assertTrue(_year_range('2014\u20132015'))

    def test_en_dash_2000_2010(self):
        self.assertTrue(_year_range('2000\u20132010'))

    def test_en_dash_1990_2000(self):
        self.assertTrue(_year_range('1990\u20132000'))

    def test_en_dash_in_sentence(self):
        self.assertTrue(_year_range('The period 2014\u20132015 was notable.'))

    def test_en_dash_with_parens(self):
        self.assertTrue(_year_range('(2014\u20132015)'))

    def test_en_dash_1939_1945(self):
        self.assertTrue(_year_range('1939\u20131945'))

    def test_en_dash_2019_2020(self):
        self.assertTrue(_year_range('2019\u20132020'))

    def test_en_dash_reversed_not_range(self):
        self.assertTrue(_no_year_range('2015\u20132014'))

    def test_en_dash_same_year_not_range(self):
        self.assertTrue(_no_year_range('2014\u20132014'))

    def test_en_dash_out_of_range(self):
        self.assertTrue(_no_year_range('1800\u20131900'))


# ============================================================================
# Class 36 — TestEmDashForm (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY—YYYY" using em dash (U+2014)
# ============================================================================

class TestEmDashForm(unittest.TestCase):
    """Em dash (—) year ranges. Support TBD — may require xfail."""

    def test_em_dash_2014_2015(self):
        """2014\u20142015 — em dash."""
        self.assertTrue(_year_range('2014\u20142015'))

    def test_em_dash_2000_2010(self):
        self.assertTrue(_year_range('2000\u20142010'))

    def test_em_dash_1990_2000(self):
        self.assertTrue(_year_range('1990\u20142000'))

    def test_em_dash_in_sentence(self):
        self.assertTrue(_year_range('The period 2014\u20142015 was notable.'))

    def test_em_dash_with_parens(self):
        self.assertTrue(_year_range('(2014\u20142015)'))

    def test_em_dash_1939_1945(self):
        self.assertTrue(_year_range('1939\u20141945'))

    def test_em_dash_2019_2020(self):
        self.assertTrue(_year_range('2019\u20142020'))

    def test_em_dash_reversed_not_range(self):
        self.assertTrue(_no_year_range('2015\u20142014'))

    def test_em_dash_same_year_not_range(self):
        self.assertTrue(_no_year_range('2014\u20142014'))

    def test_em_dash_out_of_range(self):
        self.assertTrue(_no_year_range('1800\u20141900'))


# ============================================================================
# Class 37 — TestSpaceAroundHyphen (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY - YYYY" (spaces around hyphen)
# ============================================================================

class TestSpaceAroundHyphen(unittest.TestCase):
    """Spaces around the hyphen. Support TBD — may require xfail."""

    def test_space_hyphen_space_2014_2015(self):
        self.assertTrue(_year_range('2014 - 2015'))

    def test_space_hyphen_space_2000_2010(self):
        self.assertTrue(_year_range('2000 - 2010'))

    def test_space_hyphen_space_1990_2000(self):
        self.assertTrue(_year_range('1990 - 2000'))

    def test_space_hyphen_space_in_sentence(self):
        self.assertTrue(_year_range('The period 2014 - 2015 was notable.'))

    def test_space_hyphen_space_with_parens(self):
        self.assertTrue(_year_range('(2014 - 2015)'))

    def test_space_hyphen_space_1939_1945(self):
        self.assertTrue(_year_range('1939 - 1945'))

    def test_space_hyphen_space_consecutive(self):
        self.assertTrue(_year_range('2019 - 2020'))

    def test_space_hyphen_space_reversed_not_range(self):
        self.assertTrue(_no_year_range('2015 - 2014'))

    def test_space_hyphen_space_same_year_not_range(self):
        self.assertTrue(_no_year_range('2014 - 2014'))

    def test_space_hyphen_space_out_of_range(self):
        self.assertTrue(_no_year_range('1800 - 1900'))


# ============================================================================
# Class 38 — TestAbbreviatedYearRange (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY-YY" abbreviated second year (e.g., 2025-26)
# ============================================================================

class TestAbbreviatedYearRange(unittest.TestCase):
    """Abbreviated second year (e.g., 2025-26). Support TBD — may require xfail."""

    def test_2025_26(self):
        self.assertTrue(_year_range('2025-26'))

    def test_2024_25(self):
        self.assertTrue(_year_range('2024-25'))

    def test_2020_21(self):
        self.assertTrue(_year_range('2020-21'))

    def test_2019_20(self):
        self.assertTrue(_year_range('2019-20'))

    def test_1999_00(self):
        self.assertTrue(_year_range('1999-00'))

    def test_1989_90(self):
        self.assertTrue(_year_range('1989-90'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('The fiscal year 2025-26 budget was approved.'))

    def test_with_parens(self):
        self.assertTrue(_year_range('(FY 2024-25)'))

    def test_reversed_abbreviated_not_range(self):
        """2015-14: abbreviated reversed, should not be YEAR_RANGE."""
        self.assertTrue(_no_year_range('2015-14'))

    def test_abbreviated_at_century_boundary(self):
        self.assertTrue(_year_range('1999-00'))


# ============================================================================
# Class 39 — TestFromThroughForm (EDGE CASE — may fail; xfail TBD)
# 10 tests: "from YYYY through YYYY"
# ============================================================================

class TestFromThroughForm(unittest.TestCase):
    """'from YYYY through YYYY' form. Support TBD — may require xfail."""

    def test_from_2004_through_2008(self):
        self.assertTrue(_year_range('from 2004 through 2008'))

    def test_from_2000_through_2010(self):
        self.assertTrue(_year_range('from 2000 through 2010'))

    def test_from_1990_through_2000(self):
        self.assertTrue(_year_range('from 1990 through 2000'))

    def test_from_1939_through_1945(self):
        self.assertTrue(_year_range('from 1939 through 1945'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('The project ran from 2010 through 2015.'))

    def test_uppercase_from_through(self):
        self.assertTrue(_year_range('FROM 2004 THROUGH 2008'))

    def test_reversed_not_range(self):
        self.assertTrue(_no_year_range('from 2008 through 2004'))

    def test_same_year_not_range(self):
        self.assertTrue(_no_year_range('from 2014 through 2014'))

    def test_out_of_range(self):
        self.assertTrue(_no_year_range('from 1800 through 1900'))

    def test_consecutive(self):
        self.assertTrue(_year_range('from 2019 through 2020'))


# ============================================================================
# Class 40 — TestBareYearToYear (EDGE CASE — may fail; xfail TBD)
# 10 tests: "YYYY to YYYY" without "from"
# ============================================================================

class TestBareYearToYear(unittest.TestCase):
    """'YYYY to YYYY' (without 'from') form. Support TBD — may require xfail."""

    def test_2014_to_2015(self):
        self.assertTrue(_year_range('2014 to 2015'))

    def test_2000_to_2010(self):
        self.assertTrue(_year_range('2000 to 2010'))

    def test_1990_to_2000(self):
        self.assertTrue(_year_range('1990 to 2000'))

    def test_in_sentence(self):
        self.assertTrue(_year_range('The years 2014 to 2015 were notable.'))

    def test_consecutive(self):
        self.assertTrue(_year_range('2019 to 2020'))

    def test_1939_to_1945(self):
        self.assertTrue(_year_range('1939 to 1945'))

    def test_uppercase_to(self):
        self.assertTrue(_year_range('2014 TO 2015'))

    def test_reversed_not_range(self):
        self.assertTrue(_no_year_range('2015 to 2014'))

    def test_same_year_not_range(self):
        self.assertTrue(_no_year_range('2014 to 2014'))

    def test_out_of_range(self):
        self.assertTrue(_no_year_range('1800 to 1900'))


if __name__ == '__main__':
    unittest.main()
