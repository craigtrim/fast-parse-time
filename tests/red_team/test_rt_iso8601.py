#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team Test Suite -- ISO 8601 Datetime Strings
================================================
Target function : extract_explicit_dates(text: str) -> Dict[str, str]
Target patterns : 2017-02-03T09:04:08Z, timezone offsets, fractional seconds

Related GitHub Issue:
    #43 https://github.com/craigtrim/fast-parse-time/issues/43

ATTACK SURFACE OVERVIEW
------------------------
ISO 8601 is a rich, layered standard. A naive regex that matches the basic
``YYYY-MM-DDTHH:MM:SSZ`` form may:

  1. Miss legitimate variants: timezone offsets (+05:30), fractional seconds
     (.123 or ,123 per the standard comma-allowed alternative), reduced
     precision forms, and ordinal/week dates.

  2. Over-match look-alikes: ISO 8601 *duration* strings (PT1H30M), ISO 8601
     *interval* strings using slash notation (2024-01-01/2024-03-31),
     version strings (v2024-03T1), and ticket identifiers (ticket-2024-01T).

  3. Break silently on out-of-range field values: month 13, day 0, hour 24,
     and leap-second (60th second) which are defined in some contexts but
     invalid in others.

  4. Fail on Unicode homoglyphs: fullwidth T, fullwidth colon, fullwidth Z,
     or Arabic-Indic digits that are visually identical but byte-different.

Each parametrize section isolates one attack dimension so that a failing test
pinpoints the exact gap.

XFAIL STRATEGY
--------------
All tests carry ``pytestmark = pytest.mark.xfail`` so the suite remains green
while the implementation is incomplete. An unexpected pass (xpass) is a
promotion candidate -- move that case to the canonical test suite once the
behaviour is confirmed intentional and desired.

TRUE POSITIVE TESTS  ->  assert len(result) > 0  (parser must find something)
FALSE POSITIVE TESTS ->  assert len(result) == 0  (parser must find nothing)
BOUNDARY TESTS       ->  xfail; outcome documents current tolerance
UNICODE TESTS        ->  xfail; outcome documents normalisation behaviour
"""

import pytest
from fast_parse_time.api import extract_explicit_dates

# Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43

pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ============================================================================
# SECTION 1 -- TRUE POSITIVES: BASIC UTC (Z suffix)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Core RFC 3339 / ISO 8601 combined datetimes in UTC.
    # Every entry has a valid year, month, day, hour, minute, second and the
    # literal 'Z' suffix indicating UTC (zero-offset). A robust parser must
    # recognise all of these as explicit date references.
    '2024-01-01T00:00:00Z',
    '2024-06-15T12:30:45Z',
    '2024-12-31T23:59:59Z',
    '2017-02-03T09:04:08Z',    # original motivating example from issue #43
    '2000-01-01T00:00:00Z',    # Y2K boundary
    '1999-12-31T23:59:59Z',    # one second before Y2K
    '2020-02-29T12:00:00Z',    # leap day 2020
    '2024-02-29T00:00:00Z',    # leap day 2024
    '2023-03-26T01:00:00Z',    # DST changeover (UTC unaffected, but a real event)
    '2023-10-29T01:00:00Z',    # DST end (UTC still valid)
    '2024-03-15T14:30:00Z',
    '2024-07-04T17:00:00Z',
    '2024-11-28T08:00:00Z',
    '2021-09-11T08:46:00Z',
    '2024-01-15T09:00:00Z',
    '2024-02-14T18:00:00Z',
    '2024-05-01T00:00:00Z',
    '2024-08-31T23:00:00Z',
    '2024-09-30T12:00:00Z',
    '2024-10-31T06:00:00Z',
    '2026-01-01T00:00:00Z',
    '2025-06-30T15:45:00Z',
    '2030-12-31T23:59:59Z',
    '1970-01-01T00:00:00Z',    # Unix epoch
    '2038-01-19T03:14:07Z',    # 32-bit Unix timestamp overflow boundary
    '2001-09-11T12:46:00Z',
    '2004-12-26T00:58:53Z',
    '2011-03-11T05:46:23Z',
    '2019-04-10T21:00:00Z',
    '2022-02-24T04:00:00Z',
    '1926-01-01T00:00:00Z',    # parser min-year boundary (if applicable)
    '2036-12-31T23:59:59Z',    # parser max-year boundary (if applicable)
])
def test_iso_basic_utc_true_positive(text):
    """
    Attack vector: well-formed ISO 8601 datetime strings with UTC ('Z') suffix.

    Why a parser might fail: if the regex only handles the specific example
    '2017-02-03T09:04:08Z' and was hand-crafted rather than generalised, then
    variations in year, month, day, or time component will silently fall through.
    Leap-day entries (2020-02-29, 2024-02-29) are particularly telling: a parser
    that validates the calendar date strictly will reject them if leap-year logic
    is absent; one that does not validate dates at all will accept everything
    including invalid dates like 2023-02-29.

    What failure reveals: the parser does not recognise basic UTC ISO datetimes
    as explicit date references, which is the most fundamental ISO 8601 gap.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 2 -- TRUE POSITIVES: TIMEZONE OFFSETS
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISO 8601 allows numeric timezone offsets in place of 'Z'.
    # The offset is appended directly after the time: +HH:MM or -HH:MM.
    # A parser that only looks for the literal 'Z' character will miss all of
    # these, even though they are equally valid ISO 8601 datetimes.
    '2024-01-01T00:00:00+00:00',    # UTC expressed as numeric offset
    '2024-06-15T12:30:45+01:00',    # British Summer Time
    '2024-03-15T08:00:00+05:30',    # India Standard Time (half-hour offset)
    '2024-07-04T12:00:00+09:30',    # Australia Central Standard Time
    '2024-11-01T07:00:00+14:00',    # Line Islands -- extreme eastern offset
    '2024-01-15T10:00:00-05:00',    # Eastern Standard Time
    '2024-06-20T09:00:00-07:00',    # Mountain Daylight Time
    '2024-08-15T11:30:00-08:00',    # Pacific Standard Time
    '2024-02-29T00:00:00-12:00',    # extreme western offset (Baker Island)
    '2017-02-03T09:04:08+00:00',    # motivating example with numeric UTC offset
    '2017-02-03T09:04:08+05:30',    # motivating example with India offset
    '2017-02-03T09:04:08-05:00',    # motivating example with US Eastern offset
    '2024-01-01T00:00:00+02:00',
    '2024-01-01T00:00:00+03:00',
    '2024-01-01T00:00:00+04:00',
    '2024-01-01T00:00:00+06:00',
    '2024-01-01T00:00:00+07:00',
    '2024-01-01T00:00:00+08:00',
    '2024-01-01T00:00:00+09:00',
    '2024-01-01T00:00:00+10:00',
    '2024-01-01T00:00:00+11:00',
    '2024-01-01T00:00:00+12:00',
    '2024-01-01T00:00:00-01:00',
    '2024-01-01T00:00:00-02:00',
    '2024-01-01T00:00:00-03:00',
    '2024-01-01T00:00:00-04:00',
    '2024-01-01T00:00:00-06:00',
    '2024-01-01T00:00:00-09:00',
    '2024-01-01T00:00:00-10:00',
    '2024-01-01T00:00:00-11:00',
    '2024-06-15T23:30:00+05:45',    # Nepal Time -- 45-minute offset
    '2024-06-15T23:30:00+08:45',    # Australian Central Western Standard Time
    '2024-06-15T23:30:00+09:30',
    '2024-03-15T14:30:00+05:30',
    '2024-09-22T06:00:00-06:00',
    '2024-12-25T00:00:00+12:45',    # Chatham Islands (UTC+12:45)
    '2024-07-04T16:00:00-04:30',    # historical Venezuela Standard Time
    '2023-11-05T01:00:00-08:00',
    '2023-03-12T02:00:00-07:00',
    '2024-10-27T02:00:00+01:00',
    '2024-06-30T12:00:00+05:30',
    '2024-09-15T00:00:00-03:00',
    '2026-01-01T00:00:00+01:00',
    '2025-12-31T23:59:59-05:00',
    '2030-06-15T08:00:00+09:00',
    '1970-01-01T00:00:00+00:00',    # Unix epoch with numeric UTC offset
])
def test_iso_timezone_offset_true_positive(text):
    """
    Attack vector: ISO 8601 datetimes with explicit numeric timezone offsets.

    Why a parser might fail: a regex anchored on the literal character 'Z' will
    not match '+00:00' even though the two are semantically identical (both
    represent UTC). More exotic offsets like +05:30 or +14:00 extend this gap
    further. A parser that only anchors on Z will miss the majority of real-world
    ISO timestamps found in API payloads, log files, and database exports.

    The half-hour and 45-minute offsets (+05:30, +05:45, +09:30, +08:45) are
    particularly important: a regex that only allows two-digit hour offsets
    followed by ':00' will fail to match them, despite their being unambiguous
    and common in production traffic from India, Nepal, and Australia.

    What failure reveals: the parser's ISO 8601 support is partial -- it handles
    only the UTC shorthand and not the full offset grammar defined in RFC 3339.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0



# ============================================================================
# SECTION 3 -- TRUE POSITIVES: FRACTIONAL SECONDS (DOT separator)
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISO 8601 section 4.2.2.4 permits a decimal fraction on the seconds (or
    # minutes or hours) component, separated by a full stop (.) or comma (,).
    # A parser that requires exactly HH:MM:SS before the timezone suffix will
    # reject all fractional-second variants.
    '2024-01-01T00:00:00.1Z',
    '2024-01-01T00:00:00.12Z',
    '2024-01-01T00:00:00.123Z',
    '2024-01-01T00:00:00.1234Z',
    '2024-01-01T00:00:00.12345Z',
    '2024-01-01T00:00:00.123456Z',    # microsecond precision (Python datetime default)
    '2024-01-01T00:00:00.999Z',
    '2024-01-01T00:00:00.999999Z',
    '2017-02-03T09:04:08.000Z',       # motivating example with zero fraction
    '2017-02-03T09:04:08.500Z',       # motivating example with half-second
    '2017-02-03T09:04:08.123456Z',    # motivating example microsecond precision
    '2024-06-15T12:30:45.001Z',
    '2024-06-15T12:30:45.999Z',
    '2024-06-15T12:30:45.0Z',
    '2024-06-15T12:30:45.00Z',
    '2024-12-31T23:59:59.999999Z',
    '2024-03-15T08:00:00.100+05:30',  # fraction + offset combined
    '2024-03-15T08:00:00.250-05:00',
    '2024-03-15T08:00:00.750+00:00',
    '2024-11-28T08:00:00.001Z',
    '2024-09-30T12:00:00.050Z',
    '2024-07-04T17:00:00.500Z',
    '2020-02-29T12:00:00.123Z',       # leap day with fraction
    '2000-01-01T00:00:00.0Z',
    '1970-01-01T00:00:00.000Z',
    '2026-06-15T12:30:45.678Z',
    '2028-02-29T00:00:00.999Z',       # leap day 2028 with fraction
    '2030-01-01T00:00:00.100Z',
    '2024-08-15T11:30:00.250-08:00',
    '2024-04-30T23:59:59.001Z',
])
def test_iso_fractional_seconds_dot_true_positive(text):
    """
    Attack vector: ISO 8601 datetimes with dot-separated fractional seconds.

    Why a parser might fail: a regex that terminates the seconds field with a
    fixed ``\d{2}`` group and then expects ``[Z+-]`` immediately will fail to
    advance past the decimal point. Even if the regex uses a greedy quantifier
    on the seconds, it may not account for the fractional part followed by a
    timezone designator.

    PostgreSQL returns timestamps in the form '2024-01-01T00:00:00.123456+00:00',
    AWS CloudWatch uses '2024-01-01T00:00:00.001Z', and Python's own
    ``datetime.isoformat()`` produces '2024-01-01T00:00:00.123456'. All of these
    will be silently dropped by a parser without fractional-second support.

    The number of fractional digits varies from 1 (tenths) to 6 (microseconds).
    Production systems emit all widths, so the regex must use a variable-width
    quantifier on the fraction group (e.g., ``\.\d+`` or ``\.\d{1,9}``).

    What failure reveals: the parser drops sub-second precision timestamps, which
    are ubiquitous in structured logs and database timestamp columns.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 4 -- TRUE POSITIVES: FRACTIONAL SECONDS (COMMA separator)
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISO 8601 section 4.2.2.4 explicitly states that the decimal sign shall be
    # either a comma or a full stop. European systems frequently use the comma form.
    '2024-01-01T00:00:00,1Z',
    '2024-01-01T00:00:00,12Z',
    '2024-01-01T00:00:00,123Z',
    '2024-01-01T00:00:00,999Z',
    '2024-01-01T00:00:00,123456Z',
    '2017-02-03T09:04:08,000Z',
    '2017-02-03T09:04:08,500Z',
    '2024-06-15T12:30:45,001Z',
    '2024-06-15T12:30:45,999Z',
    '2024-12-31T23:59:59,999999Z',
    '2024-03-15T08:00:00,100+05:30',
    '2024-03-15T08:00:00,250-05:00',
    '2020-02-29T12:00:00,123Z',
    '2000-01-01T00:00:00,0Z',
    '1970-01-01T00:00:00,000Z',
    '2026-06-15T12:30:45,678Z',
    '2030-01-01T00:00:00,001Z',
    '2024-09-15T14:22:33,456Z',
    '2025-03-20T10:00:00,500+02:00',
    '2028-11-11T11:11:11,111Z',
])
def test_iso_fractional_seconds_comma_true_positive(text):
    """
    Attack vector: ISO 8601 datetimes with comma-separated fractional seconds.

    Why a parser might fail: English-language regex writers rarely think of comma
    as a decimal separator. A regex that uses ``\.`` for the decimal point will
    not match ``,``. This gap causes silent data loss when timestamps arrive from
    European-locale systems or certain database drivers (e.g., MySQL DATETIME
    exported through ODBC drivers with European locale settings, or timestamps
    originating from SAP or German-locale Java applications).

    ISO 8601 section 4.2.2.4 says: "The decimal sign is a comma or a full stop
    (according to the preference of the user)." A parser that ignores this is only
    half compliant.

    What failure reveals: the parser is not ISO 8601 compliant in its treatment of
    the decimal separator, which is a subtle but real interoperability defect.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 5 -- TRUE POSITIVES: SENTENCE EMBEDDED
# ============================================================================

@pytest.mark.parametrize('text', [
    # Real-world inputs arrive embedded in natural-language sentences or structured
    # log lines. The parser must handle leading/trailing prose, punctuation adjacent
    # to the timestamp, and mid-sentence placement.
    'the event at 2024-03-15T14:30:00Z was critical',
    'logged at 2017-02-03T09:04:08Z by the system',
    'between 2024-01-01T00:00:00Z and 2024-12-31T23:59:59Z',
    'ERROR 2024-06-15T12:30:45Z connection refused',
    'deployed on 2024-07-04T17:00:00Z successfully',
    'timestamp: 2024-08-15T11:30:00-08:00 -- user logged in',
    'created_at=2024-09-01T09:00:00Z, updated_at=2024-09-02T10:00:00Z',
    'the server restarted at 2024-01-15T03:00:00+00:00.',
    'alert fired (2024-11-28T08:00:00Z) -- disk usage 95%',
    'effective from 2024-01-01T00:00:00Z through 2026-12-31T23:59:59Z',
    'start: 2024-03-01T08:00:00Z; end: 2024-03-01T17:00:00Z',
    '2024-05-20T15:00:00Z is the submission deadline',
    'we received 2024-02-29T00:00:00Z (leap day) correctly',
    'backup completed 2024-06-15T12:30:45.123Z without errors',
    'job ran from 2024-01-01T06:00:00+05:30 to noon',
    'event_time:2024-10-31T00:00:00Z,severity:HIGH',
    '[2024-12-25T00:00:00Z] christmas deployment',
    'version bump at 2024-09-15T14:22:33Z and tested',
    'prior to 2024-01-01T00:00:00Z the system was down',
    'after 2023-12-31T23:59:59Z the new rules apply',
    'scheduled for 2024-06-30T23:59:59Z before rollover',
    'incident opened 2024-04-15T09:30:00+01:00, closed 2024-04-15T11:45:00+01:00',
    'THE INCIDENT OCCURRED AT 2024-03-15T14:30:00Z IN PRODUCTION',
    'Incident: 2024-07-04T17:00:00Z, severity: critical',
    '[INFO] 2024-01-15T09:00:00Z server started',
    '[ERROR] 2024-06-15T12:30:45.123Z exception thrown',
    '[WARN] 2024-09-30T00:00:00+05:30 threshold exceeded',
    'commit 2024-08-01T12:00:00Z merged to main',
    'patch released at 2024-11-15T08:00:00Z addresses CVE-2024-1234',
    'see audit log entry from 2025-01-01T00:00:00Z onwards',
])
def test_iso_sentence_embedded_true_positive(text):
    """
    Attack vector: ISO 8601 timestamps embedded in natural-language or structured prose.

    Why a parser might fail: a regex anchored with ``^`` or ``$`` will only match
    when the timestamp is the entire input string. Real log lines have prefixes
    (log level, module name), suffixes (message text), or surround the timestamp
    with punctuation (colons, brackets, parentheses).

    Log aggregation systems (Splunk, Elasticsearch, Loki) pass raw log lines
    containing timestamps embedded in structured text. A parser that cannot
    locate the timestamp within prose will fail to function in those contexts.

    What failure reveals: the parser cannot extract timestamps from real log lines,
    limiting its practical utility to artificially clean inputs.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ============================================================================
# SECTION 6 -- TRUE POSITIVES: BOUNDARY DATES (valid calendar extremes)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Calendar extremes that stress-test the regex date-component ranges.
    '2024-01-01T00:00:00Z',      # January 1 -- start of year
    '2024-12-31T23:59:59Z',      # December 31 -- end of year
    '2024-01-31T23:59:59Z',      # January 31 -- valid 31-day month
    '2024-03-31T23:59:59Z',      # March 31
    '2024-05-31T23:59:59Z',      # May 31
    '2024-07-31T23:59:59Z',      # July 31
    '2024-08-31T23:59:59Z',      # August 31
    '2024-10-31T23:59:59Z',      # October 31
    '2024-02-29T23:59:59Z',      # February 29 -- leap day (2024 IS a leap year)
    '2023-02-28T23:59:59Z',      # February 28 -- last day in non-leap year
    '2024-04-30T23:59:59Z',      # April 30 -- 30-day month
    '2024-06-30T23:59:59Z',      # June 30
    '2024-09-30T23:59:59Z',      # September 30
    '2024-11-30T23:59:59Z',      # November 30
    '2024-01-01T00:00:00.000Z',  # midnight with fraction
    '2024-12-31T23:59:59.999Z',  # last millisecond of year
    '1926-01-01T00:00:00Z',      # parser min-year (if parser has year floor)
    '2036-12-31T23:59:59Z',      # parser max-year (if parser has year ceiling)
    '1970-01-01T00:00:00Z',      # Unix epoch -- universally significant boundary
    '2038-01-19T03:14:07Z',      # Y2K38 -- 32-bit Unix timestamp overflow boundary
])
def test_iso_boundary_dates_true_positive(text):
    """
    Attack vector: ISO 8601 timestamps at valid calendar extremes.

    Why a parser might fail: a parser that validates dates (rather than just
    matching digit groups) may have off-by-one errors in month-day validation.
    Leap day (Feb 29) is particularly sensitive because it requires knowing whether
    the year is a leap year.

    The 1926/2036 boundary tests are specific to this project: if the prose-year
    extractor has a year-range guard [1926, 2036], these tests reveal whether that
    same guard is applied consistently in the ISO extractor.

    What failure reveals: the parser has unexpected gaps at valid calendar
    boundaries, possibly due to restrictive range checks in the regex or
    post-match validation logic.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0



# ============================================================================
# SECTION 7 -- FALSE POSITIVES: PARTIAL ISO STRINGS
# ============================================================================

@pytest.mark.parametrize('text', [
    # Incomplete ISO 8601 expressions -- missing required components.
    '2024-03-15T',              # trailing T with no time component
    'T09:04:08Z',               # time-only with no date portion
    'T12:30:45',                # time-only, no date, no timezone
    '2024-03',                  # year-month only (no day, no T)
    'T',                        # bare T
    '2024T',                    # year followed by bare T
    '20240315',                 # compact ISO date (no T, no time)
    '090408Z',                  # time-only, no date
    '2024-W12-3',               # ISO week date (no T separator, not a datetime)
    '2024-075T',                # ordinal date with trailing T but no time
    '2024-01-01+00:00',         # date with offset but no T or time
    '2024-13-15T',              # invalid month + trailing T only
    'YYYY-MM-DDTHH:MM:SSZ',     # literal format string (not a real timestamp)
    '--01-01T',                 # ISO 8601 specific date without year
    '---01T',                   # ISO 8601 specific day without year/month
])
def test_iso_partial_false_positive(text):
    """
    Attack vector: partial or malformed ISO 8601 strings that are missing key components.

    Why a parser might fail: a greedy regex that matches ``\d{4}-\d{2}-\d{2}``
    will incorrectly match '2024-03-15' even when there is no time component,
    classifying a bare date as an ISO datetime. Similarly, a regex that
    matches ``T\d{2}:\d{2}:\d{2}`` without requiring a preceding date will
    accept time-only strings.

    The format string 'YYYY-MM-DDTHH:MM:SSZ' (commonly found in documentation,
    README files, and API specs) is a textbook false positive: it contains all the
    structural characters of an ISO timestamp but represents a format descriptor,
    not a real date.

    What failure reveals (false positive produced): the parser is over-matching,
    treating partial ISO fragments as full ISO datetimes.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 8 -- FALSE POSITIVES: ISO 8601 DURATION STRINGS
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISO 8601 section 4.4 defines *duration* strings beginning with 'P'.
    # These look like they contain date components but represent interval lengths.
    'PT1H30M',
    'P1Y2M3DT4H5M6S',
    'P30D',
    'PT15M',
    'PT0S',
    'P1Y',
    'P6M',
    'P1Y6M',
    'PT24H',
    'PT1H',
    'PT30M',
    'PT45S',
    'P2Y3M4DT5H6M7S',
    'P0Y0M0DT0H0M0S',
    'P1DT12H',
    'P7D',
    'P52W',                     # ISO 8601 week duration
    'P1Y2M',
    'PT0.5S',                   # fractional seconds in duration
    'PT1H30M0S',
    'P3Y6M4DT12H30M5S',
    'P23DT23H',
    'P4DT12H30M5S',
    'P1M',
    'P1W2D',
    'P0D',
    'PT0H',
    'P1Y0M0DT0H0M0S',
    'P10Y',
    'PT168H',
])
def test_iso_duration_false_positive(text):
    """
    Attack vector: ISO 8601 duration (period) strings.

    Why a parser might fail: duration strings contain the same letters used in
    datetime strings (T for time separator, H for hour, M for minute/month,
    D for day, S for second, Y for year) but in a completely different positional
    grammar. A parser that looks for an isolated 'T' followed by digit groups
    may accidentally fire on the interior of a duration string like
    ``P1Y2M3DT4H5M6S``.

    Duration strings are ubiquitous: FHIR resources use them for medication dosage
    intervals, iCalendar (RFC 5545) uses them for event durations, and REST API
    timeout parameters use them in configuration files.

    What failure reveals (false positive produced): the parser cannot distinguish
    ISO 8601 durations from ISO 8601 datetimes.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 9 -- FALSE POSITIVES: LOOKS-LIKE-ISO (version strings, ticket IDs)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Strings containing 'T' and digit groups that resemble ISO 8601 but are not.
    'Project T-2024',
    'v2024-03T1',
    'ticket-2024-01T',
    'model-T2024',
    'T-bone steak from 2024',
    'TICKET-2024-001',
    'BUILD-2024-03-T7',
    'API-v2-T2024',
    'spec-2024T',
    'config.T2024-01',
    'SKU-2024-T1-001',
    'RFC-2024T',
    'T:2024',
    'ref:2024-03-T',
    '2024T-specification',
    'v1.2024-T3',
    'changelog-2024-T1',
    'T2024.Q1',
    'item-T-2024-A',
    '2024-revision-T1',
    'feature-T2024-01-alpha',
    'MODEL-T-2024-EDITION',
    'T+2024',
    'prefix-T-suffix',
    '2024-T-series',
])
def test_iso_looks_like_false_positive(text):
    """
    Attack vector: strings containing 'T' and digit groups that resemble ISO 8601
    but are identifiers, version strings, or ticket references.

    Why a parser might fail: a regex that matches ``\d{4}.*T.*\d{2}`` as a
    heuristic will fire on product codes, ticket identifiers, and version strings
    that happen to contain the letter T adjacent to a 4-digit year.

    What failure reveals (false positive produced): the parser is tagging
    non-temporal identifiers as dates.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 10 -- FALSE POSITIVES: ISO INTERVAL (slash-separated, date-only)
# ============================================================================

@pytest.mark.parametrize('text', [
    # ISO 8601 section 4.4.4 time intervals using slash -- date-only forms.
    '2024-01-01/2024-03-31',
    '2023-01-01/2023-12-31',
    '2020-01-01/P1Y',
    'P1Y/2021-01-01',
    '2024-06-01/2024-06-30',
    '2024-01/2024-06',
    '2024-001/2024-366',
    '2024-W01/2024-W52',
])
def test_iso_interval_false_positive(text):
    """
    Attack vector: ISO 8601 time interval strings using slash notation (date-only form).

    Why a parser might fail: the left-hand side of an interval string like
    ``2024-01-01/2024-03-31`` begins with a valid ISO date. A parser that searches
    for ISO dates anywhere in the text will match the left side. The test asserts
    that bare date-only intervals (no T separator, no time component) should not
    trigger the ISO 8601 *datetime* handler.

    What failure reveals (false positive produced): the parser is matching bare
    YYYY-MM-DD date strings as ISO datetimes.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ============================================================================
# SECTION 11 -- BOUNDARY: INVALID FIELD VALUES
# ============================================================================

@pytest.mark.parametrize('text', [
    # Syntactically ISO-like but contain out-of-range field values.
    # No directional assertion -- recording behaviour for documentation.
    '2024-13-01T00:00:00Z',          # month 13 (invalid)
    '2024-00-01T00:00:00Z',          # month 0 (invalid)
    '2024-01-00T00:00:00Z',          # day 0 (invalid)
    '2024-01-32T00:00:00Z',          # day 32 (invalid in all months)
    '2024-02-30T00:00:00Z',          # Feb 30 (invalid)
    '2023-02-29T00:00:00Z',          # Feb 29 in non-leap year (invalid)
    '2024-01-01T24:00:00Z',          # hour 24 (permitted in ISO for end-of-day only)
    '2024-01-01T25:00:00Z',          # hour 25 (always invalid)
    '2024-01-01T00:60:00Z',          # minute 60 (invalid)
    '2024-01-01T00:00:60Z',          # second 60 without leap-second context
    '2024-06-30T23:59:60Z',          # leap second (valid in UTC but rarely supported)
    '2024-01-01T00:00:61Z',          # second 61 (always invalid)
    '9999-12-31T23:59:59Z',          # far-future date (beyond typical range)
    '0000-01-01T00:00:00Z',          # year 0 (proleptic Gregorian calendar)
    '2024-01-01T00:00:00+25:00',     # offset > 14 hours (invalid per RFC 3339)
    '2024-01-01T00:00:00-13:00',     # offset < -12 hours (invalid per RFC 3339)
    '2024-04-31T00:00:00Z',          # April has only 30 days
    '2024-06-31T00:00:00Z',          # June has only 30 days
    '2024-09-31T00:00:00Z',          # September has only 30 days
    '2024-11-31T00:00:00Z',          # November has only 30 days
])
def test_iso_invalid_field_values_boundary(text):
    """
    Attack vector: syntactically ISO-like strings with out-of-range field values.

    Why a parser might fail to reject: a pure regex approach that does not validate
    calendar or time arithmetic will match any string that fits the digit-group
    pattern, regardless of whether month 13, day 0, or hour 25 are semantically
    valid. This is sometimes called 'structural matching without semantic validation'.

    The leap-second case (23:59:60) is especially nuanced: it is defined in the UTC
    standard for days on which IERS inserts a leap second, but most software
    (including Python's datetime module) does not support it.

    This test does not assert a direction -- it records whatever the parser does
    so that the development team can make an explicit decision about tolerance policy.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert isinstance(result, dict)


# ============================================================================
# SECTION 12 -- UNICODE HOMOGLYPH ATTACKS
# ============================================================================

@pytest.mark.parametrize('text, description', [
    # Fullwidth Latin letter T (U+FF34) -- looks like ASCII T but byte-distinct.
    ('2024-01-01Ｔ00:00:00Z', 'fullwidth T capital (U+FF34) between date and time'),
    ('2024-01-01ｔ00:00:00Z', 'fullwidth t lowercase (U+FF54) between date and time'),

    # Fullwidth colon (U+FF1A).
    ('2024-01-01T00：00：00Z', 'fullwidth colons in time component (U+FF1A)'),

    # Fullwidth Z (U+FF3A) -- looks like 'Z' but not the ASCII UTC designator.
    ('2024-01-01T00:00:00Ｚ', 'fullwidth Z (U+FF3A) as timezone designator'),

    # Fullwidth digits (U+FF10-U+FF19).
    ('２０２４-01-01T00:00:00Z', 'fullwidth digits in year (2024 fullwidth)'),
    ('2024-０１-01T00:00:00Z', 'fullwidth digits in month'),
    ('2024-01-０１T00:00:00Z', 'fullwidth digits in day'),

    # Zero-width space (U+200B) -- breaks tokenisation invisibly.
    ('2024-01-01​T00:00:00Z', 'zero-width space before T (U+200B)'),
    ('2024-01-01T​00:00:00Z', 'zero-width space after T (U+200B)'),
    ('2024-01-01T00:00:00​Z', 'zero-width space before Z (U+200B)'),

    # Soft hyphen (U+00AD) in place of ASCII hyphen.
    ('2024­01­01T00:00:00Z', 'soft hyphens in date separators (U+00AD)'),

    # Arabic-Indic digits (U+0660-U+0669).
    ('٢٠٢٤-01-01T00:00:00Z', 'Arabic-Indic digits in year'),

    # Minus sign (U+2212) in place of hyphen-minus (U+002D).
    ('2024−01−01T00:00:00Z', 'minus sign (U+2212) in date separators'),

    # RTL override character (U+202E).
    ('2024-01-01T‮00:00:00Z', 'RTL override character (U+202E) inside timestamp'),

    # En-dash (U+2013) replacing hyphen-minus.
    ('2024–01–01T00:00:00Z', 'en-dashes in date separators (U+2013)'),

    # Non-breaking hyphen (U+2011).
    ('2024‑01‑01T00:00:00Z', 'non-breaking hyphens in date separators (U+2011)'),
])
def test_iso_unicode_homoglyph(text, description):
    """
    Attack vector: ISO 8601 strings with Unicode homoglyphs replacing ASCII characters.

    Why a parser might be fooled: visual similarity between Unicode characters and
    their ASCII counterparts means that a human auditing a test input sees what
    appears to be a valid ISO timestamp, but the byte sequence is different. A
    parser that does not perform Unicode normalisation (NFC/NFKC) before regex
    matching will treat these as non-matching inputs.

    Conversely, a parser that uses Python's ``re.UNICODE`` flag (the default in
    Python 3) may unintentionally match fullwidth digits via ``\d``, producing
    an unexpected match where none was intended.

    Security relevance: homoglyph attacks are used to bypass input validation in
    security-sensitive contexts. A parser that accepts homoglyphs as valid dates
    is potentially vulnerable to temporal data injection attacks.

    This test records current behaviour without asserting direction.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert isinstance(result, dict)


# ============================================================================
# SECTION 13 -- ADDITIONAL TRUE POSITIVES (reaching 250+ total cases)
# ============================================================================

@pytest.mark.parametrize('text', [
    # Reduced-precision forms (hours + minutes, no seconds).
    '2024-01-01T00:00Z',
    '2024-06-15T12:30Z',
    '2024-12-31T23:59Z',
    '2017-02-03T09:04Z',         # motivating example without seconds
    '2024-03-15T14:30+05:30',
    '2024-07-04T17:00-05:00',
    '2024-01-01T00:00+00:00',
    '2024-08-15T08:00-07:00',
    '2024-09-22T06:00+09:00',
    '2026-06-15T12:30Z',
    '2027-01-01T00:00Z',
    '2028-02-29T12:00Z',
    '2029-11-15T08:30Z',
    '2030-12-31T23:59Z',
    '2031-07-04T17:00Z',
    '2033-12-25T00:00Z',
    '2034-01-01T00:00Z',
    '2035-06-30T23:59Z',
    '2036-12-31T23:58Z',
    # Hours-only precision.
    '2024-01-01T00Z',
    '2024-06-15T12Z',
    '2024-12-31T23Z',
    '2017-02-03T09Z',
    # Multiple timestamps in one string.
    'start 2024-01-01T00:00:00Z end 2024-12-31T23:59:59Z',
    'range: 2024-03-01T08:00:00Z to 2024-03-31T17:00:00Z',
    'from 2024-06-01T00:00:00Z through 2024-06-30T23:59:59Z',
    # JSON-like context.
    '{"timestamp": "2024-01-01T00:00:00Z"}',
    '{"created_at": "2024-06-15T12:30:45.123Z", "id": 42}',
    '{"start": "2024-01-01T00:00:00Z", "end": "2024-12-31T23:59:59Z"}',
    # Surrounding punctuation.
    '(2024-01-01T00:00:00Z)',
    '[2024-06-15T12:30:45Z]',
    '<2024-12-31T23:59:59Z>',
    # Extended year range coverage.
    '1930-06-15T12:00:00Z',
    '1940-01-01T00:00:00Z',
    '1950-12-31T23:59:59Z',
    '1960-07-04T17:00:00Z',
    '1975-11-28T08:00:00Z',
    '1985-09-11T08:46:00Z',
    '1995-04-10T21:00:00Z',
    '2005-02-24T04:00:00Z',
    '2015-03-11T05:46:23Z',
    '2025-09-15T14:22:33Z',
    '2026-08-01T12:00:00Z',
    '2028-11-11T11:11:11Z',
    # Assorted additional dates.
    '2024-04-15T09:30:00Z',
    '2024-05-20T15:00:00Z',
    '2024-06-25T18:30:00Z',
    '2024-07-10T06:00:00Z',
    '2024-10-05T20:00:00+03:00',
    '2024-11-11T11:11:11Z',
    '2024-12-01T00:00:01Z',
    '2025-01-31T23:00:00Z',
    '2025-02-14T14:00:00Z',
    '2025-03-21T09:00:00+00:00',
    '2025-04-01T12:00:00Z',
    '2025-05-05T05:05:05Z',
    # Fractional seconds AND timezone offsets combined.
    '2024-03-15T08:00:00.123+05:30',
    '2024-07-04T17:00:00.500-07:00',
    '2024-12-25T00:00:00.001+00:00',
    '2025-01-01T00:00:00.000Z',
    '2026-06-15T12:30:45.678+02:00',
    # Additional Z variants.
    '2024-02-15T10:00:00Z',
    '2024-03-20T16:00:00Z',
    '2024-04-25T22:00:00Z',
    '2024-05-30T04:00:00Z',
    '2024-06-05T08:00:00Z',
    '2024-07-11T14:00:00Z',
    '2024-08-16T20:00:00Z',
    '2024-09-21T02:00:00Z',
    '2024-10-26T18:00:00Z',
    '2024-11-30T11:00:00Z',
    '2024-12-15T07:00:00Z',
    '2025-01-20T13:00:00Z',
    '2025-02-25T19:00:00Z',
    '2025-03-30T01:00:00Z',
    '2025-04-04T05:00:00Z',
    '2025-05-09T09:00:00Z',
    '2025-06-14T15:00:00Z',
    '2025-07-19T21:00:00Z',
    '2025-08-24T03:00:00Z',
    '2025-09-28T17:00:00Z',
])
def test_iso_additional_true_positive(text):
    """
    Attack vector: additional ISO 8601 variants covering reduced-precision forms,
    multi-timestamp strings, JSON-embedded contexts, and extended year ranges.

    Why a parser might fail: reduced-precision forms (hours-only, hours+minutes
    without seconds) are valid under ISO 8601 section 4.2.2.3 but are rarely
    included in regex patterns built to match the canonical 6-component form
    (HH:MM:SS). JSON embedding tests whether the parser handles quoted strings
    correctly. Multi-timestamp strings test whether the parser returns multiple
    matches rather than stopping after the first.

    The extended year coverage (1930s through 2036) ensures that the parser's
    year-range filter (if any) correctly includes the full expected range without
    off-by-one errors at either boundary.

    What failure reveals: each parametrised failure locates a specific coverage
    gap -- whether in precision handling, JSON context, multi-match behaviour, or
    year-range filtering.

    Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0
