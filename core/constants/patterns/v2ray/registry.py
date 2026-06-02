from core.constants.patterns.v2ray.url import (
    PATTERN_URL_ANYTLS,
    PATTERN_URL_HYSTERIA2,
    PATTERN_URL_SS,
    PATTERN_URL_SS_BASE64,
    PATTERN_URL_SSR_BASE64,
    PATTERN_URL_TROJAN,
    PATTERN_URL_TUIC,
    PATTERN_URL_VLESS,
    PATTERN_URL_VMESS,
    PATTERN_URL_VMESS_BASE64,
    PATTERN_URL_WIREGUARD,
)
from core.typing import (
    V2RayPatternsByProtocol,
)

__all__ = [
    "PATTERNS_V2RAY_URLS_BY_PROTOCOL",
]

PATTERNS_V2RAY_URLS_BY_PROTOCOL: V2RayPatternsByProtocol = {
    "anytls": (
        PATTERN_URL_ANYTLS,
    ),
    "hy2": (
        PATTERN_URL_HYSTERIA2,
    ),
    "hysteria2": (
        PATTERN_URL_HYSTERIA2,
    ),
    "ss": (
        PATTERN_URL_SS,
        PATTERN_URL_SS_BASE64,
    ),
    "ssr": (
        PATTERN_URL_SSR_BASE64,
    ),
    "trojan": (
        PATTERN_URL_TROJAN,
    ),
    "tuic": (
        PATTERN_URL_TUIC,
    ),
    "vless": (
        PATTERN_URL_VLESS,
    ),
    "vmess": (
        PATTERN_URL_VMESS,
        PATTERN_URL_VMESS_BASE64,
    ),
    "wireguard": (
        PATTERN_URL_WIREGUARD,
    ),
}
