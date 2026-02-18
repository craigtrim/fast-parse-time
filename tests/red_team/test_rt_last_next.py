#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Last/Next Patterns (last week, next month, last 10 days, next couple of weeks)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_FRAMES_S = ['second','minute','hour','day','week','month','year','decade']
_FRAMES_P = ['seconds','minutes','hours','days','weeks','months','years','decades']

# ── TRUE POSITIVES: last + singular frame ────────────────────────────────────
_TP_LAST_SINGULAR = [f'last {f}' for f in _FRAMES_S]

@pytest.mark.parametrize('text', _TP_LAST_SINGULAR)
def test_tp_last_singular_frames(text):
    """'last FRAME' for all 8 singular time frames. Failure: frame not in last-pattern lexicon."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: next + singular frame ────────────────────────────────────
_TP_NEXT_SINGULAR = [f'next {f}' for f in _FRAMES_S]

@pytest.mark.parametrize('text', _TP_NEXT_SINGULAR)
def test_tp_next_singular_frames(text):
    """'next FRAME' for all 8 singular time frames. Failure: frame not in next-pattern lexicon."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: last + numeric + frame ───────────────────────────────────
_TP_LAST_NUMERIC = (
    [f'last 1 {f}' for f in _FRAMES_P] +
    [f'last 5 {f}' for f in _FRAMES_P] +
    [f'last 10 {f}' for f in _FRAMES_P] +
    [f'last 30 {f}' for f in _FRAMES_P] +
    [f'last 90 {f}' for f in _FRAMES_P] +
    [f'last 100 {f}' for f in _FRAMES_P] +
    [f'last 365 {f}' for f in _FRAMES_P] +
    [f'last 1000 {f}' for f in _FRAMES_P]
)

@pytest.mark.parametrize('text', _TP_LAST_NUMERIC)
def test_tp_last_numeric_frames(text):
    """'last N FRAME' for all 8 frames and multiple cardinalities.
    Failure: numeric cardinality not supported in last-pattern."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: next + numeric + frame ───────────────────────────────────
_TP_NEXT_NUMERIC = (
    [f'next 1 {f}' for f in _FRAMES_P] +
    [f'next 5 {f}' for f in _FRAMES_P] +
    [f'next 10 {f}' for f in _FRAMES_P] +
    [f'next 30 {f}' for f in _FRAMES_P] +
    [f'next 90 {f}' for f in _FRAMES_P] +
    [f'next 100 {f}' for f in _FRAMES_P]
)

@pytest.mark.parametrize('text', _TP_NEXT_NUMERIC)
def test_tp_next_numeric_frames(text):
    """'next N FRAME' for all 8 frames and multiple cardinalities.
    Failure: numeric cardinality not supported in next-pattern."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: quantifier forms ─────────────────────────────────────────
_TP_QUANT = [
    'last couple of days','last couple of weeks','last couple of months','last couple of years',
    'last few days','last few weeks','last few months','last few years',
    'next couple of days','next couple of weeks','next couple of months','next couple of years',
    'next few days','next few weeks','next few months','next few years',
]

@pytest.mark.parametrize('text', _TP_QUANT)
def test_tp_last_next_quantifier(text):
    """'last/next couple of/few FRAME' quantifier forms.
    Failure: quantifier forms not supported in last/next patterns."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence embedded ────────────────────────────────────────
_TP_EMBEDDED = [
    'show me data from last week','what happened last month',
    'the next quarter starts soon','next year we will revisit',
    'last 30 days performance report','next 90 days roadmap',
    'review the last 12 months','plan for next 6 months',
]

@pytest.mark.parametrize('text', _TP_EMBEDDED)
def test_tp_sentence_embedded(text):
    """Last/next embedded in natural sentences. Failure: prose context breaks extraction."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: last as adjective/noun ──────────────────────────────────
_FP_LAST_NOUN = [
    'the last chapter','last name','last call','last resort','last rites',
    'at last','the very last','breathing his last','the last of the mohicans',
    'last but not least','saving the best for last','last in first out',
    'his last words','she came in last','that is the last straw',
]

@pytest.mark.parametrize('text', _FP_LAST_NOUN)
def test_fp_last_as_adjective_or_noun(text):
    """'last' used as adjective or noun without a following time unit.
    Failure: 'last' matched as temporal without a time unit anchor."""
    assert len(extract_relative_times(text)) == 0

# ── FALSE POSITIVES: next as adjective/noun ──────────────────────────────────
_FP_NEXT_NOUN = [
    'next please','next door','next in line','what comes next',
    'next of kin','the next big thing','next to nothing','up next',
    'next on the agenda','who is next','take it to the next level',
    'next steps','you are next','the sequel comes next',
]

@pytest.mark.parametrize('text', _FP_NEXT_NOUN)
def test_fp_next_as_adjective_or_noun(text):
    """'next' used without following time unit. Failure: 'next' alone matched as temporal."""
    assert len(extract_relative_times(text)) == 0

# ── FALSE POSITIVES: last seen/modified ──────────────────────────────────────
_FP_LAST_VERB = [
    'last seen online','last modified','last updated','last accessed',
    'last changed','last run','last deployed','last audited',
]

@pytest.mark.parametrize('text', _FP_LAST_VERB)
def test_fp_last_verb_phrases(text):
    """'last VERB' phrases where the following word is a participle not a time unit.
    Failure: 'last' + non-time-unit verb matched as temporal."""
    assert len(extract_relative_times(text)) == 0

# ── BOUNDARY ──────────────────────────────────────────────────────────────────
def test_boundary_last_zero_days():
    """last 0 days — degenerate cardinality. xfail."""
    extract_relative_times('last 0 days')  # should not raise

def test_boundary_last_negative():
    """last -5 days — nonsensical. Should not match."""
    assert len(extract_relative_times('last -5 days')) == 0

def test_boundary_very_large():
    """last 999999 years — extreme cardinality."""
    assert len(extract_relative_times('last 999999 years')) > 0
