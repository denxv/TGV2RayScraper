from argparse import Namespace
from datetime import datetime
from json import dumps
from pathlib import Path
from typing import Any
from logging import DEBUG, FileHandler, Filter, Formatter, getLogger, INFO, Logger, LogRecord, StreamHandler


class ColorLevelFilter(Filter):
    COLORS: dict[str, str] = {
        "DEBUG": "\033[37m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[31m",
        "RESET": "\033[0m",
    }

    def __init__(self, color: bool = True) -> None:
        super().__init__()
        self.color = color

    def _color_level(self, levelname: str) -> str:
        level_color = self.COLORS.get(levelname.strip(), "")
        reset_color = self.COLORS.get("RESET", "")
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
    name: str = "TGV2RayScraper",
    console_level: int = INFO,
    file_level: int = DEBUG,
    color_console: bool = True,
) -> Logger:
    logger = getLogger("TGV2RayScraper")
    logger.setLevel(DEBUG)

    console_handler = StreamHandler()
    console_handler.addFilter(ColorLevelFilter(
        color=color_console,
    ))
    console_handler.setFormatter(MicrosecondFormatter(
        "<%(asctime)s> [%(colored_levelname)s] %(message)s",
    ))
    console_handler.setLevel(console_level)

    file_handler = FileHandler(
        Path(__file__).parent / f"../logs/{datetime.now():%Y-%m-%d}.log",
        encoding="utf-8",
    )
    file_handler.addFilter(ColorLevelFilter(
        color=False,
    ))
    file_handler.setFormatter(MicrosecondFormatter(
        "<%(asctime)s> [%(levelname)s] %(message)s",
    ))
    file_handler.setLevel(file_level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_debug_object(title: str, obj: Any, *, indent: int = 4) -> None:
    try:
        formatted = dumps(
            vars(obj) if isinstance(obj, Namespace) else obj,
            default=str,
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )
        logger.debug(f"{title}:\n{formatted}")
    except (TypeError, ValueError) as exception:
        logger.debug(f"Failed to serialize object '{title}': {exception}")


logger = create_logger()
