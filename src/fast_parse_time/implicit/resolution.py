#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Resolve Time Solutions Located in the Text """


from datetime import datetime
from datetime import timedelta
from fast_parse_time.models import RelativeTime

from fast_parse_time._logging import configure_logger
from fast_parse_time._timing import Stopwatch


class ResolveTimeReferences(object):
    """ Resolve Time Solutions Located in the Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        self.logger = configure_logger(__name__)

    @staticmethod
    def _get_timedelta(solution: list) -> timedelta:
        return RelativeTime(
            solution.cardinality, solution.frame, solution.tense
        ).to_timedelta()

    def _process(self,
                 solutions: list,
                 current_time: str) -> list:
        new_time = current_time
        for solution in solutions:
            new_time = new_time + self._get_timedelta(solution)

        return new_time

    def process(self,
                solutions: list,
                current_time: datetime) -> str | None:

        sw = Stopwatch()

        if not solutions or not len(solutions):
            return None

        new_time = self._process(solutions=solutions,
                                 current_time=current_time)

        self.logger.debug('\n'.join([
            'Time Resolution Completd',
            f'\tTotal Time: {str(sw)}',
            f'\tTotal Solutions:  {len(solutions)}',
            f'\tInput Time: {current_time}',
            f'\tOutput Time: {new_time}']))

        return new_time
