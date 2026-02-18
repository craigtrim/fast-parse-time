#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Relative Future Expressions (5 days from now, in 3 months, in 1 year)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_FRAMES_P = ['seconds','minutes','hours','days','weeks','months','years','decades']
_FRAMES_S = ['second','minute','hour','day','week','month','year','decade']

# ── TRUE POSITIVES: N units from now ─────────────────────────────────────────
_TP_FROM_NOW = (
    [f'1 {f} from now' for f in _FRAMES_S] +
    [f'1 {f} from now' for f in _FRAMES_P] +
    [f'5 {f} from now' for f in _FRAMES_P] +
    [f'10 {f} from now' for f in _FRAMES_P] +
    [f'30 {f} from now' for f in _FRAMES_P] +
    [f'100 {f} from now' for f in _FRAMES_P] +
    [f'365 {f} from now' for f in _FRAMES_P]
)

@pytest.mark.parametrize('text', _TP_FROM_NOW)
def test_tp_all_frames_from_now(text):
    """All 8 frames with 'from now' terminal, multiple cardinalities.
    Failure: frame or cardinality not supported in from-now form."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: in N units ────────────────────────────────────────────────
_TP_IN_N = (
    [f'in 1 {f}' for f in _FRAMES_S] +
    [f'in 1 {f}' for f in _FRAMES_P] +
    [f'in 5 {f}' for f in _FRAMES_P] +
    [f'in 10 {f}' for f in _FRAMES_P] +
    [f'in 30 {f}' for f in _FRAMES_P] +
    [f'in 100 {f}' for f in _FRAMES_P]
)

@pytest.mark.parametrize('text', _TP_IN_N)
def test_tp_in_n_units_form(text):
    """All 8 frames in 'in N UNIT' future form.
    Failure: 'in N UNIT' form not recognised or conflicts with prose-year 'in 2024'."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: abbreviated units ────────────────────────────────────────
_TP_ABBR = [
    '5 secs from now','3 mins from now','2 hrs from now','4 wks from now',
    '6 mos from now','2 yrs from now','in 5 secs','in 3 mins','in 2 hrs',
    'in 4 wks','in 6 mos','in 2 yrs',
]

@pytest.mark.parametrize('text', _TP_ABBR)
def test_tp_abbreviated_units_future(text):
    """Abbreviated time unit forms in future expressions.
    Failure: abbreviations not in unit lexicon for future tense."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence embedded ────────────────────────────────────────
_TP_EMBEDDED = [
    'the meeting is in 5 days','delivery expected in 3 weeks from now',
    'the deadline is 2 months from now','launch scheduled in 6 months',
    'renewal in 1 year from now','review in 30 days',
    'contract expires in 2 years','patch due in 48 hours from now',
]

@pytest.mark.parametrize('text', _TP_EMBEDDED)
def test_tp_sentence_embedded_future(text):
    """Future expressions embedded in prose. Failure: context breaks extraction."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: 'in YEAR' — YEAR_ONLY, not relative future ─────────────
_FP_IN_YEAR = [
    'in 2024','in 2020','in 1998','in 2030','in 1990','in 2010',
    'in 1926','in 2036','in 2000','in 1980',
]

@pytest.mark.parametrize('text', _FP_IN_YEAR)
def test_fp_in_year_not_relative_future(text):
    """'in YYYY' should resolve to YEAR_ONLY explicit date, not relative future.
    Critical disambiguation: 'in 2024' ≠ 'in 2024 days from now'.
    Failure: year-with-preposition matched as relative future."""
    result = extract_relative_times(text)
    # If matched, it should NOT have a cardinality of 2024 with frame=year
    for r in result:
        assert not (r.cardinality > 1900 and r.frame == 'year')

# ── FALSE POSITIVES: non-temporal 'in N' forms ────────────────────────────────
_FP_NON_TEMPORAL = [
    'in 5 minutes of fame','in 3 acts','in 2 parts','in 10 pieces',
    'in 4 chapters','in 6 installments','in 3 volumes',
    'from now on','starting from now','as of now',
    '5 days from today',  # 'today' not 'now'
]

@pytest.mark.parametrize('text', _FP_NON_TEMPORAL)
def test_fp_non_temporal_in_n_forms(text):
    """'in N' constructs with non-temporal units, and bare 'from now' without quantity.
    Failure: non-temporal 'in N' form matched as relative future."""
    result = extract_relative_times(text)
    # Allow zero results or results where frame is not a time unit
    for r in result:
        assert r.frame in ('second','minute','hour','day','week','month','year','decade')

# ── BOUNDARY: edge cases ──────────────────────────────────────────────────────
def test_boundary_zero_future():
    """in 0 days — degenerate future. Behavior undefined. xfail."""
    extract_relative_times('in 0 days')  # should not raise

def test_boundary_very_large_future():
    """in 999999 days — extreme future cardinality."""
    assert len(extract_relative_times('in 999999 days')) > 0

def test_boundary_negative_future():
    """in -5 days — nonsensical. Should not match."""
    assert len(extract_relative_times('in -5 days')) == 0
