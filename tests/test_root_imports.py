from typing import Callable
from baseblock import Stopwatch

from fast_parse_time import has_time_references
from fast_parse_time import transform


def test_root_imports():

    def wrap_has_time_references(input_text: str) -> None:
        sw = Stopwatch()
        result = has_time_references(input_text)
        print(f"Result in {str(sw)}: {result}")

    def wrap_transform(input_text: str) -> None:
        sw = Stopwatch()
        result = transform(input_text)
        print(f"Result in {str(sw)}: {result}")

    wrap_has_time_references('give me everything for the last 8 hours')
    wrap_has_time_references('the next 24 hours')
    wrap_has_time_references('2 weeks back')
    wrap_has_time_references('14 days ago')

    wrap_transform('give me everything for the last 8 hours')   
    # wrap_transform('the next 24 hours') # TODO: doesn't work; please fix
    wrap_transform('2 weeks back')
    wrap_transform('14 days ago')


def main():
    test_root_imports()


if __name__ == "__main__":
    main()
