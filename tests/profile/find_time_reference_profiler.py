from baseblock import Stopwatch

from fast_parse_time.runtime.svc import FindTimeReference


def has_candidate_match(input_text: str):

    sw = Stopwatch()
    svc = FindTimeReference()
    print(f"Time to Initialize: {str(sw)}")

    sw = Stopwatch()
    results = svc.find_matches(input_text)
    print(f"Time to Find Matches: {str(sw)}: {results}")

    # sw = Stopwatch()
    # results = svc.has_candidate_match(input_text)
    # print(f"Time to Assess Candidates: {str(sw)}: {results}")



def main():
    has_candidate_match('some mins ago we heard the noise')


if __name__ == "__main__":
    main()
