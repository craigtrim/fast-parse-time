#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" NLP API for Parsing Dates of all Kinds """

import re

from fast_parse_time.core import configure_logger, Stopwatch
from fast_parse_time.explicit.dto import DateType, MONTH_NAMES, MIN_YEAR, MAX_YEAR
from fast_parse_time.explicit.dmo.stdlib_date_validator import try_parse_date
from fast_parse_time.explicit.svc import (
    PreClassifyNumericComponents,
    TokenizeNumericComponents,
    ClassifyNumericComponents,
    ValidateNumericComponents,
)


class ExplicitTimeExtractor(object):
    """ NLP API for Parsing Dates of all Kinds """

    __preclassify_numeric: PreClassifyNumericComponents = None
    __tokenize_numeric: TokenizeNumericComponents = None
    __classify_numeric: ClassifyNumericComponents = None
    __validate_numeric: ValidateNumericComponents = None

    def __init__(self):
        """ Change Log

        Created:
            5-Apr-2024
            craigtrim@gmail.com
            *   https://github.com/craigtrim/fast-parse-time/issues/1
        """
        self.logger = configure_logger(__name__)

    def extract_numeric_dates(self, input_text: str) -> dict[str, DateType]:
        """
        Extracts numeric dates from the given input text.

        Args:
            input_text (str): The input text from which to extract numeric dates.

        Returns:
            Optional[List[str]]: A list of extracted numeric dates, or None if no dates were found.
        """
        sw = Stopwatch()

        if not self.__preclassify_numeric:
            self.__preclassify_numeric = PreClassifyNumericComponents()

        if not self.__preclassify_numeric.process(input_text):
            return None

        if not self.__tokenize_numeric:
            self.__tokenize_numeric = TokenizeNumericComponents()

        date_tokens: list[str] | None = \
            self.__tokenize_numeric.process(input_text)
        if not date_tokens or not len(date_tokens):
            return None

        if not self.__classify_numeric:
            self.__classify_numeric = ClassifyNumericComponents()

        d_classified_dates: dict[str, DateType] | None = \
            self.__classify_numeric.process(date_tokens)

        if not d_classified_dates or not len(d_classified_dates):
            return None

        if not self.__validate_numeric:
            self.__validate_numeric = ValidateNumericComponents()

        d_classified_dates: dict[str, DateType] | None = \
            self.__validate_numeric.process(d_classified_dates)

        if not d_classified_dates or not len(d_classified_dates):
            return None

        self.logger.info(
            f"Date Classification for '{input_text}' is {d_classified_dates} in {str(sw)}")

        return d_classified_dates

    def _has_month_name(self, input_text: str) -> bool:
        """Check if text contains a month name."""
        tokens = re.findall(r'[a-zA-Z]+', input_text.lower())
        return any(token in MONTH_NAMES for token in tokens)

    def _strip_ordinal(self, text: str) -> str:
        """Strip ordinal suffixes (1st -> 1, 2nd -> 2, etc.) and commas."""
        # Remove ordinal suffixes
        text = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', text)
        # Remove commas (Python's date parser doesn't handle "15 March, 2018")
        text = text.replace(',', '')
        return text

    def _extract_date_patterns(self, input_text: str) -> list[str]:
        """Extract potential date patterns from text."""
        # Build month name pattern
        month_pattern = '|'.join(sorted(MONTH_NAMES, key=len, reverse=True))

        # Pattern for: Month Day, Year (e.g., March 15, 2024 or Mar 15th, 2024)
        # Includes optional period after month abbreviation (Aug., Dec., etc.)
        pattern1 = rf'(?i)({month_pattern})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}'

        # Pattern for: Day Month Year (e.g., 15 March 2024 or 15th March, 2024)
        # Includes optional period after month abbreviation (Aug., Dec., etc.)
        # Allow optional comma between month and year
        pattern2 = rf'(?i)\d{{1,2}}(?:st|nd|rd|th)?\s+({month_pattern})\.?,?\s+\d{{4}}'

        matches = []
        for pattern in [pattern1, pattern2]:
            for match in re.finditer(pattern, input_text):
                matches.append(match.group())

        return matches

    def extract_hyphen_month_year(self, input_text: str) -> dict[str, DateType]:
        """
        Extract hyphen-delimited month-year patterns from text.

        Handles forward and reversed forms for abbreviated and full month names,
        with both 2-digit and 4-digit years:

        - Forward  (→ MONTH_YEAR): Oct-23, Oct-2023, October-23, October-2023
        - Reversed (→ YEAR_MONTH): 23-Oct, 2023-Oct, 23-October, 2023-October

        Matching is case-insensitive. 2-digit years are accepted as-is.
        4-digit years must fall within MIN_YEAR–MAX_YEAR.

        Args:
            input_text (str): The input text to search.

        Returns:
            dict: Mapping of matched date strings to DateType names, or None.

        Related GitHub Issue:
            #21 - Gap: abbreviated month-year format not supported (Oct-23, May-23)
            https://github.com/craigtrim/fast-parse-time/issues/21
        """
        if not input_text or not isinstance(input_text, str):
            return None

        month_pattern = '|'.join(sorted(MONTH_NAMES, key=len, reverse=True))

        # Forward: MonthName-Year  →  MONTH_YEAR
        # Includes optional period after month abbreviation (Aug., Dec., etc.)
        pattern_forward = rf'(?i)\b({month_pattern})\.?-(\d{{4}}|\d{{2}})\b'
        # Reversed: Year-MonthName  →  YEAR_MONTH
        # Includes optional period after month abbreviation (Aug., Dec., etc.)
        pattern_reversed = rf'(?i)\b(\d{{4}}|\d{{2}})-({month_pattern})\.?\b'

        def _valid_year(raw: str) -> bool:
            n = int(raw)
            if len(raw) == 2:
                return True  # all 2-digit years accepted (interpreted as 2000+YY)
            return MIN_YEAR <= n <= MAX_YEAR

        result = {}

        for match in re.finditer(pattern_forward, input_text):
            year_tok = match.group(2)
            if _valid_year(year_tok):
                result[match.group()] = DateType.MONTH_YEAR.name

        for match in re.finditer(pattern_reversed, input_text):
            year_tok = match.group(1)
            if _valid_year(year_tok):
                result[match.group()] = DateType.YEAR_MONTH.name

        return result if result else None

    def extract_prose_year(self, input_text: str) -> dict[str, DateType]:
        """
        Extract year references preceded by temporal prepositions and year ranges.

        Part A — YEAR_ONLY: Recognises preposition + 4-digit-year patterns such as:
            'in 2004', 'since 2019', 'by 2024', 'until 2030', 'before 2004',
            'after 2004', 'during 2020', 'circa 2004', 'around 2019', 'from 2019',
            'through 2019', 'as of 2004', 'back to 1998', 'prior to 2010'.

        Part B — YEAR_RANGE: Recognises prose year-range patterns such as:
            'from 2004 to 2008', 'from 2004 through 2008',
            'between 2010 and 2020', '2014 to 2015', '2025-26'.

        Year validity: 4-digit years are accepted only within MIN_YEAR–MAX_YEAR.
        Abbreviated second year (YYYY-YY) uses century-rollover logic.

        Args:
            input_text (str): The input text to search.

        Returns:
            dict: Mapping of matched tokens to DateType names, or None.

        Related GitHub Issues:
            #24 - Gap: year-only references not extracted from prose (in 2004, in 2008)
            https://github.com/craigtrim/fast-parse-time/issues/24
            #40 - feat: Parse year-range expressions (e.g., 2014-2015)
            https://github.com/craigtrim/fast-parse-time/issues/40
        """
        if not input_text or not isinstance(input_text, str):
            return None

        def _valid_year(raw: str) -> bool:
            try:
                n = int(raw)
                return MIN_YEAR <= n <= MAX_YEAR
            except ValueError:
                return False

        result = {}

        # ── Part B: prose year-range patterns (run first to avoid double-counting) ──

        # "YYYY-YYYY" hyphen form (e.g., 2014-2015)
        # The numeric tokenizer rejects single-hyphen tokens, so we detect here.
        for match in re.finditer(r'\b(\d{4})-(\d{4})\b', input_text):
            y1, y2 = match.group(1), match.group(2)
            if _valid_year(y1) and _valid_year(y2) and int(y1) < int(y2):
                result[match.group()] = DateType.YEAR_RANGE.name

        # "from YYYY to YYYY" / "from YYYY through YYYY"
        pattern_from_to = r'(?i)\bfrom\s+(\d{4})\s+(?:to|through)\s+(\d{4})\b'
        for match in re.finditer(pattern_from_to, input_text):
            y1, y2 = match.group(1), match.group(2)
            if _valid_year(y1) and _valid_year(y2) and int(y1) < int(y2):
                result[f'{y1}-{y2}'] = DateType.YEAR_RANGE.name

        # "between YYYY and YYYY"
        pattern_between = r'(?i)\bbetween\s+(\d{4})\s+and\s+(\d{4})\b'
        for match in re.finditer(pattern_between, input_text):
            y1, y2 = match.group(1), match.group(2)
            if _valid_year(y1) and _valid_year(y2) and int(y1) < int(y2):
                result[f'{y1}-{y2}'] = DateType.YEAR_RANGE.name

        # "YYYY to YYYY" (bare, without "from") — e.g., "2014 to 2015"
        pattern_bare_to = r'(?i)\b(\d{4})\s+to\s+(\d{4})\b'
        for match in re.finditer(pattern_bare_to, input_text):
            y1, y2 = match.group(1), match.group(2)
            if _valid_year(y1) and _valid_year(y2) and int(y1) < int(y2):
                result[f'{y1}-{y2}'] = DateType.YEAR_RANGE.name

        # "YYYY-YY" abbreviated second year — e.g., "2025-26", "1999-00"
        # Uses century-rollover: 1999-00 → 1900+0=1900 ≤ 1999 → add 100 → 2000
        #
        # Guard 1: if the 2-digit component is a valid calendar month (01–12) the
        # token is a YYYY-MM partial ISO 8601 date, NOT a year range.  We skip it
        # here so the ISO 8601 extractor can classify it correctly.
        #
        # Related GitHub Issue:
        #     #52 - Bug: YYYY-MM falsely matched as YEAR_RANGE for years <= 2000
        #     https://github.com/craigtrim/fast-parse-time/issues/52
        #
        # Guard 2: if the match appears within a written-month date range context
        # (e.g., "31 Oct 2021 - 28 Nov 2021" → "2021-28"), skip it to avoid false
        # positives. Check for month names before the year and after the 2-digit part.
        #
        # Related GitHub Issue:
        #     #61 - False positive: written-month date range with hyphen triggers spurious YEAR_RANGE
        #     https://github.com/craigtrim/fast-parse-time/issues/61
        pattern_abbrev = r'\b(\d{4})-(\d{2})\b'
        for match in re.finditer(pattern_abbrev, input_text):
            y1_full = int(match.group(1))
            y2_abbrev = int(match.group(2))

            # Guard 1: Skip valid month values (01–12): those are YYYY-MM, not YYYY-YY
            if 1 <= y2_abbrev <= 12:
                continue

            # Guard 2: Check if this match is part of a written-month date range
            # Pattern: "D Month YYYY - D Month YYYY" → after normalization → "D Month YYYY-D"
            # We look for month names within a reasonable window before and after the match
            match_start = match.start()
            match_end = match.end()

            # Look back ~20 chars for a month name before the year
            # (allows for "day + month + space" like "31 Oct 2021")
            lookback_start = max(0, match_start - 20)
            lookback_text = input_text[lookback_start:match_start].lower()

            # Look forward ~20 chars for a month name after the 2-digit part
            # (allows for "space + month" like "28 Nov")
            lookforward_end = min(len(input_text), match_end + 20)
            lookforward_text = input_text[match_end:lookforward_end].lower()

            # Import month names from dto
            from fast_parse_time.explicit.dto import MONTH_NAMES

            # Check if any month name appears in the context
            has_month_before = any(month in lookback_text for month in MONTH_NAMES)
            has_month_after = any(month in lookforward_text for month in MONTH_NAMES)

            # If both month names are present, this is likely a false positive
            if has_month_before and has_month_after:
                continue

            century = (y1_full // 100) * 100
            y2_full = century + y2_abbrev
            if y2_full <= y1_full:
                y2_full += 100  # century rollover (e.g., 1999-00 → 2000)
            if (MIN_YEAR <= y1_full <= MAX_YEAR
                    and MIN_YEAR <= y2_full <= MAX_YEAR
                    and y1_full < y2_full):
                result[match.group()] = DateType.YEAR_RANGE.name

        # ── Part A: preposition-preceded single year → YEAR_ONLY ──

        # Multi-word prepositions (must come before single-word to avoid partial matches)
        multi_word_preps = [
            r'as\s+of',
            r'back\s+to',
            r'prior\s+to',
        ]
        single_word_preps = [
            'in', 'since', 'by', 'until', 'before', 'after',
            'during', 'circa', 'around', 'from', 'through',
        ]

        all_preps = multi_word_preps + [re.escape(p) for p in single_word_preps]
        prep_pattern = '|'.join(all_preps)
        pattern_year_only = rf'(?i)\b(?:{prep_pattern})\s+(\d{{4}})\b'

        for match in re.finditer(pattern_year_only, input_text):
            year = match.group(1)
            if _valid_year(year):
                # Skip if this year is already part of a YEAR_RANGE key
                already_in_range = any(
                    year in k for k in result if result[k] == DateType.YEAR_RANGE.name
                )
                if not already_in_range:
                    result[year] = DateType.YEAR_ONLY.name

        return result if result else None

    def extract_iso8601_dates(self, input_text: str) -> dict[str, DateType]:
        """
        Extract date portions from ISO 8601 datetime strings.

        Handles all standard ISO 8601 / RFC 3339 datetime formats:
        - YYYY-MM-DDThh:mm:ssZ
        - YYYY-MM-DDThh:mm:ss+HH:MM
        - YYYY-MM-DDThh:mm:ss-HH:MM
        - YYYY-MM-DDThh:mm:ss.NNNZ  (dot-decimal fractional seconds)
        - YYYY-MM-DDThh:mm:ss,NNNZ  (comma-decimal fractional seconds)

        Only the date component (YYYY-MM-DD) is extracted and returned.
        The time, timezone, and fractional-second portions are discarded.

        Args:
            input_text (str): The input text to search.

        Returns:
            dict: Mapping of 'YYYY-MM-DD' strings to 'FULL_EXPLICIT_DATE', or None.

        Related GitHub Issue:
            #23 - Gap: ISO 8601 datetime strings not extracted
            https://github.com/craigtrim/fast-parse-time/issues/23
        """
        if not input_text or not isinstance(input_text, str):
            return None

        _ISO_8601 = re.compile(
            r'\b(\d{4}-\d{2}-\d{2})'   # date: YYYY-MM-DD
            r'T\d{2}:\d{2}:\d{2}'      # time: Thh:mm:ss
            r'(?:[.,]\d+)?'             # optional fractional seconds (. or ,)
            r'(?:Z|[+-]\d{2}:\d{2})\b' # timezone: Z or ±HH:MM
        )

        matches = _ISO_8601.findall(input_text)
        if not matches:
            return None

        return {date: DateType.FULL_EXPLICIT_DATE.name for date in matches}

    def extract_ordinal_dates(self, input_text: str) -> dict[str, DateType]:
        """
        Extract dates that use ordinal day references (1st, 2nd, 3rd, 4th … 31st).

        Handles four pattern families:

        1. ``NNth day of Month[,] [YYYY]``
           e.g. ``12th day of December, 2001``, ``3rd day of March``

        2. ``[the] NNth of Month [YYYY]``
           e.g. ``the 12th of December``, ``2nd of February 2023``

        3. ``Month NNth`` (no year)
           e.g. ``December 12th``, ``Dec 12th``, ``Oct 23rd``

        4. ``NNth Month`` (no year)
           e.g. ``3rd March``, ``1st Jan``, ``25th December``

        Classification:
        - Pattern includes a 4-digit year → ``FULL_EXPLICIT_DATE``
        - Pattern has no year → ``DAY_MONTH``

        Matching is case-insensitive.  All ordinal suffixes (st/nd/rd/th) are accepted.
        Day values outside 1–31 are silently ignored.

        Args:
            input_text (str): The input text to search.

        Returns:
            dict: Mapping of matched strings to DateType names, or None.

        Related GitHub Issue:
            #22 - Gap: ordinal day format not supported (12th day of December, 19th day of May)
            https://github.com/craigtrim/fast-parse-time/issues/22
        """
        if not input_text or not isinstance(input_text, str):
            return None

        month_pat = '|'.join(sorted(MONTH_NAMES, key=len, reverse=True))

        def _valid_day(s: str) -> bool:
            return 1 <= int(s) <= 31

        def _valid_year(s: str) -> bool:
            try:
                return MIN_YEAR <= int(s) <= MAX_YEAR
            except ValueError:
                return False

        result = {}

        # ── Pattern 1: NNth day of Month[,] [YYYY] ───────────────────────────
        # Only match if a 4-digit year is present (strict mode).
        # Without a year, this is not a parseable, actionable date.
        #
        # Related GitHub Issue:
        #     #63 - False positive: '19th day of May' (no year) returns DAY_MONTH
        #     https://github.com/craigtrim/fast-parse-time/issues/63
        pat1 = re.compile(
            r'\b(\d{1,2})(?:st|nd|rd|th)\s+day\s+of\s+'
            r'(' + month_pat + r')\.?'
            r'(?:,?\s+(\d{4}))?',
            re.IGNORECASE,
        )
        for m in pat1.finditer(input_text):
            day, year = m.group(1), m.group(3)
            if not _valid_day(day):
                continue
            # Require year component — skip matches without year
            if year and _valid_year(year):
                result[m.group()] = DateType.FULL_EXPLICIT_DATE.name

        # ── Pattern 2: [the] NNth of Month [YYYY] ────────────────────────────
        # Unlike Pattern 1, "the Nth of Month" without year returns DAY_MONTH.
        # Only "Nth day of Month" requires year (strict mode per #63).
        pat2 = re.compile(
            r'(?:the\s+)?(\d{1,2})(?:st|nd|rd|th)\s+of\s+'
            r'(' + month_pat + r')\.?'
            r'(?:\s+(\d{4}))?\b',
            re.IGNORECASE,
        )
        for m in pat2.finditer(input_text):
            day, year = m.group(1), m.group(3)
            if not _valid_day(day):
                continue
            if year and _valid_year(year):
                result[m.group()] = DateType.FULL_EXPLICIT_DATE.name
            else:
                result[m.group()] = DateType.DAY_MONTH.name

        # ── Pattern 3: Month NNth (no year) ──────────────────────────────────
        # Negative lookahead prevents matching when a 4-digit year follows
        # (those are handled by the existing extract_written_dates pipeline).
        pat3 = re.compile(
            r'\b(' + month_pat + r')\.?\s+(\d{1,2})(?:st|nd|rd|th)\b'
            r'(?!\s*,?\s*\d{4})',
            re.IGNORECASE,
        )
        for m in pat3.finditer(input_text):
            day = m.group(2)
            if not _valid_day(day):
                continue
            result[m.group()] = DateType.DAY_MONTH.name

        # ── Pattern 4: NNth Month (no year) ──────────────────────────────────
        # Negative lookahead prevents matching when a 4-digit year follows.
        # Handles both "15th March 2018" and "15th March, 2018" (with comma).
        # "of" before the month is excluded (those are patterns 1/2).
        pat4 = re.compile(
            r'\b(\d{1,2})(?:st|nd|rd|th)\s+(' + month_pat + r')\.?\b'
            r'(?!,?\s*\d{4})',
            re.IGNORECASE,
        )
        for m in pat4.finditer(input_text):
            day = m.group(1)
            if not _valid_day(day):
                continue
            # Skip if the ordinal is part of 'NNth of Month' (pattern 2)
            # by checking whether 'of' immediately precedes the month token.
            before_match = input_text[:m.start(2)].rstrip()
            if re.search(r'\bof\s*$', before_match, re.IGNORECASE):
                continue
            # Skip if 'day of' precedes (pattern 1 territory)
            if re.search(r'\bday\s+of\s*$', before_match, re.IGNORECASE):
                continue
            result[m.group()] = DateType.DAY_MONTH.name

        return result if result else None

    def extract_written_dates(self, input_text: str) -> dict[str, DateType]:
        """
        Extract dates with written month names (e.g., 'March 15, 2024').

        Args:
            input_text (str): The input text from which to extract written dates.

        Returns:
            dict: Dictionary mapping date strings to DateType, or None if no dates found.
        """
        sw = Stopwatch()

        if not self._has_month_name(input_text):
            return None

        # Try to extract date patterns from text
        date_matches = self._extract_date_patterns(input_text)

        if date_matches:
            # Found explicit date patterns
            result = {}
            for date_str in date_matches:
                normalized = self._strip_ordinal(date_str)
                if try_parse_date(normalized):
                    result[date_str] = DateType.FULL_EXPLICIT_DATE.name

            if result:
                self.logger.info(
                    f"Written Date Classification for '{input_text}' is {result} in {str(sw)}")
                return result

        # Fallback: try parsing the whole text (for simple cases like "March 15, 2024")
        normalized_text = self._strip_ordinal(input_text)
        if not try_parse_date(normalized_text):
            return None

        # Determine if this is a full date or partial
        tokens = [re.sub(r'[,.]', '', t) for t in input_text.split()]
        has_year = any(t.isdigit() and len(t) == 4 for t in tokens)
        has_day = any(
            re.match(r'\d{1,2}(st|nd|rd|th)?$', t)
            for t in tokens
        )

        if has_year and has_day:
            date_type = DateType.FULL_EXPLICIT_DATE
        elif has_year:
            date_type = DateType.MONTH_YEAR
        elif has_day:
            date_type = DateType.DAY_MONTH
        else:
            return None

        result = {input_text: date_type.name}

        self.logger.info(
            f"Written Date Classification for '{input_text}' is {result} in {str(sw)}")

        return result

    def extract_space_month_number(self, input_text: str) -> dict[str, str]:
        """
        Extract space-delimited MonthName + 2-digit-number patterns from text.

        Classifies based on available evidence, in priority order:

        1. NN > 31 → ``MONTH_YEAR`` (impossible calendar day, must be year)
        2. Preposition "in" → ``MONTH_YEAR`` ("in" signals a time period, not a day)
        3. Preposition "on" → ``DAY_MONTH`` ("on" signals a specific calendar day)
        4. No context, NN ≤ 31 → ``DAY_MONTH_AMBIGUOUS``

        2-digit years are accepted as-is (interpreted as 2000+NN by callers).
        4-digit years are handled by the existing ``extract_written_dates`` pipeline
        and are intentionally excluded here (pattern requires exactly 2-digit NN).

        Matching is case-insensitive for both month names and prepositions.

        Args:
            input_text (str): The input text to search.

        Returns:
            dict: Mapping of matched date strings to DateType names, or None.

        Examples:
            >>> extractor.extract_space_month_number('Oct 99')
            {'Oct 99': 'MONTH_YEAR'}
            >>> extractor.extract_space_month_number('in Oct 23')
            {'Oct 23': 'MONTH_YEAR'}
            >>> extractor.extract_space_month_number('on Oct 23')
            {'Oct 23': 'DAY_MONTH'}
            >>> extractor.extract_space_month_number('Oct 23')
            {'Oct 23': 'DAY_MONTH_AMBIGUOUS'}

        Related GitHub Issue:
            #38 - Gap: space-delimited MonthName+2-digit-number not classified
            https://github.com/craigtrim/fast-parse-time/issues/38
        """
        if not input_text or not isinstance(input_text, str):
            return None

        # Build month-name alternation, longest-first to avoid partial matches
        month_pattern = '|'.join(sorted(MONTH_NAMES, key=len, reverse=True))

        # Match optional preposition + MonthName + exactly 2-digit number.
        # Negative lookahead 1: exclude more digits (NN must be exactly 2 digits).
        # Negative lookahead 2: exclude ordinal suffixes (st/nd/rd/th) — those are
        #   handled by extract_ordinal_dates() and extract_written_dates().
        # Negative lookahead 3: exclude cases where NN is followed by optional
        #   comma/space and a 4-digit year — e.g. "March 15, 2024" must not also
        #   yield a spurious "March 15" hit.
        pattern = (
            rf'(?i)'
            rf'(?:(?P<prep>in|on)\s+)?'
            rf'(?P<month>{month_pattern})\s+'
            rf'(?P<nn>\d{{2}})'
            rf'(?!\d)'           # not followed by more digits
            rf'(?!(?:st|nd|rd|th))'  # not followed by ordinal suffix
            rf'(?!,?\s*\d{{4}})'     # not followed by (optional comma +) 4-digit year
        )

        result = {}

        for match in re.finditer(pattern, input_text):
            prep = (match.group('prep') or '').lower()
            month_tok = match.group('month')
            nn_tok = match.group('nn')
            nn = int(nn_tok)

            matched_text = f'{month_tok} {nn_tok}'

            # Priority 1: NN > 31 → unambiguously a year
            if nn > 31:
                result[matched_text] = DateType.MONTH_YEAR.name
            # Priority 2: preposition "in" → year context
            elif prep == 'in':
                result[matched_text] = DateType.MONTH_YEAR.name
            # Priority 3: preposition "on" → day context
            elif prep == 'on':
                result[matched_text] = DateType.DAY_MONTH.name
            # Priority 4: no context → ambiguous
            else:
                result[matched_text] = DateType.DAY_MONTH_AMBIGUOUS.name

        return result if result else None
