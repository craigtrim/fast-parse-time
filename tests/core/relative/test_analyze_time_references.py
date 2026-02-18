"""Tests for AnalyzeTimeReferences service covering relative temporal expressions."""
from fast_parse_time.implicit.svc import AnalyzeTimeReferences
from fast_parse_time.implicit.dto.index_by_slot_kb import Slot

svc = AnalyzeTimeReferences()
assert svc


def test_01():
    input_text = 'from here show me all 5 items all the history from 5 days ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(5, 'day', 'past')]


def test_02():
    input_text = 'the explosion happened 5 minutes ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(5, 'minute', 'past')]


def test_03():
    input_text = 'I want to see my history for the past 30 minutes'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(30, 'minute', 'past')]


def test_04():
    input_text = 'show me all records from the last couple of weeks please'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(2, 'week', 'past')]


def test_05():
    """3 hours ago should resolve to cardinality 3, frame hour, tense past."""
    input_text = 'something happened 3 hours ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(3, 'hour', 'past')]


def test_06():
    """2 months ago should resolve to cardinality 2, frame month, tense past."""
    input_text = 'I signed up 2 months ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(2, 'month', 'past')]


def test_07():
    """last year should resolve to cardinality 1, frame year, tense past."""
    input_text = 'this started last year'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'year', 'past')]


def test_08():
    """yesterday should resolve to cardinality 1, frame day, tense past."""
    input_text = 'I saw that yesterday'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'day', 'past')]


def test_09():
    """next week should resolve to cardinality 1, frame week, tense future."""
    input_text = 'let us meet next week'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'week', 'future')]


def test_10():
    """10 seconds ago should resolve to cardinality 10, frame second, tense past."""
    input_text = 'the alert fired 10 seconds ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(10, 'second', 'past')]


def test_11():
    """last week should resolve to cardinality 1, frame week, tense past."""
    input_text = 'show me everything from last week'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'week', 'past')]


def test_12():
    """1 day ago should resolve to cardinality 1, frame day, tense past."""
    input_text = 'the job ran 1 day ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'day', 'past')]


def test_13():
    """last month should resolve to cardinality 1, frame month, tense past."""
    input_text = 'revenue was down last month'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'month', 'past')]


def test_14():
    """tomorrow should resolve to cardinality 1, frame day, tense future."""
    input_text = 'the deployment is tomorrow'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'day', 'future')]


def test_15():
    """15 minutes ago should resolve to cardinality 15, frame minute, tense past."""
    input_text = 'the server went down 15 minutes ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(15, 'minute', 'past')]


def test_16():
    """a week ago should resolve to cardinality 1, frame week, tense past."""
    input_text = 'we launched a week ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        Slot(1, 'week', 'past')]


def main():
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()
    test_08()
    test_09()
    test_10()
    test_11()
    test_12()
    test_13()
    test_14()
    test_15()
    test_16()


if __name__ == '__main__':
    main()
