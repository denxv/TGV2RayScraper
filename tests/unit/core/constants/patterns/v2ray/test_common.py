import pytest

from core.constants.patterns.v2ray.common import (
    PATTERN_VMESS_JSON,
)
from tests.unit.core.constants.test_cases.patterns.v2ray.common import (
    VMESS_JSON_INVALID_ARGS,
    VMESS_JSON_INVALID_CASES,
    VMESS_JSON_VALID_ARGS,
    VMESS_JSON_VALID_CASES,
)


@pytest.mark.parametrize(
    VMESS_JSON_INVALID_ARGS,
    VMESS_JSON_INVALID_CASES,
)
def test_pattern_vmess_json_invalid(
    text: str,
) -> None:
    match = PATTERN_VMESS_JSON.search(text)

    assert match is None


@pytest.mark.parametrize(
    VMESS_JSON_VALID_ARGS,
    VMESS_JSON_VALID_CASES,
)
def test_pattern_vmess_json_valid(
    text: str,
    expected: str,
) -> None:
    match = PATTERN_VMESS_JSON.search(text)

    assert match is not None
    assert match.group("json") == expected
