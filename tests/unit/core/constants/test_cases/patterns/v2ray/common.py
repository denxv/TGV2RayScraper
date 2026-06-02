import pytest

from tests.unit.core.constants.examples.patterns.v2ray.common import (
    VMESS_JSON_INVALID_EXAMPLES,
    VMESS_JSON_VALID_EXAMPLES,
)

__all__ = [
    "VMESS_JSON_INVALID_ARGS",
    "VMESS_JSON_INVALID_CASES",
    "VMESS_JSON_VALID_ARGS",
    "VMESS_JSON_VALID_CASES",
]

VMESS_JSON_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
)
VMESS_JSON_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        text,
        id=case_id,
    )
    for (
        text,
        case_id,
    ) in VMESS_JSON_INVALID_EXAMPLES
)

VMESS_JSON_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
    "expected",
)
VMESS_JSON_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        text,
        expected,
        id=case_id,
    )
    for (
        text,
        expected,
        case_id,
    ) in VMESS_JSON_VALID_EXAMPLES
)
