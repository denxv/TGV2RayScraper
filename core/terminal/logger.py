from argparse import (
    Namespace,
)
from datetime import (
    datetime,
    timezone,
)
from json import (
    dumps,
)
from logging import (
    FileHandler,
    Formatter,
    Logger,
    LogRecord,
    getLogger,
)

from rich.console import (
    Console,
)
from rich.logging import (
    RichHandler,
)

from core.constants.common import (
    DEBUG,
    DEFAULT_JSON_INDENT,
    DEFAULT_LOGGER_NAME,
    DEFAULT_PATH_LOGS,
    INFO,
)
from core.constants.formats import (
    FORMAT_LOG_DATE,
    FORMAT_LOG_FILEPATH,
    FORMAT_LOG_RECORD,
    FORMAT_LOG_TIME,
)
from core.constants.templates.debug.common import (
    TEMPLATE_DEBUG_FAILED_SERIALIZATION,
    TEMPLATE_DEBUG_PRETTY_OBJECT,
)
from core.terminal.console import (
    console,
)

__all__ = [
    "create_logger",
    "log_debug_object",
    "logger",
    "set_console_level",
]


class MicrosecondFormatter(Formatter):
    def formatTime(  # noqa: N802
        self,
        record: LogRecord,
        datefmt: str | None = None,
    ) -> str:
        fmt = FORMAT_LOG_TIME

        if (
            isinstance(datefmt, str)
            and (stripped := datefmt.strip())
        ):
            fmt = stripped

        created_dt = datetime.fromtimestamp(
            record.created,
            tz=timezone.utc,
        )

        return created_dt.astimezone().strftime(fmt)


def create_logger(
    *,
    console: Console = console,
    console_level: int = INFO,
    file_level: int = DEBUG,
    name: str = DEFAULT_LOGGER_NAME,
) -> Logger:
    logger = getLogger(
        name=name,
    )
    logger.setLevel(
        level=DEBUG,
    )

    if logger.handlers:
        return logger

    rich_handler = RichHandler(
        console=console,
        level=console_level,
        log_time_format=FORMAT_LOG_TIME,
        omit_repeated_times=False,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
    )

    file_handler = FileHandler(
        filename=FORMAT_LOG_FILEPATH.format(
            dir=DEFAULT_PATH_LOGS,
            name=datetime.now().astimezone().strftime(
                FORMAT_LOG_DATE,
            ),
        ),
        encoding="utf-8",
    )
    file_handler.setFormatter(
        fmt=MicrosecondFormatter(
            fmt=FORMAT_LOG_RECORD,
        ),
    )
    file_handler.setLevel(
        level=file_level,
    )

    logger.addHandler(
        hdlr=rich_handler,
    )
    logger.addHandler(
        hdlr=file_handler,
    )

    return logger


def log_debug_object(
    obj: object,
    *,
    title: str,
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
    except (
        TypeError,
        ValueError,
    ) as e:
        logger.debug(
            msg=TEMPLATE_DEBUG_FAILED_SERIALIZATION.format(
                title=title,
                object=obj,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
    else:
        logger.debug(
            msg=TEMPLATE_DEBUG_PRETTY_OBJECT.format(
                title=title,
                payload=serialized_obj,
            ),
        )


def set_console_level(
    logger: Logger,
    *,
    debug: bool = False,
    level: int = INFO,
) -> None:
    for handler in logger.handlers:
        if not isinstance(handler, RichHandler):
            continue

        handler.setLevel(
            level=DEBUG if debug else level,
        )


logger = create_logger()
