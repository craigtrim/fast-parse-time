#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" NLP API for Parsing Dates of all Kinds """

import re
import dateparser

from fast_parse_time.core import configure_logger, Stopwatch
from fast_parse_time.explicit.dto import DateType, MONTH_NAMES
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
        """Strip ordinal suffixes (1st -> 1, 2nd -> 2, etc.)."""
        return re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', text)

    def _extract_date_patterns(self, input_text: str) -> list[str]:
        """Extract potential date patterns from text."""
        # Build month name pattern
        month_pattern = '|'.join(sorted(MONTH_NAMES, key=len, reverse=True))

        # Pattern for: Month Day, Year (e.g., March 15, 2024 or Mar 15th, 2024)
        pattern1 = rf'(?i)({month_pattern})\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}'

        # Pattern for: Day Month Year (e.g., 15 March 2024 or 15th March 2024)
        pattern2 = rf'(?i)\d{{1,2}}(?:st|nd|rd|th)?\s+({month_pattern})\s+\d{{4}}'

        matches = []
        for pattern in [pattern1, pattern2]:
            for match in re.finditer(pattern, input_text):
                matches.append(match.group())

        return matches

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
                # Verify with dateparser
                normalized = self._strip_ordinal(date_str)
                if dateparser.parse(normalized):
                    result[date_str] = DateType.FULL_EXPLICIT_DATE.name

            if result:
                self.logger.info(
                    f"Written Date Classification for '{input_text}' is {result} in {str(sw)}")
                return result

        # Fallback: try parsing the whole text (for simple cases like "March 15, 2024")
        normalized_text = self._strip_ordinal(input_text)
        parsed = dateparser.parse(normalized_text)
        if not parsed:
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
