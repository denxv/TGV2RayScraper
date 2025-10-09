from argparse import SUPPRESS
from logging import DEBUG, INFO
from pathlib import Path
from re import compile, DOTALL

GET_ABS_PATH = lambda path: str((Path(__file__).parent / path).resolve())

DEFAULT_COUNT = 0
DEFAULT_CURRENT_ID = 1
DEFAULT_LAST_ID = -1
DEFAULT_POST_ID = 0

DEFAULT_CHANNEL_VALUES = {
    "count": DEFAULT_COUNT,
    "current_id": DEFAULT_CURRENT_ID,
    "last_id": DEFAULT_LAST_ID,
}

DEFAULT_INDENT = 4
DEFAULT_MIN_VALUE = 1
DEFAULT_MAX_VALUE = 100

BASE64_BLOCK_SIZE = 4
DEFAULT_LOG_LINE_LENGTH = 100

COLORS = {
    "DEBUG": "\033[37m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[31m",
    "RESET": "\033[0m",
}

DEFAULT_LOGGER_NAME = "TGV2RayScraper"
DEFAULT_CONSOLE_LOG_FORMAT = "<%(asctime)s> [%(colored_levelname)s] %(message)s"
DEFAULT_FILE_LOG_FORMAT    = "<%(asctime)s> [%(levelname)s] %(message)s"
DEFAULT_LOG_DIR = GET_ABS_PATH("../logs")

DEFAULT_BACKUP_DATE_FORMAT = "%Y%m%d_%H%M%S_%f"
BACKUP_FILENAME_TEMPLATE = "{stem}-backup-{date}{suffix}"

CHANNEL_ACTIVE_THRESHOLD = 1
CHANNEL_MIN_ID_DIFF = 0
CHANNEL_FAILED_ATTEMPTS_THRESHOLD = -3
CHANNEL_REMOVE_THRESHOLD = 0

DEFAULT_CHANNEL_BATCH_EXTRACT = 20
DEFAULT_CHANNEL_BATCH_UPDATE = 100
DEFAULT_CHANNEL_PROGRESS_BAR_FORMAT = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "

LEN_NAME = 32
LEN_NUMBER = 7
TOTAL_CHANNELS_POST = 0

POST_DEFAULT_INDEX = 0
POST_FIRST_ID = 1
POST_FIRST_INDEX = 0
POST_LAST_INDEX = -1

DEFAULT_HELP_INDENT = 30
DEFAULT_HELP_WIDTH = 120

FORMAT_CONFIG_NAME = "{protocol}-{host}-{port}"
SSR_BODY_TEMPLATE = "{host}:{port}:{origin}:{method}:{obfs}:{password}/?{params}"

FURL_TG = "https://t.me/s/{name}"
FURL_TG_AFTER = FURL_TG + "?after={id}"
FURL_TG_BEFORE = FURL_TG + "?before={id}"

DEFAULT_FILE_CHANNELS = "current.json"
DEFAULT_FILE_CONFIGS_CLEAN = "v2ray-clean.txt"
DEFAULT_FILE_CONFIGS_RAW = "v2ray-raw.txt"
DEFAULT_FILE_URLS = "urls.txt"

DEFAULT_PATH_CHANNELS = GET_ABS_PATH(f"../channels/{DEFAULT_FILE_CHANNELS}")
DEFAULT_PATH_CONFIGS_CLEAN = GET_ABS_PATH(f"../configs/{DEFAULT_FILE_CONFIGS_CLEAN}")
DEFAULT_PATH_CONFIGS_RAW = GET_ABS_PATH(f"../configs/{DEFAULT_FILE_CONFIGS_RAW}")
DEFAULT_PATH_URLS = GET_ABS_PATH(f"../channels/{DEFAULT_FILE_URLS}")

XPATH_POST_IDS = "//div[@class='tgme_widget_message text_not_supported_wrap js-widget_message']/@data-post"
XPATH_TG_MESSAGES_TEXT = "//div[@class='tgme_widget_message_text js-message_text']//text()"

CLI_SCRIPTS_CONFIG = {
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

PATTERN_CONFIG_FIELD = compile(r"\w+(?:\.\w+)*")
PATTERN_PARAM_SEPARATOR = compile(r"[ ,]+")
PATTERN_TG_CHANNEL_NAME = compile(r"http[s]?://t.me/[s/]{0,2}([\w]+)")

PATTERN_VMESS_JSON = compile(r'(?P<json>{.*})', DOTALL)
PATTERN_URL_V2RAY_ALL = compile(
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
PATTERN_URL_ANYTLS = compile(
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
PATTERN_URL_HYSTERIA2 = compile(
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
PATTERN_URL_SS = compile(
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
PATTERN_URL_SSR = compile(
    r'(?P<url>'
        r'(?P<protocol>ssr)://'
        r'(?P<base64>[\w+/-]+={0,2})'
        r'(?P<name>){0,1}'
    r')'
)

# ssr://host:port:protocol:method:obfs:base64(password)/?param=base64(value)
PATTERN_URL_SSR_PLAIN = compile(
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
PATTERN_URL_TROJAN = compile(
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
PATTERN_URL_TUIC = compile(
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
PATTERN_URL_VLESS = compile(
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
PATTERN_URL_VMESS = compile(
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
PATTERN_URL_WIREGUARD = compile(
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

PATTERNS_URL_ALL = [
    PATTERN_URL_ANYTLS,
    PATTERN_URL_HYSTERIA2,
    PATTERN_URL_SS,
    PATTERN_URL_SSR,
    PATTERN_URL_TROJAN,
    PATTERN_URL_TUIC,
    PATTERN_URL_VLESS,
    PATTERN_URL_VMESS,
    PATTERN_URL_WIREGUARD,
]
