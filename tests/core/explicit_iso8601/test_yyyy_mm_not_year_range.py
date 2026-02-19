#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests that YYYY-MM patterns are not falsely classified as YEAR_RANGE.

A 4-digit year followed by a hyphen and a 2-digit month (01–12) is a partial
ISO 8601 date (YYYY-MM), not a year range. The year-range pattern
'YYYY-YY' should only trigger when the 2-digit component is outside the
valid month range (13–99, or 00).

Related GitHub Issue:
    #52 - Bug: YYYY-MM falsely matched as YEAR_RANGE for years <= 2000
    https://github.com/craigtrim/fast-parse-time/issues/52
"""

import pytest
from fast_parse_time import extract_explicit_dates

YEAR_RANGE = 'YEAR_RANGE'


# ===========================================================================
# Section 1: Years ≤ 2000 with all valid months (01–12) — must NOT be YEAR_RANGE
# ===========================================================================

class TestYear2000AllMonths:
    """YYYY-MM where year=2000 should never produce a YEAR_RANGE entry."""

    def test_2000_01(self):
        result = extract_explicit_dates('2000-01')
        assert not result or result.get('2000-01') != YEAR_RANGE

    def test_2000_02(self):
        result = extract_explicit_dates('2000-02')
        assert not result or result.get('2000-02') != YEAR_RANGE

    def test_2000_03(self):
        result = extract_explicit_dates('2000-03')
        assert not result or result.get('2000-03') != YEAR_RANGE

    def test_2000_04(self):
        result = extract_explicit_dates('2000-04')
        assert not result or result.get('2000-04') != YEAR_RANGE

    def test_2000_05(self):
        result = extract_explicit_dates('2000-05')
        assert not result or result.get('2000-05') != YEAR_RANGE

    def test_2000_06(self):
        result = extract_explicit_dates('2000-06')
        assert not result or result.get('2000-06') != YEAR_RANGE

    def test_2000_07(self):
        result = extract_explicit_dates('2000-07')
        assert not result or result.get('2000-07') != YEAR_RANGE

    def test_2000_08(self):
        result = extract_explicit_dates('2000-08')
        assert not result or result.get('2000-08') != YEAR_RANGE

    def test_2000_09(self):
        result = extract_explicit_dates('2000-09')
        assert not result or result.get('2000-09') != YEAR_RANGE

    def test_2000_10(self):
        result = extract_explicit_dates('2000-10')
        assert not result or result.get('2000-10') != YEAR_RANGE

    def test_2000_11(self):
        result = extract_explicit_dates('2000-11')
        assert not result or result.get('2000-11') != YEAR_RANGE

    def test_2000_12(self):
        result = extract_explicit_dates('2000-12')
        assert not result or result.get('2000-12') != YEAR_RANGE


class TestYear1999AllMonths:
    """YYYY-MM where year=1999 should never produce a YEAR_RANGE entry."""

    def test_1999_01(self):
        result = extract_explicit_dates('1999-01')
        assert not result or result.get('1999-01') != YEAR_RANGE

    def test_1999_06(self):
        result = extract_explicit_dates('1999-06')
        assert not result or result.get('1999-06') != YEAR_RANGE

    def test_1999_12(self):
        result = extract_explicit_dates('1999-12')
        assert not result or result.get('1999-12') != YEAR_RANGE


class TestYear1998AllMonths:
    """YYYY-MM where year=1998."""

    def test_1998_01(self):
        result = extract_explicit_dates('1998-01')
        assert not result or result.get('1998-01') != YEAR_RANGE

    def test_1998_06(self):
        result = extract_explicit_dates('1998-06')
        assert not result or result.get('1998-06') != YEAR_RANGE

    def test_1998_12(self):
        result = extract_explicit_dates('1998-12')
        assert not result or result.get('1998-12') != YEAR_RANGE


class TestYear1990sAllMonths:
    """Various years in the 1990s."""

    def test_1990_01(self):
        result = extract_explicit_dates('1990-01')
        assert not result or result.get('1990-01') != YEAR_RANGE

    def test_1991_03(self):
        result = extract_explicit_dates('1991-03')
        assert not result or result.get('1991-03') != YEAR_RANGE

    def test_1992_06(self):
        result = extract_explicit_dates('1992-06')
        assert not result or result.get('1992-06') != YEAR_RANGE

    def test_1993_09(self):
        result = extract_explicit_dates('1993-09')
        assert not result or result.get('1993-09') != YEAR_RANGE

    def test_1994_12(self):
        result = extract_explicit_dates('1994-12')
        assert not result or result.get('1994-12') != YEAR_RANGE

    def test_1995_01(self):
        result = extract_explicit_dates('1995-01')
        assert not result or result.get('1995-01') != YEAR_RANGE

    def test_1996_07(self):
        result = extract_explicit_dates('1996-07')
        assert not result or result.get('1996-07') != YEAR_RANGE

    def test_1997_11(self):
        result = extract_explicit_dates('1997-11')
        assert not result or result.get('1997-11') != YEAR_RANGE


class TestYear1980s:
    """Years in the 1980s."""

    def test_1980_01(self):
        result = extract_explicit_dates('1980-01')
        assert not result or result.get('1980-01') != YEAR_RANGE

    def test_1985_06(self):
        result = extract_explicit_dates('1985-06')
        assert not result or result.get('1985-06') != YEAR_RANGE

    def test_1989_12(self):
        result = extract_explicit_dates('1989-12')
        assert not result or result.get('1989-12') != YEAR_RANGE


class TestYear1970s:
    """Years in the 1970s."""

    def test_1970_01(self):
        result = extract_explicit_dates('1970-01')
        assert not result or result.get('1970-01') != YEAR_RANGE

    def test_1975_06(self):
        result = extract_explicit_dates('1975-06')
        assert not result or result.get('1975-06') != YEAR_RANGE

    def test_1979_12(self):
        result = extract_explicit_dates('1979-12')
        assert not result or result.get('1979-12') != YEAR_RANGE


# ===========================================================================
# Section 2: ISO 8601 full datetimes with year ≤ 2000 — no spurious YEAR_RANGE
# ===========================================================================

class TestIso8601FullDateNoYearRange:
    """Full ISO 8601 datetimes must not produce spurious YEAR_RANGE entries."""

    def test_2000_01_01_z(self):
        result = extract_explicit_dates('2000-01-01T00:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_2000_06_15_z(self):
        result = extract_explicit_dates('2000-06-15T12:30:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_1999_12_31_z(self):
        result = extract_explicit_dates('1999-12-31T23:59:59Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_1990_01_01_z(self):
        result = extract_explicit_dates('1990-01-01T00:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_1985_07_04_z(self):
        result = extract_explicit_dates('1985-07-04T00:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_2000_01_full_date_only(self):
        result = extract_explicit_dates('2000-01-01')
        assert not result or YEAR_RANGE not in result.values()

    def test_1999_06_15(self):
        result = extract_explicit_dates('1999-06-15')
        assert not result or YEAR_RANGE not in result.values()

    def test_1995_03_25(self):
        result = extract_explicit_dates('1995-03-25')
        assert not result or YEAR_RANGE not in result.values()

    def test_2000_01_01_utc_offset(self):
        result = extract_explicit_dates('2000-01-01T00:00:00+00:00')
        assert not result or YEAR_RANGE not in result.values()

    def test_1999_09_09_utc_offset(self):
        result = extract_explicit_dates('1999-09-09T09:09:09+00:00')
        assert not result or YEAR_RANGE not in result.values()


# ===========================================================================
# Section 3: Years just above 2000 — also must not produce YEAR_RANGE for MM
# ===========================================================================

class TestYears2001To2012:
    """Years 2001–2012 with valid months should not be YEAR_RANGE."""

    def test_2001_01(self):
        result = extract_explicit_dates('2001-01')
        assert not result or result.get('2001-01') != YEAR_RANGE

    def test_2001_12(self):
        result = extract_explicit_dates('2001-12')
        assert not result or result.get('2001-12') != YEAR_RANGE

    def test_2005_06(self):
        result = extract_explicit_dates('2005-06')
        assert not result or result.get('2005-06') != YEAR_RANGE

    def test_2010_01(self):
        result = extract_explicit_dates('2010-01')
        assert not result or result.get('2010-01') != YEAR_RANGE

    def test_2010_12(self):
        result = extract_explicit_dates('2010-12')
        assert not result or result.get('2010-12') != YEAR_RANGE

    def test_2012_01(self):
        result = extract_explicit_dates('2012-01')
        assert not result or result.get('2012-01') != YEAR_RANGE

    def test_2012_12(self):
        result = extract_explicit_dates('2012-12')
        assert not result or result.get('2012-12') != YEAR_RANGE


# ===========================================================================
# Section 4: Regression — legitimate YEAR_RANGE patterns must still work
# ===========================================================================

class TestLegitimateYearRanges:
    """Patterns that ARE genuine year ranges must continue to work."""

    def test_2014_2015_hyphen(self):
        result = extract_explicit_dates('2014-2015')
        assert result and result.get('2014-2015') == YEAR_RANGE

    def test_2025_26(self):
        result = extract_explicit_dates('2025-26')
        assert result and result.get('2025-26') == YEAR_RANGE

    def test_1999_00(self):
        # 1999-00 → century rollover → 1999-2000 → YEAR_RANGE
        result = extract_explicit_dates('1999-00')
        assert result and result.get('1999-00') == YEAR_RANGE

    def test_2020_21(self):
        result = extract_explicit_dates('2020-21')
        assert result and result.get('2020-21') == YEAR_RANGE

    def test_2023_24(self):
        result = extract_explicit_dates('2023-24')
        assert result and result.get('2023-24') == YEAR_RANGE

    def test_2000_13(self):
        # 2000-13: NN=13 is not a valid month → must be year abbreviation
        result = extract_explicit_dates('2000-13')
        assert result and result.get('2000-13') == YEAR_RANGE

    def test_1990_13(self):
        result = extract_explicit_dates('1990-13')
        assert result and result.get('1990-13') == YEAR_RANGE

    def test_from_2004_to_2008(self):
        result = extract_explicit_dates('from 2004 to 2008')
        assert result and YEAR_RANGE in result.values()

    def test_between_2010_and_2020(self):
        result = extract_explicit_dates('between 2010 and 2020')
        assert result and YEAR_RANGE in result.values()

    def test_2014_to_2015(self):
        result = extract_explicit_dates('2014 to 2015')
        assert result and YEAR_RANGE in result.values()


# ===========================================================================
# Section 5: All 12 months for year 1990 — none must be YEAR_RANGE
# ===========================================================================

class TestYear1990AllMonths:
    """1990-MM for every valid month must not yield YEAR_RANGE."""

    def test_1990_01(self): assert (extract_explicit_dates('1990-01') or {}).get('1990-01') != YEAR_RANGE
    def test_1990_02(self): assert (extract_explicit_dates('1990-02') or {}).get('1990-02') != YEAR_RANGE
    def test_1990_03(self): assert (extract_explicit_dates('1990-03') or {}).get('1990-03') != YEAR_RANGE
    def test_1990_04(self): assert (extract_explicit_dates('1990-04') or {}).get('1990-04') != YEAR_RANGE
    def test_1990_05(self): assert (extract_explicit_dates('1990-05') or {}).get('1990-05') != YEAR_RANGE
    def test_1990_06(self): assert (extract_explicit_dates('1990-06') or {}).get('1990-06') != YEAR_RANGE
    def test_1990_07(self): assert (extract_explicit_dates('1990-07') or {}).get('1990-07') != YEAR_RANGE
    def test_1990_08(self): assert (extract_explicit_dates('1990-08') or {}).get('1990-08') != YEAR_RANGE
    def test_1990_09(self): assert (extract_explicit_dates('1990-09') or {}).get('1990-09') != YEAR_RANGE
    def test_1990_10(self): assert (extract_explicit_dates('1990-10') or {}).get('1990-10') != YEAR_RANGE
    def test_1990_11(self): assert (extract_explicit_dates('1990-11') or {}).get('1990-11') != YEAR_RANGE
    def test_1990_12(self): assert (extract_explicit_dates('1990-12') or {}).get('1990-12') != YEAR_RANGE


# ===========================================================================
# Section 6: All 12 months for year 1980 — none must be YEAR_RANGE
# ===========================================================================

class TestYear1980AllMonths:
    """1980-MM for every valid month must not yield YEAR_RANGE."""

    def test_1980_01(self): assert (extract_explicit_dates('1980-01') or {}).get('1980-01') != YEAR_RANGE
    def test_1980_02(self): assert (extract_explicit_dates('1980-02') or {}).get('1980-02') != YEAR_RANGE
    def test_1980_03(self): assert (extract_explicit_dates('1980-03') or {}).get('1980-03') != YEAR_RANGE
    def test_1980_04(self): assert (extract_explicit_dates('1980-04') or {}).get('1980-04') != YEAR_RANGE
    def test_1980_05(self): assert (extract_explicit_dates('1980-05') or {}).get('1980-05') != YEAR_RANGE
    def test_1980_06(self): assert (extract_explicit_dates('1980-06') or {}).get('1980-06') != YEAR_RANGE
    def test_1980_07(self): assert (extract_explicit_dates('1980-07') or {}).get('1980-07') != YEAR_RANGE
    def test_1980_08(self): assert (extract_explicit_dates('1980-08') or {}).get('1980-08') != YEAR_RANGE
    def test_1980_09(self): assert (extract_explicit_dates('1980-09') or {}).get('1980-09') != YEAR_RANGE
    def test_1980_10(self): assert (extract_explicit_dates('1980-10') or {}).get('1980-10') != YEAR_RANGE
    def test_1980_11(self): assert (extract_explicit_dates('1980-11') or {}).get('1980-11') != YEAR_RANGE
    def test_1980_12(self): assert (extract_explicit_dates('1980-12') or {}).get('1980-12') != YEAR_RANGE


# ===========================================================================
# Section 7: All 12 months for year 1970 — none must be YEAR_RANGE
# ===========================================================================

class TestYear1970AllMonths:
    """1970-MM for every valid month must not yield YEAR_RANGE."""

    def test_1970_01(self): assert (extract_explicit_dates('1970-01') or {}).get('1970-01') != YEAR_RANGE
    def test_1970_02(self): assert (extract_explicit_dates('1970-02') or {}).get('1970-02') != YEAR_RANGE
    def test_1970_03(self): assert (extract_explicit_dates('1970-03') or {}).get('1970-03') != YEAR_RANGE
    def test_1970_04(self): assert (extract_explicit_dates('1970-04') or {}).get('1970-04') != YEAR_RANGE
    def test_1970_05(self): assert (extract_explicit_dates('1970-05') or {}).get('1970-05') != YEAR_RANGE
    def test_1970_06(self): assert (extract_explicit_dates('1970-06') or {}).get('1970-06') != YEAR_RANGE
    def test_1970_07(self): assert (extract_explicit_dates('1970-07') or {}).get('1970-07') != YEAR_RANGE
    def test_1970_08(self): assert (extract_explicit_dates('1970-08') or {}).get('1970-08') != YEAR_RANGE
    def test_1970_09(self): assert (extract_explicit_dates('1970-09') or {}).get('1970-09') != YEAR_RANGE
    def test_1970_10(self): assert (extract_explicit_dates('1970-10') or {}).get('1970-10') != YEAR_RANGE
    def test_1970_11(self): assert (extract_explicit_dates('1970-11') or {}).get('1970-11') != YEAR_RANGE
    def test_1970_12(self): assert (extract_explicit_dates('1970-12') or {}).get('1970-12') != YEAR_RANGE


# ===========================================================================
# Section 8: Sentence context — YYYY-MM embedded in prose
# ===========================================================================

class TestSentenceContext:
    """YYYY-MM embedded in prose must not produce a spurious YEAR_RANGE entry."""

    def test_sentence_2000_01(self):
        result = extract_explicit_dates('The record dates back to 2000-01.')
        assert not result or result.get('2000-01') != YEAR_RANGE

    def test_sentence_1999_12(self):
        result = extract_explicit_dates('The contract expired in 1999-12.')
        assert not result or result.get('1999-12') != YEAR_RANGE

    def test_sentence_1990_06(self):
        result = extract_explicit_dates('Data from 1990-06 is available.')
        assert not result or result.get('1990-06') != YEAR_RANGE

    def test_sentence_1985_03(self):
        result = extract_explicit_dates('Published in 1985-03 according to archives.')
        assert not result or result.get('1985-03') != YEAR_RANGE

    def test_sentence_2000_01_iso(self):
        result = extract_explicit_dates('Timestamp: 2000-01-01T00:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_sentence_1999_06_iso(self):
        result = extract_explicit_dates('Event logged at 1999-06-15T12:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_sentence_1980_11_iso(self):
        result = extract_explicit_dates('Created on 1980-11-04T08:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_sentence_1970_07_iso(self):
        result = extract_explicit_dates('Unix epoch region: 1970-07-04T00:00:00Z')
        assert not result or YEAR_RANGE not in result.values()

    def test_sentence_2005_06(self):
        result = extract_explicit_dates('The fiscal period was 2005-06.')
        assert not result or result.get('2005-06') != YEAR_RANGE

    def test_sentence_2010_03(self):
        result = extract_explicit_dates('Snapshot from 2010-03 shows growth.')
        assert not result or result.get('2010-03') != YEAR_RANGE


# ===========================================================================
# Section 9: Boundary month values (01 and 12) across multiple years
# ===========================================================================

class TestBoundaryMonths:
    """NN=01 and NN=12 (boundary months) across various years."""

    def test_2000_01_boundary(self): assert (extract_explicit_dates('2000-01') or {}).get('2000-01') != YEAR_RANGE
    def test_2000_12_boundary(self): assert (extract_explicit_dates('2000-12') or {}).get('2000-12') != YEAR_RANGE
    def test_1995_01_boundary(self): assert (extract_explicit_dates('1995-01') or {}).get('1995-01') != YEAR_RANGE
    def test_1995_12_boundary(self): assert (extract_explicit_dates('1995-12') or {}).get('1995-12') != YEAR_RANGE
    def test_1985_01_boundary(self): assert (extract_explicit_dates('1985-01') or {}).get('1985-01') != YEAR_RANGE
    def test_1985_12_boundary(self): assert (extract_explicit_dates('1985-12') or {}).get('1985-12') != YEAR_RANGE
    def test_1975_01_boundary(self): assert (extract_explicit_dates('1975-01') or {}).get('1975-01') != YEAR_RANGE
    def test_1975_12_boundary(self): assert (extract_explicit_dates('1975-12') or {}).get('1975-12') != YEAR_RANGE
    def test_2010_01_boundary(self): assert (extract_explicit_dates('2010-01') or {}).get('2010-01') != YEAR_RANGE
    def test_2010_12_boundary(self): assert (extract_explicit_dates('2010-12') or {}).get('2010-12') != YEAR_RANGE
