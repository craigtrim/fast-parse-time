#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Filter Sequences for Invalid Keys """


from fast_parse_time.implicit.dto import d_index_by_slot_kb


class KeywordSequenceFilter(object):
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
    """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        pass

    def process(self,
                sequences: list) -> list:
        """ Filter Sequences for Invalid Keys

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
