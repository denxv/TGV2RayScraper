from re import compile

DEFAULT_CHANNEL_VALUES = {
    "count": 0,
    "current_id": 1,
    "last_id": -1,
}

DEFAULT_PATH_CHANNELS = "../channels/current.json"
DEFAULT_PATH_CONFIGS_CLEAN = "../configs/v2ray-clean.txt"
DEFAULT_PATH_CONFIGS_RAW = "../configs/v2ray-raw.txt"
DEFAULT_PATH_URLS = "../channels/urls.txt"

FORMAT_CONFIG_NAME = "{protocol}-{host}-{port}"
FURL_TG = "https://t.me/s/{name}"
FURL_TG_AFTER = FURL_TG + "?after={id}"
FURL_TG_BEFORE = FURL_TG + "?before={id}"

LEN_NAME = 32
LEN_NUMBER = 7
TOTAL_CHANNELS_POST = 0

SCRIPTS_CONFIG = {
    "update_channels": {
        "flags": [
            "--channels",
            "--urls",
        ],
        "mode": "any",
    },
    "async_scraper": {
        "flags": [
            "--batch-extract",
            "--batch-update",
            "--channels",
            "--configs-raw",
        ],
        "mode": "async",
    },
    "scraper": {
        "flags": [
            "--channels",
            "--configs-raw",
        ],
        "mode": "sync",
    },
    "v2ray_cleaner": {
        "flags": [
            "--configs-clean",
            "--configs-raw",
            "--duplicate",
            "--filter",
            "--no-normalize",
            "--reverse",
            "--sort",
        ],
        "mode": "any",
    },
}

XPATH_V2RAY = "//div[@class='tgme_widget_message_text js-message_text']//text()"
XPATH_POST_ID = "//div[@class='tgme_widget_message text_not_supported_wrap js-widget_message']/@data-post"

REGEX_CHANNELS_NAME = compile(r"http[s]?://t.me/[s/]{0,2}([\w]+)")
REGEX_V2RAY = compile(
    r'(?:'
        r'anytls'
    r'|'
        r'hy2'
    r'|'
        r'hysteria2'
    r'|'
        r'\bss\b'
    r'|'
        r'ssr'
    r'|'
        r'trojan'
    r'|'
        r'tuic'
    r'|'
        r'vless'
    r'|'
        r'vmess'
    r'|'
        r'wireguard'
    r')://(?:(?!://)[\S])+'
)

# anytls://password@host:port/path?params#name
# anytls://password@host:port?params#name
ANYTLS_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>anytls)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# hy2://password@host:port/path?params#name
# hy2://password@host:port?params#name
# hysteria2://password@host:port/path?params#name
# hysteria2://password@host:port?params#name
HYSTERIA2_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>hy2|hysteria2)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# ss://method:password@host:port#name
# ss://base64(method:password)@host:port#name
# ss://base64(method:password@host:port)#name
SS_URL_PATTERN = compile(
    r'(?P<url>(?P<protocol>\bss)://'
        r'(?:'
            r'(?P<method>[^\s:@#]+)'
            r':(?P<password>(?:(?!//).)+)(?=@)'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})(?![^\s@#])'
        r')'
        r'(?:'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
        r'){0,1}'
        r'(?=(?:[\s#]|$))(?!\?)'
        r'(?P<name>){0,1}'
    r')'
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
SSR_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>ssr)://'
        r'(?P<base64>[\w+/-]+={0,2})'
        r'(?P<name>){0,1}'
    r')'
)

# ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
SSR_PLAIN_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>ssr)://'
        r'(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r':(?P<origin>[^\s:]+)'
        r':(?P<method>[^\s:]+)'
        r':(?P<obfs>[^\s:]+)'
        r':(?P<password>[\w+/-]+={0,2})(?=/)'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
    r')'
)

# trojan://password@host:port/path?params#name
# trojan://password@host:port?params#name
TROJAN_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>trojan)://'
        r'(?P<password>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# tuic://uuid:password@host:port/path?params#name
# tuic://uuid:password@host:port?params#name
TUIC_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>tuic)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r':(?P<password>(?:(?!//).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# vless://uuid@host:port/path?params#name
# vless://uuid@host:port?params#name
VLESS_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>vless)://'
        r'(?P<uuid>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

# vmess://base64(json)
# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
VMESS_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>vmess)://'
        r'(?:'
            r'(?P<uuid>(?:(?!://).)+)'
            r'@(?P<host>[\w\-\[:%\].]+)'
            r':(?P<port>\d{1,5})'
            r'(?P<path>/[^\s?#]*){0,1}'
            r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
            r'(?P<name>){0,1}'
        r'|'
            r'(?P<base64>[\w+/]+={0,2})'
        r')'
    r')'
)

# wireguard://privatekey@host:port/path?params#name
# wireguard://privatekey@host:port?params#name
WIREGUARD_URL_PATTERN = compile(
    r'(?P<url>'
        r'(?P<protocol>wireguard)://'
        r'(?P<privatekey>(?:(?!://).)+)'
        r'@(?P<host>[\w\-\[:%\].]+)'
        r':(?P<port>\d{1,5})'
        r'(?P<path>/[^\s?#]*){0,1}'
        r'(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}'
        r'(?P<name>){0,1}'
    r')'
)

URL_PATTERNS = [
    ANYTLS_URL_PATTERN,
    HYSTERIA2_URL_PATTERN,
    SS_URL_PATTERN,
    SSR_URL_PATTERN,
    TROJAN_URL_PATTERN,
    TUIC_URL_PATTERN,
    VLESS_URL_PATTERN,
    VMESS_URL_PATTERN,
    WIREGUARD_URL_PATTERN,
]
