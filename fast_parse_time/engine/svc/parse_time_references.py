#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Parse the Time References Spreadsheet """


import os

import pandas as pd

from baseblock import FileIO
from baseblock import BaseObject


class ParseTimeReferences(BaseObject):
    """ Parse the Time References Spreadsheet """

    def __init__(self):
        """ Change Log

        Created:
            11-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _filepath(self) -> str:
        path = os.path.normpath(os.path.join(
            os.getcwd(), 'resources/data/Time References.xlsx'))
        FileIO.exists_or_error(path)

        return path

    def process(self) -> list:

        pd.read_excel(self._filepath())


if __name__ == "__main__":
    ParseTimeReferences().process()
