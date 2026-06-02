import pytest

from core.typing import (
    CompiledRegex,
)
from tests.unit.core.constants.test_cases.patterns.v2ray.url import (
    V2RAY_URL_PATTERNS_INVALID_ARGS,
    V2RAY_URL_PATTERNS_INVALID_CASES,
    V2RAY_URL_PATTERNS_VALID_ARGS,
    V2RAY_URL_PATTERNS_VALID_CASES,
)


@pytest.mark.parametrize(
    V2RAY_URL_PATTERNS_INVALID_ARGS,
    V2RAY_URL_PATTERNS_INVALID_CASES,
)
def test_v2ray_url_patterns_invalid(
    pattern: CompiledRegex,
    text: str,
) -> None:
    match = pattern.search(text)

    assert match is None


@pytest.mark.parametrize(
    V2RAY_URL_PATTERNS_VALID_ARGS,
    V2RAY_URL_PATTERNS_VALID_CASES,
)
def test_v2ray_url_patterns_valid(
    pattern: CompiledRegex,
    text: str,
    expected: dict[str, str | None],
) -> None:
    match = pattern.search(text)

    assert match is not None
    assert match.groupdict() == expected
