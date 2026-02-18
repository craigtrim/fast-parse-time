#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Compound Multi-Unit Expressions
(1 year 2 months ago, in 1 year 2 months, 1 year and 2 months ago)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

Academic Context
----------------
Compound multi-unit temporal expressions combine two or more time-unit clauses
into a single temporal offset. The parsing challenge is threefold:

  1. UNIT BOUNDARY DETECTION: The parser must segment the expression into
     individual unit clauses without a hard delimiter between them.
     "1 year 2 months ago" has no separator between "year" and "2".

  2. CONNECTOR HANDLING: The optional word "and" ("1 year and 2 months ago")
     is syntactically inert — its presence or absence must not change parsing.

  3. RESULT MULTIPLICITY: The API returns one RelativeTime per unit clause.
     A compound expression with N unit clauses yields N RelativeTime objects.
     Tests assert len(result) >= 2 for two-unit compounds.
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

# Adjacent frame pairs (ordered largest→smallest)
_ADJACENT_PAIRS = [
    ('year','month'),('month','week'),('week','day'),
    ('day','hour'),('hour','minute'),('minute','second'),
]
_DISTANT_PAIRS = [
    ('year','day'),('year','hour'),('decade','month'),
    ('year','second'),('month','hour'),
]

# ── TRUE POSITIVES: 2-unit adjacent pairs × ago ──────────────────────────────
_TP_2UNIT_AGO = [f'1 {a} 2 {b}s ago' for a,b in _ADJACENT_PAIRS] +                 [f'1 {a} 2 {b}s ago' for a,b in _DISTANT_PAIRS] +                 [f'2 {a}s 3 {b}s ago' for a,b in _ADJACENT_PAIRS] +                 [f'3 {a}s 1 {b} ago' for a,b in _ADJACENT_PAIRS]

@pytest.mark.parametrize('text', _TP_2UNIT_AGO)
def test_tp_two_unit_ago(text):
    """Two-unit compound expressions with 'ago'. Expects >= 2 RelativeTime results.
    Failure: only first unit parsed, second unit dropped."""
    result = extract_relative_times(text)
    assert len(result) >= 2

# ── TRUE POSITIVES: with 'and' connector ─────────────────────────────────────
_TP_AND = [f'1 {a} and 2 {b}s ago' for a,b in _ADJACENT_PAIRS] +           [f'1 year and 2 months and 3 days ago',
           '2 years and 1 month ago','3 months and 2 weeks ago',
           '1 week and 4 days ago','2 days and 6 hours ago']

@pytest.mark.parametrize('text', _TP_AND)
def test_tp_two_unit_with_and_connector(text):
    """Two-unit compounds with 'and' connector. 'And' is syntactically inert.
    Failure: 'and' treated as content word breaking the unit-clause segmentation."""
    result = extract_relative_times(text)
    assert len(result) >= 2

# ── TRUE POSITIVES: future forms ─────────────────────────────────────────────
_TP_FUTURE = [f'1 {a} 2 {b}s from now' for a,b in _ADJACENT_PAIRS] +              [f'in 1 {a} 2 {b}s' for a,b in _ADJACENT_PAIRS] +              ['1 year 2 months from now','in 1 year 2 months',
              '3 months 2 weeks from now','in 2 weeks 5 days',
              '1 year and 6 months from now','in 2 years 3 months']

@pytest.mark.parametrize('text', _TP_FUTURE)
def test_tp_compound_future_forms(text):
    """Compound multi-unit future expressions. Failure: compound future not supported."""
    result = extract_relative_times(text)
    assert len(result) >= 2

# ── TRUE POSITIVES: abbreviated units ────────────────────────────────────────
_TP_ABBR = [
    '1 yr 2 mos ago','3 mos 2 wks ago','1 yr and 2 mos ago',
    '2 yrs 6 mos ago','1 mo 2 wks ago','3 wks 4 days ago',
    '1 yr 2 mos from now','in 1 yr 2 mos',
]
@pytest.mark.parametrize('text', _TP_ABBR)
def test_tp_compound_abbreviated_units(text):
    """Compound expressions with abbreviated unit forms. Failure: abbreviations break compound parsing."""
    result = extract_relative_times(text)
    assert len(result) >= 2

# ── TRUE POSITIVES: 3-unit expressions ───────────────────────────────────────
_TP_3UNIT = [
    '1 year 2 months 3 days ago',
    '2 years 1 month 1 week ago',
    'in 1 year 2 months 3 days',
    '1 year 2 months and 3 days ago',
    '3 days 4 hours 5 minutes ago',
]
@pytest.mark.parametrize('text', _TP_3UNIT)
def test_tp_three_unit_expressions(text):
    """Three-unit compound expressions. Expects >= 3 RelativeTime results.
    Failure: third unit dropped during compound parsing."""
    result = extract_relative_times(text)
    assert len(result) >= 3

# ── FALSE POSITIVES: non-temporal compound ────────────────────────────────────
_FP = [
    '1 dollar 2 cents ago','3 floors 2 rooms back','5 miles 3 blocks from now',
    '1 foot 2 inches ago','2 pounds 3 ounces back',
]
@pytest.mark.parametrize('text', _FP)
def test_fp_non_temporal_compound(text):
    """Compound 'N unit N unit ago' with non-temporal units (dollars, floors, miles).
    Failure: any N-unit compound matched regardless of time-unit membership."""
    assert len(extract_relative_times(text)) == 0

# ── BOUNDARY ─────────────────────────────────────────────────────────────────
@pytest.mark.parametrize('text',[
    '1 year 2 years ago',       # same unit repeated
    '1 year 0 months ago',      # zero inner unit
    '2 months 1 year ago',      # reversed order (smaller before larger)
    '1 and 2 ago',              # connector without units
    '100 years 50 months ago',  # large values
])
def test_boundary_unusual_compounds(text):
    """Unusual compound forms: repeated units, zero units, reversed order, no units.
    xfail: behavior for these edge cases is undefined."""
    extract_relative_times(text)  # should not raise
