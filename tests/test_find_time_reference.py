from fast_parse_time.svc import FindTimeReference


def test_service():

    svc = FindTimeReference()
    assert svc

    assert svc.find_matches('some mins ago we heard the noise')