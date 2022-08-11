from fast_parse_time import transform


def driver(input_text: str):
    result = transform(input_text)
    print(f"Resolved input of \"{input_text}\" into: {result}")


def main(input_text):
    driver(input_text)


if __name__ == "__main__":
    import plac

    plac.call(main)
