from datetime import datetime

from fast_parse_time.svc import ResolveTimeReferences


def execute(current_time: datetime,
            solutions: list) -> datetime:
    svc = ResolveTimeReferences()
    assert svc

    current_time = datetime.now()

    return svc.process(solutions=solutions, current_time=current_time)


def test_01():
    solutions = [{'Cardinality': 5, 'Frame': 'minute', 'Tense': 'past'}]
    execute(datetime.now(), solutions)


def test_02():
    solutions = [
        {'Cardinality': 5, 'Frame': 'minute', 'Tense': 'past'},
        {'Cardinality': 5, 'Frame': 'minute', 'Tense': 'future'}
    ]

    now = datetime.now()
    assert execute(now, solutions) == now


def test_03():
    solutions = [
        {'Cardinality': 1, 'Frame': 'year', 'Tense': 'past'},
        {'Cardinality': 2, 'Frame': 'month', 'Tense': 'past'},
        {'Cardinality': 3, 'Frame': 'week', 'Tense': 'past'},
        {'Cardinality': 4, 'Frame': 'day', 'Tense': 'past'},
        {'Cardinality': 5, 'Frame': 'hour', 'Tense': 'past'},
        {'Cardinality': 6, 'Frame': 'minute', 'Tense': 'past'},
        {'Cardinality': 7, 'Frame': 'second', 'Tense': 'past'},
    ]

    execute(datetime.now(), solutions)


def main():
    test_03()


if __name__ == "__main__":
    main()
