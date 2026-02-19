#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


import re
from typing import Optional
from baseblock import ServiceEventGenerator

from fast_parse_time.core import configure_logger, Stopwatch
from fast_parse_time.implicit.dmo import DigitTextReplacer
from fast_parse_time.implicit.dmo import KeywordSequenceFilter
from fast_parse_time.implicit.dmo import KeywordSequenceExtractor
from fast_parse_time.implicit.dmo import SequenceSolutionFinder


# All recognized time unit words (singular, plural, abbreviated forms)
# Related GitHub Issue:
#     #20 - Gap: compound multi-unit expressions not supported
#     https://github.com/craigtrim/fast-parse-time/issues/20
_COMPOUND_UNIT_WORDS = {
    'second', 'seconds', 'sec', 'secs',
    'minute', 'minutes', 'min', 'mins',
    'hour', 'hours', 'hr', 'hrs',
    'day', 'days',
    'week', 'weeks', 'wk', 'wks',
    'month', 'months', 'mo', 'mos',
    'year', 'years', 'yr', 'yrs',
    'decade', 'decades',
}

# Tokens that act as connectors between unit pairs — stripped during compound parsing
_COMPOUND_CONNECTORS = {'and'}

# Past tense terminal markers
# Related GitHub Issue:
#     #58 - Support 'before' as past-tense marker and singular uninflected time frames
#     https://github.com/craigtrim/fast-parse-time/issues/58
_PAST_MARKERS = {'ago', 'back', 'before'}

# Future tense terminal suffix tokens (requires preceding 'from')
_FUTURE_TERMINALS = {'now', 'today'}

# Compact token letter-to-frame mapping
# Related GitHub Issue:
#     #57 - Support compact number+letter unit tokens (1d, 2y) in relative time parsing
#     https://github.com/craigtrim/fast-parse-time/issues/57
_COMPACT_UNIT_MAP = {
    'd': 'day',
    'w': 'week',
    'mo': 'month',
    'm': 'month',
    'y': 'year',
    'h': 'hour',
    'min': 'minute',
    's': 'second',
}

# Regex pattern to detect compact tokens: number + unit letter(s)
# Examples: 1d, 2w, 3mo, 5h, 10min, 30s
# Pattern breakdown:
#   \b         - word boundary
#   (\d+)      - one or more digits (cardinality)
#   (mo|min|d|w|m|y|h|s) - unit letter(s), ordered by length (mo and min before m and s)
#   \b         - word boundary
# Related GitHub Issue:
#     #57 - Support compact number+letter unit tokens (1d, 2y) in relative time parsing
#     https://github.com/craigtrim/fast-parse-time/issues/57
_COMPACT_TOKEN_PATTERN = re.compile(
    r'\b(\d+)(mo|min|d|w|m|y|h|s)\b',
    re.IGNORECASE
)


class AnalyzeTimeReferences(object):
    """ Analyze Time References in Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        Updated:
            18-Feb-2026
            craigtrim@gmail.com
            *   Add compound multi-unit expression support
                https://github.com/craigtrim/fast-parse-time/issues/20
        """
        self.logger = configure_logger(__name__)
        self._generate_event = ServiceEventGenerator().process

        self._digit_replacer = DigitTextReplacer().process
        self._filter_sequences = KeywordSequenceFilter().process
        self._extract_sequences = KeywordSequenceExtractor().process
        self._find_solutions = SequenceSolutionFinder().process

    @staticmethod
    def _is_numeric(token: str) -> bool:
        """Return True if token is an integer or decimal digit string."""
        return token.isdigit() or (
            '.' in token and token.replace('.', '', 1).isdigit()
        )

    @staticmethod
    def _expand_compact_tokens(input_text: str) -> str:
        """Expand compact number+unit tokens into separate number and unit tokens.

        Recognizes and expands patterns like:
            '1d ago'     → '1 day ago'
            '2w'         → '2 week ago'  (implicit past - 'ago' added)
            '3mo ago'    → '3 month ago'
            'posted 5h'  → 'posted 5 hour ago'  (implicit past)

        If no tense marker (ago, back, from now, etc.) follows the compact token,
        'ago' is automatically appended to create an implicit past-tense reference.

        Zero cardinality (0d, 0w, etc.) is NOT expanded (invalid time reference).

        Args:
            input_text (str): input text that may contain compact tokens

        Returns:
            str: text with compact tokens expanded and implicit 'ago' added where needed

        Related GitHub Issue:
            #57 - Support compact number+letter unit tokens (1d, 2y) in relative time parsing
            https://github.com/craigtrim/fast-parse-time/issues/57
        """
        # Pattern to detect if a tense marker follows the compact token
        # Looks for: compact token + optional whitespace + tense marker
        # Related GitHub Issue:
        #     #58 - Support 'before' as past-tense marker and singular uninflected time frames
        #     https://github.com/craigtrim/fast-parse-time/issues/58
        tense_markers_pattern = r'\b(ago|back|before)\b'

        def replace_compact_token(match):
            """Replace a compact token with expanded form."""
            cardinality_str = match.group(1)
            unit_letter = match.group(2).lower()
            match_end = match.end()

            # Reject zero cardinality
            cardinality = int(cardinality_str)
            if cardinality == 0:
                return match.group(0)  # return original token unchanged

            # Map unit letter to full unit name (singular form)
            unit_name = _COMPACT_UNIT_MAP.get(unit_letter)
            if not unit_name:
                return match.group(0)  # return original if no mapping found

            # Pluralize unit name if cardinality > 1
            # Standard pluralization: add 's' to the singular form
            if cardinality > 1:
                unit_name = unit_name + 's'

            # Check if a tense marker follows the compact token
            remaining_text = input_text[match_end:]
            has_tense_marker = re.match(r'^\s+(' + tense_markers_pattern + ')', remaining_text)

            # If no tense marker follows, add 'ago' for implicit past
            if has_tense_marker:
                # Tense marker present, just expand the token
                return f'{cardinality_str} {unit_name}'
            else:
                # No tense marker, add 'ago' for implicit past
                return f'{cardinality_str} {unit_name} ago'

        return _COMPACT_TOKEN_PATTERN.sub(replace_compact_token, input_text)

    def _extract_compound_sub_tokens(self, tokens: list) -> Optional[list]:
        """Detect and expand a compound multi-unit token list.

        Recognises patterns like:
            ['1', 'year', '2', 'months', 'ago']
            ['in', '1', 'year', '2', 'months']
            ['1', 'year', 'and', '2', 'months', 'from', 'now']

        Returns a list of single-unit token lists (one per unit pair) if the
        input is a compound expression containing 2 or more N-unit pairs.
        Returns None if the tokens do not represent a compound expression.

        Args:
            tokens (list): normalized token list (after DigitTextReplacer)

        Returns:
            Optional[list]: list of sub-token lists, or None

        Related GitHub Issue:
            #20 - Gap: compound multi-unit expressions not supported
            https://github.com/craigtrim/fast-parse-time/issues/20
        """
        if len(tokens) < 4:
            # Minimum compound: N unit N unit (4 tokens, no tense marker)
            return None

        # --- Determine tense and strip tense markers from body ---
        if tokens[-1] in _PAST_MARKERS:
            tense_suffix = [tokens[-1]]
            body = tokens[:-1]
        elif (len(tokens) >= 2
              and tokens[-2] == 'from'
              and tokens[-1] in _FUTURE_TERMINALS):
            tense_suffix = ['from', 'now']
            body = tokens[:-2]
        elif tokens[0] == 'in':
            tense_suffix = ['from', 'now']
            body = tokens[1:]
        else:
            # No explicit tense marker; treat as implicit past
            tense_suffix = ['ago']
            body = tokens

        # --- Strip connectors from body (commas already stripped upstream) ---
        body = [t for t in body if t not in _COMPOUND_CONNECTORS]

        # --- Parse contiguous N-unit pairs ---
        pairs = []
        i = 0
        while i < len(body):
            token = body[i]
            if (self._is_numeric(token)
                    and i + 1 < len(body)
                    and body[i + 1] in _COMPOUND_UNIT_WORDS):
                pairs.append((token, body[i + 1]))
                i += 2
            else:
                i += 1

        if len(pairs) < 2:
            # Single-unit or no unit — not a compound expression
            return None

        # Expand each pair into a standalone single-unit sub-expression
        return [[n, unit] + tense_suffix for n, unit in pairs]

    def _solve_sub_tokens(self, sub_tokens: list) -> list:
        """Run the KB pipeline on a single-unit token list.

        Args:
            sub_tokens (list): e.g. ['2', 'months', 'ago']

        Returns:
            list: solutions found (0 or 1 entries)
        """
        seqs = self._extract_sequences(sub_tokens)
        seqs = self._filter_sequences(seqs)
        return self._find_solutions(seqs)

    def _process(self,
                 input_text: str) -> dict:

        # Expand compact tokens (1d → 1 day, 2y → 2 year, etc.) before tokenization
        # Related GitHub Issue:
        #     #57 - Support compact number+letter unit tokens (1d, 2y) in relative time parsing
        #     https://github.com/craigtrim/fast-parse-time/issues/57
        input_text = self._expand_compact_tokens(input_text)

        tokens = input_text.lower().strip().split()

        tokens = self._digit_replacer(tokens)

        # Extract sequences before KB filtering (needed for compound detection below)
        all_sequences = self._extract_sequences(tokens)

        sequences = self._filter_sequences(all_sequences)
        solutions = self._find_solutions(sequences)

        # --- Compound expansion ---
        # For each sequence that didn't resolve via the normal pipeline, attempt
        # compound detection and expansion. Running per-sequence (not on the full
        # token list) correctly handles 'in' prefixes embedded in longer sentences.
        #
        # Example: 'the contract expires in 2 years 6 months'
        #   Sequence extractor yields: [['in', '2', 'years', '6', 'months']]
        #   Compound detects 'in' at position 0 of that sequence → future tense.
        #
        # Also fixes the partial-match bug where '1 year ... 1 minute ago'
        # previously returned only the last unit.
        #
        # Related GitHub Issue:
        #     #20 - Gap: compound multi-unit expressions not supported
        #     https://github.com/craigtrim/fast-parse-time/issues/20
        compound_solutions = []
        for seq in all_sequences:
            expanded = self._extract_compound_sub_tokens(seq)
            if expanded:
                for sub_tokens in expanded:
                    compound_solutions.extend(self._solve_sub_tokens(sub_tokens))

        # Use compound results when they yield more solutions (handles partial-match bug)
        if len(compound_solutions) > len(solutions):
            solutions = compound_solutions

        return {
            'input_text': input_text,
            'tokens': tokens,
            'sequences': sequences,
            'solutions': solutions
        }

    def process(self,
                input_text: str) -> Optional[list]:
        sw = Stopwatch()

        d_result = self._process(input_text)

        # COR-80; Generate an Event Record
        d_event = self._generate_event(
            service_name=__name__,
            event_name='analyze-time-references',
            stopwatch=sw,
            data=d_result)

        if not d_result['solutions'] or not len(d_result['solutions']):
            self.logger.debug('\n'.join([
                'No Solutions Found',
                f'\tTotal Time: {str(sw)}',
                f'\tInput Text: {input_text}']))

        else:
            self.logger.debug('\n'.join([
                'Time Reference Solutions Found',
                f'\tTotal Time: {str(sw)}',
                f'\tInput Text: {input_text}',
                f"\tTotal Solutions: {len(d_result['solutions'])}"]))

        return {
            'result': d_result['solutions'],
            'events': [d_event]
        }
