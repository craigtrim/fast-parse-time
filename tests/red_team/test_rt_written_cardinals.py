#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Written Cardinal Numbers as Temporal Cardinalities
(twenty-three days ago, one hundred and fifty minutes, thirty days from now)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

Academic Context
----------------
English written-out numbers introduce three distinct parsing challenges:

  1. COMPOSITIONALITY: "twenty-three" is two tokens fused by hyphen or space.
     The parser must reassemble them before mapping to a cardinality integer.

  2. SCALE-WORD LIFTING: "one hundred" requires recognizing "hundred" as a
     multiplier scale word, not a noun. "one hundred and fifty" further
     requires dropping the syntactic "and" connector.

  3. TEMPORAL UNIT AGREEMENT: Written numbers can precede any time unit.
     The discriminating signal between temporal and non-temporal use is
     whether the immediately following noun is a time unit.
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

_ONES = ['one','two','three','four','five','six','seven','eight','nine','ten',
         'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen',
         'eighteen','nineteen']
_TENS = ['twenty','thirty']
_COMPOUND = [f'twenty-{o}' for o in ['one','two','three','four','five','six',
             'seven','eight','nine','ten']] + ['thirty-one']
_COMPOUND_NOHYPHEN = [c.replace('-',' ') for c in _COMPOUND]

# ── TRUE POSITIVES: ones × days × ago ────────────────────────────────────────
_TP_ONES_DAYS = [f'{n} days ago' for n in _ONES]
@pytest.mark.parametrize('text', _TP_ONES_DAYS)
def test_tp_ones_days_ago(text):
    """Written numbers 1-19 + 'days ago'. Failure: written number not converted to cardinality."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: tens × days × ago ────────────────────────────────────────
_TP_TENS = [f'{n} days ago' for n in _TENS]
@pytest.mark.parametrize('text', _TP_TENS)
def test_tp_tens_days_ago(text):
    """'twenty days ago', 'thirty days ago'. Failure: round-ten forms not supported."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: compound hyphenated × days × ago ─────────────────────────
_TP_COMPOUND_HYPHEN = [f'{c} days ago' for c in _COMPOUND]
@pytest.mark.parametrize('text', _TP_COMPOUND_HYPHEN)
def test_tp_compound_hyphenated_days_ago(text):
    """Hyphenated compound written numbers + 'days ago' (twenty-one through thirty-one).
    Failure: hyphenated compound not reassembled before cardinality lookup."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: compound non-hyphenated × days × ago ─────────────────────
_TP_COMPOUND_NOHYPHEN = [f'{c} days ago' for c in _COMPOUND_NOHYPHEN]
@pytest.mark.parametrize('text', _TP_COMPOUND_NOHYPHEN)
def test_tp_compound_no_hyphen_days_ago(text):
    """Space-separated compound written numbers + 'days ago' (twenty one through thirty one).
    Failure: non-hyphenated compound not reassembled."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: hundreds ──────────────────────────────────────────────────
_TP_HUNDREDS = [
    'one hundred days ago','two hundred days ago','three hundred days ago',
    'five hundred days ago','one hundred years ago','two hundred years ago',
]
@pytest.mark.parametrize('text', _TP_HUNDREDS)
def test_tp_hundreds_days_ago(text):
    """'one hundred', 'two hundred', 'five hundred' + time unit + ago.
    Failure: scale-word 'hundred' not processed as multiplier."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: hundreds with 'and' connector ────────────────────────────
_TP_HUNDREDS_AND = [
    'one hundred and fifty days ago','two hundred and thirty days ago',
    'one hundred and twenty years ago','three hundred and sixty days ago',
]
@pytest.mark.parametrize('text', _TP_HUNDREDS_AND)
def test_tp_hundreds_with_and_connector(text):
    """'one hundred AND fifty days ago' — syntactic 'and' connector.
    Failure: 'and' in written number not recognized as connector (treated as content word)."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: other time units ─────────────────────────────────────────
_TP_OTHER_UNITS = [
    'three weeks ago','five months ago','two years ago','ten hours ago',
    'four minutes ago','seven seconds ago','six decades ago',
    'three weeks from now','five months from now','two years from now',
    'in three weeks','in five months','in two years',
]
@pytest.mark.parametrize('text', _TP_OTHER_UNITS)
def test_tp_written_numbers_other_units(text):
    """Written numbers with non-day time units across all tenses.
    Failure: written cardinal support only implemented for days."""
    assert len(extract_relative_times(text)) > 0

# ── FALSE POSITIVES: written number + non-temporal noun ──────────────────────
_FP = [
    'twenty-three apples ago','ten miles back','five pages ago',
    'three floors up','twelve steps away','six blocks over',
    'first place','second base','third degree','fourth quarter',
    'twenty questions','forty acres','a hundred reasons',
]
@pytest.mark.parametrize('text', _FP)
def test_fp_written_number_non_temporal_unit(text):
    """Written numbers with non-temporal nouns (apples, miles, pages, etc).
    Failure: any noun matched as time unit after a written number."""
    assert len(extract_relative_times(text)) == 0

# ── BOUNDARY ──────────────────────────────────────────────────────────────────
@pytest.mark.parametrize('text', [
    'zero days ago','negative five days ago','eleventy-one days ago',
    'one million days ago','twenty-thirteen days ago','hundred days ago',
])
def test_boundary_unusual_written_numbers(text):
    """Zero, negative, non-standard ('eleventy-one'), and very large written numbers.
    xfail: these are outside the standard written-number lexicon."""
    extract_relative_times(text)  # should not raise

@pytest.mark.parametrize('text', ['half a day ago','half an hour ago','half a week ago'])
def test_boundary_half_written(text):
    """'half a DAY ago' — fractional written cardinality. May match or not.
    xfail: fractional written cardinalities not defined in spec."""
    extract_relative_times(text)  # should not raise
