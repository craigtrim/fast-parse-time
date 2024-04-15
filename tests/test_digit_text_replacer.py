from fast_parse_time.implicit.dmo import DigitTextReplacer

dmo = DigitTextReplacer()
assert dmo


def test_lib():
    print(dmo.process('here are twenty-three choices and thirty one options'))


def main():
    test_lib()


if __name__ == '__main__':
    main()
