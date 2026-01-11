import pytest

from tests.unit.domain.constants.examples.channel import (
    ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_EXAMPLES,
    ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_EXAMPLES,
    DELETE_CHANNELS_EXAMPLES,
    DIFF_CHANNEL_ID_EXAMPLES,
    FORMAT_CHANNEL_STATUS_EXAMPLES,
    GET_FILTERED_KEYS_EXAMPLES,
    GET_NORMALIZED_CURRENT_ID_EXAMPLES,
    GET_SORTED_KEYS_EXAMPLES,
    NORMALIZE_CHANNEL_NAMES_EXAMPLES,
    PRINT_CHANNEL_INFO_VARIOUS_EXAMPLES,
    PROCESS_CHANNELS_CALLS_EXAMPLES,
    RESET_CHANNELS_EXAMPLES,
    SORT_CHANNEL_NAMES_EXAMPLES,
    UPDATE_LAST_ID_AND_STATE_EXAMPLES,
    UPDATE_WITH_NEW_CHANNELS_EXAMPLES,
)

__all__ = [
    "ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_ARGS",
    "ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_CASES",
    "ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_ARGS",
    "ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_CASES",
    "DELETE_CHANNELS_ARGS",
    "DELETE_CHANNELS_CASES",
    "DIFF_CHANNEL_ID_ARGS",
    "DIFF_CHANNEL_ID_CASES",
    "FORMAT_CHANNEL_STATUS_ARGS",
    "FORMAT_CHANNEL_STATUS_CASES",
    "GET_FILTERED_KEYS_ARGS",
    "GET_FILTERED_KEYS_CASES",
    "GET_NORMALIZED_CURRENT_ID_ARGS",
    "GET_NORMALIZED_CURRENT_ID_CASES",
    "GET_SORTED_KEYS_ARGS",
    "GET_SORTED_KEYS_CASES",
    "NORMALIZE_CHANNEL_NAMES_ARGS",
    "NORMALIZE_CHANNEL_NAMES_CASES",
    "PRINT_CHANNEL_INFO_VARIOUS_ARGS",
    "PRINT_CHANNEL_INFO_VARIOUS_CASES",
    "PROCESS_CHANNELS_CALLS_ARGS",
    "PROCESS_CHANNELS_CALLS_CASES",
    "RESET_CHANNELS_ARGS",
    "RESET_CHANNELS_CASES",
    "SORT_CHANNEL_NAMES_ARGS",
    "SORT_CHANNEL_NAMES_CASES",
    "UPDATE_LAST_ID_AND_STATE_ARGS",
    "UPDATE_LAST_ID_AND_STATE_CASES",
    "UPDATE_WITH_NEW_CHANNELS_ARGS",
    "UPDATE_WITH_NEW_CHANNELS_CASES",
]

ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_ARGS = (
    "invalid_offset",
)
ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_CASES = tuple(
    pytest.param(
        invalid_offset,
        id=case_id,
    )
    for (
        invalid_offset,
        case_id,
    ) in ASSIGN_CURRENT_ID_TO_CHANNELS_INVALID_OFFSET_EXAMPLES
)

ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_ARGS = (
    "channels",
    "message_offset",
    "dry_run",
    "expected_current_ids",
)
ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_CASES = tuple(
    pytest.param(
        channels,
        message_offset,
        dry_run,
        expected_current_ids,
        id=case_id,
    )
    for (
        channels,
        message_offset,
        dry_run,
        expected_current_ids,
        case_id,
    ) in ASSIGN_CURRENT_ID_TO_CHANNELS_VARIOUS_EXAMPLES
)

DELETE_CHANNELS_ARGS = (
    "channels",
    "expected_keys_to_keep",
    "expected_deleted",
)
DELETE_CHANNELS_CASES = tuple(
    pytest.param(
        channels,
        expected_keys_to_keep,
        expected_deleted,
        id=case_id,
    )
    for (
        channels,
        expected_keys_to_keep,
        expected_deleted,
        case_id,
    ) in DELETE_CHANNELS_EXAMPLES
)

DIFF_CHANNEL_ID_ARGS = (
    "channel_info",
    "expected",
)
DIFF_CHANNEL_ID_CASES = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in DIFF_CHANNEL_ID_EXAMPLES
)

FORMAT_CHANNEL_STATUS_ARGS = (
    "channel_name",
    "channel_info",
)
FORMAT_CHANNEL_STATUS_CASES = tuple(
    pytest.param(
        channel_name,
        channel_info,
        id=case_id,
    )
    for (
        channel_name,
        channel_info,
        case_id,
    ) in FORMAT_CHANNEL_STATUS_EXAMPLES
)

GET_FILTERED_KEYS_ARGS = (
    "channels",
    "expected",
)
GET_FILTERED_KEYS_CASES = tuple(
    pytest.param(
        channels,
        expected,
        id=case_id,
    )
    for (
        channels,
        expected,
        case_id,
    ) in GET_FILTERED_KEYS_EXAMPLES
)

GET_NORMALIZED_CURRENT_ID_ARGS = (
    "channel_info",
    "expected",
)
GET_NORMALIZED_CURRENT_ID_CASES = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in GET_NORMALIZED_CURRENT_ID_EXAMPLES
)

GET_SORTED_KEYS_ARGS = (
    "channels",
    "apply_filter",
    "reverse",
    "expected",
)
GET_SORTED_KEYS_CASES = tuple(
    pytest.param(
        channels,
        apply_filter,
        reverse,
        expected,
        id=case_id,
    )
    for (
        channels,
        apply_filter,
        reverse,
        expected,
        case_id,
    ) in GET_SORTED_KEYS_EXAMPLES
)

NORMALIZE_CHANNEL_NAMES_ARGS = (
    "channels",
    "expected",
)
NORMALIZE_CHANNEL_NAMES_CASES = tuple(
    pytest.param(
        channels,
        expected,
        id=case_id,
    )
    for (
        channels,
        expected,
        case_id,
    ) in NORMALIZE_CHANNEL_NAMES_EXAMPLES
)

PRINT_CHANNEL_INFO_VARIOUS_ARGS = (
    "channels",
)
PRINT_CHANNEL_INFO_VARIOUS_CASES = tuple(
    pytest.param(
        channels,
        id=case_id,
    )
    for (
        channels,
        case_id,
    ) in PRINT_CHANNEL_INFO_VARIOUS_EXAMPLES
)

PROCESS_CHANNELS_CALLS_ARGS = (
    "message_offset",
    "dry_run",
    "delete_channels_flag",
    "reset_all",
)
PROCESS_CHANNELS_CALLS_CASES = tuple(
    pytest.param(
        message_offset,
        dry_run,
        delete_channels_flag,
        reset_all,
        id=case_id,
    )
    for (
        message_offset,
        dry_run,
        delete_channels_flag,
        reset_all,
        case_id,
    ) in PROCESS_CHANNELS_CALLS_EXAMPLES
)

RESET_CHANNELS_ARGS = (
    "channel_overrides",
    "channel_predicate",
    "dry_run",
    "reset_to_defaults",
)
RESET_CHANNELS_CASES = tuple(
    pytest.param(
        channel_overrides,
        channel_predicate,
        dry_run,
        reset_to_defaults,
        id=(
            f"{case_id}_"
            f"{'dry' if dry_run else 'no_dry'}_"
            f"{'reset_defaults' if reset_to_defaults else 'no_reset'}"
        ),
    )
    for (
        channel_overrides,
        channel_predicate,
        case_id,
    ) in RESET_CHANNELS_EXAMPLES
    for dry_run in (
        True,
        False,
    )
    for reset_to_defaults in (
        False,
        True,
    )
)

SORT_CHANNEL_NAMES_ARGS = (
    "channel_names",
    "ignore_case",
    "reverse",
)
SORT_CHANNEL_NAMES_CASES = tuple(
    pytest.param(
        names,
        ignore_case,
        reverse,
        id=(
            f"{case_id}_"
            f"{'ignore_case' if ignore_case else 'sensitive'}_"
            f"{'reverse' if reverse else 'normal'}"
        ),
    )
    for (
        names,
        case_id,
    ) in SORT_CHANNEL_NAMES_EXAMPLES
    for ignore_case in (
        True,
        False,
    )
    for reverse in (
        False,
        True,
    )
)

UPDATE_LAST_ID_AND_STATE_ARGS = (
    "channel_name",
    "channel_info",
    "last_post_id",
    "expected",
)
UPDATE_LAST_ID_AND_STATE_CASES = tuple(
    pytest.param(
        channel_name,
        channel_info,
        last_post_id,
        expected,
        id=case_id,
    )
    for (
        channel_name,
        channel_info,
        last_post_id,
        expected,
        case_id,
    ) in UPDATE_LAST_ID_AND_STATE_EXAMPLES
)

UPDATE_WITH_NEW_CHANNELS_ARGS = (
    "current_channels",
    "new_channel_names",
    "expected_keys",
)
UPDATE_WITH_NEW_CHANNELS_CASES = tuple(
    pytest.param(
        current_channels,
        new_channel_names,
        expected_keys,
        id=case_id,
    )
    for (
        current_channels,
        new_channel_names,
        expected_keys,
        case_id,
    ) in UPDATE_WITH_NEW_CHANNELS_EXAMPLES
)
