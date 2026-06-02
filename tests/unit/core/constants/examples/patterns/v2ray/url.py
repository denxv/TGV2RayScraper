from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
)
from core.constants.patterns.v2ray.url import (
    PATTERN_URL_ANYTLS,
    PATTERN_URL_HYSTERIA2,
    PATTERN_URL_SS,
    PATTERN_URL_SS_BASE64,
    PATTERN_URL_SSR_BASE64,
    PATTERN_URL_SSR_PLAIN,
    PATTERN_URL_TROJAN,
    PATTERN_URL_TUIC,
    PATTERN_URL_VLESS,
    PATTERN_URL_VMESS,
    PATTERN_URL_VMESS_BASE64,
    PATTERN_URL_WIREGUARD,
)
from core.typing import (
    CompiledRegex,
)

__all__ = [
    "V2RAY_URL_PATTERNS_INVALID_EXAMPLES",
    "V2RAY_URL_PATTERNS_VALID_EXAMPLES",
]

_BASE_INVALID: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    (
        "",
        "empty",
    ),
    (
        "random text",
        "no_match",
    ),
)

_BROKEN: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = tuple(
    (
        f"{name}://@@@",
        f"broken_{name}_format",
    )
    for name in PATTERNS_V2RAY_URLS_BY_PROTOCOL
)

_INCOMPLETE: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = tuple(
    (
        f"{name}://",
        f"incomplete_{name}",
    )
    for name in PATTERNS_V2RAY_URLS_BY_PROTOCOL
)

_WRONG_SCHEMES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = tuple(
    (
        f"{scheme}://example.com",
        f"wrong_scheme_{scheme}",
    )
    for scheme in (
        "ftp",
        "http",
        "https",
    )
)

V2RAY_URL_PATTERNS_INVALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
    ],
    ...,
] = (
    *_BASE_INVALID,
    *_BROKEN,
    *_INCOMPLETE,
    *_WRONG_SCHEMES,
)

V2RAY_URL_PATTERNS_VALID_EXAMPLES: tuple[
    tuple[
        CompiledRegex,
        str,
        dict[str, str | None],
        str,
    ],
    ...,
] = (
    (
        PATTERN_URL_ANYTLS,  # anytls://password@host:port/path?params#name
        "anytls://mypassword@example.com:443/api/v1?token=1&debug=true#protocol-anytls",
        {
            "url": "anytls://mypassword@example.com:443/api/v1?token=1&debug=true",
            "protocol": "anytls",
            "password": "mypassword",
            "host": "example.com",
            "port": "443",
            "path": "/api/v1",
            "params": "token=1&debug=true",
            "name": "",
        },
        "protocol_anytls_full",
    ),
    (
        PATTERN_URL_HYSTERIA2,  # hy2://password@host:port/path?params#name
        "hy2://secretpassword@example.com:443/?debug=true#protocol-hy2",
        {
            "url": "hy2://secretpassword@example.com:443/?debug=true",
            "protocol": "hy2",
            "password": "secretpassword",
            "host": "example.com",
            "port": "443",
            "path": "/",
            "params": "debug=true",
            "name": "",
        },
        "protocol_hy2_full_with_path_params",
    ),
    (
        PATTERN_URL_HYSTERIA2,  # hysteria2://password@host:port?params#name
        "hysteria2://secretpass@host.local:8443?token=TOKEN#protocol-hysteria2",
        {
            "url": "hysteria2://secretpass@host.local:8443?token=TOKEN",
            "protocol": "hysteria2",
            "password": "secretpass",
            "host": "host.local",
            "port": "8443",
            "path": None,
            "params": "token=TOKEN",
            "name": "",
        },
        "protocol_hysteria2_minimal_with_params",
    ),
    (
        PATTERN_URL_SS_BASE64,  # ss://base64(method:password)@host:port/path?params#name
        "ss://YWVzLTI1Ni1nY206cGFzczEyMw==@server1.example.com:8388/api/v1?udp=true#protocol-ss-base64",
        {
            "url": "ss://YWVzLTI1Ni1nY206cGFzczEyMw==@server1.example.com:8388/api/v1?udp=true",
            "protocol": "ss",
            "base64": "YWVzLTI1Ni1nY206cGFzczEyMw==",
            "host": "server1.example.com",
            "port": "8388",
            "path": "/api/v1",
            "params": "udp=true",
            "name": "",
        },
        "protocol_ss_base64_full_with_path_params",
    ),
    (
        PATTERN_URL_SS_BASE64,  # ss://base64(method:password@host:port)#name
        "ss://YWVzLTI1Ni1nY206cGFzcw==@10.0.0.5:443#protocol-ss-base64",
        {
            "url": "ss://YWVzLTI1Ni1nY206cGFzcw==@10.0.0.5:443",
            "protocol": "ss",
            "base64": "YWVzLTI1Ni1nY206cGFzcw==",
            "host": "10.0.0.5",
            "port": "443",
            "path": None,
            "params": None,
            "name": "",
        },
        "protocol_ss_base64_minimal",
    ),
    (
        PATTERN_URL_SS,  # ss://method:password@host:port/path?params#name
        "ss://aes-256-gcm:pass123@server1.example.com:8388/api/v1?udp=true#protocol-ss",
        {
            "url": "ss://aes-256-gcm:pass123@server1.example.com:8388/api/v1?udp=true",
            "protocol": "ss",
            "method": "aes-256-gcm",
            "password": "pass123",
            "host": "server1.example.com",
            "port": "8388",
            "path": "/api/v1",
            "params": "udp=true",
            "name": "",
        },
        "protocol_ss_full_with_path_params",
    ),
    (
        PATTERN_URL_SS,  # ss://method:password@host:port#name
        "ss://aes-256-gcm:pass123@server2.example.com:8388#protocol-ss",
        {
            "url": "ss://aes-256-gcm:pass123@server2.example.com:8388",
            "protocol": "ss",
            "method": "aes-256-gcm",
            "password": "pass123",
            "host": "server2.example.com",
            "port": "8388",
            "path": None,
            "params": None,
            "name": "",
        },
        "protocol_ss_minimal_no_path_no_params",
    ),
    (
        PATTERN_URL_SSR_BASE64,  # ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
        "ssr://c2VydmVyOjQ0Mzp0Y3A6YWVzLTI1Ni1jZmI6b3Blbjp0ZXN0cGFzc3dvcmQ=#protocol-ssr-base64",
        {
            "url": "ssr://c2VydmVyOjQ0Mzp0Y3A6YWVzLTI1Ni1jZmI6b3Blbjp0ZXN0cGFzc3dvcmQ=",
            "protocol": "ssr",
            "base64": "c2VydmVyOjQ0Mzp0Y3A6YWVzLTI1Ni1jZmI6b3Blbjp0ZXN0cGFzc3dvcmQ=",  # noqa: E501
        },
        "protocol_ssr_base64_basic",
    ),
    (
        PATTERN_URL_SSR_PLAIN,  # ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
        "ssr://example.com:443:origin:aes-256-cfb:plain:cGFzc3dvcmQ=/api/v1?remarks=cHJvdG9jb2wtc3NyLXBsYWluCg==",
        {
            "url": "ssr://example.com:443:origin:aes-256-cfb:plain:cGFzc3dvcmQ=/api/v1?remarks=cHJvdG9jb2wtc3NyLXBsYWluCg==",
            "protocol": "ssr",
            "host": "example.com",
            "port": "443",
            "origin": "origin",
            "method": "aes-256-cfb",
            "obfs": "plain",
            "password": "cGFzc3dvcmQ=",
            "path": "/api/v1",
            "params": "remarks=cHJvdG9jb2wtc3NyLXBsYWluCg==",
        },
        "protocol_ssr_plain_full",
    ),
    (
        PATTERN_URL_TROJAN,  # trojan://password@host:port/path?params#name
        "trojan://mypassword@trojan.example.com:443/api/v1?allowInsecure=1#protocol-trojan",
        {
            "url": "trojan://mypassword@trojan.example.com:443/api/v1?allowInsecure=1",
            "protocol": "trojan",
            "password": "mypassword",
            "host": "trojan.example.com",
            "port": "443",
            "path": "/api/v1",
            "params": "allowInsecure=1",
            "name": "",
        },
        "protocol_trojan_full",
    ),
    (
        PATTERN_URL_TUIC,  # tuic://uuid:password@host:port/path?params#name
        "tuic://550e8400-e29b-41d4-a716-446655440000:secretpass@tuic.example.com:443/api/v1?token=1#protocol-tuic",
        {
            "url": "tuic://550e8400-e29b-41d4-a716-446655440000:secretpass@tuic.example.com:443/api/v1?token=1",
            "protocol": "tuic",
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "password": "secretpass",
            "host": "tuic.example.com",
            "port": "443",
            "path": "/api/v1",
            "params": "token=1",
            "name": "",
        },
        "protocol_tuic_full",
    ),
    (
        PATTERN_URL_VLESS,  # vless://uuid@host:port/path?params#name
        "vless://550e8400-e29b-41d4-a716-446655440000@vless.example.com:443/api/v1?encryption=none&security=tls#protocol-vless",
        {
            "url": "vless://550e8400-e29b-41d4-a716-446655440000@vless.example.com:443/api/v1?encryption=none&security=tls",
            "protocol": "vless",
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "host": "vless.example.com",
            "port": "443",
            "path": "/api/v1",
            "params": "encryption=none&security=tls",
            "name": "",
        },
        "protocol_vless_full",
    ),
    (
        PATTERN_URL_VMESS,  # vmess://uuid@host:port/path?params#name
        "vmess://550e8400-e29b-41d4-a716-446655440000@vmess.example.com:443/api/v1?alterId=0&security=tls#protocol-vmess",
        {
            "url": "vmess://550e8400-e29b-41d4-a716-446655440000@vmess.example.com:443/api/v1?alterId=0&security=tls",
            "protocol": "vmess",
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "host": "vmess.example.com",
            "port": "443",
            "path": "/api/v1",
            "params": "alterId=0&security=tls",
            "name": "",
        },
        "protocol_vmess_full",
    ),
    (
        PATTERN_URL_VMESS_BASE64,  # vmess://base64(json)
        "vmess://eyJhZGQiOiJ2bWVzcy5leGFtcGxlLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6IjU1MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMCIsImFpZCI6IjAiLCJzY3kiOiJhdXRvIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSJ9",
        {
            "url": "vmess://eyJhZGQiOiJ2bWVzcy5leGFtcGxlLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6IjU1MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMCIsImFpZCI6IjAiLCJzY3kiOiJhdXRvIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSJ9",
            "protocol": "vmess",
            "base64": "eyJhZGQiOiJ2bWVzcy5leGFtcGxlLmNvbSIsInBvcnQiOiI0NDMiLCJpZCI6IjU1MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMCIsImFpZCI6IjAiLCJzY3kiOiJhdXRvIiwibmV0Ijoid3MiLCJ0eXBlIjoibm9uZSJ9",  # noqa: E501
        },
        "protocol_vmess_base64_full",
    ),
    (
        PATTERN_URL_WIREGUARD,  # wireguard://privatekey@host:port/path?params#name
        "wireguard://privatekey123@wg.example.com:51820/api/v1?keepalive=25#protocol-wireguard",
        {
            "url": "wireguard://privatekey123@wg.example.com:51820/api/v1?keepalive=25",
            "protocol": "wireguard",
            "privatekey": "privatekey123",
            "host": "wg.example.com",
            "port": "51820",
            "path": "/api/v1",
            "params": "keepalive=25",
            "name": "",
        },
        "protocol_wireguard_full",
    ),
)
