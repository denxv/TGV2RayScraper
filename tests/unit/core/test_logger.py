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
    Logger,
    LogRecord,
)
from unittest.mock import (
    Mock,
)

import pytest

from core.logger import (
    ColorLevelFilter,
    MicrosecondFormatter,
    create_logger,
    log_debug_object,
    logger,
)
from tests.unit.core.constants.common import (
    COLORS,
    DEBUG,
    DEFAULT_JSON_INDENT,
    DEFAULT_LOGGER_NAME,
    DEFAULT_PATH_LOGS,
    FORMAT_LOG_FILENAME_DATE,
    INFO,
    TEMPLATE_ERROR_FAILED_SERIALIZATION,
    TEMPLATE_FORMAT_FILE_LOG_PATH,
    TEMPLATE_FORMAT_STRING_COLORED_LEVEL,
    TEMPLATE_FORMAT_TITLE_OBJECT_PRETTY,
)
from tests.unit.core.constants.test_cases.logger import (
    COLOR_LEVEL_FILTER_ARGS,
    COLOR_LEVEL_FILTER_CASES,
    LOG_DEBUG_OBJECT_ARGS,
    LOG_DEBUG_OBJECT_CASES,
    MICROSECOND_FORMATTER_ARGS,
    MICROSECOND_FORMATTER_CASES,
)


@pytest.mark.parametrize(
    COLOR_LEVEL_FILTER_ARGS,
    COLOR_LEVEL_FILTER_CASES,
)
def test_color_level_filter(
    *,
    color_enabled: bool,
) -> None:
    record = LogRecord(
        name="test_color",
        level=INFO,
        pathname="",
        lineno=0,
        msg="Test message!",
        args=(),
        exc_info=None,
    )

    color_level_filter = ColorLevelFilter(
        color=color_enabled,
    )

    assert color_level_filter.filter(record) is True
    assert hasattr(record, "colored_levelname") is color_enabled

    if color_enabled:
        expected_colored_level = TEMPLATE_FORMAT_STRING_COLORED_LEVEL.format(
            color=COLORS.get("INFO", ""),
            levelname="INFO",
            reset=COLORS.get("RESET", ""),
        )

        assert record.colored_levelname == expected_colored_level  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    COLOR_LEVEL_FILTER_ARGS,
    COLOR_LEVEL_FILTER_CASES,
)
def test_create_logger_with_color_filter(
    mock_logger_components: dict[str, Mock],
    *,
    color_enabled: bool,
) -> None:
    _mock_log_comps = mock_logger_components

    mock_fh = _mock_log_comps["FileHandler"].return_value
    mock_fmt = _mock_log_comps["MicrosecondFormatter"].return_value
    mock_sh = _mock_log_comps["StreamHandler"].return_value

    log = create_logger(
        name="test_logger",
        console_level=INFO,
        file_level=DEBUG,
        color_console=color_enabled,
    )

    assert log.name == "test_logger"
    assert mock_fh in log.handlers
    assert mock_sh in log.handlers

    mock_fh.addFilter.assert_called_once_with(
        filter=ColorLevelFilter(
            color=False,
        ),
    )
    mock_sh.addFilter.assert_called_once_with(
        filter=ColorLevelFilter(
            color=color_enabled,
        ),
    )

    mock_fh.setFormatter.assert_called_once_with(
        fmt=mock_fmt,
    )
    mock_sh.setFormatter.assert_called_once_with(
        fmt=mock_fmt,
    )

    mock_fh.setLevel.assert_called_with(
        level=DEBUG,
    )
    mock_sh.setLevel.assert_called_with(
        level=INFO,
    )


def test_create_logger_uses_correct_log_path(
    mock_logger_components: dict[str, Mock],
    frozen_datetime_offset: datetime,
) -> None:
    mock_fh_cls = mock_logger_components["FileHandler"]

    create_logger()

    mock_fh_cls.assert_called_once_with(
        filename=TEMPLATE_FORMAT_FILE_LOG_PATH.format(
            dir=DEFAULT_PATH_LOGS,
            name=frozen_datetime_offset.strftime(
                FORMAT_LOG_FILENAME_DATE,
            ),
        ),
        encoding="utf-8",
    )


def test_log_debug_object_failure(
    mock_logger: Mock,
) -> None:

    class BadObject:
        def __str__(
            self,
        ) -> str:
            raise TypeError("TEST_FAIL")

    log_debug_object(
        title=BadObject.__name__,
        obj=BadObject(),
    )

    mock_logger.debug.assert_called_once_with(
        msg=TEMPLATE_ERROR_FAILED_SERIALIZATION.format(
            title=BadObject.__name__,
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
        title=title,
        obj=obj,
    )

    mock_logger.debug.assert_called_once_with(
        msg=TEMPLATE_FORMAT_TITLE_OBJECT_PRETTY.format(
            title=title,
            formatted=dumps(
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
    frozen_datetime_local_tz: datetime,
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
    record.created = frozen_datetime_local_tz.timestamp()

    actual_str = MicrosecondFormatter().formatTime(
        record=record,
        datefmt=datefmt,
    )

    expected_str = frozen_datetime_local_tz.strftime(
        datefmt,
    )

    assert actual_str == expected_str
