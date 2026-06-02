import pytest

from core.constants.patterns.v2ray.detector import (
    PATTERN_V2RAY_URL_DETECTOR,
)
from tests.unit.core.constants.test_cases.patterns.v2ray.detector import (
    V2RAY_URL_DETECTOR_INVALID_ARGS,
    V2RAY_URL_DETECTOR_INVALID_CASES,
    V2RAY_URL_DETECTOR_VALID_ARGS,
    V2RAY_URL_DETECTOR_VALID_CASES,
)


@pytest.mark.parametrize(
    V2RAY_URL_DETECTOR_INVALID_ARGS,
    V2RAY_URL_DETECTOR_INVALID_CASES,
)
def test_pattern_v2ray_url_detector_invalid(
    text: str,
) -> None:
    match = PATTERN_V2RAY_URL_DETECTOR.search(text)

    assert match is None


@pytest.mark.parametrize(
    V2RAY_URL_DETECTOR_VALID_ARGS,
    V2RAY_URL_DETECTOR_VALID_CASES,
)
def test_pattern_v2ray_url_detector_valid(
    text: str,
    expected_url: str,
    expected_protocol: str,
    expected_body: str,
) -> None:
    match = PATTERN_V2RAY_URL_DETECTOR.search(text)

    assert match is not None
    assert match.group("url") == expected_url
    assert match.group("protocol") == expected_protocol
    assert match.group("body") == expected_body
