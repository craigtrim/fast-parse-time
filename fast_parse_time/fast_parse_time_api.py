#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" NLP API for Parsing Dates of all Kinds """


from baseblock import BaseObject
from typing import Dict, Optional

from fast_parse_time.explicit.dto import DateType
from fast_parse_time.explicit.bp import ExplicitTimeExtractor


class FastParseTimeAPI(BaseObject):
    """ NLP API for Parsing Dates of all Kinds """

    def __init__(self):
        """ Change Log

        Created:
            5-Apr-2024
            craigtrim@gmail.com
            *   https://github.com/craigtrim/fast-parse-time/issues/1
        """
        BaseObject.__init__(self, __name__)

    def extract_numeric_dates(input_text: str) -> Optional[Dict[str, DateType]]:
        """
        Extracts numeric dates from the given input text.

        Args:
            input_text (str): The input text from which to extract numeric dates.

        Returns:
            Optional[List[str]]: A list of extracted numeric dates, or None if no dates were found.
        """
        return ExplicitTimeExtractor().extract_numeric_dates(input_text=input_text)
