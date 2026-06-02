import pytest

from tests.unit.core.constants.examples.terminal.logger import (
    LOG_DEBUG_OBJECT_EXAMPLES,
    MICROSECOND_FORMATTER_EXAMPLES,
    SET_CONSOLE_LEVEL_EXAMPLES,
)

__all__ = [
    "LOG_DEBUG_OBJECT_ARGS",
    "LOG_DEBUG_OBJECT_CASES",
    "MICROSECOND_FORMATTER_ARGS",
    "MICROSECOND_FORMATTER_CASES",
    "SET_CONSOLE_LEVEL_ARGS",
    "SET_CONSOLE_LEVEL_CASES",
]

LOG_DEBUG_OBJECT_ARGS: tuple[
    str,
    ...,
] = (
    "title",
    "obj",
)
LOG_DEBUG_OBJECT_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        title,
        obj,
        id=case_id,
    )
    for (
        title,
        obj,
        case_id,
    ) in LOG_DEBUG_OBJECT_EXAMPLES
)

MICROSECOND_FORMATTER_ARGS: tuple[
    str,
    ...,
] = (
    "datefmt",
)
MICROSECOND_FORMATTER_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        datefmt,
        id=case_id,
    )
    for (
        datefmt,
        case_id,
    ) in MICROSECOND_FORMATTER_EXAMPLES
)

SET_CONSOLE_LEVEL_ARGS: tuple[
    str,
    ...,
] = (
    "debug",
    "level",
    "expected",
)
SET_CONSOLE_LEVEL_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        debug,
        level,
        expected,
        id=case_id,
    )
    for (
        debug,
        level,
        expected,
        case_id,
    ) in SET_CONSOLE_LEVEL_EXAMPLES
)
