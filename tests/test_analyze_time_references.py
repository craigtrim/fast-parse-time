from fast_parse_time.runtime.svc import AnalyzeTimeReferences


def test_service():

    svc = AnalyzeTimeReferences()
    assert svc

    print(svc.process('the explosion happened 5 minutes ago'))
    print(svc.process('I want to see my history for the past 30 minutes'))


def main():
    test_service()


if __name__ == "__main__":
    main()
