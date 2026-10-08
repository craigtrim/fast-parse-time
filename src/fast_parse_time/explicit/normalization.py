#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Pre-normalization of hyphen-like characters before any parsing logic runs.

Normalizes all Unicode dash/hyphen variants to ASCII hyphen-minus (U+002D)
and collapses digit-flanked space-padded hyphens so downstream extractors
only ever see the canonical form.

Related GitHub Issue:
    #44 - feat: Normalize hyphen-like characters and space-padded hyphens before parsing
    https://github.com/craigtrim/fast-parse-time/issues/44
    Prerequisite for: #40
"""

import re


# ---------------------------------------------------------------------------
# Unicode characters to normalize → ASCII hyphen-minus (U+002D)
#
# Intentionally excluded (not hyphens):
#   U+00AD SOFT HYPHEN   — a line-break hint, invisible, not a separator
#   U+200B ZERO-WIDTH SPACE — not a dash at all
# ---------------------------------------------------------------------------
_UNICODE_HYPHENS = re.compile(
    r'['
    r'\u2010'   # HYPHEN (proper)
    r'\u2011'   # NON-BREAKING HYPHEN
    r'\u2012'   # FIGURE DASH
    r'\u2013'   # EN DASH
    r'\u2014'   # EM DASH
    r'\u2015'   # HORIZONTAL BAR
    r'\u2212'   # MINUS SIGN
    r'\ufe63'   # SMALL HYPHEN-MINUS
    r'\uff0d'   # FULLWIDTH HYPHEN-MINUS
    r']'
)

# Digit-flanked space-padded hyphen:  DDDDD \s* - \s* DDDDD  →  DDDDD-DDDDD
# Requires at least one space on either side (asymmetric ok: "2014 -2015" or
# "2014- 2015"), but also handles symmetric and multi-space cases.
# Applied AFTER Unicode normalization so en/em dashes with spaces also collapse.
# Using * (zero-or-more) on both sides is safe — the idempotent case (no
# spaces) just normalizes "2014-2015" to itself with no observable effect.
_SPACED_HYPHEN = re.compile(
    r'(\d)(?:[\s\u00a0]+-[\s\u00a0]*|[\s\u00a0]*-[\s\u00a0]+)(\d)'
)


def normalize_text(text: str) -> str:
    """Normalize Unicode dash variants and space-padded hyphens to ASCII hyphen.

    This is a pre-processing step applied before any extractor runs.
    It is intentionally narrow: only digit-flanked spaces are collapsed,
    so compound words and prose punctuation are left untouched.

    Args:
        text: Raw input string.

    Returns:
        Normalized string with canonical ASCII hyphens.
        Returns the input unchanged if it is not a non-empty string.

    Example:
        >>> normalize_text('2014\u20132015')   # en dash
        '2014-2015'
        >>> normalize_text('2014 - 2015')      # space-padded
        '2014-2015'
        >>> normalize_text('north\u2013south') # en dash between words, unchanged
        'north-south'
    """
    if not text or not isinstance(text, str):
        return text

    # Step 1: replace Unicode hyphen variants with ASCII hyphen-minus
    text = _UNICODE_HYPHENS.sub('-', text)

    # Step 2: collapse spaces around hyphens that are flanked by digits
    text = _SPACED_HYPHEN.sub(r'\1-\2', text)

    return text
