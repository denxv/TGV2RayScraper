from re import (
    compile as re_compile,
)

from core.typing import (
    CompiledRegex,
    RegexPattern,
)

__all__ = [
    "PATTERN_URL_ANYTLS",
    "PATTERN_URL_HYSTERIA2",
    "PATTERN_URL_SS",
    "PATTERN_URL_SSR_BASE64",
    "PATTERN_URL_SSR_PLAIN",
    "PATTERN_URL_SS_BASE64",
    "PATTERN_URL_TROJAN",
    "PATTERN_URL_TUIC",
    "PATTERN_URL_VLESS",
    "PATTERN_URL_VMESS",
    "PATTERN_URL_VMESS_BASE64",
    "PATTERN_URL_WIREGUARD",
]

_REGEX_URL_BASE64: RegexPattern = (
    r"(?P<base64>[\w+/]+={0,2})"
)
_REGEX_URL_HOST: RegexPattern = (
    r"(?P<host>[\w\-\[:%\].]+)"
)
_REGEX_URL_METHOD: RegexPattern = (
    r"(?P<method>[^\s:@#]+)"
)
_REGEX_URL_NAME: RegexPattern = (
    r"(?:#(?P<name>.*))?"
)
_REGEX_URL_PARAMS: RegexPattern = (
    r"(?:\?(?P<params>[^\s#]*))?"
)
_REGEX_URL_PASSWORD: RegexPattern = (
    r"(?P<password>.+)"  # noqa: S105
)
_REGEX_URL_PATH: RegexPattern = (
    r"(?P<path>/[^\s?#]*)?"
)
_REGEX_URL_PORT: RegexPattern = (
    r"(?P<port>\d{1,5})"
)
_REGEX_URL_PRIVATE_KEY: RegexPattern = (
    r"(?P<privatekey>.+)"
)
_REGEX_URL_UUID: RegexPattern = (
    r"(?P<uuid>.+)"
)

_REGEX_URL_HOST_PORT: RegexPattern = (
    rf"{_REGEX_URL_HOST}"
    r":"
    rf"{_REGEX_URL_PORT}"
)
_REGEX_URL_HOST_PORT_PATH_PARAMS: RegexPattern = (
    rf"{_REGEX_URL_HOST_PORT}"
    rf"{_REGEX_URL_PATH}"
    rf"{_REGEX_URL_PARAMS}"
)

# anytls://password@host:port/path?params#name
# anytls://password@host:port?params#name
PATTERN_URL_ANYTLS: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>anytls)://"
        r"(?P<body>"
            rf"{_REGEX_URL_PASSWORD}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# hy2://password@host:port/path?params#name
# hy2://password@host:port?params#name
# hysteria2://password@host:port/path?params#name
# hysteria2://password@host:port?params#name
PATTERN_URL_HYSTERIA2: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>hy2|hysteria2)://"
        r"(?P<body>"
            rf"{_REGEX_URL_PASSWORD}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# ss://method:password@host:port#name
# ss://method:password@host:port/path?params#name
PATTERN_URL_SS: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ss)://"
        r"(?P<body>"
            rf"{_REGEX_URL_METHOD}"
            r":"
            rf"{_REGEX_URL_PASSWORD}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# ss://base64(method:password)@host:port#name
# ss://base64(method:password)@host:port/path?params#name
# ss://base64(method:password@host:port)#name
PATTERN_URL_SS_BASE64: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ss)://"
        r"(?P<body>"
            rf"{_REGEX_URL_BASE64}"
            r"(?![^\s@#])"
            r"(?:"
                r"@"
                rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
            r")?"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
PATTERN_URL_SSR_BASE64: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ssr)://"
        r"(?P<body>"
            rf"{_REGEX_URL_BASE64}"
            r"(?![^\s#])"
        r")"
    r")",
)

# ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
PATTERN_URL_SSR_PLAIN: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ssr)://"
        r"(?P<body>"
            rf"{_REGEX_URL_HOST_PORT}"
            r":"
            r"(?P<origin>[^\s:]+)"
            r":"
            r"(?P<method>[^\s:]+)"
            r":"
            r"(?P<obfs>[^\s:]+)"
            r":"
            r"(?P<password>"
                r"(?:"
                    r"[\w+\-]"
                    r"|"
                    r"/(?!\?)"
                r")+={0,2}"
            r")"
            rf"{_REGEX_URL_PATH}"
            rf"{_REGEX_URL_PARAMS}"
        r")"
    r")",
)

# trojan://password@host:port/path?params#name
# trojan://password@host:port?params#name
PATTERN_URL_TROJAN: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>trojan)://"
        r"(?P<body>"
            rf"{_REGEX_URL_PASSWORD}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# tuic://uuid:password@host:port/path?params#name
# tuic://uuid:password@host:port?params#name
PATTERN_URL_TUIC: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>tuic)://"
        r"(?P<body>"
            rf"{_REGEX_URL_UUID}"
            r":"
            rf"{_REGEX_URL_PASSWORD}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# vless://uuid@host:port/path?params#name
# vless://uuid@host:port?params#name
PATTERN_URL_VLESS: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vless)://"
        r"(?P<body>"
            rf"{_REGEX_URL_UUID}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
PATTERN_URL_VMESS: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vmess)://"
        r"(?P<body>"
            rf"{_REGEX_URL_UUID}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)

# vmess://base64(json)
PATTERN_URL_VMESS_BASE64: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vmess)://"
        r"(?P<body>"
            rf"{_REGEX_URL_BASE64}"
            r"(?![^\s#])"
        r")"
    r")",
)

# wireguard://privatekey@host:port/path?params#name
# wireguard://privatekey@host:port?params#name
PATTERN_URL_WIREGUARD: CompiledRegex = re_compile(
    r"(?P<url>"
        r"(?P<protocol>wireguard)://"
        r"(?P<body>"
            rf"{_REGEX_URL_PRIVATE_KEY}"
            r"@"
            rf"{_REGEX_URL_HOST_PORT_PATH_PARAMS}"
        r")"
    r")"
    rf"{_REGEX_URL_NAME}",
)
