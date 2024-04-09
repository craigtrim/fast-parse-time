#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Replace Spelled-Out forms of Numbers with their Digits """


from word2number import w2n

from baseblock import BaseObject


class DigitTextReplacer(BaseObject):
    """ Replace Spelled-Out forms of Numbers with their Digits

    e.g., 'three' => 3
    """

    def __init__(self):
        """ Change Log

        Created:
            11-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                tokens: list) -> list:
        normalized = []

        for token in tokens:
            try:
                normalized.append(str(w2n.word_to_num(token)))
            except ValueError:
                normalized.append(token)

        return tokens
