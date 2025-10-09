from argparse import Namespace
from datetime import datetime
from json import dumps
from logging import (
    FileHandler,
    Filter,
    Formatter,
    Logger,
    LogRecord,
    StreamHandler,
    getLogger,
)
from pathlib import Path

from core.constants import (
    COLORS,
    DEBUG,
    DEFAULT_CONSOLE_LOG_FORMAT,
    DEFAULT_FILE_LOG_FORMAT,
    DEFAULT_INDENT,
    DEFAULT_LOGGER_NAME,
    DEFAULT_LOG_DIR,
    INFO,
)
from core.typing import Any


class ColorLevelFilter(Filter):
    def __init__(self, color: bool = True) -> None:
        super().__init__()
        self.color = color

    def _color_level(self, levelname: str) -> str:
        level_color = COLORS.get(levelname.strip(), "")
        reset_color = COLORS.get("RESET", "")
        return f"{level_color}{levelname}{reset_color}"

    def filter(self, record: LogRecord) -> bool:
        if self.color:
            record.colored_levelname = self._color_level(record.levelname)
        return True


class MicrosecondFormatter(Formatter):
    def formatTime(self, record: LogRecord, datefmt: str = "") -> str:
        fmt = "%H:%M:%S.%f"
        if isinstance(datefmt, str) and datefmt.strip():
            fmt = datefmt.strip()
        ct = datetime.fromtimestamp(record.created)
        return ct.strftime(fmt)


def create_logger(
    name: str = DEFAULT_LOGGER_NAME,
    console_level: int = INFO,
    file_level: int = DEBUG,
    color_console: bool = True,
) -> Logger:
    logger = getLogger(name)
    logger.setLevel(DEBUG)

    console_handler = StreamHandler()
    console_handler.addFilter(ColorLevelFilter(color=color_console))
    console_handler.setFormatter(MicrosecondFormatter(DEFAULT_CONSOLE_LOG_FORMAT))
    console_handler.setLevel(console_level)

    file_handler = FileHandler(
        f"{DEFAULT_LOG_DIR}/{datetime.now():%Y-%m-%d}.log",
        encoding="utf-8",
    )
    file_handler.addFilter(ColorLevelFilter(color=False))
    file_handler.setFormatter(MicrosecondFormatter(DEFAULT_FILE_LOG_FORMAT))
    file_handler.setLevel(file_level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_debug_object(title: str, obj: Any, *, indent: int = DEFAULT_INDENT) -> None:
    try:
        formatted = dumps(
            vars(obj) if isinstance(obj, Namespace) else obj,
            default=str,
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )
        logger.debug(f"{title}:\n{formatted}")
    except (TypeError, ValueError) as e:
        logger.debug(f"Failed to serialize object '{title}': {e}")


logger = create_logger()
