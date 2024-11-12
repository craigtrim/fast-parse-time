#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from fast_parse_time.implicit.dto import d_keyterm_counter_kb


class KeywordSequenceExtractor(object):
    """ Extract Keyword Sequences

    This is an extraction and correlation of contiguous time sequences within text

    Example 1:
        Sample Input Text:              "from Joe Smith 5 days ago"
        Sample Keyword Sequence:        [ ['from'], ['5', 'days', 'ago'] ]

    Example 2:
        Sample Input Text:              "from Joe Smith 4 years and 3 months ago"
        Sample Keyword Sequence:        [ ['from'], ['4', 'years'], ['3', 'months', 'ago'] ],
    """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        self._keyterms = set(d_keyterm_counter_kb.keys())

    def process(self,
                tokens: list) -> list:
        """ Extract Keyword Sequences

        Args:
            tokens (list): an incoming list of tokens from the user input text

        Returns:
            list: a list of lists
        """

        master = []

        buffer = []
        for token in tokens:
            if token in self._keyterms:
                buffer.append(token)
            else:
                if len(buffer):
                    master.append(buffer)
                    buffer = []
        if len(buffer):
            master.append(buffer)

        return master
