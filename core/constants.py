from argparse import SUPPRESS as _SUPPRESS
from logging import DEBUG as _DEBUG
from logging import INFO as _INFO
from pathlib import Path
from re import DOTALL
from re import compile as re_compile

from core.typing import AbsPath, Callable, ChannelInfo, FilePath

GET_ABS_PATH: Callable[[FilePath], AbsPath] = (  # noqa: E731
    lambda path: str((Path(__file__).parent / path).resolve())
)

DEBUG = _DEBUG
INFO = _INFO
SUPPRESS = _SUPPRESS

DEFAULT_FILE_CHANNELS = "current.json"
DEFAULT_FILE_CONFIGS_CLEAN = "v2ray-clean.txt"
DEFAULT_FILE_CONFIGS_RAW = "v2ray-raw.txt"
DEFAULT_FILE_URLS = "urls.txt"

DEFAULT_LOGGER_NAME = "TGV2RayScraper"
DEFAULT_LOG_DIR = GET_ABS_PATH("../logs")

DEFAULT_PATH_CHANNELS = GET_ABS_PATH(
    f"../channels/{DEFAULT_FILE_CHANNELS}",
)
DEFAULT_PATH_CONFIGS_CLEAN = GET_ABS_PATH(
    f"../configs/{DEFAULT_FILE_CONFIGS_CLEAN}",
)
DEFAULT_PATH_CONFIGS_RAW = GET_ABS_PATH(
    f"../configs/{DEFAULT_FILE_CONFIGS_RAW}",
)
DEFAULT_PATH_URLS = GET_ABS_PATH(
    f"../channels/{DEFAULT_FILE_URLS}",
)

FORMAT_CHANNEL_PROGRESS_BAR = (
    " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
)
FORMAT_CONSOLE_LOG = "<%(asctime)s> [%(colored_levelname)s] %(message)s"
FORMAT_FILE_LOG = "<%(asctime)s> [%(levelname)s] %(message)s"

FORMAT_BACKUP_DATE = "%Y%m%d_%H%M%S_%f"
TEMPLATE_BACKUP_FILENAME = "{stem}-backup-{date}{suffix}"

DEFAULT_COUNT = 0
DEFAULT_CURRENT_ID = 1
DEFAULT_LAST_ID = -1
DEFAULT_POST_ID = 0

DEFAULT_CHANNEL_VALUES: ChannelInfo = {
    "count": DEFAULT_COUNT,
    "current_id": DEFAULT_CURRENT_ID,
    "last_id": DEFAULT_LAST_ID,
}

BASE64_BLOCK_SIZE = 4

CHANNEL_ACTIVE_THRESHOLD = 1
CHANNEL_FAILED_ATTEMPTS_THRESHOLD = -3
CHANNEL_MAX_BATCH_EXTRACT = 100
CHANNEL_MAX_BATCH_UPDATE = 1000
CHANNEL_MAX_MESSAGE_OFFSET = 1000
CHANNEL_MIN_BATCH_EXTRACT = 1
CHANNEL_MIN_BATCH_UPDATE = 1
CHANNEL_MIN_ID_DIFF = 0
CHANNEL_MIN_MESSAGE_OFFSET = 1
CHANNEL_REMOVE_THRESHOLD = 0

DEFAULT_CHANNEL_BATCH_EXTRACT = 20
DEFAULT_CHANNEL_BATCH_UPDATE = 100
DEFAULT_CHANNEL_MESSAGE_OFFSET = 50
DEFAULT_HELP_INDENT = 30
DEFAULT_HELP_WIDTH = 120
DEFAULT_HTTP_TIMEOUT = 30.0
DEFAULT_INDENT = 4
DEFAULT_LOG_LINE_LENGTH = 100
DEFAULT_MAX_VALUE = 100
DEFAULT_MIN_VALUE = 1

HTTP_MAX_TIMEOUT = 100.0
HTTP_MIN_TIMEOUT = 0.1

LEN_MSG_OFFSET = 4
LEN_NAME = 32
LEN_NUMBER = 7

POST_DEFAULT_INDEX = 0
POST_FIRST_ID = 1
POST_FIRST_INDEX = 0
POST_LAST_INDEX = -1

COLORS = {
    "DEBUG": "\033[37m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[31m",
    "RESET": "\033[0m",
}

MESSAGE_CHANNEL_SKIP_DELETE = "Channel deletion skipped (default: disabled)."
MESSAGE_DELETE_STARTED = "Deleting inactive channels..."
MESSAGE_DELETE_COMPLETED = "Inactive channels deleted successfully."
MESSAGE_DEDUP_SKIPPED = "Deduplication skipped: no fields specified."
MESSAGE_EXIT = "Exit from the program."
MESSAGE_LOAD_STARTED = "Loading all channels..."
MESSAGE_LOAD_COMPLETED = "All channels loaded successfully."
MESSAGE_NO_FIELDS_PROVIDED = "No fields provided."
MESSAGE_NO_POSTS_FOUND = "No posts found."
MESSAGE_SAVE_STARTED = "Saving all channels..."
MESSAGE_SAVE_COMPLETED = ""
MESSAGE_SHOW_CHANNELS_INFO = (
    "Showing information about the remaining channels..."
)
MESSAGE_UNEXPECTED_ERROR = "Unexpected error occurred."
MESSAGE_UPDATE_STARTED = "Adding missing channels..."
MESSAGE_UPDATE_COMPLETED = "Missing channels added successfully."

TEMPLATE_CONFIG_NAME = "{protocol}-{host}-{port}"
TEMPLATE_MSG_ASSIGNMENT_OFFSET = "Channel '{name}': current_id = {offset}."
TEMPLATE_MSG_CHANNEL_MISSING = "Channel '{name}' missing, adding to list."
TEMPLATE_MSG_CHANNELS_LEFT = "Channels left to check: {count}."
TEMPLATE_MSG_CONFIGS_FOUND = "Found: {count} configs."
TEMPLATE_MSG_COUNT_DIFF = (
    "Old count: {old_size} | New count: {new_size} | ({diff:+})"
)
TEMPLATE_MSG_DEBUG_OFFSET = (
    "Debug info for channel '{name}' (check_only={check_only})"
)
TEMPLATE_MSG_DEDUP_COMPLETED = (
    "Duplicate removal completed: "
    "{remain} configs remain, {removed} removed."
)
TEMPLATE_MSG_DEDUP_STARTED = (
    "Removing duplicates from {count} configs using keys: {fields}..."
)
TEMPLATE_MSG_DELETING_CHANNEL = (
    "Deleting channel '{name}' with the following information"
)
TEMPLATE_MSG_DIFF_OFFSET = (
    f"Channel {{name:<{LEN_NAME + 2}}} | "
    f"ID diff = {{diff:<{LEN_MSG_OFFSET}}} | "
    f"offset = {{offset:<{LEN_MSG_OFFSET}}} | "
    "skipped messages due to diff > offset."
)
TEMPLATE_MSG_DIFF_OFFSET_APPLIED = "{message} — assignment applied."
TEMPLATE_MSG_DUPLICATE_FIELD = "Duplicate field detected: {field!r}"
TEMPLATE_MSG_ERROR_POST_ID = (
    "Failed to extract post ID from '{url}': {exc_type}: {exc_msg}"
)
TEMPLATE_MSG_ERROR_SCRIPT = "Script '{name}' exited with an error!"
TEMPLATE_MSG_EXPECTED_STRING = "Expected string, got {type_name!r}."
TEMPLATE_MSG_EXTRACTING_CONFIGS = (
    "Extracting configs from channel '{name}'..."
)
TEMPLATE_MSG_FILE_BACKED_UP = (
    "File '{src_name}' backed up as '{backup_name}'."
)
TEMPLATE_MSG_FILE_DOES_NOT_EXIST = "The file does not exist: '{filepath}'."
TEMPLATE_MSG_FILTER_COMPLETED = (
    "Filtered: {count} configs kept, {removed} removed by condition."
)
TEMPLATE_MSG_FILTER_STARTED = (
    "Filtering {count} configs by condition: `{condition}`..."
)
TEMPLATE_MSG_INVALID_FIELD_FORMAT = "Invalid field format: {field!r}"
TEMPLATE_MSG_INVALID_NUMBER = "Invalid number: {value}."
TEMPLATE_MSG_INVALID_OFFSET = (
    "Invalid offset {offset}, "
    "expected positive integer — assignment skipped."
)
TEMPLATE_MSG_IS_DIRECTORY = "'{filepath}' is a directory, expected a file."
TEMPLATE_MSG_LOADED_CONFIGS = "Loaded {count} configs from '{path}'."
TEMPLATE_MSG_LOADING_CONFIGS = "Loading configs from '{path}'..."
TEMPLATE_MSG_LOG_STATUS = (
    "| <SS> | "
    f"{{name:<{LEN_NAME}}} | "
    f"{{current_id:>{LEN_NUMBER}}} / "
    f"{{last_id:<{LEN_NUMBER}}} | "
    "(+{diff:,})"
)
TEMPLATE_MSG_LOG_UPDATE = (
    "| <UU> | "
    f"{{name:<{LEN_NAME}}} | "
    f"{{last_id:>{LEN_NUMBER}}} -> "
    f"{{last_post_id:<{LEN_NUMBER}}} |"
)
TEMPLATE_MSG_NORM_COMPLETED = (
    "Configs normalized: {count} (removed: {removed})."
)
TEMPLATE_MSG_NORM_STARTED = "Normalizing {count} configs..."
TEMPLATE_MSG_NUMBER_OUT_OF_RANGE = (
    "Expected {min_value} to {max_value}, got {value}."
)
TEMPLATE_MSG_PARENT_DIR_MISSING = (
    "Parent directory does not exist: '{parent}'."
)
TEMPLATE_MSG_SAVE_CHANNELS = "Saved {count} channels in '{path}'."
TEMPLATE_MSG_SAVED_CONFIGS = "Saved {count} configs in '{path}'."
TEMPLATE_MSG_SAVING_CONFIGS = "Saving {count} configs to '{path}'..."
TEMPLATE_MSG_SCRIPT_COMPLETED = "Script '{name}' completed successfully."
TEMPLATE_MSG_SCRIPT_STARTED = "Starting script '{name}'..."
TEMPLATE_MSG_SKIP_ASSIGNMENT = (
    "Skipping assignment because check_only={check_only}."
)
TEMPLATE_MSG_SORT_COMPLETED = "Sorting completed: {count} configs sorted."
TEMPLATE_MSG_SORT_STARTED = (
    "Sorting {count} configs by fields: {fields} (reverse={reverse})..."
)
TEMPLATE_MSG_TOTAL_CHANNELS = (
    "Total channels are available for extracting configs: {count}."
)
TEMPLATE_MSG_TOTAL_MESSAGES = "Total messages on channels: {count:,}."
TEMPLATE_MSG_UPDATING_CHANNEL_INFO = (
    "Updating channel information for {count} channels..."
)
TEMPLATE_SSR_BODY = (
    "{host}:{port}:{origin}:{method}:{obfs}:{password}/?{params}"
)

TEMPLATE_TG_URL = "https://t.me/s/{name}"
TEMPLATE_TG_URL_AFTER = TEMPLATE_TG_URL + "?after={id}"

XPATH_POST_IDS = (
    "//div[@class='tgme_widget_message text_not_supported_wrap "
    "js-widget_message']/@data-post"
)
XPATH_TG_MESSAGES_TEXT = (
    "//div[@class='tgme_widget_message_text js-message_text']//text()"
)

CLI_SCRIPTS_CONFIG = {
    "update_channels": {
        "flags": [
            "--channels",
            "--delete-channels",
            "--include-new",
            "--message-offset",
            "--no-backup",
            "--no-dry-run",
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
            "--time-out",
        ],
        "mode": "async",
    },
    "scraper": {
        "flags": [
            "--channels",
            "--configs-raw",
            "--time-out",
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

PATTERN_CONFIG_FIELD = re_compile(r"\w+(?:\.\w+)*")
PATTERN_PARAM_SEPARATOR = re_compile(r"[ ,]+")
PATTERN_TG_CHANNEL_NAME = re_compile(r"http[s]?://t.me/[s/]{0,2}([\w]+)")

PATTERN_VMESS_JSON = re_compile(r"(?P<json>{.*})", DOTALL)
PATTERN_URL_V2RAY_ALL = re_compile(
    r"(?:"
        r"anytls"
    r"|"
        r"hy2"
    r"|"
        r"hysteria2"
    r"|"
        r"\bss\b"
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
    r")://(?:(?!://)[\S])+",
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
# ss://base64(method:password)@host:port#name
# ss://base64(method:password@host:port)#name
PATTERN_URL_SS = re_compile(
    r"(?P<url>(?P<protocol>\bss)://"
        r"(?:"
            r"(?P<method>[^\s:@#]+)"
            r":(?P<password>(?:(?!//).)+)(?=@)"
        r"|"
            r"(?P<base64>[\w+/]+={0,2})(?![^\s@#])"
        r")"
        r"(?:"
            r"@(?P<host>[\w\-\[:%\].]+)"
            r":(?P<port>\d{1,5})"
        r"){0,1}"
        r"(?=(?:[\s#]|$))(?!\?)"
        r"(?P<name>){0,1}"
    r")",
)

# ssr://base64(host:port:protocol:method:obfs:base64(password)/?param=base64(value))
PATTERN_URL_SSR = re_compile(
    r"(?P<url>"
        r"(?P<protocol>ssr)://"
        r"(?P<base64>[\w+/-]+={0,2})"
        r"(?P<name>){0,1}"
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
        r":(?P<password>[\w+/-]+={0,2})(?=/)"
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

# vmess://base64(json)
# vmess://uuid@host:port/path?params#name
# vmess://uuid@host:port?params#name
PATTERN_URL_VMESS = re_compile(
    r"(?P<url>"
        r"(?P<protocol>vmess)://"
        r"(?:"
            r"(?P<uuid>(?:(?!://).)+)"
            r"@(?P<host>[\w\-\[:%\].]+)"
            r":(?P<port>\d{1,5})"
            r"(?P<path>/[^\s?#]*){0,1}"
            r"(?:\?(?P<params>(?:(?!://)[^\s#])*)){0,1}"
            r"(?P<name>){0,1}"
        r"|"
            r"(?P<base64>[\w+/]+={0,2})"
        r")"
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
