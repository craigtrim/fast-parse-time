#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" NLP API for Parsing Dates of all Kinds """


from typing import List, Dict, Optional
from baseblock import BaseObject, Stopwatch

from fast_parse_time.explicit.dto import DateType
from fast_parse_time.explicit.svc import (
    PreClassifyNumericComponents,
    TokenizeNumericComponents,
    ClassifyNumericComponents,
)


class ExplicitTimeExtractor(BaseObject):
    """ NLP API for Parsing Dates of all Kinds """

    __preclassify_numeric: PreClassifyNumericComponents = None
    __tokenize_numeric: TokenizeNumericComponents = None
    __classify_numeric: ClassifyNumericComponents = None

    def __init__(self):
        """ Change Log

        Created:
            5-Apr-2024
            craigtrim@gmail.com
            *   https://github.com/craigtrim/fast-parse-time/issues/1
        """
        BaseObject.__init__(self, __name__)

    def extract_numeric_dates(self, input_text: str) -> Dict[str, DateType]:
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

        date_tokens: Optional[
            List[str]
        ] = self.__tokenize_numeric.process(input_text)
        if not date_tokens or not len(date_tokens):
            return None

        if not self.__classify_numeric:
            self.__classify_numeric = ClassifyNumericComponents()

        d_classified_dates: Optional[
            Dict[str, DateType]
        ] = self.__classify_numeric.process(date_tokens)

        if not d_classified_dates or not len(d_classified_dates):
            return None

        if self.isEnabledForInfo:
            self.logger.info(
                f'Date Classification Completed in {str(sw)} for {input_text} with {d_classified_dates}')

        return d_classified_dates
