from argparse import (
    SUPPRESS,
)
from logging import (
    DEBUG,
    INFO,
)
from pathlib import (
    Path,
)

from core.typing import (
    AbsPath,
    Callable,
    ChannelInfo,
    FilePath,
)

__all__ = [
    "ABS_PATH",
    "BASE64_BLOCK_SIZE",
    "BATCH_EXTRACT_DEFAULT",
    "BATCH_EXTRACT_MAX",
    "BATCH_EXTRACT_MIN",
    "BATCH_UPDATE_DEFAULT",
    "BATCH_UPDATE_MAX",
    "BATCH_UPDATE_MIN",
    "CHANNEL_FAILED_ATTEMPTS_THRESHOLD",
    "CHANNEL_MIN_ID_DIFF",
    "CHANNEL_REMOVE_THRESHOLD",
    "CHANNEL_STATE_AVAILABLE",
    "CHANNEL_STATE_UNAVAILABLE",
    "CLI_SCRIPTS_CONFIG",
    "COLORS",
    "DEBUG",
    "DEFAULT_CHANNEL_VALUES",
    "DEFAULT_COUNT",
    "DEFAULT_CURRENT_ID",
    "DEFAULT_FILE_CHANNELS",
    "DEFAULT_FILE_CONFIGS_CLEAN",
    "DEFAULT_FILE_CONFIGS_RAW",
    "DEFAULT_FILE_URLS",
    "DEFAULT_HELP_INDENT",
    "DEFAULT_HELP_WIDTH",
    "DEFAULT_JSON_INDENT",
    "DEFAULT_LAST_ID",
    "DEFAULT_LOGGER_NAME",
    "DEFAULT_LOG_DIR",
    "DEFAULT_LOG_LINE_LENGTH",
    "DEFAULT_PATH_CHANNELS",
    "DEFAULT_PATH_CONFIGS_CLEAN",
    "DEFAULT_PATH_CONFIGS_RAW",
    "DEFAULT_PATH_URLS",
    "DEFAULT_STATE",
    "DEFAULT_VALUE_MAX",
    "DEFAULT_VALUE_MIN",
    "HTTP_TIMEOUT_DEFAULT",
    "HTTP_TIMEOUT_MAX",
    "HTTP_TIMEOUT_MIN",
    "INFO",
    "MESSAGE_OFFSET_DEFAULT",
    "MESSAGE_OFFSET_MAX",
    "MESSAGE_OFFSET_MIN",
    "POST_DEFAULT_ID",
    "POST_DEFAULT_INDEX",
    "POST_FIRST_ID",
    "POST_FIRST_INDEX",
    "POST_LAST_INDEX",
    "SUPPRESS",
    "TEXT_LENGTH_MSG_OFFSET",
    "TEXT_LENGTH_NAME",
    "TEXT_LENGTH_NUMBER",
    "XPATH_POST_IDS",
    "XPATH_TG_MESSAGES_TEXT",
]

ABS_PATH: Callable[  # noqa: E731
    [FilePath],
    AbsPath,
] = lambda path: str(
    (Path(__file__).parent / path).resolve(),
)

BASE64_BLOCK_SIZE = 4

BATCH_EXTRACT_DEFAULT = 20
BATCH_EXTRACT_MAX = 100
BATCH_EXTRACT_MIN = 1

BATCH_ID = 20

BATCH_UPDATE_DEFAULT = 100
BATCH_UPDATE_MAX = 1000
BATCH_UPDATE_MIN = 1

CHANNEL_FAILED_ATTEMPTS_THRESHOLD = -3
CHANNEL_MIN_ID_DIFF = 0
CHANNEL_REMOVE_THRESHOLD = 0
CHANNEL_STATE_AVAILABLE = 1
CHANNEL_STATE_UNAVAILABLE = -1

CLI_SCRIPTS_CONFIG = {
    "update_channels": {
        "flags": [
            "--channels",
            "--delete-channels",
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

COLORS = {
    "DEBUG": "\033[37m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[31m",
    "RESET": "\033[0m",
}

DEFAULT_COUNT = 0
DEFAULT_CURRENT_ID = 1
DEFAULT_LAST_ID = -1
DEFAULT_STATE = 0

DEFAULT_CHANNEL_VALUES: ChannelInfo = {
    "count": DEFAULT_COUNT,
    "current_id": DEFAULT_CURRENT_ID,
    "last_id": DEFAULT_LAST_ID,
    "state": DEFAULT_STATE,
}

DEFAULT_HELP_INDENT = 30
DEFAULT_HELP_WIDTH = 120

DEFAULT_FILE_CHANNELS = "current.json"
DEFAULT_FILE_CONFIGS_CLEAN = "v2ray-clean.txt"
DEFAULT_FILE_CONFIGS_RAW = "v2ray-raw.txt"
DEFAULT_FILE_URLS = "urls.txt"

DEFAULT_JSON_INDENT = 4

DEFAULT_LOG_LINE_LENGTH = 100
DEFAULT_LOG_DIR = ABS_PATH("../../logs")
DEFAULT_LOGGER_NAME = "TGV2RayScraper"

DEFAULT_PATH_CHANNELS = ABS_PATH(
    f"../../channels/{DEFAULT_FILE_CHANNELS}",
)
DEFAULT_PATH_CONFIGS_CLEAN = ABS_PATH(
    f"../../configs/{DEFAULT_FILE_CONFIGS_CLEAN}",
)
DEFAULT_PATH_CONFIGS_RAW = ABS_PATH(
    f"../../configs/{DEFAULT_FILE_CONFIGS_RAW}",
)
DEFAULT_PATH_URLS = ABS_PATH(
    f"../../channels/{DEFAULT_FILE_URLS}",
)

DEFAULT_VALUE_MAX = 100
DEFAULT_VALUE_MIN = 1

HTTP_TIMEOUT_DEFAULT = 30.0
HTTP_TIMEOUT_MAX = 100.0
HTTP_TIMEOUT_MIN = 0.1

MESSAGE_OFFSET_DEFAULT = 50
MESSAGE_OFFSET_MAX = 1000
MESSAGE_OFFSET_MIN = 1

POST_DEFAULT_ID = 0
POST_DEFAULT_INDEX = 0
POST_FIRST_ID = 1
POST_FIRST_INDEX = 0
POST_LAST_INDEX = -1

TEXT_LENGTH_MSG_OFFSET = 4
TEXT_LENGTH_NAME = 32
TEXT_LENGTH_NUMBER = 7

XPATH_POST_IDS = (
    "//div["
        "contains(@class, 'tgme_widget_message')"
        " and contains(@class, 'text_not_supported_wrap')"
        " and contains(@class, 'js-widget_message')"
    "]//@data-post"
)
XPATH_TG_MESSAGES_TEXT = (
    "//div["
        "contains(@class, 'tgme_widget_message_text')"
        " and contains(@class, 'js-message_text')"
    "]//text()"
)
