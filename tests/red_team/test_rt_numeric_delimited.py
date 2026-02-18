#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Red Team: Numeric-Delimited Date Patterns
==========================================
This module adversarially probes the fast-parse-time parser handling of
numeric date strings that use the three canonical delimiters: slash (/),
hyphen (-), and dot (.). These formats are ubiquitous in computing contexts
and represent one of the highest-density ambiguity zones in temporal NLP.

The core challenge is that character sequences composing valid dates --
two or four digit numeric tokens separated by a single punctuation character --
are structurally identical to IP addresses (192.168.1.1), version strings
(1.2.3), file paths (foo/bar/baz), phone/ISBN numbers (0-306-40615-2), and
many other domain-specific encodings. A naive lexical parser that matches
on shape alone will produce an unacceptable false-positive rate across these
categories. This file tests the boundaries of parser discrimination.

Attack surface taxonomy:
  A. Delimiter-variant true positives (/, -, .)
  B. IP address false positives (dot-notation quad octets)
  C. Semantic version false positives (SemVer: MAJOR.MINOR.PATCH)
  D. File path false positives (slash-delimited non-date path segments)
  E. Phone/ISBN false positives (hyphen-delimited numeric identifiers)
  F. Year boundary edge cases (parser range clipping behavior)
  G. Calendar logic edge cases (day 0, month 0, Feb 29 leap/non-leap)
  H. Unicode homoglyph and script substitution attacks

Related GitHub Issue: #43 https://github.com/craigtrim/fast-parse-time/issues/43
"""

import pytest
from fast_parse_time import extract_explicit_dates

# Every test in this module is provisional. Failures indicate either a gap in
# parser coverage (for true-positive sections) or a false-positive leak (for
# false-positive sections). All cases require triage before being promoted to
# the main test suite.
pytestmark = pytest.mark.xfail(reason='red_team: not yet validated')


# ===========================================================================
# SECTION 1 -- TRUE POSITIVES: SLASH-DELIMITED DATES (MM/DD/YYYY)
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Standard slash-delimited full dates embedded in sentence context.
    # These represent the canonical North American date format and should
    # reliably trigger FULL_EXPLICIT_DATE recognition. The surrounding
    # sentence context exercises the parser boundary detection logic,
    # ensuring that whitespace tokenization does not discard the match.
    'The meeting is on 04/08/2024.',
    'Please review the report dated 01/15/2023.',
    'Contract signed 12/31/2022 is attached.',
    'Invoice due 07/04/2021 has been paid.',
    'The event was held on 11/11/2011.',
    'We need it done by 03/03/2033.',
    'Submission deadline: 09/09/2029.',
    'Last updated 06/15/2025.',
    'Born on 05/20/1985.',
    'Expires 08/01/2030.',
    # Leading zero variants -- tests whether the parser handles zero-padded
    # month and day fields identically to non-padded variants.
    'Dated 01/01/2024.',
    'Dated 02/05/2024.',
    'Dated 03/09/2024.',
    'Dated 04/08/2024.',
    'Dated 05/07/2024.',
    'Dated 06/06/2024.',
    'Dated 07/05/2024.',
    'Dated 08/04/2024.',
    'Dated 09/03/2024.',
    'Dated 10/02/2024.',
    'Dated 11/01/2024.',
    'Dated 12/31/2024.',
    # Non-zero-padded variant -- same dates without leading zeros.
    # A robust parser must handle both 04/08/2024 and 4/8/2024 identically.
    'Dated 1/1/2024.',
    'Dated 2/5/2024.',
    'Dated 3/9/2024.',
    'Dated 4/8/2024.',
    'Dated 5/7/2024.',
    'Dated 6/6/2024.',
    'Dated 7/5/2024.',
    'Dated 8/4/2024.',
    'Dated 9/3/2024.',
    'Dated 10/2/2024.',
    'Dated 11/1/2024.',
    'Dated 12/31/2024.',
    # Padded whitespace
    '   04/08/2024   ',
    '  01/01/2026  ',
    # Boundary years (min=1926, max=2036)
    'Born 01/01/1926.',
    'Expires 12/31/2036.',
    # All months at valid day ranges
    'January: 01/15/2024.',
    'February: 02/15/2024.',
    'March: 03/15/2024.',
    'April: 04/15/2024.',
    'May: 05/15/2024.',
    'June: 06/15/2024.',
    'July: 07/15/2024.',
    'August: 08/15/2024.',
    'September: 09/15/2024.',
    'October: 10/15/2024.',
    'November: 11/15/2024.',
    'December: 12/15/2024.',
    # Additional padded and contextual variants
    'Report finalized on 04/08/2024 and sent.',
    'Event scheduled for 04/08/2024 at noon.',
    'Confirm by 04/08/2024 or earlier.',
    'Signed off 04/08/2024 by the team.',
    'The deadline was 12/31/2024.',
    'Review period: 01/01/2024 to 12/31/2024.',
    'Filed 06/15/1980.',
    'Closed 06/15/2000.',
    'Opened 06/15/2024.',
])
def test_true_positive_slash_delimited(text):
    """
    True positive: slash-delimited MM/DD/YYYY dates should be detected.

    Attack vector: Standard North American numeric date format using the
    forward-slash delimiter. This is the highest-frequency date format in
    English-language business and legal documents.

    Why a parser might fail: Overly restrictive word-boundary anchoring may
    require surrounding whitespace or punctuation patterns that do not always
    hold. Additionally, parsers that strip leading zeros before matching may
    fail on the un-padded variants (4/8/2024 vs 04/08/2024).

    Failure reveals: Core numeric date extraction is not firing on a canonical
    format that must be a first-order priority for any date parser.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 2 -- TRUE POSITIVES: HYPHEN-DELIMITED DATES (MM-DD-YYYY)
# ===========================================================================

@pytest.mark.parametrize('text', [
    'Report dated 04-08-2024.',
    'Invoice 06-05-2016 submitted.',
    'Deadline 12-31-2023.',
    'Event on 01-01-2027.',
    'Filed 03-15-2024.',
    'Closed 07-04-2021.',
    'Opened 09-09-2019.',
    'Scheduled for 11-11-2025.',
    'Last seen 05-20-1985.',
    'Renewed 08-01-2030.',
    'Date: 01-01-2024.',
    'Date: 02-05-2024.',
    'Date: 03-09-2024.',
    'Date: 10-02-2024.',
    'Date: 11-01-2024.',
    'Date: 12-31-2024.',
    'Date: 1-1-2024.',
    'Date: 3-9-2024.',
    'Date: 6-6-2024.',
    'Date: 9-3-2024.',
    'Date: 11-1-2024.',
    'Date: 12-31-2024.',
    'Record from 01-01-1926.',
    'Expiry on 12-31-2036.',
    '01-15-2024 was a Monday.',
    '02-15-2024 was a Thursday.',
    '03-15-2024 was a Friday.',
    '04-15-2024 was a Monday.',
    '05-15-2024 was a Wednesday.',
    '06-15-2024 was a Saturday.',
    '07-15-2024 was a Monday.',
    '08-15-2024 was a Thursday.',
    '09-15-2024 was a Sunday.',
    '10-15-2024 was a Tuesday.',
    '11-15-2024 was a Friday.',
    '12-15-2024 was a Sunday.',
    'The report for 04-08-2024 is ready.',
    'As of 06-05-2016 the contract is active.',
    'Effective 01-01-2027 new rules apply.',
    'Invoice generated 12-31-2023 is overdue.',
    'Log entry from 03-15-2024 flagged.',
])
def test_true_positive_hyphen_delimited(text):
    """
    True positive: hyphen-delimited MM-DD-YYYY dates should be detected.

    Attack vector: Hyphen-delimited numeric date format. The hyphen presents
    the highest disambiguation challenge because it is also used to join
    month abbreviations to year tokens (Oct-23), to form ISO 8601 dates
    (2024-04-08), and to construct compound identifiers throughout computing
    contexts (version strings, phone numbers, ISBN, product codes).

    Why a parser might fail: A parser relying on the same hyphen-pattern
    recognition for both MONTH-YEAR and DAY-MONTH-YEAR may have ordering or
    priority conflicts that cause full date suppression.

    Failure reveals: The hyphen extractor priority or conflict resolution
    logic is incorrectly discarding full MM-DD-YYYY matches in favor of
    partial sub-patterns.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 3 -- TRUE POSITIVES: DOT-DELIMITED DATES (MM.DD.YYYY)
# ===========================================================================

@pytest.mark.parametrize('text', [
    'Completed 04.08.2024.',
    'Deadline 12.31.2023.',
    'Filed on 01.15.2023.',
    'Submitted 07.04.2021.',
    'Renewed 08.01.2030.',
    'Issued 06.15.2025.',
    'Effective 03.01.2027.',
    'Cancelled 09.09.2029.',
    'Received 11.11.2011.',
    'Shipped 05.20.1985.',
    'Date: 01.01.2024.',
    'Date: 02.05.2024.',
    'Date: 03.09.2024.',
    'Date: 10.02.2024.',
    'Date: 11.01.2024.',
    'Date: 12.31.2024.',
    'Date: 1.1.2024.',
    'Date: 3.9.2024.',
    'Date: 6.6.2024.',
    'Date: 9.3.2024.',
    'Date: 12.31.2024.',
    'Born 01.01.1926.',
    'Expiry 12.31.2036.',
    '01.15.2024 -- January date.',
    '02.15.2024 -- February date.',
    '03.15.2024 -- March date.',
    '04.15.2024 -- April date.',
    '05.15.2024 -- May date.',
    '06.15.2024 -- June date.',
    '07.15.2024 -- July date.',
    '08.15.2024 -- August date.',
    '09.15.2024 -- September date.',
    '10.15.2024 -- October date.',
    '11.15.2024 -- November date.',
    '12.15.2024 -- December date.',
    'Completed on 04.08.2024 as required.',
    'Submission for 12.31.2023 reviewed.',
    'Entered into system 01.15.2023.',
    'Transaction 07.04.2021 processed.',
    'Renewal due 08.01.2030 confirmed.',
])
def test_true_positive_dot_delimited(text):
    """
    True positive: dot-delimited MM.DD.YYYY dates should be detected.

    Attack vector: Period/dot as date delimiter. This is the format most
    prone to confounding with IP addresses and semantic version strings
    because all three use the ASCII period (U+002E) as their separator.

    Why a parser might fail: If IP-address and version-string suppression
    rules are implemented as prefix guards (i.e., if the string looks like
    an IP, reject it), there is a risk of over-broad suppression that also
    eliminates valid dates where the first two components happen to fall in
    octet-range (e.g., 12.31 could be naively read as a partial IP).

    Failure reveals: The IP-guard heuristic is either too broad or incorrectly
    anchored, causing valid dates to be rejected at the pre-filter stage.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 4 -- FALSE POSITIVES: IP ADDRESSES
# ===========================================================================

@pytest.mark.parametrize('text', [
    # IPv4 addresses are structurally dot.digit.digit.digit, the same surface
    # form as a date when the parser performs only character-class matching
    # without calendar-logic validation. A production parser MUST reject these.
    #
    # Key discriminator: IP addresses have four numeric components; dates have
    # three. Additionally, IP octets range 0-255 while date fields have tighter
    # bounds (month 1-12, day 1-31).
    'Server address is 192.168.1.1.',
    'Connect to 10.0.0.255 for internal access.',
    'The gateway is at 172.16.254.1.',
    'DNS server: 8.8.8.8.',
    'Localhost is 127.0.0.1.',
    'Null route: 0.0.0.0.',
    'Broadcast: 255.255.255.255.',
    'Private network: 10.10.10.10.',
    'Host at 192.0.2.1.',
    'Reserved: 169.254.1.1.',
    'Multicast: 224.0.0.1.',
    'Loopback alt: 127.0.0.2.',
    'APIPA: 169.254.0.1.',
    'Class A: 10.20.30.40.',
    'Class B: 172.31.0.1.',
    'Class C: 192.168.100.200.',
    'Connect to host 10.0.1.100 now.',
    'Primary DNS 8.8.8.8, secondary 8.8.4.4.',
    'Failed to reach 192.168.0.254.',
    'Internal: 10.100.200.1.',
    'External: 203.0.113.1.',
    'The server at 198.51.100.42 is down.',
    'Check 172.20.10.1 for the proxy.',
    'IANA reserved 100.64.0.1.',
    'IPv4 mapped: 0.0.0.128.',
    'IP 192.168.1.1 is unreachable',
    'Ping 10.0.0.1 failed',
    'Route via 172.16.0.1 expired',
    'Firewall rule for 10.0.0.0.',
    'Subnet mask 255.255.0.0.',
    'Configured 192.168.10.254.',
    'Test host 172.17.0.1.',
    'Local network 10.1.2.3.',
    'BGP peer 1.2.3.4.',
    'Blacklisted: 203.0.113.99.',
    'NAT source: 10.50.100.1.',
    'Traceroute via 8.8.4.4.',
    'VPN endpoint 172.18.0.1.',
    'The device at 192.168.2.100 is offline.',
    'Scanning 10.0.1.0/24 for hosts.',
    'Default gateway: 192.168.1.254.',
])
def test_false_positive_ip_addresses(text):
    """
    False positive guard: IP addresses must not be classified as dates.

    Attack vector: IPv4 dot-quad notation (A.B.C.D) is structurally similar
    to dot-delimited date strings (MM.DD.YYYY). A parser that tokenizes on
    periods and checks for numeric fields will encounter both formats and must
    apply discriminating logic to separate them.

    Discrimination strategy the parser should implement:
      1. Component count: IP addresses have 4 components; dates have 3.
      2. Year anchor: the last component of a date must be a 4-digit number
         in a valid year range; IP octets are always <= 3 digits.
      3. Octet-range suppression: if ALL components are in range [0, 255]
         and there are exactly 4 components, treat as IP.

    Why a parser might fail: Regex-first parsers that match on a greedy
    sub-sequence might match a 3-component sub-sequence of an IP address.

    Failure reveals: The parser is matching on structural shape alone without
    calendar-logic validation, producing systematic false positives on network
    configuration content.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 5 -- FALSE POSITIVES: SEMANTIC VERSION STRINGS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # SemVer strings (MAJOR.MINOR.PATCH) share the three-component dot-delimited
    # structure with dot-delimited dates. For version strings where all three
    # components fall within calendar-valid ranges, purely lexical or range-based
    # disambiguation will fail.
    'Software version 1.2.3 is installed.',
    'Upgrade to 2.0.1 immediately.',
    'Running kernel 10.0.4.',
    'Library version 3.14.159.',
    'Release 1.0.0 is now live.',
    'Patch version 12.0.1 fixes the bug.',
    'Version 4.2.0 introduces new features.',
    'Downgrade to 0.9.1 if needed.',
    'API at version 5.3.2.',
    'Build 7.1.0 passed all checks.',
    'Current: v1.2.3.',
    'Latest: v2.0.1.',
    'Tagged v10.0.4 in git.',
    'SemVer 3.14.159.',
    'Frozen at 1.0.0-rc1.',
    'Beta: 2.1.0-beta.',
    'Alpha: 0.0.1-alpha.',
    'The package is at 6.5.4.',
    'Requires >=1.2.3.',
    'Compatible with 3.0.0.',
    'Breaking change in 2.0.0.',
    'Pinned to 4.1.2.',
    'Updated dependency from 1.0.0 to 1.1.0.',
    'Node version 18.0.0.',
    'Python 3.11.0 released.',
    'npm 9.0.0 ships with node 18.',
    'pip 23.0.1 available.',
    'gcc 12.3.0 compiler.',
    'clang 16.0.4 installed.',
    'openssl 3.0.9 patched.',
    'Django 4.2.0 is the LTS release.',
    'Flask 3.0.0 dropped Python 2.',
    'React 18.0.0 released with concurrent mode.',
    'Vue 3.3.0 ships composition API improvements.',
    'TensorFlow 2.0.0 broke backward compat.',
    'PyTorch 1.13.0 has new features.',
    'numpy 1.24.0 deprecates several APIs.',
    'scipy 1.10.0 adds new solvers.',
    'pandas 2.0.0 changes the index.',
    'matplotlib 3.7.0 released.',
])
def test_false_positive_version_strings(text):
    """
    False positive guard: semantic version strings must not be classified as dates.

    Attack vector: Semantic version numbers (SemVer: MAJOR.MINOR.PATCH) are
    three-component dot-delimited numeric sequences -- structurally identical
    to dot-delimited date strings. For version strings where all three
    components fall within calendar-valid ranges, purely lexical or range-based
    disambiguation will fail.

    Why a parser might fail: A parser that only validates component ranges
    (month 1-12, day 1-31) will still fire on '1.2.3' because all values are
    in range. Only the absence of a four-digit year component or the presence
    of contextual cues (the word 'version', 'v' prefix) can reliably
    disambiguate.

    Failure reveals: The parser lacks four-digit year enforcement and/or
    contextual suppression for software version notation.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 6 -- FALSE POSITIVES: FILE PATHS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Slash-delimited file paths can contain numeric directory components
    # that superficially resemble date fragments.
    'See path/to/file/2024 for details.',
    'Stored in 12/something/else.',
    'Navigate to foo/bar/baz.',
    'Check /var/log/app/error.txt.',
    'Located at /home/user/documents/report.',
    'Path: /usr/local/share/2024.',
    'Backup in /data/backups/archive.',
    'Logs at /var/log/2024/01/.',
    'Source: /opt/myapp/config/settings.',
    'Artifact: build/outputs/release.',
    'File at 99/foo/bar.',
    'Dir: a1/b2/c3.',
    'Relative: ./src/main/java.',
    'URL path: /api/v1/users.',
    'Route: /orders/2024/list.',
    'Endpoint: /v2/reports/summary.',
    'Resource: /assets/images/logo.png.',
    'CDN: /static/js/bundle.min.js.',
    'Archive: /backup/2024/01/dump.sql.',
    'Config at /etc/myapp/settings.conf.',
    'Log entry in /var/log/syslog.',
    'Data at /mnt/data/raw/input.',
    'Output to /tmp/results/run.',
    'Import from /imports/batch/file.csv.',
    'Cache at /cache/v1/index.',
])
def test_false_positive_file_paths(text):
    """
    False positive guard: slash-delimited file paths must not trigger date extraction.

    Attack vector: File and URL paths use the forward slash as a structural
    delimiter, the same character used in MM/DD/YYYY date notation. Paths
    containing numeric directory names (e.g., /var/log/2024/01/) can look
    superficially similar to partial date strings.

    Why a parser might fail: A path-unaware parser that searches for
    slash-delimited numeric sequences will encounter path components and
    attempt to interpret them as date fields. If the parser does not validate
    that the matched sequence is surrounded by word boundaries appropriate for
    dates (not preceded by alphanumeric path context), false positives occur.

    Failure reveals: The parser boundary anchoring or context-awareness is
    insufficient to suppress matches within file path token sequences.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 7 -- FALSE POSITIVES: PHONE / ISBN / HYPHEN IDENTIFIERS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Hyphen-delimited numeric identifiers (ISBN, phone numbers, product codes)
    # share the structural shape of hyphen-delimited dates.
    'ISBN: 0-306-40615-2.',
    'ISBN-13: 978-3-16-148410-0.',
    'ISBN: 978-0-306-40615-7.',
    'Call us at 555-867-5309.',
    'Toll free: 800-555-0199.',
    'Fax: 212-555-0100.',
    'International: +1-800-555-0199.',
    'Product code: A1-2023-XYZ.',
    'Serial: 1234-5678-9012.',
    'License: ABCD-1234-EFGH-5678.',
    'Order: ORD-2024-001.',
    'Ticket: TKT-001-2025.',
    'Reference: REF-12345-67890.',
    'Case: CASE-2024-001.',
    'Part number: PN-01-2345.',
    'Barcode: 123-45-6789.',
    'SKU: SKU-001-2024-A.',
    'UPC: 01234-56789.',
    'EAN: 4-012345-678901.',
    'ISSN: 0378-5955.',
    'Social security: 123-45-6789.',
    'Driver license: D1234-56789-0.',
    'Employee ID: EMP-001-2024.',
    'Contract ref: CR-2024-00042.',
    'Purchase order: PO-2024-0001.',
])
def test_false_positive_phone_isbn_identifiers(text):
    """
    False positive guard: phone numbers, ISBNs, and hyphen-joined IDs must
    not be classified as dates.

    Attack vector: Hyphen-delimited numeric identifiers. Phone numbers in
    NANP format (NXX-NXX-XXXX) have three hyphen-separated components,
    similar to MM-DD-YYYY. ISBNs have four components but the first is a
    known prefix (978, 979, 0, etc.) that falls in month-range.

    Why a parser might fail: A parser that tokenizes on hyphens and validates
    only that there are three numeric groups may match the first three
    components of a phone number. Similarly, a partial-ISBN match on 978-3-16
    could confuse the parser into treating 3 as a month and 16 as a day.

    Failure reveals: The parser lacks field-width and component-count
    validation that would disambiguate these from calendar dates.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 8 -- BOUNDARY: YEAR RANGE ENFORCEMENT
# ===========================================================================

@pytest.mark.parametrize('text, expect_match', [
    # Year boundary enforcement tests. The parser supports years [1926, 2036].
    # These tests probe the exact boundaries and the values immediately outside.
    ('Event on 01/01/1926.', True),
    ('Event on 12/31/2036.', True),
    ('Filed 06/15/1926.', True),
    ('Filed 06/15/2036.', True),
    ('Event on 01/01/1925.', False),
    ('Filed 12/31/1924.', False),
    ('Filed 01/01/1900.', False),
    ('Filed 12/31/1800.', False),
    ('Event on 01/01/2037.', False),
    ('Filed 12/31/2038.', False),
    ('Filed 01/01/2100.', False),
    ('Filed 12/31/9999.', False),
    ('Filed 06/15/1980.', True),
    ('Filed 06/15/2000.', True),
    ('Filed 06/15/2024.', True),
    ('Filed 01/01/1927.', True),
    ('Filed 12/31/2035.', True),
    ('Filed 07/04/1976.', True),
    ('Filed 06/06/1944.', True),
    ('Filed 11/11/1935.', True),
])
def test_boundary_year_range(text, expect_match):
    """
    Boundary: year range enforcement at min=1926 and max=2036.

    Attack vector: Dates with years at or beyond the documented supported
    range. The parser claims to support years [1926, 2036]. Years outside
    this range should be rejected; years at the exact boundary must be
    accepted. Off-by-one errors at range boundaries are a classic parser bug.

    Why a parser might fail: Boundary conditions (<= vs <, >= vs >) are
    notoriously prone to implementation error. A parser using strict inequality
    (year > 1926) instead of non-strict (year >= 1926) would incorrectly
    reject the minimum boundary year.

    Failure reveals: The year boundary condition uses an incorrect comparator
    (off-by-one), causing the boundary years to be wrongly rejected or accepted.
    """
    result = extract_explicit_dates(text)
    if expect_match:
        assert len(result) > 0, f'Expected match for: {text!r}'
    else:
        assert len(result) == 0, f'Expected no match for: {text!r}'


# ===========================================================================
# SECTION 9 -- BOUNDARY: CALENDAR LOGIC (INVALID DATES)
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Calendar-invalid dates -- structurally match but are impossible calendar values.
    'Filed on 01/00/2024.',
    'Filed on 00/01/2024.',
    'Filed on 13/01/2024.',
    'Filed on 01/32/2024.',
    'Filed on 02/30/2024.',
    'Filed on 02/31/2024.',
    'Filed on 04/31/2024.',
    'Filed on 06/31/2024.',
    'Filed on 09/31/2024.',
    'Filed on 11/31/2024.',
    'Filed on 99/99/9999.',
    'Filed on 13/32/2024.',
    'Filed on 02/29/2023.',
    'Filed on 02/29/1900.',
    'Filed on 02/29/1800.',
    'Filed on 02/29/1700.',
    'Filed on 12/00/2024.',
    'Filed on 00/31/2024.',
    'Filed on 13/13/2024.',
])
def test_boundary_calendar_invalid(text):
    """
    Boundary: calendar-invalid dates must be rejected.

    Attack vector: Syntactically valid date strings that represent impossible
    calendar values. Examples include month=0, day=0, month=13, day=32,
    February 30, April 31, and non-leap-year February 29.

    Why a parser might fail: Parsers that operate purely at the lexical level
    (matching digit patterns) without a semantic validation pass will accept
    any three-component numeric sequence whose components fall in a loose
    numeric range. Without calendar-logic validation (including Gregorian
    leap-year rules), invalid dates pass through undetected.

    Failure reveals: The parser does not apply calendar-logic validation after
    pattern matching, meaning it will accept impossible dates and potentially
    confuse downstream consumers that rely on the parsed date being a real
    calendar date.
    """
    result = extract_explicit_dates(text)
    assert len(result) == 0


# ===========================================================================
# SECTION 10 -- BOUNDARY: VALID LEAP YEAR FEBRUARY 29
# ===========================================================================

@pytest.mark.parametrize('text', [
    # February 29 is valid only in leap years.
    # 2024 is a leap year (divisible by 4, not by 100).
    # 2000 is a leap year (divisible by 400).
    'Filed on 02/29/2024.',
    'Filed on 02/29/2000.',
    'Filed on 02/29/2028.',
    'Filed on 02/29/1928.',
    'Filed on 02/29/1932.',
    'Filed on 02/29/1936.',
    'Filed on 02/29/1940.',
    'Filed on 02/29/1980.',
])
def test_boundary_valid_leap_year_feb29(text):
    """
    Boundary: February 29 in valid leap years must be accepted.

    Attack vector: February 29 is the rarest calendar date and the one most
    often handled incorrectly in date parsers. The Gregorian leap year rule
    has three nested conditions (div-4, div-100, div-400) and parsers
    frequently implement only the first condition (div-4), missing the
    century correction.

    Why a parser might fail: The parser correctly validates February 29 exists
    only in leap years but either rejects all Feb 29 dates, accepts only the
    simple div-4 case and rejects the div-400 case, or applies no leap year
    check at all.

    Failure reveals: The leap year validation logic is absent, incomplete, or
    incorrectly applied to the div-100/div-400 century correction cases.
    """
    result = extract_explicit_dates(text)
    assert len(result) > 0


# ===========================================================================
# SECTION 11 -- UNICODE ATTACKS: HOMOGLYPHS AND ALTERNATE SCRIPTS
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Full-width digits (Unicode block: Fullwidth Digit, U+FF10..U+FF19).
    # These are visually identical to ASCII digits but have different code points.
    'Filed on ０４/０８/２０２４.',
    # Arabic-Indic digits (U+0660..U+0669) -- used in Arabic, Persian, Urdu scripts.
    'Filed on ٠٤/٠٨/٢٠٢٤.',
    # Mathematical division slash (U+2215) homoglyph for /
    'Filed on 04∕08∕2024.',
    # Zero-width space (U+200B) injected between date components.
    'Filed on 04/0​8/2024.',
    'Filed on 04​/08/2024.',
    # RTL override (U+202E) prefix
    'Filed on ‮04/08/2024.',
    # Non-breaking hyphen (U+2011)
    'Filed on 04‑08‑2024.',
    # En-dash (U+2013)
    'Filed on 04–08–2024.',
    # Em-dash (U+2014)
    'Filed on 04—08—2024.',
    # Soft hyphen (U+00AD)
    'Filed on 04­08­2024.',
    # Zero-width joiner (U+200D) between digits
    'Filed on 04/‍08/2024.',
    # Right-to-left mark (U+200F) before date
    'Filed on ‏04/08/2024.',
])
def test_unicode_attacks(text):
    """
    Unicode attack: homoglyph and alternate script substitutions.

    Attack vector: Unicode contains many characters that are visually
    indistinguishable from or closely resemble ASCII punctuation and digits.
    Adversarial inputs may substitute full-width digits, Arabic-Indic numerals,
    mathematical division slashes, non-breaking hyphens, en-dashes, em-dashes,
    zero-width spaces, and directional override characters.

    Why a parser might fail: Regex-based parsers anchored to ASCII character
    classes ([0-9], [-/\.]) will silently fail to match Unicode homoglyphs.
    Conversely, parsers that normalize Unicode before matching may normalize
    homoglyphs to their ASCII equivalents -- which could be either correct
    behavior (normalization is desirable) or a security concern depending on
    the application.

    These tests are informational: we assert only that the parser does not
    throw an exception, since the correct match/no-match outcome is product-
    defined by the normalization policy.

    Failure reveals: The parser raises an unhandled exception on Unicode input.
    """
    try:
        result = extract_explicit_dates(text)
        assert isinstance(result, dict)
    except Exception as exc:
        pytest.fail(
            f'Parser raised exception on Unicode input: {exc!r}\nInput: {text!r}'
        )


# ===========================================================================
# SECTION 12 -- ALL MONTHS: DAY RANGE COVERAGE (SLASH)
# ===========================================================================

@pytest.mark.parametrize('month,max_day', [
    (1, 31), (2, 28), (3, 31), (4, 30),
    (5, 31), (6, 30), (7, 31), (8, 31),
    (9, 30), (10, 31), (11, 30), (12, 31),
])
def test_true_positive_month_day_range(month, max_day):
    """
    True positive: first and last day of every month must be detected.

    Attack vector: Month-specific day-range limits. Different months have
    different maximum day counts (28/29/30/31), and a parser must correctly
    handle dates at both ends of each month range.

    Why a parser might fail: Parsers that implement a single global day
    upper bound (e.g., day <= 31) without month-awareness will accept invalid
    dates like April 31, but may also incorrectly reject valid dates at
    month boundaries if the bound is set too conservatively.

    Failure reveals: Month-specific day bounds are not correctly applied,
    either accepting invalid end-of-month dates or rejecting valid ones.
    """
    first = f'{month:02d}/01/2024'
    last = f'{month:02d}/{max_day:02d}/2024'
    for date_str in [first, last]:
        result = extract_explicit_dates(f'Filed on {date_str}.')
        assert len(result) > 0, f'Expected match for valid date: {date_str}'


# ===========================================================================
# SECTION 13 -- MIXED DELIMITER IN SAME SENTENCE
# ===========================================================================

@pytest.mark.parametrize('text', [
    # Sentences containing multiple dates with different delimiters.
    # The parser must correctly identify all dates regardless of which
    # delimiter each uses.
    'Compare 04/08/2024 with 04-08-2024.',
    'The slash date 01/15/2023 and dot date 01.15.2023 are the same.',
    'From 03-01-2024 to 03/31/2024.',
    'Both 12.31.2023 and 12/31/2023 are year-end.',
    'Filed 06-05-2016 and updated 06/05/2016.',
    'Event 05.01.2024 confirmed; see also 05-01-2024.',
    'Issued 01/01/2024; renewed 01-01-2025.',
    'Quarter start 07/01/2024 and end 09.30.2024.',
])
def test_true_positive_mixed_delimiters_in_sentence(text):
    """
    True positive: multiple dates with different delimiters in one sentence.

    Attack vector: A sentence containing two or more date references that
    use different delimiter characters. The parser must not experience
    delimiter-conflict where matching one format suppresses recognition
    of another.

    Why a parser might fail: If the parser uses a first-match strategy
    (find first date, return), it will miss the second date. If the parser
    state machine is confused by the delimiter switch mid-sentence, it may
    produce partial or incorrect matches.

    Failure reveals: The multi-date extraction loop either short-circuits
    after the first match or has state contamination between delimiter modes.
    """
    result = extract_explicit_dates(text)
    assert len(result) >= 2, f'Expected at least 2 dates in: {text!r}'
