#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Resolve Time Solutions Located in the Text """


from baseblock import BaseObject


class ResolveTimeReferences(BaseObject):
    """ Resolve Time Solutions Located in the Text """

    def __init__(self):
        """ Change Log

        Created:
            10-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                input_text: str,
                current_time: str) -> list:
        pass
