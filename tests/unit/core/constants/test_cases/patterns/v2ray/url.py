import pytest

from core.constants.patterns.v2ray.detector import (
    PATTERN_V2RAY_URL_DETECTOR,
)
from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from tests.unit.core.constants.examples.patterns.v2ray.url import (
    V2RAY_URL_PATTERNS_INVALID_EXAMPLES,
    V2RAY_URL_PATTERNS_VALID_EXAMPLES,
)

__all__ = [
    "V2RAY_URL_PATTERNS_INVALID_ARGS",
    "V2RAY_URL_PATTERNS_INVALID_CASES",
    "V2RAY_URL_PATTERNS_VALID_ARGS",
    "V2RAY_URL_PATTERNS_VALID_CASES",
]

V2RAY_URL_PATTERNS_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "pattern",
    "text",
)
V2RAY_URL_PATTERNS_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        pattern,
        text,
        id=case_id,
    )
    for (
        text,
        case_id,
    ) in V2RAY_URL_PATTERNS_INVALID_EXAMPLES
    for url_match in PATTERN_V2RAY_URL_DETECTOR.finditer(
        string=text,
    )
    for pattern in PATTERNS_V2RAY_URLS_BY_PROTOCOL.get(
        url_match.group("protocol"),
        (),
    )
)

V2RAY_URL_PATTERNS_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "pattern",
    "text",
    "expected",
)
V2RAY_URL_PATTERNS_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        pattern,
        text,
        expected,
        id=case_id,
    )
    for (
        pattern,
        text,
        expected,
        case_id,
    ) in V2RAY_URL_PATTERNS_VALID_EXAMPLES
)
