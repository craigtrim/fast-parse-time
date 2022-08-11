#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Find Time Based Words or References in Text """


from baseblock import BaseObject

from fast_parse_time.dto import d_day_words_kb
from fast_parse_time.dto import d_deitic_words_kb
from fast_parse_time.dto import d_month_words_kb
from fast_parse_time.dto import d_time_words_kb


class FindTimeReference(BaseObject):
    """ Find Time Based Words or References in Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    # def has_candidate_match(self,
    #                         input_text: str) -> bool:
    #     input_text = input_text.lower()

    #     for d in [
    #         d_day_words_kb,
    #         d_deitic_words_kb,
    #         d_month_words_kb,
    #         d_time_words_kb,
    #     ]:
    #         for k in d:
    #             if k in input_text:
    #                 return True

    #     return False

    def find_matches(self,
                     input_text: str) -> list:
        tokens = input_text.lower().strip().split()

        dicts = [
            d_day_words_kb,
            d_deitic_words_kb,
            d_month_words_kb,
            d_time_words_kb,
        ]

        matches = []
        for token in tokens:
            for d in dicts:
                if token in d:
                    matches.append(token)

        return matches
