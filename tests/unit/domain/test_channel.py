from argparse import (
    Namespace,
)
from unittest.mock import (
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
    sort_channel_names,
    update_count_and_last_id,
    update_with_new_channels,
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
    TEMPLATE_CHANNEL_TOTAL_AVAILABLE,
    TEMPLATE_CHANNEL_TOTAL_MESSAGES,
    TEMPLATE_ERROR_INVALID_OFFSET,
    TEMPLATE_FORMAT_STRING_QUOTED_NAME,
    TEMPLATE_TITLE_DEBUG_OFFSET,
    TEMPLATE_TITLE_DELETING_CHANNEL,
)
from tests.unit.domain.constants.fixtures.channel import (
    CHANNEL_INFO_BY_NAMES,
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
    SORT_CHANNEL_NAMES_ARGS,
    SORT_CHANNEL_NAMES_CASES,
    UPDATE_COUNT_AND_LAST_ID_ARGS,
    UPDATE_COUNT_AND_LAST_ID_CASES,
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
    check_only: bool,
    expected_current_ids: dict[str, int],
) -> None:
    updated_channels = assign_current_id_to_channels(
        channels=channels,
        message_offset=message_offset,
        check_only=check_only,
    )

    for name, expected_id in expected_current_ids.items():
        assert updated_channels[name]["current_id"] == expected_id

    for name, info in channels.items():
        diff = diff_channel_id(
            channel_info=info,
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

        if check_only:
            mock_log_debug_object.assert_called_with(
                title=TEMPLATE_TITLE_DEBUG_OFFSET.format(
                    name=name,
                    check_only=check_only,
                ),
                obj=info,
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

    if check_only:
        mock_logger.debug.assert_any_call(
            msg=TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED.format(
                check_only=check_only,
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
                title=TEMPLATE_TITLE_DELETING_CHANNEL.format(
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
    expected_calls = [
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
    check_only: bool,
    delete_channels_flag: bool,
) -> None:
    channels = CHANNEL_INFO_BY_NAMES([
        "channel_available",
        "channel_new",
        "channel_unavailable",
    ])

    mock_delete = mocker.patch(
        "domain.channel.delete_channels",
        wraps=delete_channels,
    )
    mock_assign = mocker.patch(
        "domain.channel.assign_current_id_to_channels",
        wraps=assign_current_id_to_channels,
    )

    args = Namespace(
        delete_channels=delete_channels_flag,
        message_offset=message_offset,
        check_only=check_only,
    )

    result = process_channels(
        channels=channels,
        args=args,
    )

    if delete_channels_flag or message_offset:
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
            channels=channels,
            message_offset=message_offset,
            check_only=check_only,
        )
    else:
        mock_assign.assert_not_called()


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
    UPDATE_COUNT_AND_LAST_ID_ARGS,
    UPDATE_COUNT_AND_LAST_ID_CASES,
)
def test_update_count_and_last_id(
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

    update_count_and_last_id(
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
