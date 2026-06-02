__all__ = [
    "V2RAY_URL_DETECTOR_INVALID_EXAMPLES",
    "V2RAY_URL_DETECTOR_VALID_EXAMPLES",
]

V2RAY_URL_DETECTOR_INVALID_EXAMPLES: tuple[
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
        "vmess://",
        "empty_body",
    ),
    (
        "random text",
        "plain_text",
    ),
    (
        "https://example.com",
        "unsupported_protocol",
    ),
)


V2RAY_URL_DETECTOR_VALID_EXAMPLES: tuple[
    tuple[
        str,
        str,
        str,
        str,
        str,
    ],
    ...,
] = (
    (
        "trojan://password@example.com:443",
        "trojan://password@example.com:443",
        "trojan",
        "password@example.com:443",
        "simple_trojan",
    ),
    (
        "vmess://eyJhZGQiOiJleGFtcGxlLmNvbSJ9",
        "vmess://eyJhZGQiOiJleGFtcGxlLmNvbSJ9",
        "vmess",
        "eyJhZGQiOiJleGFtcGxlLmNvbSJ9",
        "simple_vmess",
    ),
    (
        "vmess://abc vless://def",
        "vmess://abc",
        "vmess",
        "abc",
        "stops_before_next_protocol",
    ),
    (
        "prefix vless://uuid@example.com:443 suffix",
        "vless://uuid@example.com:443",
        "vless",
        "uuid@example.com:443",
        "vless_with_noise",
    ),
)
