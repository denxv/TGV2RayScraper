import pytest

from tests.unit.domain.constants.examples.channel import (
    APPLY_CHANNEL_CHANGES_EXAMPLES,
    DELETE_CHANNELS_EXAMPLES,
    DIFF_CHANNEL_ID_EXAMPLES,
    DISPLAY_CHANNEL_INFO_VARIOUS_EXAMPLES,
    FORMAT_CHANNEL_STATUS_EXAMPLES,
    GET_FILTERED_KEYS_EXAMPLES,
    GET_NORMALIZED_COUNT_EXAMPLES,
    GET_NORMALIZED_CURRENT_ID_EXAMPLES,
    GET_NORMALIZED_LAST_ID_EXAMPLES,
    GET_NORMALIZED_STATE_EXAMPLES,
    GET_SORTED_KEYS_EXAMPLES,
    NORMALIZE_CHANNEL_EXAMPLES,
    NORMALIZE_CHANNEL_NAMES_EXAMPLES,
    NORMALIZE_CHANNELS_EXAMPLES,
    PROCESS_CHANNELS_CALLS_EXAMPLES,
    SORT_CHANNEL_NAMES_EXAMPLES,
    UPDATE_LAST_ID_AND_STATE_EXAMPLES,
    UPDATE_WITH_NEW_CHANNELS_EXAMPLES,
)

__all__ = [
    "APPLY_CHANNEL_CHANGES_ARGS",
    "APPLY_CHANNEL_CHANGES_CASES",
    "DELETE_CHANNELS_ARGS",
    "DELETE_CHANNELS_CASES",
    "DIFF_CHANNEL_ID_ARGS",
    "DIFF_CHANNEL_ID_CASES",
    "DISPLAY_CHANNEL_INFO_VARIOUS_ARGS",
    "DISPLAY_CHANNEL_INFO_VARIOUS_CASES",
    "FORMAT_CHANNEL_STATUS_ARGS",
    "FORMAT_CHANNEL_STATUS_CASES",
    "GET_FILTERED_KEYS_ARGS",
    "GET_FILTERED_KEYS_CASES",
    "GET_NORMALIZED_COUNT_ARGS",
    "GET_NORMALIZED_COUNT_CASES",
    "GET_NORMALIZED_CURRENT_ID_ARGS",
    "GET_NORMALIZED_CURRENT_ID_CASES",
    "GET_NORMALIZED_LAST_ID_ARGS",
    "GET_NORMALIZED_LAST_ID_CASES",
    "GET_NORMALIZED_STATE_ARGS",
    "GET_NORMALIZED_STATE_CASES",
    "GET_SORTED_KEYS_ARGS",
    "GET_SORTED_KEYS_CASES",
    "NORMALIZE_CHANNELS_ARGS",
    "NORMALIZE_CHANNELS_CASES",
    "NORMALIZE_CHANNEL_ARGS",
    "NORMALIZE_CHANNEL_CASES",
    "NORMALIZE_CHANNEL_NAMES_ARGS",
    "NORMALIZE_CHANNEL_NAMES_CASES",
    "PROCESS_CHANNELS_CALLS_ARGS",
    "PROCESS_CHANNELS_CALLS_CASES",
    "SORT_CHANNEL_NAMES_ARGS",
    "SORT_CHANNEL_NAMES_CASES",
    "UPDATE_LAST_ID_AND_STATE_ARGS",
    "UPDATE_LAST_ID_AND_STATE_CASES",
    "UPDATE_WITH_NEW_CHANNELS_ARGS",
    "UPDATE_WITH_NEW_CHANNELS_CASES",
]

APPLY_CHANNEL_CHANGES_ARGS: tuple[
    str,
    ...,
] = (
    "channel_overrides",
    "channel_predicate",
    "dry_run",
    "reset_to_defaults",
)
APPLY_CHANNEL_CHANGES_CASES: tuple[
    object,
    ...,
] = tuple(
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
    ) in APPLY_CHANNEL_CHANGES_EXAMPLES
    for dry_run in (
        True,
        False,
    )
    for reset_to_defaults in (
        False,
        True,
    )
)

DELETE_CHANNELS_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
    "expected_keys_to_keep",
    "expected_deleted",
)
DELETE_CHANNELS_CASES: tuple[
    object,
    ...,
] = tuple(
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

DIFF_CHANNEL_ID_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
DIFF_CHANNEL_ID_CASES: tuple[
    object,
    ...,
] = tuple(
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

DISPLAY_CHANNEL_INFO_VARIOUS_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
)
DISPLAY_CHANNEL_INFO_VARIOUS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channels,
        id=case_id,
    )
    for (
        channels,
        case_id,
    ) in DISPLAY_CHANNEL_INFO_VARIOUS_EXAMPLES
)

FORMAT_CHANNEL_STATUS_ARGS: tuple[
    str,
    ...,
] = (
    "channel_name",
    "channel_info",
)
FORMAT_CHANNEL_STATUS_CASES: tuple[
    object,
    ...,
] = tuple(
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

GET_FILTERED_KEYS_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
    "expected",
)
GET_FILTERED_KEYS_CASES: tuple[
    object,
    ...,
] = tuple(
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

GET_NORMALIZED_COUNT_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
GET_NORMALIZED_COUNT_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in GET_NORMALIZED_COUNT_EXAMPLES
)

GET_NORMALIZED_CURRENT_ID_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
GET_NORMALIZED_CURRENT_ID_CASES: tuple[
    object,
    ...,
] = tuple(
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

GET_NORMALIZED_LAST_ID_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
GET_NORMALIZED_LAST_ID_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in GET_NORMALIZED_LAST_ID_EXAMPLES
)

GET_NORMALIZED_STATE_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
GET_NORMALIZED_STATE_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in GET_NORMALIZED_STATE_EXAMPLES
)

GET_SORTED_KEYS_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
    "apply_filter",
    "reverse",
    "expected",
)
GET_SORTED_KEYS_CASES: tuple[
    object,
    ...,
] = tuple(
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

NORMALIZE_CHANNEL_ARGS: tuple[
    str,
    ...,
] = (
    "channel_info",
    "expected",
)
NORMALIZE_CHANNEL_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channel_info,
        expected,
        id=case_id,
    )
    for (
        channel_info,
        expected,
        case_id,
    ) in NORMALIZE_CHANNEL_EXAMPLES
)

NORMALIZE_CHANNEL_NAMES_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
    "expected",
)
NORMALIZE_CHANNEL_NAMES_CASES: tuple[
    object,
    ...,
] = tuple(
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

NORMALIZE_CHANNELS_ARGS: tuple[
    str,
    ...,
] = (
    "channels",
    "expected",
)
NORMALIZE_CHANNELS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        channels,
        expected,
        id=case_id,
    )
    for (
        channels,
        expected,
        case_id,
    ) in NORMALIZE_CHANNELS_EXAMPLES
)

PROCESS_CHANNELS_CALLS_ARGS: tuple[
    str,
    ...,
] = (
    "dry_run",
    "reset_all",
    "should_delete",
)
PROCESS_CHANNELS_CALLS_CASES: tuple[
    object,
    ...,
] = tuple(
    pytest.param(
        dry_run,
        reset_all,
        should_delete,
        id=case_id,
    )
    for (
        dry_run,
        reset_all,
        should_delete,
        case_id,
    ) in PROCESS_CHANNELS_CALLS_EXAMPLES
)

SORT_CHANNEL_NAMES_ARGS: tuple[
    str,
    ...,
] = (
    "channel_names",
    "ignore_case",
    "reverse",
)
SORT_CHANNEL_NAMES_CASES: tuple[
    object,
    ...,
] = tuple(
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

UPDATE_LAST_ID_AND_STATE_ARGS: tuple[
    str,
    ...,
] = (
    "channel_name",
    "channel_info",
    "last_post_id",
    "expected",
)
UPDATE_LAST_ID_AND_STATE_CASES: tuple[
    object,
    ...,
] = tuple(
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

UPDATE_WITH_NEW_CHANNELS_ARGS: tuple[
    str,
    ...,
] = (
    "current_channels",
    "new_channel_names",
    "expected_keys",
)
UPDATE_WITH_NEW_CHANNELS_CASES: tuple[
    object,
    ...,
] = tuple(
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
