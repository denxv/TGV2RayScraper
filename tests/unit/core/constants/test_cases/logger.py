import pytest

from tests.unit.core.constants.examples.logger import (
    COLOR_LEVEL_FILTER_EXAMPLES,
    LOG_DEBUG_OBJECT_EXAMPLES,
    MICROSECOND_FORMATTER_EXAMPLES,
)

COLOR_LEVEL_FILTER_ARGS = (
    "color_enabled",
)
COLOR_LEVEL_FILTER_CASES = tuple(
    pytest.param(
        color_enabled,
        id=case_id,
    )
    for (
        color_enabled,
        case_id,
    ) in COLOR_LEVEL_FILTER_EXAMPLES
)

LOG_DEBUG_OBJECT_ARGS = (
    "title",
    "obj",
)
LOG_DEBUG_OBJECT_CASES = tuple(
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

MICROSECOND_FORMATTER_ARGS = (
    "datefmt",
)
MICROSECOND_FORMATTER_CASES = tuple(
    pytest.param(
        datefmt,
        id=case_id,
    )
    for (
        datefmt,
        case_id,
    ) in MICROSECOND_FORMATTER_EXAMPLES
)
