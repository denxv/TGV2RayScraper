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
    ChannelInfo,
)

__all__ = [
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
    "DEFAULT_HELP_INDENT",
    "DEFAULT_HELP_WIDTH",
    "DEFAULT_JSON_INDENT",
    "DEFAULT_LAST_ID",
    "DEFAULT_LOGGER_NAME",
    "DEFAULT_LOG_LINE_LENGTH",
    "DEFAULT_PATH_CHANNELS",
    "DEFAULT_PATH_CONFIGS_CLEAN",
    "DEFAULT_PATH_CONFIGS_EXPORT",
    "DEFAULT_PATH_CONFIGS_IMPORT",
    "DEFAULT_PATH_CONFIGS_RAW",
    "DEFAULT_PATH_LOGS",
    "DEFAULT_PATH_PROJECT",
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

CLI_SCRIPTS_CONFIG = {
    "update_channels": {
        "flags": sorted([
            *(
                f"--reset-{field.replace('_', '-')}"
                for field in DEFAULT_CHANNEL_VALUES
            ),
            "--channel-filter",
            "--channels",
            "--delete-channels",
            "--message-offset",
            "--no-backup",
            "--no-dry-run",
            "--reset-all",
            "--urls",
        ]),
    },
    "scraper": {
        "flags": [
            "--batch-extract",
            "--batch-update",
            "--channels",
            "--configs-raw",
            "--time-out",
        ],
    },
    "v2ray_cleaner": {
        "flags": [
            "--config-filter",
            "--configs-clean",
            "--configs-raw",
            "--duplicate",
            "--export",
            "--import",
            "--no-normalize",
            "--reverse",
            "--sort",
        ],
    },
}

DEFAULT_HELP_INDENT = 40
DEFAULT_HELP_WIDTH = 150
DEFAULT_JSON_INDENT = 4
DEFAULT_LOG_LINE_LENGTH = 100
DEFAULT_LOGGER_NAME = "TGV2RayScraper"

DEFAULT_PATH_PROJECT = (Path(__file__).parent / "../../").resolve()

DEFAULT_PATH_CHANNELS = (
    DEFAULT_PATH_PROJECT / "channels/current.json"
)
DEFAULT_PATH_CONFIGS_CLEAN = (
    DEFAULT_PATH_PROJECT / "configs/v2ray-clean.txt"
)
DEFAULT_PATH_CONFIGS_EXPORT = (
    DEFAULT_PATH_PROJECT / "configs/v2ray.json"
)
DEFAULT_PATH_CONFIGS_IMPORT = (
    DEFAULT_PATH_PROJECT / "configs/v2ray.json"
)
DEFAULT_PATH_CONFIGS_RAW = (
    DEFAULT_PATH_PROJECT / "configs/v2ray-raw.txt"
)
DEFAULT_PATH_LOGS = (
    DEFAULT_PATH_PROJECT / "logs"
)
DEFAULT_PATH_URLS = (
    DEFAULT_PATH_PROJECT / "channels/urls.txt"
)

DEFAULT_VALUE_MAX = float("inf")
DEFAULT_VALUE_MIN = float("-inf")

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
TEXT_LENGTH_NUMBER = 9

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
