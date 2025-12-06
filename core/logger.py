from argparse import (
    Namespace,
)
from datetime import (
    datetime,
)
from json import (
    dumps,
)
from logging import (
    FileHandler,
    Filter,
    Formatter,
    Logger,
    LogRecord,
    StreamHandler,
    getLogger,
)

from core.constants.common import (
    COLORS,
    DEBUG,
    DEFAULT_JSON_INDENT,
    DEFAULT_LOG_DIR,
    DEFAULT_LOGGER_NAME,
    INFO,
)
from core.constants.formats import (
    FORMAT_LOG_CONSOLE,
    FORMAT_LOG_FILE,
    FORMAT_LOG_FILENAME_DATE,
    FORMAT_LOG_TIME_MICROSECONDS,
)
from core.constants.templates import (
    TEMPLATE_ERROR_FAILED_SERIALIZATION,
    TEMPLATE_FORMAT_FILE_LOG_PATH,
    TEMPLATE_FORMAT_STRING_COLORED_LEVEL,
    TEMPLATE_TITLE_OBJECT_PRETTY_PRINT,
)

__all__ = [
    "create_logger",
    "log_debug_object",
    "logger",
]


class ColorLevelFilter(
    Filter,
):
    def __init__(
        self,
        *,
        color: bool = True,
    ) -> None:
        super().__init__()
        self.color = color

    def __eq__(
        self,
        other: object,
    ) -> bool:
        return (
            isinstance(other, ColorLevelFilter)
            and self.color is other.color
        )

    def __hash__(
        self,
    ) -> int:
        return hash(self.color)  # pragma: no cover

    def _color_level(
        self,
        levelname: str,
    ) -> str:
        level_color = COLORS.get(
            levelname.strip().upper(),
            "",
        )
        reset_color = COLORS.get("RESET", "")

        return TEMPLATE_FORMAT_STRING_COLORED_LEVEL.format(
            color=level_color,
            levelname=levelname,
            reset=reset_color,
        )

    def filter(
        self,
        record: LogRecord,
    ) -> bool:
        if self.color:
            record.colored_levelname = self._color_level(
                levelname=record.levelname,
            )

        return True


class MicrosecondFormatter(
    Formatter,
):
    def formatTime(  # noqa: N802
        self,
        record: LogRecord,
        datefmt: str | None = None,
    ) -> str:
        fmt = FORMAT_LOG_TIME_MICROSECONDS

        if (
            isinstance(datefmt, str)
            and (stripped := datefmt.strip())
        ):
            fmt = stripped

        ct = datetime.fromtimestamp(
            record.created,
            tz=datetime.now().astimezone().tzinfo,
        )

        return ct.strftime(fmt)


def create_logger(
    name: str = DEFAULT_LOGGER_NAME,
    console_level: int = INFO,
    file_level: int = DEBUG,
    *,
    color_console: bool = True,
) -> Logger:
    logger = getLogger(
        name=name,
    )
    logger.setLevel(
        level=DEBUG,
    )

    console_handler = StreamHandler()
    console_handler.addFilter(
        filter=ColorLevelFilter(
            color=color_console,
        ),
    )
    console_handler.setFormatter(
        fmt=MicrosecondFormatter(
            fmt=FORMAT_LOG_CONSOLE,
        ),
    )
    console_handler.setLevel(
        level=console_level,
    )

    file_handler = FileHandler(
        filename=TEMPLATE_FORMAT_FILE_LOG_PATH.format(
            dir=DEFAULT_LOG_DIR,
            name=datetime.now().astimezone().strftime(
                FORMAT_LOG_FILENAME_DATE,
            ),
        ),
        encoding="utf-8",
    )
    file_handler.addFilter(
        filter=ColorLevelFilter(
            color=False,
        ),
    )
    file_handler.setFormatter(
        fmt=MicrosecondFormatter(
            fmt=FORMAT_LOG_FILE,
        ),
    )
    file_handler.setLevel(
        level=file_level,
    )

    logger.addHandler(
        hdlr=console_handler,
    )
    logger.addHandler(
        hdlr=file_handler,
    )

    return logger


def log_debug_object(
    title: str,
    obj: object,
    *,
    indent: int = DEFAULT_JSON_INDENT,
) -> None:
    try:
        serialized_obj = dumps(
            obj=vars(obj) if isinstance(obj, Namespace) else obj,
            default=str,
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )

        logger.debug(
            msg=TEMPLATE_TITLE_OBJECT_PRETTY_PRINT.format(
                title=title,
                formatted=serialized_obj,
            ),
        )
    except (
        TypeError,
        ValueError,
    ) as e:
        logger.debug(
            msg=TEMPLATE_ERROR_FAILED_SERIALIZATION.format(
                title=title,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )


logger = create_logger()
