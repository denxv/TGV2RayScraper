import pytest

from core.typing import (
    ChannelInfo,
    ConditionStr,
    Record,
)
from domain.predicates import (
    is_channel_available,
    is_channel_fully_scanned,
    is_new_channel,
    make_predicate,
    should_delete_channel,
    should_set_current_id,
    should_update_channel,
)
from tests.unit.domain.constants.test_cases.predicates import (
    IS_CHANNEL_AVAILABLE_ARGS,
    IS_CHANNEL_AVAILABLE_CASES,
    IS_CHANNEL_FULLY_SCANNED_ARGS,
    IS_CHANNEL_FULLY_SCANNED_CASES,
    IS_NEW_CHANNEL_ARGS,
    IS_NEW_CHANNEL_CASES,
    MAKE_PREDICATE_ARGS,
    MAKE_PREDICATE_CASES,
    SHOULD_DELETE_CHANNEL_ARGS,
    SHOULD_DELETE_CHANNEL_CASES,
    SHOULD_SET_CURRENT_ID_ARGS,
    SHOULD_SET_CURRENT_ID_CASES,
    SHOULD_UPDATE_CHANNEL_ARGS,
    SHOULD_UPDATE_CHANNEL_CASES,
)


@pytest.mark.parametrize(
    IS_CHANNEL_AVAILABLE_ARGS,
    IS_CHANNEL_AVAILABLE_CASES,
)
def test_is_channel_available(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = is_channel_available(
        channel_info=channel_info,
    )

    assert result is expected


@pytest.mark.parametrize(
    IS_CHANNEL_FULLY_SCANNED_ARGS,
    IS_CHANNEL_FULLY_SCANNED_CASES,
)
def test_is_channel_fully_scanned(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = is_channel_fully_scanned(
        channel_info=channel_info,
    )

    assert result is expected


@pytest.mark.parametrize(
    IS_NEW_CHANNEL_ARGS,
    IS_NEW_CHANNEL_CASES,
)
def test_is_new_channel(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = is_new_channel(
        channel_info=channel_info,
    )

    assert result is expected


@pytest.mark.parametrize(
    MAKE_PREDICATE_ARGS,
    MAKE_PREDICATE_CASES,
)
def test_make_predicate(
    condition: ConditionStr | None,
    record: Record,
    *,
    expected: bool,
) -> None:
    predicate = make_predicate(
        condition=condition,
    )
    result = (
        predicate(record)
        if predicate is not None else expected
    )

    assert result is expected


@pytest.mark.parametrize(
    SHOULD_DELETE_CHANNEL_ARGS,
    SHOULD_DELETE_CHANNEL_CASES,
)
def test_should_delete_channel(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = should_delete_channel(
        channel_info=channel_info,
    )

    assert result is expected


@pytest.mark.parametrize(
    SHOULD_SET_CURRENT_ID_ARGS,
    SHOULD_SET_CURRENT_ID_CASES,
)
def test_should_set_current_id(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = should_set_current_id(
        channel_info=channel_info,
    )

    assert result is expected


@pytest.mark.parametrize(
    SHOULD_UPDATE_CHANNEL_ARGS,
    SHOULD_UPDATE_CHANNEL_CASES,
)
def test_should_update_channel(
    channel_info: ChannelInfo,
    *,
    expected: bool,
) -> None:
    result = should_update_channel(
        channel_info=channel_info,
    )

    assert result is expected
