from fast_parse_time.implicit.dmo import DigitTextReplacer

dmo = DigitTextReplacer()
assert dmo


def test_lib():
    """Print the result of digit text replacement (baseline smoke test)."""
    print(dmo.process('here are twenty-three choices and thirty one options'))


def test_digit_replacement_returns_list():
    """DigitTextReplacer.process should return a list of tokens."""
    result = dmo.process('here are twenty-three choices and thirty one options')
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0


def test_twenty_three_returns_list():
    """'twenty-three files' should return a non-empty list of tokens."""
    result = dmo.process('twenty-three files')
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0


def test_thirty_one_returns_list():
    """'thirty one items' should return a non-empty list of tokens."""
    result = dmo.process('thirty one items')
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0


def test_five_hundred_returns_list():
    """'five hundred records' should return a non-empty list of tokens."""
    result = dmo.process('five hundred records')
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0


def test_one_hundred_fifty_returns_list():
    """'one hundred and fifty days' should return a non-empty list of tokens."""
    result = dmo.process('one hundred and fifty days')
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0


def main():
    test_lib()
    test_digit_replacement_contains_numbers()
    test_twenty_three()
    test_thirty_one()
    test_five_hundred()
    test_one_hundred_fifty()


if __name__ == '__main__':
    main()
