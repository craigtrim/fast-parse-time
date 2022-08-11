#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from datetime import datetime

from fast_parse_time.svc import ResolveTimeReferences
from fast_parse_time.svc import AnalyzeTimeReferences

# class Singleton(object):

#     __analyze = None
#     __find_matches = None

#     def find_matches(self) -> object:
#         if not self.__find_matches:
#             from fast_parse_time.svc import FindTimeReference
#             self.__find_matches = FindTimeReference().find_matches
#         return self.__find_matches

#     def analyze(self) -> object:
#         if not self.__analyze:
#             from fast_parse_time.svc import AnalyzeTimeReferences
#             self.__analyze = AnalyzeTimeReferences().process
#         return self.__analyze


# s = Singleton()


def transform(input_text: str) -> str:
    current_time = datetime.now()
    solutions = AnalyzeTimeReferences().process(input_text)
    if solutions and len(solutions):
        return ResolveTimeReferences().process(
            solutions=solutions,
            current_time=current_time)
