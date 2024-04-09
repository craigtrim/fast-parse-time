#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Pre-Classify Text for Explicit Dates """


from typing import List
from baseblock import BaseObject, Enforcer
from fast_parse_time.explicit.dto import date_delims


class PreClassifyNumericComponents(BaseObject):
    """ Pre-Classify Text for Explicit Dates

    This Component won't classify the specific type of explicit date in the text
    but will determine if an explicit date is likely to exist in the text
    """

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_text: str) -> bool:
        """
        Process the input text and check if it contains any numeric components.

        Args:
            input_text (str): The input text to be processed.

        Returns:
            bool: True if the input text contains numeric components, False otherwise.
        """
        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        input_tokens: List[str] = input_text.split()
        for input_token in input_tokens:

            for date_delim in date_delims:
                if date_delim in input_token:
                    if sum([
                        token.isnumeric() for token in input_token.split(date_delim)
                    ]):
                        return True

            if input_token.isnumeric():
                return True

        return False
