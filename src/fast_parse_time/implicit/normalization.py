#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Replace Spelled-Out forms of Numbers with their Digits """


from datetime import date
from word2number import w2n


class DigitTextReplacer(object):
    """ Replace Spelled-Out forms of Numbers with their Digits

    e.g., 'three' => 3
    """

    # Indefinite articles that imply cardinality of 1
    INDEFINITE_ARTICLES = {'a', 'an'}

    # Informal quantity words mapped to numeric values
    # Note: 'couple' is already in KB with explicit patterns like 'last couple of weeks'
    INFORMAL_QUANTITIES = {'several': '3', 'few': '3'}

    # Multi-token phrase replacements (order matters - longer phrases first)
    # Related GitHub Issues:
    #     #18 - Gap: near-past/near-future idioms not supported
    #           https://github.com/craigtrim/fast-parse-time/issues/18
    PHRASE_REPLACEMENTS = [
        # Near-past idioms — 2 days ago
        # Longer 'the day before yesterday' must precede 'day before yesterday'
        ('the day before yesterday', '2 days ago'),
        ('day before yesterday', '2 days ago'),
        # Near-future idioms — 2 days from now
        # Fix: 'the day after tomorrow' previously matched embedded 'tomorrow' (→1 day)
        # Longer form must precede shorter to avoid partial match
        ('the day after tomorrow', '2 days from now'),
        ('day after tomorrow', '2 days from now'),
        # Archaic single-token synonym for 2 days from now
        ('overmorrow', '2 days from now'),
        # Present-anchored idioms — normalize to 'today' (already in KB)
        ('till date', 'today'),
        ('to date', 'today'),
        # Existing phrase replacements
        ('half an hour', '30 minutes'),
        ('half a day', '12 hours'),
    ]

    # All time unit words recognized in compound expressions.
    # Used to detect 'and' connectors between unit pairs for removal.
    # Related GitHub Issue:
    #     #20 - Gap: compound multi-unit expressions not supported
    #     https://github.com/craigtrim/fast-parse-time/issues/20
    COMPOUND_UNIT_WORDS = {
        'second', 'seconds', 'sec', 'secs',
        'minute', 'minutes', 'min', 'mins',
        'hour', 'hours', 'hr', 'hrs',
        'day', 'days',
        'week', 'weeks', 'wk', 'wks',
        'month', 'months', 'mo', 'mos',
        'year', 'years', 'yr', 'yrs',
        'decade', 'decades',
    }

    # Singular abbreviated unit forms to normalize to plural when N > 1
    # e.g., '5 min ago' → '5 mins ago', '5 hr from now' → '5 hrs from now'
    # Related GitHub Issue:
    #     #9 - Support abbreviated unit forms (min, hr, hour) for N > 1
    #     https://github.com/craigtrim/fast-parse-time/issues/9
    UNIT_SINGULAR_TO_PLURAL = {
        'min': 'mins',
        'hr': 'hrs',
        'hour': 'hours',
    }

    # Weekday name/abbreviation → ISO weekday number (Monday=0 ... Sunday=6)
    # Related GitHub Issues:
    #     #11 - Gap: named weekday references not supported (next friday, last monday)
    #           https://github.com/craigtrim/fast-parse-time/issues/11
    #     #12 - feat: Support forward day-of-week references (next Friday, next Monday)
    #           https://github.com/craigtrim/fast-parse-time/issues/12
    WEEKDAY_NAMES = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1, 'tues': 1,
        'wednesday': 2, 'wed': 2, 'weds': 2,
        'thursday': 3, 'thu': 3, 'thurs': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6,
    }

    # Tense prefixes for weekday references
    FUTURE_WEEKDAY_PREFIXES = {'next', 'this', 'coming'}
    PAST_WEEKDAY_PREFIXES = {'last', 'past'}

    def __init__(self):
        """ Change Log

        Created:
            11-Aug-2022
            craigtrim@gmail.com
        Updated:
            23-Jan-2026
            craigtrim@gmail.com
            *   Handle indefinite articles 'a' and 'an' as 1
                https://github.com/craigtrim/fast-parse-time/issues/4
            *   Handle informal expressions 'half an hour', 'several'
                https://github.com/craigtrim/fast-parse-time/issues/5
            18-Feb-2026
            craigtrim@gmail.com
            *   Handle named weekday references (next friday, last monday)
                https://github.com/craigtrim/fast-parse-time/issues/11
                https://github.com/craigtrim/fast-parse-time/issues/12
        """
        pass

    def _remove_compound_and(self, tokens: list) -> list:
        """Remove 'and' tokens that act as connectors between compound unit pairs.

        In compound expressions like '1 year and 2 months ago', 'and' connects
        adjacent N-unit pairs. Since 'and' is not a KB keyterm it breaks sequence
        extraction, preventing compound detection. Removing it allows the sequence
        extractor to keep the full compound as one continuous sequence.

        Only removes 'and' when the preceding token is a time unit word and the
        following token is a digit — this avoids removing 'and' from unrelated phrases.

        Example:
            ['1', 'year', 'and', '2', 'months', 'ago']
            → ['1', 'year', '2', 'months', 'ago']

        Related GitHub Issue:
            #20 - Gap: compound multi-unit expressions not supported
            https://github.com/craigtrim/fast-parse-time/issues/20
        """
        def _is_numeric(tok: str) -> bool:
            return tok.isdigit() or ('.' in tok and tok.replace('.', '', 1).isdigit())

        result = []
        n = len(tokens)
        for i, token in enumerate(tokens):
            if token == 'and' and i >= 2 and i + 1 < n:
                prev = tokens[i - 1]
                prev_prev = tokens[i - 2]
                # Only remove 'and' when pattern is: digit unit 'and' digit
                # e.g., '1 year and 2 months' → remove; 'next week and 5 days' → keep
                if (prev in self.COMPOUND_UNIT_WORDS
                        and _is_numeric(prev_prev)
                        and _is_numeric(tokens[i + 1])):
                    continue  # skip this compound connector 'and'
            result.append(token)
        return result

    def _strip_trailing_commas(self, tokens: list) -> list:
        """Strip trailing commas from tokens.

        Comma-separated compound expressions like '1 year, 2 months ago' produce
        tokens with attached commas ('year,') after splitting. Stripping them allows
        KB lookup to match 'year' as a keyterm.

        Related GitHub Issue:
            #20 - Gap: compound multi-unit expressions not supported
            https://github.com/craigtrim/fast-parse-time/issues/20
        """
        return [t.rstrip(',') if t.endswith(',') else t for t in tokens]

    def _replace_phrases(self, tokens: list) -> list:
        """Replace multi-token phrases before individual token processing."""
        text = ' '.join(tokens)
        for phrase, replacement in self.PHRASE_REPLACEMENTS:
            text = text.replace(phrase, replacement)
        return text.split()

    def _round_float_tokens(self, tokens: list) -> list:
        """Truncate float tokens to integer strings.

        Converts decimal numeric strings (e.g. '7.2', '22.355') to their
        truncated integer equivalent ('7', '22') so the KB can match them.
        Integer tokens and non-numeric tokens are passed through unchanged.

        Truncation uses int(float()) which discards the fractional part:
            1.5 → '1',  2.9 → '2',  10.75 → '10',  0.5 → '0'

        Related GitHub Issues:
            #15 - Gap: float/decimal cardinalities not supported
            #59 - Support decimal/float cardinalities in relative time expressions
            https://github.com/craigtrim/fast-parse-time/issues/59
        """
        result = []
        for token in tokens:
            if '.' in token:
                try:
                    result.append(str(int(float(token))))
                except ValueError:
                    result.append(token)
            else:
                result.append(token)
        return result

    def _normalize_unit_plurals(self, tokens: list) -> list:
        """Pluralize singular abbreviated units when preceded by N > 1.

        '5 min ago' → '5 mins ago', '3 hr from now' → '3 hrs from now'
        Cardinality-1 forms ('1 min ago') are left unchanged — they have
        their own exact KB entries.
        """
        result = list(tokens)
        for i, token in enumerate(result):
            if token in self.UNIT_SINGULAR_TO_PLURAL and i > 0:
                prev = result[i - 1]
                if prev.isdigit() and int(prev) > 1:
                    result[i] = self.UNIT_SINGULAR_TO_PLURAL[token]
        return result

    def _replace_weekday_refs(self, tokens: list) -> list:
        """Replace named weekday references with computed day offsets.

        'next friday'  → ['5', 'days', 'from', 'now']  (if today is Sunday)
        'last monday'  → ['6', 'days', 'ago']           (if today is Sunday)
        'this friday'  → ['5', 'days', 'from', 'now']
        'coming wed'   → ['3', 'days', 'from', 'now']
        'past tuesday' → ['5', 'days', 'ago']

        Cardinality is always 1-7: the number of days to/from the target weekday.
        """
        if len(tokens) < 2:
            return tokens

        today_wd = date.today().weekday()  # Monday=0, Sunday=6
        result = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token in self.WEEKDAY_NAMES:
                    target_wd = self.WEEKDAY_NAMES[next_token]
                    if token in self.FUTURE_WEEKDAY_PREFIXES:
                        days = (target_wd - today_wd) % 7
                        if days == 0:
                            days = 7  # 'next' always means upcoming, not today
                        result.extend([str(days), 'days', 'from', 'now'])
                        i += 2
                        continue
                    elif token in self.PAST_WEEKDAY_PREFIXES:
                        days = (today_wd - target_wd) % 7
                        if days == 0:
                            days = 7  # 'last' always means most recent past
                        result.extend([str(days), 'days', 'ago'])
                        i += 2
                        continue
            result.append(token)
            i += 1
        return result

    def process(self,
                tokens: list) -> list:
        # Strip trailing commas before any other processing
        # (handles comma-separated compound expressions: '1 year, 2 months ago')
        tokens = self._strip_trailing_commas(tokens)

        # Remove 'and' connectors between compound unit pairs before phrase matching
        # so they don't break sequence extraction: '1 year and 2 months ago'
        tokens = self._remove_compound_and(tokens)

        # First, handle multi-token phrase replacements
        tokens = self._replace_phrases(tokens)

        # Round float tokens to nearest integer before KB lookup
        tokens = self._round_float_tokens(tokens)

        # Replace named weekday references with computed day offsets
        tokens = self._replace_weekday_refs(tokens)

        normalized = []

        for token in tokens:
            # Handle indefinite articles as 1
            if token in self.INDEFINITE_ARTICLES:
                normalized.append('1')
            # Handle informal quantity words
            elif token in self.INFORMAL_QUANTITIES:
                normalized.append(self.INFORMAL_QUANTITIES[token])
            else:
                try:
                    normalized.append(str(w2n.word_to_num(token)))
                except ValueError:
                    normalized.append(token)

        # Normalize singular abbreviated units to plural for N > 1
        normalized = self._normalize_unit_plurals(normalized)

        return normalized
