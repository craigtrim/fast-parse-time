#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Classify Date/Time Extracted Comopnents """


from typing import List, Dict, Optional
from baseblock import BaseObject, Enforcer
from fast_parse_time.explicit.dmo import DelimitedDateClassifier
from fast_parse_time.explicit.dto import DateType, date_delims, MIN_YEAR, MAX_YEAR


class ClassifyNumericComponents(BaseObject):
    """ Classify Date/Time Extracted Components """

    __delimited_classifer: DelimitedDateClassifier = None

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _classify_date_type(self,
                            input_text: str) -> Optional[DateType]:

        _date_delims = [
            date_delim for date_delim in date_delims
            if date_delim in input_text
        ]

        if len(_date_delims) >= 2 and self.isEnabledForWarning:
            self.logger.warning(
                f'Unexpected Pattern: Multiple Delimiters Found: {_date_delims} in {input_text}')

        elif len(_date_delims) == 1:
            if not self.__delimited_classifer:
                self.__delimited_classifer = DelimitedDateClassifier()
            return self.__delimited_classifer.process(input_text=input_text, delimiter=_date_delims[0])

        if '-' in input_text:

            def is_valid_year(candidate: str) -> bool:
                try:
                    n = int(candidate)
                    return MIN_YEAR <= n <= MAX_YEAR
                except ValueError:
                    pass
                return False

            input_tokens: List[str] = input_text.split('-')
            input_tokens = [
                is_valid_year(input_token)
                for input_token in input_tokens
            ]

            if len(input_tokens) == 2 and int(input_tokens[0]) < int(input_tokens[1]):
                return DateType.YEAR_RANGE

    def process(self,
                input_tokens: List[str]) -> Optional[Dict[str, DateType]]:

        if self.isEnabledForDebug:
            Enforcer.is_list_of_str(input_tokens)

        d: Dict[str, DateType] = {}
        for input_token in input_tokens:
            date_type = self._classify_date_type(input_token)
            if date_type:
                d[input_token] = date_type.name

        if not d or not len(d):
            return None

        return d
