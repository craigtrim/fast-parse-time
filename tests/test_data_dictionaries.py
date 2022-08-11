from baseblock import Enforcer

from fast_parse_time.runtime.dto import d_day_words_kb
from fast_parse_time.runtime.dto import d_deitic_words_kb
from fast_parse_time.runtime.dto import d_month_words_kb
from fast_parse_time.runtime.dto import d_time_words_kb


def test_datatypes():
    Enforcer.is_dict(d_day_words_kb)
    Enforcer.is_dict(d_deitic_words_kb)
    Enforcer.is_dict(d_month_words_kb)
    Enforcer.is_dict(d_time_words_kb)
