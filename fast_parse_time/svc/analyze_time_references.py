#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from baseblock import BaseObject

from natural_time import natural_time


class AnalyzeTimeReferences(BaseObject):
    """ Analyze Time References in Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_text: str) -> list:
        return natural_time(input_text)
