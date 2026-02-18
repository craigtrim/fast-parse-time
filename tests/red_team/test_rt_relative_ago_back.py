#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Relative Past Expressions (5 days ago, 10 hours back, 100 years ago)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_FRAMES = ['second','minute','hour','day','week','month','year','decade']
_FRAMES_PLURAL = ['seconds','minutes','hours','days','weeks','months','years','decades']
_ABBR = [('sec','secs'),('min','mins'),('hr','hrs'),('day','days'),
         ('wk','wks'),('mo','mos'),('yr','yrs'),('decade','decades')]

# ── TRUE POSITIVES: all 8 frames × ago × cardinality 1,5,10,100 ─────────────
_TP_AGO = (
    [f'1 {f} ago' for f in _FRAMES] +
    [f'1 {f} ago' for f in _FRAMES_PLURAL] +
    [f'5 {f} ago' for f in _FRAMES_PLURAL] +
    [f'10 {f} ago' for f in _FRAMES_PLURAL] +
    [f'100 {f} ago' for f in _FRAMES_PLURAL] +
    [f'30 {f} ago' for f in _FRAMES_PLURAL] +
    [f'365 {f} ago' for f in _FRAMES_PLURAL] +
    [f'52 {f} ago' for f in _FRAMES_PLURAL]
)

@pytest.mark.parametrize('text', _TP_AGO)
def test_tp_all_frames_ago(text):
    """All 8 time frames with 'ago' terminal, multiple cardinalities.
    Failure: frame or cardinality not supported in ago-form."""
    assert len(extract_relative_times(text)) > 0

_TP_BACK = (
    [f'1 {f} back' for f in _FRAMES] +
    [f'1 {f} back' for f in _FRAMES_PLURAL] +
    [f'5 {f} back' for f in _FRAMES_PLURAL] +
    [f'10 {f} back' for f in _FRAMES_PLURAL] +
    [f'100 {f} back' for f in _FRAMES_PLURAL]
)

@pytest.mark.parametrize('text', _TP_BACK)
def test_tp_all_frames_back(text):
    """All 8 time frames with 'back' terminal marker.
    Failure: 'back' not recognised as past-tense terminal."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: abbreviated unit forms ────────────────────────────────────
_TP_ABBR = (
    [f'5 {sg} ago' for sg, _ in _ABBR] +
    [f'5 {pl} ago' for _, pl in _ABBR] +
    [f'3 {sg} back' for sg, _ in _ABBR] +
    [f'3 {pl} back' for _, pl in _ABBR]
)

@pytest.mark.parametrize('text', _TP_ABBR)
def test_tp_abbreviated_unit_forms(text):
    """Abbreviated time unit forms (sec, min, hr, wk, mo, yr, etc).
    Failure: abbreviations not in unit lexicon."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence embedded ────────────────────────────────────────
_TP_EMBEDDED = [
    'the incident occurred 5 days ago in the morning',
    'we saw this 3 weeks back during testing',
    'the outage 10 hours ago was resolved',
    'this bug was introduced 6 months ago',
    '2 years ago we redesigned the system',
    'the meeting 30 minutes ago ran long',
    'an update 1 year ago changed the behaviour',
    'performance degraded 2 weeks back',
]

@pytest.mark.parametrize('text', _TP_EMBEDDED)
def test_tp_sentence_embedded(text):
    """Relative past expressions embedded in prose sentences.
    Failure: surrounding context breaks relative time extraction."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: large cardinalities ─────────────────────────────────────
_TP_LARGE = [
    '365 days ago','730 days ago','999 days ago',
    '52 weeks ago','104 weeks ago',
    '24 hours ago','48 hours ago','72 hours ago',
    '12 months ago','24 months ago',
    '3 years ago','5 years ago','10 years ago','50 years ago','100 years ago',
]

@pytest.mark.parametrize('text', _TP_LARGE)
def test_tp_large_cardinalities(text):
    """Large numeric cardinalities with 'ago'. Failure: upper cardinality limit too low."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: non-temporal units ──────────────────────────────────────
_FP_NON_TEMPORAL = [
    '5 miles ago','3 pages back','10 floors ago','2 chapters back',
    '7 steps ago','4 items back','6 blocks ago','8 songs back',
    '3 rows ago','5 seats back','10 questions ago','2 levels back',
    '4 moves ago','12 rounds back','3 innings ago',
]

@pytest.mark.parametrize('text', _FP_NON_TEMPORAL)
def test_fp_non_temporal_units(text):
    """Non-temporal unit nouns after cardinality + ago/back (miles, pages, floors).
    Failure: 'ago'/'back' matched regardless of whether preceding noun is a time unit."""
    assert len(extract_relative_times(text)) == 0

# ── FALSE POSITIVES: ago/back without quantity ────────────────────────────────
_FP_NO_QTY = [
    'the meeting, ago','long ago','ages ago','years and years ago',
    'he went back','back to school','set things back','holding back',
    'step back','back in the day','way back','a while back',
    'once upon a time, long ago',
]

@pytest.mark.parametrize('text', _FP_NO_QTY)
def test_fp_ago_back_without_quantity(text):
    """'ago' and 'back' used without a specific numeric or quantifier cardinality.
    'Long ago' and 'a while back' should not yield structured RelativeTime.
    Failure: unanchored ago/back matched without cardinality."""
    assert len(extract_relative_times(text)) == 0

# ── BOUNDARY: edge cardinalities ─────────────────────────────────────────────
def test_boundary_zero_cardinality():
    """0 days ago — degenerate cardinality. Behavior undefined (same as 'now'?).
    xfail: zero cardinality semantics not defined."""
    result = extract_relative_times('0 days ago')
    # If matched, cardinality should be 0
    if result:
        assert result[0].cardinality == 0

def test_boundary_very_large_cardinality():
    """999999 days ago — extreme cardinality. Should match if no upper bound.
    Failure: arbitrary upper bound on cardinality blocks large values."""
    assert len(extract_relative_times('999999 days ago')) > 0

def test_boundary_negative_cardinality():
    """-5 days ago — negative cardinality. Should NOT match (nonsensical).
    Failure: negative numbers matched as cardinalities."""
    assert len(extract_relative_times('-5 days ago')) == 0

# ── UNICODE: digit homoglyphs ─────────────────────────────────────────────────
_UNICODE = [
    '⁵ days ago',          # superscript 5
    '② days ago',          # circled 2
    '٥ days ago',          # Arabic-Indic 5
    '5​ days ago',         # ZWS between digit and space
    '５ days ago',          # fullwidth 5
    '৫ days ago',          # Bengali 5
    '5̈ days ago',         # combining diaeresis on 5
]

@pytest.mark.parametrize('text', _UNICODE)
def test_unicode_digit_homoglyphs_ago(text):
    """Non-ASCII digit homoglyphs in cardinality position of 'ago' expressions.
    Failure: Unicode digits accepted as cardinalities (may cause silent errors)."""
    assert len(extract_relative_times(text)) == 0
