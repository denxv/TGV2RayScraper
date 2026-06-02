import pytest

from tests.unit.core.constants.examples.patterns.telegram import (
    TG_CHANNEL_NAME_INVALID_EXAMPLES,
    TG_CHANNEL_NAME_VALID_EXAMPLES,
)

__all__ = [
    "TG_CHANNEL_NAME_INVALID_ARGS",
    "TG_CHANNEL_NAME_INVALID_CASES",
    "TG_CHANNEL_NAME_VALID_ARGS",
    "TG_CHANNEL_NAME_VALID_CASES",
]

TG_CHANNEL_NAME_INVALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
)
TG_CHANNEL_NAME_INVALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        text,
        id=case_id,
    )
    for (
        text,
        case_id,
    ) in TG_CHANNEL_NAME_INVALID_EXAMPLES
)

TG_CHANNEL_NAME_VALID_ARGS: tuple[
    str,
    ...,
] = (
    "text",
    "expected",
)

TG_CHANNEL_NAME_VALID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        text,
        expected,
        id=case_id,
    )
    for (
        text,
        expected,
        case_id,
    ) in TG_CHANNEL_NAME_VALID_EXAMPLES
)
