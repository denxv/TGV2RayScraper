from core.constants.common import (
    TEXT_LENGTH_NAME,
)

__all__ = [
    "FORMAT_BACKUP_DATE",
    "FORMAT_LOG_CONSOLE",
    "FORMAT_LOG_FILE",
    "FORMAT_LOG_FILENAME_DATE",
    "FORMAT_LOG_TIME_MICROSECONDS",
    "FORMAT_PROGRESS_BAR",
]

FORMAT_BACKUP_DATE = (
    "%Y%m%d_%H%M%S_%f"
)
FORMAT_LOG_CONSOLE = (
    "<%(asctime)s>"
    " "
    "[%(colored_levelname)s]"
    " "
    "%(message)s"
)
FORMAT_LOG_FILE = (
    "<%(asctime)s>"
    " "
    "[%(levelname)s]"
    " "
    "%(message)s"
)
FORMAT_LOG_FILENAME_DATE = (
    "%Y-%m-%d"
)
FORMAT_LOG_TIME_MICROSECONDS = (
    "%H:%M:%S.%f"
)
FORMAT_PROGRESS_BAR = (
    " | "
    f"{{desc:<{TEXT_LENGTH_NAME}}}"
    " | "
    "{percentage:5.1f}%"
    " "
    "[{bar}]"
    " "
    "({n_fmt}/{total_fmt})"
    " "
    "[{elapsed}<{remaining}, {rate_fmt}]"
)
