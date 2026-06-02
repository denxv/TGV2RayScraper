import pytest

from core.constants.patterns.telegram import (
    PATTERN_TG_CHANNEL_NAME,
)
from tests.unit.core.constants.test_cases.patterns.telegram import (
    TG_CHANNEL_NAME_INVALID_ARGS,
    TG_CHANNEL_NAME_INVALID_CASES,
    TG_CHANNEL_NAME_VALID_ARGS,
    TG_CHANNEL_NAME_VALID_CASES,
)


@pytest.mark.parametrize(
    TG_CHANNEL_NAME_INVALID_ARGS,
    TG_CHANNEL_NAME_INVALID_CASES,
)
def test_pattern_tg_channel_name_invalid(
    text: str,
) -> None:
    match = PATTERN_TG_CHANNEL_NAME.search(text)

    assert match is None


@pytest.mark.parametrize(
    TG_CHANNEL_NAME_VALID_ARGS,
    TG_CHANNEL_NAME_VALID_CASES,
)
def test_pattern_tg_channel_name_valid(
    text: str,
    expected: str,
) -> None:
    match = PATTERN_TG_CHANNEL_NAME.search(text)

    assert match is not None
    assert match.group(1) == expected
