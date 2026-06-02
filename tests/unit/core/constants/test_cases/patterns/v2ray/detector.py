import pytest

from tests.unit.core.constants.examples.patterns.v2ray.detector import (
    V2RAY_URL_DETECTOR_INVALID_EXAMPLES,
    V2RAY_URL_DETECTOR_VALID_EXAMPLES,
)

__all__ = [
    "V2RAY_URL_DETECTOR_INVALID_ARGS",
    "V2RAY_URL_DETECTOR_INVALID_CASES",
    "V2RAY_URL_DETECTOR_VALID_ARGS",
    "V2RAY_URL_DETECTOR_VALID_CASES",
]

V2RAY_URL_DETECTOR_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
)
V2RAY_URL_DETECTOR_INVALID_CASES: tuple[
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
    ) in V2RAY_URL_DETECTOR_INVALID_EXAMPLES
)


V2RAY_URL_DETECTOR_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
    "expected_url",
    "expected_protocol",
    "expected_body",
)
V2RAY_URL_DETECTOR_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        text,
        expected_url,
        expected_protocol,
        expected_body,
        id=case_id,
    )
    for (
        text,
        expected_url,
        expected_protocol,
        expected_body,
        case_id,
    ) in V2RAY_URL_DETECTOR_VALID_EXAMPLES
)
