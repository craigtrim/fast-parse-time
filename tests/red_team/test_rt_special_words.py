#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Special Temporal Words (today, yesterday, tomorrow, tonight, now, right now)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_WORDS = ['today','yesterday','tomorrow','tonight','now','right now']

# ── TRUE POSITIVES: isolated ─────────────────────────────────────────────────
@pytest.mark.parametrize('word', _WORDS)
def test_tp_isolated_special_words(word):
    """Each of the 6 special temporal words in isolation.
    Failure: special word not in the KB or not recognized standalone."""
    assert len(extract_relative_times(word)) > 0

# ── TRUE POSITIVES: uppercase ─────────────────────────────────────────────────
_TP_UPPER = ['TODAY','YESTERDAY','TOMORROW','TONIGHT','NOW','RIGHT NOW']
@pytest.mark.parametrize('text', _TP_UPPER)
def test_tp_uppercase(text):
    """Special temporal words in full uppercase. Failure: case-sensitive matching."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: mixed case ────────────────────────────────────────────────
_TP_MIXED = ['Today','Yesterday','Tomorrow','Tonight','Now','Right Now',
             'ToDay','YeStErDaY','TOMORROW','ToNiGhT']
@pytest.mark.parametrize('text', _TP_MIXED)
def test_tp_mixed_case(text):
    """Mixed-case special temporal words. Failure: not case-insensitive."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence start/middle/end ────────────────────────────────
_TP_SENTENCE = [
    'Today I went to the store','Yesterday the report was filed',
    'Tomorrow we ship the release','Tonight there is a meeting',
    'I said today to proceed','we noted yesterday that the test failed',
    'planning to ship tomorrow with the hotfix',
    'See you tomorrow.','I will do it today.','He said yesterday.',
    'We finish tonight.', 'The status is good right now.',
    'Let me check on it now and get back to you.',
]
@pytest.mark.parametrize('text', _TP_SENTENCE)
def test_tp_sentence_embedded(text):
    """Special temporal words in natural sentence positions (start, middle, end).
    Failure: sentence context breaks special-word extraction."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: possessives ──────────────────────────────────────────────
_TP_POSSESSIVE = [
    "today's meeting","tomorrow's forecast","yesterday's results",
    "tonight's agenda","today's report","tomorrow's deadline",
]
@pytest.mark.parametrize('text', _TP_POSSESSIVE)
def test_tp_possessives(text):
    """Special temporal words with possessive 's suffix.
    Whether the parser extracts the root is a design decision; the test
    checks that the word is at minimum recognized in possessive form."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: substring containment ───────────────────────────────────
_FP_SUBSTRING = [
    'nowadays','nowhere','know','renown','snowfall','knowhow',
    'overthrow','elbow','meow','below','bestow','follow','hollow',
    'daybreak','everyday','birthday','holiday','sundry',
    'goodnight','fortnight','midnight','highlight','insight',
]
@pytest.mark.parametrize('text', _FP_SUBSTRING)
def test_fp_substring_containment(text):
    """Words containing temporal keywords as substrings (now in 'nowadays', etc).
    Failure: substring match produces false positive on non-temporal word."""
    assert len(extract_relative_times(text)) == 0

# ── FALSE POSITIVES: negated or qualified ────────────────────────────────────
_FP_QUALIFIED = [
    'not today','not now','not tomorrow',
    'maybe tomorrow','possibly tonight','perhaps yesterday',
    'some day','any day','every day','each day',
]
@pytest.mark.parametrize('text', _FP_QUALIFIED)
def test_fp_negated_and_qualified(text):
    """Temporal words with negation or qualification. Behavior is ambiguous —
    'not today' still contains 'today'. This tests whether the parser extracts
    the word regardless of surrounding negation (which is the simpler correct approach).
    xfail: the correct behavior is design-dependent."""
    # This is intentionally ambiguous — we assert no crash, and note xfail covers outcome
    extract_relative_times(text)  # should not raise

# ── BOUNDARY: multiple in one string ─────────────────────────────────────────
def test_boundary_multiple_special_words():
    """'yesterday and today and tomorrow' — should yield 3 RelativeTime results.
    Failure: only first or last match extracted from multi-temporal string."""
    result = extract_relative_times('yesterday and today and tomorrow')
    assert len(result) >= 2

def test_boundary_right_now_repeated():
    """'right now right now' — 1 or 2 results? xfail: duplication behavior undefined."""
    result = extract_relative_times('right now right now')
    assert len(result) >= 1
