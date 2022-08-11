#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """

from fast_parse_time.runtime.svc import FindTimeReference
from fast_parse_time.runtime.svc import AnalyzeTimeReferences

# class Singleton(object):

#     __analyze = None
#     __find_matches = None

#     def find_matches(self) -> object:
#         if not self.__find_matches:
#             from fast_parse_time.runtime.svc import FindTimeReference
#             self.__find_matches = FindTimeReference().find_matches
#         return self.__find_matches

#     def analyze(self) -> object:
#         if not self.__analyze:
#             from fast_parse_time.runtime.svc import AnalyzeTimeReferences
#             self.__analyze = AnalyzeTimeReferences().process
#         return self.__analyze


# s = Singleton()


def has_time_references(input_text: str) -> bool:
    return FindTimeReference().find_matches(input_text)


def transform(input_text: str) -> str:
    return AnalyzeTimeReferences().process(input_text)