from core.typing import (
    FormatStr,
)

__all__ = [
    "FORMAT_BACKUP_DATE",
    "FORMAT_BACKUP_FILENAME",
    "FORMAT_BASE64_PADDING",
    "FORMAT_CHANNEL_CHANGE",
    "FORMAT_CONFIG_NAME",
    "FORMAT_CONFIG_SSR_BODY",
    "FORMAT_CONFIG_URL",
    "FORMAT_CONFIG_URL_BODY",
    "FORMAT_CONFIG_URL_LOCATION",
    "FORMAT_LOG_DATE",
    "FORMAT_LOG_FILEPATH",
    "FORMAT_LOG_RECORD",
    "FORMAT_LOG_TIME",
    "FORMAT_TG_CHANNEL_URL",
    "FORMAT_TG_CHANNEL_URL_WITH_AFTER",
]

FORMAT_BACKUP_DATE: FormatStr = (
    "%Y%m%d_%H%M%S_%f"
)
FORMAT_BACKUP_FILENAME: FormatStr = (
    "{stem}"
    "-"
    "backup"
    "-"
    "{date}"
    "{suffix}"
)
FORMAT_BASE64_PADDING: FormatStr = (
    "{value}"
    "{padding}"
)
FORMAT_CHANNEL_CHANGE: FormatStr = (
    "{before}"
    " -> "
    "{after}"
)
FORMAT_CONFIG_NAME: FormatStr = (
    "{protocol}"
    "-"
    "{host}"
    "-"
    "{port}"
)
FORMAT_CONFIG_SSR_BODY: FormatStr = (
    "{host}"
    ":"
    "{port}"
    ":"
    "{origin}"
    ":"
    "{method}"
    ":"
    "{obfs}"
    ":"
    "{password}"
    "/?"
    "{params}"
)
FORMAT_CONFIG_URL: FormatStr = (
    "{url}"
    "#"
    "{name}"
)
FORMAT_CONFIG_URL_BODY: FormatStr = (
    "{protocol}"
    "://"
    "{body}"
)
FORMAT_CONFIG_URL_LOCATION: FormatStr = (
    "@"
    "{host}"
    ":"
    "{port}"
)
FORMAT_LOG_DATE: FormatStr = (
    "%Y-%m-%d"
)
FORMAT_LOG_FILEPATH: FormatStr = (
    "{dir}"
    "/"
    "{name}"
    ".log"
)
FORMAT_LOG_RECORD: FormatStr = (
    "%(asctime)s"
    " | "
    "%(levelname)-7s"
    " | "
    "%(filename)-15s"
    " "
    "%(lineno)5d"
    " | "
    "%(funcName)-30s"
    " | "
    "%(message)s"
)
FORMAT_LOG_TIME: FormatStr = (
    "%H:%M:%S.%f"
)
FORMAT_TG_CHANNEL_URL: FormatStr = (
    "https://t.me/s/{name}"
)
FORMAT_TG_CHANNEL_URL_WITH_AFTER: FormatStr = (
    FORMAT_TG_CHANNEL_URL + "?after={id}"
)
