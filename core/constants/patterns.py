from re import (
    DOTALL,
)
from re import (
    compile as re_compile,
)

__all__ = [
    "PATTERNS_V2RAY_URLS_BY_PROTOCOL",
    "PATTERN_CONFIG_FIELD",
    "PATTERN_PARAM_SEPARATOR",
    "PATTERN_TG_CHANNEL_NAME",
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
    "PATTERN_V2RAY_PROTOCOLS_URL",
    "PATTERN_VMESS_JSON",
]

PATTERN_CONFIG_FIELD = re_compile(
    r"\w+(?:\.\w+)*",
)
PATTERN_PARAM_SEPARATOR = re_compile(
    r"\s*,\s*|\s+",
)
PATTERN_TG_CHANNEL_NAME = re_compile(
    r"\bhttps?://t\.me/(?:s/)?([\w]+)",
)
PATTERN_V2RAY_PROTOCOLS_URL = re_compile(
    r"(?P<url>"
        r"(?P<protocol>"
            r"anytls"
        r"|"
            r"hy2"
        r"|"
            r"hysteria2"
        r"|"
            r"ss"
        r"|"
            r"ssr"
        r"|"
            r"trojan"
        r"|"
            r"tuic"
        r"|"
            r"vless"
        r"|"
            r"vmess"
        r"|"
            r"wireguard"
        r")://"
        r"(?P<body>"
            r"(?:"
                r"(?!"
                    r"://"
                r"|"
                    r"(?:"
                        r"anytls"
                    r"|"
                        r"hy2"
                    r"|"
                        r"hysteria2"
                    r"|"
                        r"ss"
                    r"|"
                        r"ssr"
                    r"|"
                        r"trojan"
                    r"|"
                        r"tuic"
                    r"|"
                        r"vless"
                    r"|"
                        r"vmess"
                    r"|"
                        r"wireguard"
                    r")://"
                r")\S"
            r")+"
        r")"
    r")",
)
PATTERN_VMESS_JSON = re_compile(
    r"(?P<json>"
        r"{"
            r".*"
        r"}"
    r")",
    DOTALL,
)

# anytls://password@host:port/path?params#name
# anytls://password@host:port?params#name
PATTERN_URL_ANYTLS = re_compile(
    r"(?P<url>"
        r"(?P<protocol>anytls)://"
        r"(?P<password>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# hy2://password@host:port/path?params#name
# hy2://password@host:port?params#name
# hysteria2://password@host:port/path?params#name
# hysteria2://password@host:port?params#name
PATTERN_URL_HYSTERIA2 = re_compile(
    r"(?P<url>"
        r"(?P<protocol>hy2|hysteria2)://"
        r"(?P<password>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# ss://method:password@host:port#name
# ss://method:password@host:port/path?params#name
PATTERN_URL_SS = re_compile(
    r"(?P<url>(?P<protocol>\bss)://"
        r"(?P<method>[^\s:@#]+)"
        r":(?P<password>(?:(?!//).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# ss://base64(method:password)@host:port#name
# ss://base64(method:password)@host:port/path?params#name
# ss://base64(method:password@host:port)#name
PATTERN_URL_SS_BASE64 = re_compile(
    r"(?P<url>(?P<protocol>\bss)://"
        r"(?P<base64>[\w+/\-]+={0,2})(?![^\s@#])"
        r"(?:"
            r"@(?P<host>[\w\-\[:%\].]+)"
            r":(?P<port>\d{1,5})"
            r"(?P<path>/[^\s?#]*){0,1}"
            r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
PATTERN_URL_SSR_BASE64 = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ssr)://"
        r"(?P<base64>[\w+/\-]+={0,2})(?![^\s#])"
    r")",
)

# ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
PATTERN_URL_SSR_PLAIN = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ssr)://"
        r"(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r":(?P<origin>[^\s:]+)"
        r":(?P<method>[^\s:]+)"
        r":(?P<obfs>[^\s:]+)"
        r":(?P<password>(?:[\w+\-]|/(?!\?))+={0,2})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
    r")",
)

# trojan://password@host:port/path?params#name
# trojan://password@host:port?params#name
PATTERN_URL_TROJAN = re_compile(
    r"(?P<url>"
        r"(?P<protocol>trojan)://"
        r"(?P<password>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# tuic://uuid:password@host:port/path?params#name
# tuic://uuid:password@host:port?params#name
PATTERN_URL_TUIC = re_compile(
    r"(?P<url>"
        r"(?P<protocol>tuic)://"
        r"(?P<uuid>(?:(?!://).)+)"
        r":(?P<password>(?:(?!//).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# vless://uuid@host:port/path?params#name
# vless://uuid@host:port?params#name
PATTERN_URL_VLESS = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vless)://"
        r"(?P<uuid>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
PATTERN_URL_VMESS = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vmess)://"
        r"(?P<uuid>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

# vmess://base64(json)
PATTERN_URL_VMESS_BASE64 = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vmess)://"
        r"(?P<base64>[\w+/\-]+={0,2})(?![^\s#])"
    r")",
)

# wireguard://privatekey@host:port/path?params#name
# wireguard://privatekey@host:port?params#name
PATTERN_URL_WIREGUARD = re_compile(
    r"(?P<url>"
        r"(?P<protocol>wireguard)://"
        r"(?P<privatekey>(?:(?!://).)+)"
        r"@(?P<host>[\w\-\[:%\].]+)"
        r":(?P<port>\d{1,5})"
        r"(?P<path>/[^\s?#]*){0,1}"
        r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
        r"(?P<name>){0,1}"
    r")",
)

PATTERNS_V2RAY_URLS_BY_PROTOCOL = {
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
