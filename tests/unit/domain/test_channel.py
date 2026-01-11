from argparse import (
    Namespace,
)
from unittest.mock import (
    ANY,
    Mock,
    call,
)

import pytest
from pytest_mock import (
    MockerFixture,
)

from core.typing import (
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    PostID,
    RecordPredicate,
)
from core.utils import (
    repeat_char_line,
)
from domain.channel import (
    assign_current_id_to_channels,
    delete_channels,
    diff_channel_id,
    format_channel_status,
    get_filtered_keys,
    get_normalized_current_id,
    get_sorted_keys,
    normalize_channel_names,
    print_channel_info,
    process_channels,
    reset_channels,
    sort_channel_names,
    update_last_id_and_state,
    update_with_new_channels,
)
from domain.predicates import (
    should_set_current_id,
)
from tests.unit.domain.constants.common import (
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_LAST_ID,
    MESSAGE_CHANNEL_DELETE_SKIPPED,
    MESSAGE_CHANNEL_SHOW_INFO,
    TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED,
    TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED,
    TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED,
    TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED,
    TEMPLATE_CHANNEL_LEFT_TO_CHECK,
    TEMPLATE_CHANNEL_LOG_STATUS,
    TEMPLATE_CHANNEL_LOG_UPDATE,
    TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED,
    TEMPLATE_CHANNEL_RESET_SKIPPED,
    TEMPLATE_CHANNEL_RESET_SKIPPED_NO_CHANGES,
    TEMPLATE_CHANNEL_RESET_TOTAL,
    TEMPLATE_CHANNEL_TOTAL_AVAILABLE,
    TEMPLATE_CHANNEL_TOTAL_MESSAGES,
    TEMPLATE_ERROR_INVALID_OFFSET,
    TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS,
    TEMPLATE_FORMAT_CHANNEL_CHANGE,
    TEMPLATE_FORMAT_STRING_QUOTED_NAME,
    TEMPLATE_TITLE_CHANNEL_DELETE,
    TEMPLATE_TITLE_CHANNEL_INFO,
    TEMPLATE_TITLE_CHANNEL_RESET,
)
from tests.unit.domain.constants.fixtures.channel import (
    CHANNEL_INFO_BY_NAMES,
    CHANNELS_SAMPLE,
)
from tests.unit.domain.constants.test_cases.channel import (
    ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_ARGS,
    ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_CASES,
    ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_ARGS,
    ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_CASES,
    DELETE_CHANNELS_ARGS,
    DELETE_CHANNELS_CASES,
    DIFF_CHANNEL_ID_ARGS,
    DIFF_CHANNEL_ID_CASES,
    FORMAT_CHANNEL_STATUS_ARGS,
    FORMAT_CHANNEL_STATUS_CASES,
    GET_FILTERED_KEYS_ARGS,
    GET_FILTERED_KEYS_CASES,
    GET_NORMALIZED_CURRENT_ID_ARGS,
    GET_NORMALIZED_CURRENT_ID_CASES,
    GET_SORTED_KEYS_ARGS,
    GET_SORTED_KEYS_CASES,
    NORMALIZE_CHANNEL_NAMES_ARGS,
    NORMALIZE_CHANNEL_NAMES_CASES,
    PRINT_CHANNEL_INFO_VARIOUS_ARGS,
    PRINT_CHANNEL_INFO_VARIOUS_CASES,
    PROCESS_CHANNELS_CALLS_ARGS,
    PROCESS_CHANNELS_CALLS_CASES,
    RESET_CHANNELS_ARGS,
    RESET_CHANNELS_CASES,
    SORT_CHANNEL_NAMES_ARGS,
    SORT_CHANNEL_NAMES_CASES,
    UPDATE_LAST_ID_AND_STATE_ARGS,
    UPDATE_LAST_ID_AND_STATE_CASES,
    UPDATE_WITH_NEW_CHANNELS_ARGS,
    UPDATE_WITH_NEW_CHANNELS_CASES,
)


@pytest.mark.parametrize(
    ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_ARGS,
    ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_CASES,
)
def test_assign_current_id_to_channels_invalid_offset(
    mock_logger: Mock,
    invalid_offset: object,
) -> None:
    expected_channels = CHANNEL_INFO_BY_NAMES([
        "channel_available",
        "channel_new",
        "channel_unavailable",
    ])

    updated_channels = assign_current_id_to_channels(
        channels=expected_channels,
        message_offset=invalid_offset,
    )

    assert updated_channels == expected_channels
    assert updated_channels is not expected_channels

    mock_logger.warning.assert_any_call(
        msg=TEMPLATE_ERROR_INVALID_OFFSET.format(
            offset=invalid_offset,
        ),
    )


@pytest.mark.parametrize(
    ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_ARGS,
    ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_CASES,
)
def test_assign_current_id_to_channels_various(
    mock_log_debug_object: Mock,
    mock_logger: Mock,
    channels: ChannelsDict,
    message_offset: int,
    *,
    dry_run: bool,
    expected_current_ids: dict[str, int],
) -> None:
    updated_channels = assign_current_id_to_channels(
        channels=channels,
        message_offset=message_offset,
        dry_run=dry_run,
    )

    for name, expected_id in expected_current_ids.items():
        assert updated_channels[name]["current_id"] == expected_id

    channel_names_for_update = [
        name
        for name in channels
        if should_set_current_id(
            channel_info=channels[name],
        )
    ]

    for name in channel_names_for_update:
        diff = diff_channel_id(
            channel_info=channels[name],
        )

        if diff <= message_offset:
            continue

        _expected_msg = TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED.format(
            name=TEMPLATE_FORMAT_STRING_QUOTED_NAME.format(
                name=name,
            ),
            diff=diff,
            offset=message_offset,
        )

        if dry_run:
            mock_log_debug_object.assert_called_with(
                title=TEMPLATE_TITLE_CHANNEL_INFO.format(
                    name=name,
                ),
                obj=channels[name],
            )
            mock_logger.warning.assert_any_call(
                msg=_expected_msg,
            )
        else:
            mock_logger.debug.assert_any_call(
                msg=TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED.format(
                    message=_expected_msg,
                ),
            )
            mock_logger.info.assert_any_call(
                msg=TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED.format(
                    name=TEMPLATE_FORMAT_STRING_QUOTED_NAME.format(
                        name=name,
                    ),
                    offset=-message_offset,
                ),
            )

    if dry_run:
        mock_logger.info.assert_any_call(
            msg=TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED.format(
                count=len(channel_names_for_update),
            ),
        )


@pytest.mark.parametrize(
    DELETE_CHANNELS_ARGS,
    DELETE_CHANNELS_CASES,
)
def test_delete_channels(
    mock_log_debug_object: Mock,
    mock_logger: Mock,
    channels: ChannelsDict,
    expected_keys_to_keep: ChannelNames,
    expected_deleted: ChannelNames,
) -> None:
    remaining_channels = delete_channels(
        channels=channels,
    )

    assert list(remaining_channels) == expected_keys_to_keep

    mock_log_debug_object.assert_has_calls(
        calls=[
            call(
                title=TEMPLATE_TITLE_CHANNEL_DELETE.format(
                    name=name,
                ),
                obj=channels[name],
            )
            for name in expected_deleted
        ],
        any_order=False,
    )

    for name in expected_keys_to_keep:
        assert remaining_channels[name] == channels[name]
        assert remaining_channels[name] is not channels[name]


@pytest.mark.parametrize(
    DIFF_CHANNEL_ID_ARGS,
    DIFF_CHANNEL_ID_CASES,
)
def test_diff_channel_id(
    channel_info: ChannelInfo,
    expected: int,
) -> None:
    result = diff_channel_id(
        channel_info=channel_info,
    )

    assert result == expected


@pytest.mark.parametrize(
    FORMAT_CHANNEL_STATUS_ARGS,
    FORMAT_CHANNEL_STATUS_CASES,
)
def test_format_channel_status(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
) -> None:
    diff, message = format_channel_status(
        channel_name=channel_name,
        channel_info=channel_info,
    )

    expected_diff = diff_channel_id(
        channel_info=channel_info,
    )

    assert diff == expected_diff

    expected_message = (
        TEMPLATE_CHANNEL_LOG_STATUS.format(
            name=channel_name,
            current_id=get_normalized_current_id(
                channel_info=channel_info,
            ),
            last_id=channel_info.get(
                "last_id",
                DEFAULT_LAST_ID,
            ),
            diff=expected_diff,
        )
    )

    assert message == expected_message


@pytest.mark.parametrize(
    GET_FILTERED_KEYS_ARGS,
    GET_FILTERED_KEYS_CASES,
)
def test_get_filtered_keys(
    channels: ChannelsDict,
    expected: ChannelNames,
) -> None:
    result = get_filtered_keys(
        channels=channels,
    )

    assert result == expected


@pytest.mark.parametrize(
    GET_NORMALIZED_CURRENT_ID_ARGS,
    GET_NORMALIZED_CURRENT_ID_CASES,
)
def test_get_normalized_current_id(
    channel_info: ChannelInfo,
    expected: PostID,
) -> None:
    result = get_normalized_current_id(
        channel_info=channel_info,
    )

    assert result == expected


@pytest.mark.parametrize(
    GET_SORTED_KEYS_ARGS,
    GET_SORTED_KEYS_CASES,
)
def test_get_sorted_keys(
    channels: ChannelsDict,
    *,
    apply_filter: bool,
    reverse: bool,
    expected: ChannelNames,
) -> None:
    result = get_sorted_keys(
        channels=channels,
        apply_filter=apply_filter,
        reverse=reverse,
    )

    assert isinstance(result, list)

    for channel_name in result:
        assert isinstance(channel_name, str)

    assert result == expected


@pytest.mark.parametrize(
    NORMALIZE_CHANNEL_NAMES_ARGS,
    NORMALIZE_CHANNEL_NAMES_CASES,
)
def test_normalize_channel_names(
    channels: ChannelsDict,
    expected: ChannelsDict,
) -> None:
    result = normalize_channel_names(
        channels=channels,
    )

    assert list(result) == list(expected)
    assert result == expected
    assert result is not channels


@pytest.mark.parametrize(
    PRINT_CHANNEL_INFO_VARIOUS_ARGS,
    PRINT_CHANNEL_INFO_VARIOUS_CASES,
)
def test_print_channel_info_various(
    mock_logger: Mock,
    channels: ChannelsDict,
) -> None:
    total_diff = 0
    separator_line = repeat_char_line(
        char="-",
    )
    expected_calls = [
        separator_line,
        MESSAGE_CHANNEL_SHOW_INFO,
    ]

    filtered_names = get_sorted_keys(
        channels=channels,
        apply_filter=True,
    )

    for channel_name in filtered_names:
        diff, expected_msg = format_channel_status(
            channel_name=channel_name,
            channel_info=channels[channel_name],
        )
        total_diff += diff
        expected_calls.append(expected_msg)

    expected_calls.append(
        TEMPLATE_CHANNEL_TOTAL_AVAILABLE.format(
            count=len(channels),
        ),
    )
    expected_calls.append(
        TEMPLATE_CHANNEL_LEFT_TO_CHECK.format(
            count=len(filtered_names),
        ),
    )
    expected_calls.append(
        TEMPLATE_CHANNEL_TOTAL_MESSAGES.format(
            count=total_diff,
        ),
    )
    expected_calls.append(
        separator_line,
    )

    print_channel_info(
        channels=channels,
    )

    actual_calls = [
        call.kwargs.get("msg", "")
        for call in mock_logger.info.call_args_list
    ]

    assert actual_calls == expected_calls


@pytest.mark.parametrize(
    PROCESS_CHANNELS_CALLS_ARGS,
    PROCESS_CHANNELS_CALLS_CASES,
)
def test_process_channels_calls(
    mock_logger: Mock,
    mocker: MockerFixture,
    message_offset: int,
    *,
    dry_run: bool,
    delete_channels_flag: bool,
    reset_all: bool,
) -> None:
    channels = CHANNEL_INFO_BY_NAMES([
        "channel_available",
        "channel_new",
        "channel_unavailable",
    ])

    mock_assign = mocker.patch(
        "domain.channel.assign_current_id_to_channels",
        wraps=assign_current_id_to_channels,
    )
    mock_delete = mocker.patch(
        "domain.channel.delete_channels",
        wraps=delete_channels,
    )
    mock_reset = mocker.patch(
        "domain.channel.reset_channels",
        wraps=reset_channels,
    )

    args = Namespace(
        channel_filter=None,
        dry_run=dry_run,
        delete_channels=delete_channels_flag,
        message_offset=message_offset,
        reset_all=reset_all,
    )

    result = process_channels(
        channels=channels,
        args=args,
    )

    if delete_channels_flag or message_offset or reset_all:
        assert result is not channels
    else:
        assert result is channels

    if delete_channels_flag:
        mock_delete.assert_called_once_with(
            channels=channels,
        )
    else:
        mock_delete.assert_not_called()
        mock_logger.info.assert_any_call(
            msg=MESSAGE_CHANNEL_DELETE_SKIPPED,
        )

    if message_offset:
        mock_assign.assert_called_once_with(
            channels=ANY,
            message_offset=message_offset,
            dry_run=dry_run,
        )
    else:
        mock_assign.assert_not_called()

    channel_overrides = {
        key: value
        for key in DEFAULT_CHANNEL_VALUES
        if (value := getattr(args, f"reset_{key}", None)) is not None
    }

    if channel_overrides or reset_all:
        mock_reset.assert_called_once_with(
            channels=ANY,
            channel_overrides=channel_overrides,
            channel_predicate=ANY,
            dry_run=dry_run,
            reset_to_defaults=reset_all,
        )
    else:
        mock_reset.assert_not_called()


@pytest.mark.parametrize(
    RESET_CHANNELS_ARGS,
    RESET_CHANNELS_CASES,
)
def test_reset_channels(
    mock_log_debug_object: Mock,
    mock_logger: Mock,
    channel_overrides: ChannelInfo | None,
    channel_predicate: RecordPredicate | None,
    *,
    dry_run: bool,
    reset_to_defaults: bool,
) -> None:
    channels = CHANNELS_SAMPLE

    result = reset_channels(
        channels=channels,
        channel_overrides=channel_overrides,
        channel_predicate=channel_predicate,
        dry_run=dry_run,
        reset_to_defaults=reset_to_defaults,
    )

    overrides = channel_overrides or {}

    valid_overrides = {
        key: value
        for key, value in overrides.items()
        if value is not None
    }

    if not reset_to_defaults and not valid_overrides:
        mock_logger.debug.assert_called_with(
            msg=TEMPLATE_CHANNEL_RESET_SKIPPED_NO_CHANGES.format(
                reset_to_defaults=reset_to_defaults,
                valid_overrides=valid_overrides,
            ),
        )
        return

    channel_selector = (
        channel_predicate
        or should_set_current_id
    )
    channel_names_to_reset = [
        name
        for name in channels
        if channel_selector(
            channels[name],
        )
    ]

    if dry_run:
        mock_logger.info.assert_called_with(
            msg=TEMPLATE_CHANNEL_RESET_SKIPPED.format(
                count=len(channel_names_to_reset),
            ),
        )
        return

    mock_logger.info.assert_called_with(
        msg=TEMPLATE_CHANNEL_RESET_TOTAL.format(
            count=len(channel_names_to_reset),
        ),
    )

    mock_log_debug_object.assert_has_calls(
        calls=[
            call(
                title=TEMPLATE_TITLE_CHANNEL_RESET.format(
                    name=name,
                ),
                obj={
                    key: TEMPLATE_FORMAT_CHANNEL_CHANGE.format(
                        before=channels[name].get(key),
                        after=result[name][key],  # type: ignore[literal-required]
                    )
                    for key in result[name]
                    if channels[name].get(key) != result[name][key]  # type: ignore[literal-required]
                },
            )
            for name in channel_names_to_reset
        ],
        any_order=False,
    )


def test_reset_channels_invalid_override_key() -> None:
    with pytest.raises(
        ValueError,
        match=r".*invalid_field.*",
    ) as exc_info:
        reset_channels(
            channels=CHANNEL_INFO_BY_NAMES([
                "channel_available",
                "channel_new",
                "channel_unavailable",
            ]),
            channel_overrides={
                "count": 0,
                "invalid_field": 0,
            },
            dry_run=True,
            reset_to_defaults=False,
        )

    assert TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS.format(
        fields={
            "invalid_field",
        },
    ) == str(exc_info.value)


@pytest.mark.parametrize(
    SORT_CHANNEL_NAMES_ARGS,
    SORT_CHANNEL_NAMES_CASES,
)
def test_sort_channel_names(
    channel_names: ChannelNames,
    *,
    ignore_case: bool,
    reverse: bool,
) -> None:
    result = sort_channel_names(
        channel_names=channel_names,
        ignore_case=ignore_case,
        reverse=reverse,
    )

    expected = sorted(
        channel_names,
        key=(
            str.lower if ignore_case else None
        ),
        reverse=reverse,
    )

    assert result == expected
    assert result is not channel_names


@pytest.mark.parametrize(
    UPDATE_LAST_ID_AND_STATE_ARGS,
    UPDATE_LAST_ID_AND_STATE_CASES,
)
def test_update_last_id_and_state(
    mock_logger: Mock,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    last_post_id: PostID,
    expected: ChannelInfo,
) -> None:
    old_last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    update_last_id_and_state(
        channel_name=channel_name,
        channel_info=channel_info,
        last_post_id=last_post_id,
    )

    assert channel_info == expected

    if old_last_id != last_post_id:
        mock_logger.info.assert_called_once_with(
            msg=TEMPLATE_CHANNEL_LOG_UPDATE.format(
                name=channel_name,
                last_id=old_last_id,
                last_post_id=last_post_id,
            ),
        )
    else:
        mock_logger.info.assert_not_called()


@pytest.mark.parametrize(
    UPDATE_WITH_NEW_CHANNELS_ARGS,
    UPDATE_WITH_NEW_CHANNELS_CASES,
)
def test_update_with_new_channels(
    mock_logger: Mock,
    current_channels: ChannelsDict,
    new_channel_names: ChannelNames,
    expected_keys: ChannelNames,
) -> None:
    updated_channels = update_with_new_channels(
        current_channels=current_channels,
        channel_names=new_channel_names,
    )

    assert list(updated_channels) == expected_keys
    assert updated_channels is not current_channels
    assert mock_logger.debug.call_count == len(new_channel_names)

    for name in current_channels:
        assert updated_channels[name] == current_channels[name]
        assert updated_channels[name] is not current_channels[name]

    for name in new_channel_names:
        assert updated_channels[name] == DEFAULT_CHANNEL_VALUES
        assert updated_channels[name] is not DEFAULT_CHANNEL_VALUES

        mock_logger.debug.assert_any_call(
            msg=TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED.format(
                name=name,
            ),
        )
