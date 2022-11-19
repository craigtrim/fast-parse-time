from fast_parse_time import transform


def test_transform():

    # transform('the explosion happened 5 minutes ago')
    # transform('5 days ago')
    # transform('from 5 days ago')
    # transform('all the history from 5 days ago')
    transform('from here show me all 5 items all the history from 5 days ago')


def main():
    test_transform()


if __name__ == '__main__':
    main()
