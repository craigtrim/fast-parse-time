#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from typing import Optional
from baseblock import ServiceEventGenerator

from fast_parse_time.core import configure_logger, Stopwatch
from fast_parse_time.implicit.dmo import DigitTextReplacer
from fast_parse_time.implicit.dmo import KeywordSequenceFilter
from fast_parse_time.implicit.dmo import KeywordSequenceExtractor
from fast_parse_time.implicit.dmo import SequenceSolutionFinder


class AnalyzeTimeReferences(object):
    """ Analyze Time References in Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        self.logger = configure_logger(__name__)
        self._generate_event = ServiceEventGenerator().process

        self._digit_replacer = DigitTextReplacer().process
        self._filter_sequences = KeywordSequenceFilter().process
        self._extract_sequences = KeywordSequenceExtractor().process
        self._find_solutions = SequenceSolutionFinder().process

    def _process(self,
                 input_text: str) -> dict:

        tokens = input_text.lower().strip().split()

        tokens = self._digit_replacer(tokens)
        sequences = self._extract_sequences(tokens)
        sequences = self._filter_sequences(sequences)
        solutions = self._find_solutions(sequences)

        return {
            'input_text': input_text,
            'tokens': tokens,
            'sequences': sequences,
            'solutions': solutions
        }

    def process(self,
                input_text: str) -> Optional[list]:
        sw = Stopwatch()

        d_result = self._process(input_text)

        # COR-80; Generate an Event Record
        d_event = self._generate_event(
            service_name=__name__,
            event_name='analyze-time-references',
            stopwatch=sw,
            data=d_result)

        if not d_result['solutions'] or not len(d_result['solutions']):
            self.logger.debug('\n'.join([
                'No Solutions Found',
                f'\tTotal Time: {str(sw)}',
                f'\tInput Text: {input_text}']))

        else:
            self.logger.debug('\n'.join([
                'Time Reference Solutions Found',
                f'\tTotal Time: {str(sw)}',
                f'\tInput Text: {input_text}',
                f"\tTotal Solutions: {len(d_result['solutions'])}"]))

        return {
            'result': d_result['solutions'],
            'events': [d_event]
        }
