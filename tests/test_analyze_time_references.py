from fast_parse_time.svc import AnalyzeTimeReferences

svc = AnalyzeTimeReferences()
assert svc


def test_01():
    input_text = 'from here show me all 5 items all the history from 5 days ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        {'Cardinality': 5, 'Frame': 'day', 'Tense': 'past'}]


def test_02():
    input_text = 'the explosion happened 5 minutes ago'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        {'Cardinality': 5, 'Frame': 'minute', 'Tense': 'past'}]


def test_03():
    input_text = 'I want to see my history for the past 30 minutes'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        {'Cardinality': 30, 'Frame': 'minute', 'Tense': 'past'}]


def test_04():
    input_text = 'show me all records from the last couple of weeks please'
    d_result = svc.process(input_text)
    assert len(d_result['result']) == 1
    assert d_result['result'] == [
        {'Cardinality': 2, 'Frame': 'week', 'Tense': 'past'}]


def main():
    test_01()
    test_02()
    test_03()
    test_04()


if __name__ == "__main__":
    main()
