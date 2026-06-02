import pytest

from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from tests.unit.core.constants.test_cases.patterns.v2ray.registry import (
    V2RAY_PATTERNS_BY_PROTOCOL_MATCH_ARGS,
    V2RAY_PATTERNS_BY_PROTOCOL_MATCH_CASES,
    V2RAY_PATTERNS_BY_PROTOCOL_VALID_ARGS,
    V2RAY_PATTERNS_BY_PROTOCOL_VALID_CASES,
)


def test_patterns_v2ray_urls_by_protocol_hy2_alias() -> None:
    pattern_hy2 = PATTERNS_V2RAY_URLS_BY_PROTOCOL.get("hy2")
    pattern_hysteria2 = PATTERNS_V2RAY_URLS_BY_PROTOCOL.get("hysteria2")

    assert pattern_hy2 == pattern_hysteria2


def test_patterns_v2ray_urls_by_protocol_keys() -> None:
    assert set(PATTERNS_V2RAY_URLS_BY_PROTOCOL) == {
        "anytls",
        "hy2",
        "hysteria2",
        "ss",
        "ssr",
        "trojan",
        "tuic",
        "vless",
        "vmess",
        "wireguard",
    }


@pytest.mark.parametrize(
    V2RAY_PATTERNS_BY_PROTOCOL_MATCH_ARGS,
    V2RAY_PATTERNS_BY_PROTOCOL_MATCH_CASES,
)
def test_patterns_v2ray_urls_by_protocol_match(
    protocol: str,
    text: str,
) -> None:
    patterns = PATTERNS_V2RAY_URLS_BY_PROTOCOL.get(protocol, ())

    assert any(
        pattern.search(text) is not None
        for pattern in patterns
    )


@pytest.mark.parametrize(
    V2RAY_PATTERNS_BY_PROTOCOL_VALID_ARGS,
    V2RAY_PATTERNS_BY_PROTOCOL_VALID_CASES,
)
def test_patterns_v2ray_urls_by_protocol_valid(
    protocol: str,
    expected_count: int,
) -> None:
    patterns = PATTERNS_V2RAY_URLS_BY_PROTOCOL.get(protocol)

    assert patterns is not None
    assert len(patterns) == expected_count
