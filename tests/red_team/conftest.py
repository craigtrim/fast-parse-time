#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team Test Suite — Shared Configuration and Fixtures

Related GitHub Issue:
    #43 - Red team test suite: adversarial, unicode, and boundary inputs across all pattern types
    https://github.com/craigtrim/fast-parse-time/issues/43

PURPOSE OF THIS SUITE
─────────────────────
Standard regression tests verify that known-good inputs produce known-good outputs.
Red team testing is the adversarial complement: it asks, "what happens when we feed
the parser inputs it was never designed for — or inputs that *look* designed for it
but are subtly wrong?"

This suite is organized into three attack categories:

  1. TRUE POSITIVE ATTACKS
     Inputs that *should* parse successfully. The goal is to find inputs that a
     human would recognize as temporal but the parser silently drops. These reveal
     coverage gaps — patterns the parser doesn't yet handle.

  2. FALSE POSITIVE ATTACKS (false positive DEFENSE)
     Inputs that *should not* parse. The goal is to find inputs that superficially
     resemble temporal expressions but are not (IP addresses, version strings,
     non-temporal uses of month names, etc.). These reveal over-matching — places
     where the parser hallucinates dates.

  3. BOUNDARY AND EDGE CASES
     Inputs at or just beyond the valid range: minimum/maximum year, day 0, day 32,
     leap-day validation, zero cardinality, very large cardinality, negative numbers,
     and floating-point values. These reveal where the parser's guards begin and end.

  4. UNICODE AND HOMOGLYPH ATTACKS
     Inputs that use visually similar Unicode characters in place of ASCII: full-width
     digits, Arabic-Indic digits, homoglyph punctuation (en-dash, em-dash, fullwidth
     slash), and invisible control characters (zero-width space, RTL override, soft
     hyphen). These reveal whether the parser is brittle to Unicode normalization.

PHASE 1 VS PHASE 2
──────────────────
All tests in this suite start as `xfail` (marked at the module level in each file
with `pytestmark`). This means:

  - A test that FAILS   → reported as `xfail`  (expected failure, suite stays green)
  - A test that PASSES  → reported as `xpass`  (unexpected pass — candidate for promotion)

In Phase 2, `xpass` tests and clear-behavior tests are promoted to hard assertions.
See issue #43 for the full promotion decision matrix.

ACADEMIC INTENT
───────────────
Each test function in this suite carries a rich docstring that explains:
  - The specific attack vector being probed
  - Why a real parser might be fooled by this input
  - What a failure (or unexpected pass) reveals about the implementation
  - How to interpret the result in the context of the parser's architecture

This makes the suite useful not just as a quality gate but as educational material
for understanding the edge cases of temporal NLP parsing.
"""
