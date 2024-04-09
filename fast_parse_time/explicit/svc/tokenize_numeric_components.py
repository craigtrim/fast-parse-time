#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Elements in Text that are Date-Related """


from typing import List, Optional
from baseblock import BaseObject, Enforcer
from fast_parse_time.explicit.dto import date_delims, MIN_YEAR, MAX_YEAR


class TokenizeNumericComponents(BaseObject):
    """ Extract Elements in Text that are Date-Related """

    def __init__(self):
        """ Change Log

        Created:
            8-Apr-2024
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _is_valid_token(self, input_token: str) -> bool:
        """
        Checks if the input token is a valid numeric token.

        Args:
            input_token (str): The input token to be checked.

        Returns:
            bool: True if the input token is a valid numeric token, False otherwise.
        """
        try:
            n = int(input_token)

            # could be month-of-year or day-of-month
            if n >= 1 and n <= 31:
                return True

            # e.g., a range of viable years (given 2024, range is 1924 - 2034)
            if MIN_YEAR <= n <= MAX_YEAR:
                return True

        except ValueError:
            pass

        return False

    def _is_valid_tokens(self,
                         date_delim: str,
                         input_token: str) -> bool:
        """
        Checks if all tokens in the input string are valid.

        Args:
            date_delim (str): The delimiter used to split the input string into tokens.
            input_token (str): The input string to be checked.

        Returns:
            bool: True if all tokens are valid, False otherwise.
        """

        # I'm assuming that `4.5` and `4-5` are not valid partial date ranges, but 4/5 is
        if input_token.count(date_delim) == 1 and date_delim != '/':
            return False

        input_tokens = input_token.split(date_delim)

        return sum([
            self._is_valid_token(token)
            for token in input_tokens
        ]) == len(input_tokens)

    def process(self,
                input_text: str) -> Optional[List[str]]:
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

        # preserve input ordering, so avoid sets
        values: List[str] = []

        for input_token in input_tokens:

            # preserve input ordering, but avoid duplicates
            if input_token in values:
                continue

            def has_delimited_value() -> bool:
                for date_delim in [
                    date_delim_value for date_delim_value in date_delims
                    if date_delim_value in input_token
                ]:
                    if self._is_valid_tokens(
                            date_delim=date_delim, input_token=input_token):
                        return True

                return False

            if has_delimited_value():
                values.append(input_token)

            elif self._is_valid_token(input_token):
                values.append(input_token)

        if values and len(values):
            return list(values)

        return None
