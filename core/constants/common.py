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
from urllib.request import (
    getproxies,
)

from core.typing import (
    ChannelInfo,
    Padding,
    ScriptConfig,
    ScriptName,
)

__all__ = [
    "BASE64_BLOCK_SIZE",
    "CHANNELS_BATCH_DEFAULT",
    "CHANNELS_BATCH_MAX",
    "CHANNELS_BATCH_MIN",
    "CHANNELS_CONCURRENCY_DEFAULT",
    "CHANNELS_CONCURRENCY_MAX",
    "CHANNELS_CONCURRENCY_MIN",
    "CHANNEL_FAILED_ATTEMPTS_THRESHOLD",
    "CHANNEL_MIN_ID_DIFF",
    "CHANNEL_REMOVE_THRESHOLD",
    "CHANNEL_STATE_AVAILABLE",
    "CHANNEL_STATE_UNAVAILABLE",
    "CHANNEL_TABLE_PADDING",
    "CLI_SCRIPTS_CONFIG",
    "CONFIGS_BATCH_DEFAULT",
    "CONFIGS_BATCH_MAX",
    "CONFIGS_BATCH_MIN",
    "DEBUG",
    "DEFAULT_CHANNEL_VALUES",
    "DEFAULT_COUNT",
    "DEFAULT_CURRENT_ID",
    "DEFAULT_HELP_INDENT",
    "DEFAULT_HELP_WIDTH",
    "DEFAULT_JSON_INDENT",
    "DEFAULT_LAST_ID",
    "DEFAULT_LOGGER_NAME",
    "DEFAULT_PATH_CHANNELS",
    "DEFAULT_PATH_CONFIGS_CLEAN",
    "DEFAULT_PATH_CONFIGS_EXPORT",
    "DEFAULT_PATH_CONFIGS_IMPORT",
    "DEFAULT_PATH_CONFIGS_RAW",
    "DEFAULT_PATH_LOGS",
    "DEFAULT_PATH_PROJECT",
    "DEFAULT_PATH_URLS",
    "DEFAULT_PROXY_URL",
    "DEFAULT_STATE",
    "DEFAULT_VALUE_MAX",
    "DEFAULT_VALUE_MIN",
    "HTTP_RETRIES_DEFAULT",
    "HTTP_RETRIES_MAX",
    "HTTP_RETRIES_MIN",
    "HTTP_RETRY_DELAY_DEFAULT",
    "HTTP_RETRY_DELAY_MAX",
    "HTTP_RETRY_DELAY_MIN",
    "HTTP_TIMEOUT_DEFAULT",
    "HTTP_TIMEOUT_MAX",
    "HTTP_TIMEOUT_MIN",
    "INFO",
    "LOGGING_THEME",
    "MESSAGE_OFFSET_DEFAULT",
    "MESSAGE_OFFSET_MAX",
    "MESSAGE_OFFSET_MIN",
    "PORT_MAX",
    "PORT_MIN",
    "POST_DEFAULT_ID",
    "POST_DEFAULT_INDEX",
    "POST_FIRST_ID",
    "POST_FIRST_INDEX",
    "POST_LAST_INDEX",
    "PROGRESS_REMOVE_DELAY_DEFAULT",
    "SUPPRESS",
    "TELEGRAM_POST_PAGE_SIZE",
    "TEXT_LENGTH_NAME",
    "TEXT_LENGTH_NUMBER",
    "XPATH_POST_IDS",
    "XPATH_TG_MESSAGES_TEXT",
]

_ENV_PROXIES: dict[str, str] = getproxies()

BASE64_BLOCK_SIZE: int = 4

CHANNELS_BATCH_DEFAULT: int = 100
CHANNELS_BATCH_MAX: int = 1000
CHANNELS_BATCH_MIN: int = 1

CHANNELS_CONCURRENCY_DEFAULT: int = 5
CHANNELS_CONCURRENCY_MAX: int = 100
CHANNELS_CONCURRENCY_MIN: int = 1

CONFIGS_BATCH_DEFAULT: int = 20
CONFIGS_BATCH_MAX: int = 500
CONFIGS_BATCH_MIN: int = 1

CHANNEL_FAILED_ATTEMPTS_THRESHOLD: int = -3
CHANNEL_MIN_ID_DIFF: int = 0
CHANNEL_REMOVE_THRESHOLD: int = 0
CHANNEL_STATE_AVAILABLE: int = 1
CHANNEL_STATE_UNAVAILABLE: int = -1

CHANNEL_TABLE_PADDING: Padding = (1, 0, 1, 25)

DEFAULT_COUNT: int = 0
DEFAULT_CURRENT_ID: int = 1
DEFAULT_LAST_ID: int = -1
DEFAULT_STATE: int = 0

DEFAULT_HELP_INDENT: int = 40
DEFAULT_HELP_WIDTH: int = 150
DEFAULT_JSON_INDENT: int = 4
DEFAULT_LOGGER_NAME: str = "TGV2RayScraper"

DEFAULT_PATH_PROJECT: Path = (Path(__file__).parent / "../../").resolve()

DEFAULT_PATH_CHANNELS: Path = (
    DEFAULT_PATH_PROJECT / "channels/current.json"
)
DEFAULT_PATH_CONFIGS_CLEAN: Path = (
    DEFAULT_PATH_PROJECT / "configs/v2ray-clean.txt"
)
DEFAULT_PATH_CONFIGS_EXPORT: Path = (
    DEFAULT_PATH_PROJECT / "configs/v2ray.json"
)
DEFAULT_PATH_CONFIGS_IMPORT: Path = (
    DEFAULT_PATH_PROJECT / "configs/v2ray.json"
)
DEFAULT_PATH_CONFIGS_RAW: Path = (
    DEFAULT_PATH_PROJECT / "configs/v2ray-raw.txt"
)
DEFAULT_PATH_LOGS: Path = (
    DEFAULT_PATH_PROJECT / "logs"
)
DEFAULT_PATH_URLS: Path = (
    DEFAULT_PATH_PROJECT / "channels/urls.txt"
)

DEFAULT_VALUE_MAX: float = float("inf")
DEFAULT_VALUE_MIN: float = float("-inf")

HTTP_RETRIES_DEFAULT: int = 3
HTTP_RETRIES_MAX: int = 10
HTTP_RETRIES_MIN: int = 1

HTTP_RETRY_DELAY_DEFAULT: float = 0.5
HTTP_RETRY_DELAY_MAX: float = 60.0
HTTP_RETRY_DELAY_MIN: float = 0.0

HTTP_TIMEOUT_DEFAULT: float = 30.0
HTTP_TIMEOUT_MAX: float = 100.0
HTTP_TIMEOUT_MIN: float = 0.1

MESSAGE_OFFSET_DEFAULT: int = 50
MESSAGE_OFFSET_MAX: int = 1000
MESSAGE_OFFSET_MIN: int = 1

PORT_MAX: int = 65535
PORT_MIN: int = 1

POST_DEFAULT_ID: int = 0
POST_DEFAULT_INDEX: int = 0
POST_FIRST_ID: int = 1
POST_FIRST_INDEX: int = 0
POST_LAST_INDEX: int = -1

PROGRESS_REMOVE_DELAY_DEFAULT: float = 0.25

TELEGRAM_POST_PAGE_SIZE: int = 20

TEXT_LENGTH_NAME: int = 32
TEXT_LENGTH_NUMBER: int = 7

DEFAULT_CHANNEL_VALUES: ChannelInfo = {
    "count": DEFAULT_COUNT,
    "current_id": DEFAULT_CURRENT_ID,
    "last_id": DEFAULT_LAST_ID,
    "state": DEFAULT_STATE,
}

CLI_SCRIPTS_CONFIG: dict[ScriptName, ScriptConfig] = {
    "update_channels": {
        "flags": sorted([
            *(
                f"--reset-{field.replace('_', '-')}"
                for field in DEFAULT_CHANNEL_VALUES
            ),
            "--channel-filter",
            "--channels",
            "--debug",
            "--delete-channels",
            "--message-offset",
            "--no-dry-run",
            "--reset-all",
            "--skip-backup",
            "--urls",
        ]),
    },
    "scraper": {
        "flags": [
            "--channels",
            "--channels-batch",
            "--channels-concurrency",
            "--configs-batch",
            "--configs-raw",
            "--debug",
            "--proxy",
            "--retries",
            "--retry-delay",
            "--skip-update",
            "--time-out",
        ],
    },
    "v2ray_cleaner": {
        "flags": [
            "--config-filter",
            "--configs-clean",
            "--configs-raw",
            "--debug",
            "--duplicate",
            "--export",
            "--import",
            "--reverse",
            "--skip-normalize",
            "--sort",
        ],
    },
}

DEFAULT_PROXY_URL: str = (
    _ENV_PROXIES.get("https")       # HTTPS_PROXY
    or _ENV_PROXIES.get("http")     # HTTP_PROXY
    or _ENV_PROXIES.get("all")      # ALL_PROXY
    or "socks5://127.0.0.1:10808"   # Fallback: local proxy (v2rayN)
)

LOGGING_THEME: dict[str, str] = {
    "logging.level.debug": "cyan",
    "logging.level.info": "green",
    "logging.level.warning": "yellow",
    "logging.level.error": "red",
    "logging.level.critical": "bold red",
}

XPATH_POST_IDS: str = (
    "//div["
        "contains(@class, 'tgme_widget_message')"
        " and contains(@class, 'text_not_supported_wrap')"
        " and contains(@class, 'js-widget_message')"
    "]//@data-post"
)
XPATH_TG_MESSAGES_TEXT: str = (
    "//div["
        "contains(@class, 'tgme_widget_message_text')"
        " and contains(@class, 'js-message_text')"
    "]//text()"
)
