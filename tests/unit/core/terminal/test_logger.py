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
    Logger,
    LogRecord,
)
from unittest.mock import (
    Mock,
    create_autospec,
)

import pytest
from rich.logging import (
    RichHandler,
)

from core.terminal.logger import (
    MicrosecondFormatter,
    create_logger,
    log_channel_changes,
    log_debug_object,
    logger,
    set_console_level,
)
from tests.unit.core.constants.common import (
    DEBUG,
    DEFAULT_JSON_INDENT,
    DEFAULT_LOGGER_NAME,
    DEFAULT_PATH_LOGS,
    FORMAT_CHANNEL_CHANGE,
    FORMAT_LOG_DATE,
    FORMAT_LOG_FILEPATH,
    INFO,
    TEMPLATE_DEBUG_FAILED_SERIALIZATION,
    TEMPLATE_DEBUG_PRETTY_OBJECT,
    TEMPLATE_TITLE_CHANNEL_CHANGES,
)
from tests.unit.core.constants.test_cases.terminal.logger import (
    LOG_DEBUG_OBJECT_ARGS,
    LOG_DEBUG_OBJECT_CASES,
    MICROSECOND_FORMATTER_ARGS,
    MICROSECOND_FORMATTER_CASES,
    SET_CONSOLE_LEVEL_ARGS,
    SET_CONSOLE_LEVEL_CASES,
)
from tests.unit.domain.constants.fixtures.channel import (
    CHANNEL_BASE_SAMPLE,
)


def test_create_logger(
    mock_logger_components: dict[str, Mock],
) -> None:
    mock_fh = mock_logger_components["FileHandler"].return_value
    mock_fmt = mock_logger_components["MicrosecondFormatter"].return_value
    mock_rh = mock_logger_components["RichHandler"].return_value

    log = create_logger(
        name="test_logger",
        console_level=INFO,
        file_level=DEBUG,
    )

    assert log.name == "test_logger"
    assert mock_fh in log.handlers
    assert mock_rh in log.handlers

    mock_fh.setFormatter.assert_called_once_with(
        fmt=mock_fmt,
    )

    mock_fh.setLevel.assert_called_once_with(
        level=DEBUG,
    )


def test_create_logger_idempotent() -> None:
    logger1 = create_logger(name="test_logger")
    logger2 = create_logger(name="test_logger")

    assert logger1 is logger2


def test_create_logger_uses_correct_log_path(
    mock_logger_components: dict[str, Mock],
    mock_datetime: Mock,
    fixed_now: datetime,
) -> None:
    mock_fh_cls = mock_logger_components["FileHandler"]

    create_logger()

    expected_name = fixed_now.astimezone().strftime(
        FORMAT_LOG_DATE,
    )

    mock_fh_cls.assert_called_once_with(
        filename=FORMAT_LOG_FILEPATH.format(
            dir=DEFAULT_PATH_LOGS,
            name=expected_name,
        ),
        encoding="utf-8",
    )


def test_log_channel_changes(
    mock_log_debug_object: Mock,
) -> None:
    channel_name = "test_channel"
    before = {
        **CHANNEL_BASE_SAMPLE,
    }
    after = {
        **CHANNEL_BASE_SAMPLE,
        "count": -CHANNEL_BASE_SAMPLE.get("count"),
        "state": -CHANNEL_BASE_SAMPLE.get("state"),
    }

    log_channel_changes(
        name=channel_name,
        before=before,
        after=after,
    )

    mock_log_debug_object.assert_called_once_with(
        obj={
            key: FORMAT_CHANNEL_CHANGE.format(
                before=before.get(key),
                after=after[key],
            )
            for key in after
            if before.get(key) != after[key]
        },
        title=TEMPLATE_TITLE_CHANNEL_CHANGES.format(
            name=channel_name,
        ),
    )


def test_log_channel_changes_no_changes(
    mock_log_debug_object: Mock,
) -> None:
    log_channel_changes(
        name="test_channel",
        before=CHANNEL_BASE_SAMPLE,
        after=CHANNEL_BASE_SAMPLE,
    )

    mock_log_debug_object.assert_not_called()


def test_log_debug_object_failure(
    mock_logger: Mock,
) -> None:
    class BadObject:
        def __str__(self) -> str:
            raise TypeError("TEST_FAIL")

    bad_object = BadObject()

    log_debug_object(
        obj=bad_object,
        title=BadObject.__name__,
    )

    mock_logger.debug.assert_called_once_with(
        msg=TEMPLATE_DEBUG_FAILED_SERIALIZATION.format(
            title=BadObject.__name__,
            object=bad_object,
            exc_type=TypeError.__name__,
            exc_msg="TEST_FAIL",
        ),
    )


@pytest.mark.parametrize(
    LOG_DEBUG_OBJECT_ARGS,
    LOG_DEBUG_OBJECT_CASES,
)
def test_log_debug_object_various(
    mock_logger: Mock,
    title: str,
    obj: object,
) -> None:
    log_debug_object(
        obj=obj,
        title=title,
    )

    mock_logger.debug.assert_called_once_with(
        msg=TEMPLATE_DEBUG_PRETTY_OBJECT.format(
            title=title,
            payload=dumps(
                obj=vars(obj) if isinstance(obj, Namespace) else obj,
                default=str,
                ensure_ascii=False,
                indent=DEFAULT_JSON_INDENT,
                sort_keys=True,
            ),
        ),
    )


def test_logger_is_global() -> None:
    assert logger.name == DEFAULT_LOGGER_NAME
    assert isinstance(logger, Logger)


@pytest.mark.parametrize(
    MICROSECOND_FORMATTER_ARGS,
    MICROSECOND_FORMATTER_CASES,
)
def test_microsecond_formatter(
    fixed_now: datetime,
    datefmt: str | None,
) -> None:
    record = LogRecord(
        name="test_format",
        level=INFO,
        pathname="",
        lineno=0,
        msg="Test message!",
        args=(),
        exc_info=None,
    )

    record.created = fixed_now.timestamp()

    actual = MicrosecondFormatter().formatTime(
        record=record,
        datefmt=datefmt,
    )

    created_dt = datetime.fromtimestamp(
        record.created,
        tz=timezone.utc,
    )

    expected = created_dt.astimezone().strftime(datefmt)

    assert actual == expected


@pytest.mark.parametrize(
    SET_CONSOLE_LEVEL_ARGS,
    SET_CONSOLE_LEVEL_CASES,
)
def test_set_console_level(
    mock_logger: Mock,
    *,
    debug: bool,
    level: int,
    expected: int,
) -> None:
    rich_handler = create_autospec(
        RichHandler,
        instance=True,
    )
    other_handler = Mock()

    mock_logger.handlers = [
        rich_handler,
        other_handler,
    ]

    set_console_level(
        logger=mock_logger,
        debug=debug,
        level=level,
    )

    rich_handler.setLevel.assert_called_once_with(
        level=expected,
    )
    other_handler.setLevel.assert_not_called()
