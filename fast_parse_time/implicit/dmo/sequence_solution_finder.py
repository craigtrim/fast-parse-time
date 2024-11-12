#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Find Solutions for Sequences """


from fast_parse_time.implicit.dto import d_index_by_keyterm_kb
from fast_parse_time.implicit.dto import d_index_by_slot_kb


class SequenceSolutionFinder(object):
    """ Find Solutions for Sequences """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        pass

    @staticmethod
    def _intersection(list_of_sets: list) -> set:
        master = list_of_sets[0]

        for s in list_of_sets[1:]:
            master = master.intersection(s)

        return master

    def process(self,
                sequences: list) -> list:

        solutions = []
        for sequence in sequences:

            sets = []
            for keyterm in sequence:
                sets.append(set(d_index_by_keyterm_kb[keyterm]))

            candidates = self._intersection(sets)
            if len(candidates) == 1:
                solutions.append(d_index_by_slot_kb[list(candidates)[0]])

        return solutions
