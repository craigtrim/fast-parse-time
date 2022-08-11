#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from doctest import master
import token
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

    def _extract_keyword_sequences(self,
                                   tokens: list) -> list:
        """ Extract Keyword Sequences

        This is an extraction and correlation of contiguous time sequences within text

        Args:
            tokens (list): an incoming list of tokens from the user input text

            Example 1:
                Sample Input Text:              "from Joe Smith 5 days ago"
                Sample Keyword Sequence:        [ ['from'], ['5', 'days', 'ago'] ]

            Example 2:           
                Sample Input Text:              "from Joe Smith 4 years and 3 months ago"
                Sample Keyword Sequence:        [ ['from'], ['4', 'years'], ['3', 'months', 'ago'] ],

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

    @staticmethod
    def _intersection(list_of_sets: list) -> set:
        master = list_of_sets[0]

        for s in list_of_sets[1:]:
            master = master.intersection(s)

        return master

    @staticmethod
    def _filter(sequences: list) -> list:
        """ Filter Sequences for Invalid Keys

        Sample Input Text:
            from here show me all 5 items all the history from 5 days ago
        Sample Sequences:
            [   
                ['from'], 
                ['5'], 
                ['from', '5', 'days', 'ago']
            ]
            -   the first two sequences don't exist in 'd_index_by_slot_kb' 
                and can be discarded immediately
            -   the second sequence can be sliced and diced into candidates:
                    [
                        ['from', '5', 'days'],
                        ['5', 'days', 'ago']
                    ]
                and each candidate checked against 'd_index_by_slot_kb' for validity

        Args:
            sequences (list): the incoming sequences

        Returns:
            list: the filtered sequences
        """
        normalized = []

        for sequence in sequences:
            slot = ' '.join(sequence).strip()
            exists = slot in d_index_by_slot_kb

            if exists:
                normalized.append(sequence)
            elif not exists and len(sequence) == 1:
                continue
            elif ' '.join(sequence[1:]) in d_index_by_slot_kb:
                normalized.append(sequence[1:])
            elif ' '.join(sequence[:-1]) in d_index_by_slot_kb:
                normalized.append(sequence[:-1])

        return normalized

    def _process(self,
                 input_text: str) -> list:
        input_text = input_text.lower().strip()
        tokens = input_text.split()

        sequences = self._extract_keyword_sequences(tokens)
        print(sequences)

        sequences = self._filter(sequences)
        print(sequences)

        solutions = []
        for sequence in sequences:

            sets = []
            for keyterm in sequence:
                sets.append(set(d_index_by_keyterm_kb[keyterm]))

            candidates = self._intersection(sets)
            if len(candidates) == 1:
                solutions.append(d_index_by_slot_kb[list(candidates)[0]])

        print (solutions)
        return solutions

    def process(self,
                input_text: str) -> list or None:
        sw = Stopwatch()

        solutions = self._process(input_text)

        if self.isEnabledForDebug:
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
                    f"\tTotal Solutions: {len(solutions)}"]))

        return solutions
