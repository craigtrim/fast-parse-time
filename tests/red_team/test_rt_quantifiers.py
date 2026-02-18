#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Quantifier Patterns (a few days ago, couple of weeks ago, several months ago)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_FRAMES_P = ['seconds','minutes','hours','days','weeks','months','years','decades']

# ── TRUE POSITIVES: "a few" × all frames ─────────────────────────────────────
_TP_A_FEW = [f'a few {f} ago' for f in _FRAMES_P]
@pytest.mark.parametrize('text', _TP_A_FEW)
def test_tp_a_few_all_frames(text):
    """'a few FRAME ago' for all 8 frames. Failure: 'a few' quantifier not in KB."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: "few" (no article) ───────────────────────────────────────
_TP_FEW = [f'few {f} ago' for f in _FRAMES_P]
@pytest.mark.parametrize('text', _TP_FEW)
def test_tp_few_no_article(text):
    """'few FRAME ago' (article omitted). Failure: article required for 'few' matching."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: "a couple of" ────────────────────────────────────────────
_TP_COUPLE_OF = [f'a couple of {f} ago' for f in _FRAMES_P]
@pytest.mark.parametrize('text', _TP_COUPLE_OF)
def test_tp_a_couple_of_all_frames(text):
    """'a couple of FRAME ago' for all 8 frames. Failure: 'couple of' not in KB."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: "couple of" (no article) ─────────────────────────────────
_TP_COUPLE = [f'couple of {f} ago' for f in _FRAMES_P]
@pytest.mark.parametrize('text', _TP_COUPLE)
def test_tp_couple_of_no_article(text):
    """'couple of FRAME ago' without 'a'. Failure: 'a' required for 'couple' matching."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: "several" ────────────────────────────────────────────────
_TP_SEVERAL = [f'several {f} ago' for f in _FRAMES_P]
@pytest.mark.parametrize('text', _TP_SEVERAL)
def test_tp_several_all_frames(text):
    """'several FRAME ago' for all 8 frames. Failure: 'several' not in quantifier KB."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: future quantifiers ───────────────────────────────────────
_TP_FUTURE = (
    [f'a few {f} from now' for f in _FRAMES_P] +
    [f'a couple of {f} from now' for f in _FRAMES_P] +
    [f'in a few {f}' for f in _FRAMES_P]
)
@pytest.mark.parametrize('text', _TP_FUTURE)
def test_tp_future_quantifiers(text):
    """Quantifiers in future forms ('a few days from now', 'in a few days').
    Failure: quantifiers not supported in future tense expressions."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence embedded ────────────────────────────────────────
_TP_EMBEDDED = [
    'the outage occurred a few hours ago during peak traffic',
    'we saw this a couple of weeks ago in production',
    'a few months ago the team decided to refactor',
    'several years ago this was common practice',
    'a couple of days ago the logs showed anomalies',
]
@pytest.mark.parametrize('text', _TP_EMBEDDED)
def test_tp_sentence_embedded_quantifiers(text):
    """Quantifier temporal expressions in natural prose. Failure: context breaks extraction."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: quantifier + non-temporal noun ──────────────────────────
_FP_NON_TEMPORAL = [
    'a few good men','a few miles away','a couple of beers','a couple of items',
    'several miles from here','several pages long','a few hundred dollars',
    'a few dozen eggs','a couple of friends','several floors up',
    'a few more questions','couple of chairs','several books',
]
@pytest.mark.parametrize('text', _FP_NON_TEMPORAL)
def test_fp_quantifier_with_non_temporal_noun(text):
    """Quantifiers followed by non-temporal unit nouns (miles, beers, eggs, etc).
    Failure: 'a few' matched regardless of whether the following noun is a time unit."""
    assert len(extract_relative_times(text)) == 0

# ── BOUNDARY ──────────────────────────────────────────────────────────────────
def test_boundary_double_quantifier():
    """'couple of couple of weeks ago' — malformed double quantifier. Should not crash."""
    extract_relative_times('couple of couple of weeks ago')

def test_boundary_several_repeated():
    """'several several months ago' — malformed. Should not crash."""
    extract_relative_times('several several months ago')

def test_boundary_quantifier_no_unit():
    """'a few ago' — quantifier without time unit. Should not match."""
    assert len(extract_relative_times('a few ago')) == 0
