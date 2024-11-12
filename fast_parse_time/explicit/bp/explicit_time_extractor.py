#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" NLP API for Parsing Dates of all Kinds """


from fast_parse_time.core import configure_logger, Stopwatch
from fast_parse_time.explicit.dto import DateType
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
