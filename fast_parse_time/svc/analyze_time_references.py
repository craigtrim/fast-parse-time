#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from baseblock import Stopwatch
from baseblock import BaseObject

from fast_parse_time.dto import d_keyterm_counter_kb
from fast_parse_time.dto import d_index_by_keyterm_kb
from fast_parse_time.dto import d_index_by_slot_kb


class AnalyzeTimeReferences(BaseObject):
    """ Analyze Time References in Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._keyterms = set(d_keyterm_counter_kb.keys())

    def _process(self,
                 input_text: str) -> list:
        input_text = input_text.lower().strip()
        tokens = set(input_text.split())

        token_keyterms = tokens.intersection(self._keyterms)
        if not len(token_keyterms):
            return None

        master = set()
        for token_keyterm in token_keyterms:
            s = set(d_index_by_keyterm_kb[token_keyterm])
            if not len(master):
                master = s
            else:
                master = master.intersection(s)

        solutions = []
        for result in master:
            solutions.append(d_index_by_slot_kb[result])

        return solutions

    def process(self,
                input_text: str) -> list or None:
        sw = Stopwatch()

        solutions = self._process(input_text)

        if not solutions or not len(solutions):
            self.logger.debug('\n'.join([
                "No Solutions Found",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text}"]))

        else:
            self.logger.debug('\n'.join([
                "Time Reference Solutions Found",
                f"\tTotal Time: {str(sw)}",
                f"\tInput Text: {input_text}",
                f"\tSolutions: {solutions}"]))

        return solutions
