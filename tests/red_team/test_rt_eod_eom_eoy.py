#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: End-of-Period Abbreviations (eod, eom, eoy)
Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

Academic Context
----------------
EOD (end of day), EOM (end of month), EOY (end of year) are compact business
abbreviations for future temporal references. Their brevity makes them
particularly susceptible to two attack classes:

  1. FALSE POSITIVE RISK — SUPERSET STRINGS: Any word that contains 'eod',
     'eom', or 'eoy' as a substring could trigger a false positive if the
     parser uses substring rather than whole-word matching. The word "decode"
     contains "eod" as a proper substring (d-e-c-o-d-e → index 3-5 = "ode",
     but "eod" appears as chars 2-4 of "decode" reversed... actually 'decode'
     does NOT contain 'eod' literally. However 'period' → 'e-r-i-o-d' does
     not contain 'eod'. 'diode' → 'd-i-o-d-e' does not contain 'eod'.
     Testing these confirms the parser uses whole-word boundary matching.

  2. CONCATENATION ATTACK: "eodeom" or "eod/eom" tests whether the parser
     requires word boundaries around these tokens or allows them to appear
     adjacent to other characters.

  3. CASE SENSITIVITY: Business usage is mixed — "EOD", "eod", "Eod" all
     occur. The parser must be case-insensitive for these abbreviations.
"""
import pytest
from fast_parse_time.api import extract_relative_times
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')

# ── TRUE POSITIVES: isolated ─────────────────────────────────────────────────
@pytest.mark.parametrize('text', ['eod','eom','eoy','EOD','EOM','EOY',
                                   'Eod','Eom','Eoy','eOd','eOm','eOy',
                                   'EOd','EOm','EOy','EoD','EoM','EoY'])
def test_tp_isolated_all_cases(text):
    """EOD/EOM/EOY in all case permutations. Failure: case-sensitive matching."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: sentence embedded ────────────────────────────────────────
_TP_EMBEDDED = [
    'please finish by eod','targets are due eom','budget closes eoy',
    'all reports due EOD','pipeline runs eom','revenue targets set eoy',
    'finish by eod.','due eom,','closes eoy!',
    'the PR must be merged EOD','invoices submitted EOM',
    'headcount finalized EOY','please review by EOD today',
    'eod is the deadline','eom billing cycle complete',
    'eoy review scheduled','report needed by eod please',
]
@pytest.mark.parametrize('text', _TP_EMBEDDED)
def test_tp_sentence_embedded(text):
    """EOD/EOM/EOY embedded in natural business language with punctuation.
    Failure: surrounding tokens or punctuation prevent matching."""
    assert len(extract_relative_times(text)) > 0

# ── TRUE POSITIVES: all three in one string ────────────────────────────────
def test_tp_all_three_in_one_string_lower():
    """'eod eom eoy' — all three markers in one string. Expect 3 results."""
    result = extract_relative_times('eod eom eoy')
    assert len(result) >= 3

def test_tp_all_three_in_one_string_upper():
    """'EOD EOM EOY' — all three uppercase. Expect 3 results."""
    result = extract_relative_times('EOD EOM EOY')
    assert len(result) >= 3

# ── FALSE POSITIVES: superset strings (word contains eod/eom/eoy as substring) ─
_FP_SUPERSET = [
    'aeod','eodx','xeom','eomx','xeoy','eoyx',
    'eodeom','eomeoy','eodeoy',
    'AEOD','EODX','XEOM',
    'EODF','EOMR','EOYA',
    'reload','commode','decode',  # testing: do these contain eod/eom/eoy? 'reload' no, 'decode' no
    'geometry','theorem','poem',
]
@pytest.mark.parametrize('text', _FP_SUPERSET)
def test_fp_superset_strings(text):
    """Strings prefixing/suffixing eod/eom/eoy with extra characters.
    Tests that the parser uses word-boundary matching, not substring matching.
    Failure: partial matches on concatenated or extended tokens."""
    assert len(extract_relative_times(text)) == 0

# ── FALSE POSITIVES: joined with punctuation ─────────────────────────────────
_FP_JOINED = [
    'eod/eom','eom-eoy','eod_eom','eod.eom','eod,eom',
    'EOD/EOM','EOM-EOY',
]
@pytest.mark.parametrize('text', _FP_JOINED)
def test_fp_punctuation_joined(text):
    """EOD/EOM/EOY tokens joined directly by punctuation without spaces.
    Whether these should match as individual tokens is ambiguous.
    xfail: joined forms may or may not be supported."""
    # Not asserting specific outcome — just must not crash
    extract_relative_times(text)

# ── BOUNDARY: empty and partial ──────────────────────────────────────────────
@pytest.mark.parametrize('text', ['','e','eo','od','om','oy'])
def test_boundary_partial_tokens(text):
    """Empty string and partial token fragments. Should not match and not crash.
    Failure: partial fragments matched as temporal."""
    assert len(extract_relative_times(text)) == 0
