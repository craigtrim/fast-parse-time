#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Replace Spelled-Out forms of Numbers with their Digits """


from word2number import w2n


class DigitTextReplacer(object):
    """ Replace Spelled-Out forms of Numbers with their Digits

    e.g., 'three' => 3
    """

    # Indefinite articles that imply cardinality of 1
    INDEFINITE_ARTICLES = {'a', 'an'}

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
        """
        pass

    def process(self,
                tokens: list) -> list:
        normalized = []

        for token in tokens:
            # Handle indefinite articles as 1
            if token in self.INDEFINITE_ARTICLES:
                normalized.append('1')
            else:
                try:
                    normalized.append(str(w2n.word_to_num(token)))
                except ValueError:
                    normalized.append(token)

        return normalized
