#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Tests for indefinite articles (a/an) as cardinality."""

import pytest
from fast_parse_time import parse_time_references

class TestIndefiniteArticleAn:
    """Tests for 'an X ago' patterns."""

    def test_an_hour_ago(self):
        """'an hour ago' should imply cardinality of 1."""
        result = parse_time_references('an hour ago')
        assert len(result) == 1
        assert result[0].cardinality == 1
        assert result[0].frame == 'hour'
        assert result[0].tense == 'past'
