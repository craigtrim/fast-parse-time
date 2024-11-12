#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Resolve Time Solutions Located in the Text """


from datetime import datetime
from datetime import timedelta

from fast_parse_time.core import configure_logger, Stopwatch


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
        x = solution['Cardinality']
        if solution['Tense'] == 'past':
            x *= -1

        if solution['Frame'] == 'year':
            x *= 365
            return timedelta(days=x)

        if solution['Frame'] == 'month':
            x *= 30  # ave. of 30 days/mo
            # if you want to get clever find the current month, then step forward or backward % 12 and get 28,29,30,31 :/
            return timedelta(days=x)

        if solution['Frame'] == 'week':
            x *= 7
            return timedelta(days=x)

        if solution['Frame'] == 'day':
            return timedelta(days=x)

        if solution['Frame'] == 'hour':
            return timedelta(hours=x)

        if solution['Frame'] == 'minute':
            return timedelta(minutes=x)

        if solution['Frame'] == 'second':
            return timedelta(seconds=x)

        raise NotImplementedError(solution['Frame'])

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
