#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Analyze Time References in Text """


from datetime import datetime


class Singleton(object):

    __analyze = None
    __resolve = None

    def resolve(self) -> object:
        if not self.__resolve:
            from fast_parse_time.svc import ResolveTimeReferences
            self.__resolve = ResolveTimeReferences().process
        return self.__resolve

    def analyze(self) -> object:
        if not self.__analyze:
            from fast_parse_time.svc import AnalyzeTimeReferences
            self.__analyze = AnalyzeTimeReferences().process
        return self.__analyze


s = Singleton()


def transform(input_text: str) -> str:
    current_time = datetime.now()

    d_result = s.analyze()(input_text)
    solutions = d_result['result']

    if solutions and len(solutions):
        return s.resolve()(
            solutions=solutions,
            current_time=current_time)
