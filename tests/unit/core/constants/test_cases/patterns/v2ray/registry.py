import pytest

from tests.unit.core.constants.examples.patterns.v2ray.registry import (
    V2RAY_PATTERNS_BY_PROTOCOL_MATCH_EXAMPLES,
    V2RAY_PATTERNS_BY_PROTOCOL_VALID_EXAMPLES,
)

__all__ = [
    "V2RAY_PATTERNS_BY_PROTOCOL_MATCH_ARGS",
    "V2RAY_PATTERNS_BY_PROTOCOL_MATCH_CASES",
    "V2RAY_PATTERNS_BY_PROTOCOL_VALID_ARGS",
    "V2RAY_PATTERNS_BY_PROTOCOL_VALID_CASES",
]

V2RAY_PATTERNS_BY_PROTOCOL_MATCH_ARGS: tuple[
    str,
    ...,
] = (
    "protocol",
    "text",
)
V2RAY_PATTERNS_BY_PROTOCOL_MATCH_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        protocol,
        text,
        id=f"protocol_{protocol}",
    )
    for (
        protocol,
        text,
    ) in V2RAY_PATTERNS_BY_PROTOCOL_MATCH_EXAMPLES
)

V2RAY_PATTERNS_BY_PROTOCOL_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "protocol",
    "expected_count",
)
V2RAY_PATTERNS_BY_PROTOCOL_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        protocol,
        expected_count,
        id=f"protocol_{protocol}",
    )
    for (
        protocol,
        expected_count,
    ) in V2RAY_PATTERNS_BY_PROTOCOL_VALID_EXAMPLES
)
