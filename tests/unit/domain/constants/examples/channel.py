from core.typing import (
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    PostID,
    RecordPredicate,
)
from tests.unit.domain.constants.common import (
    CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
    CHANNEL_MIN_ID_DIFF,
    CHANNEL_STATE_AVAILABLE,
    CHANNEL_STATE_UNAVAILABLE,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    DEFAULT_STATE,
    LAST_POST_ID,
    MESSAGE_OFFSET,
    NUM1,
    NUM2,
    NUM3,
)
from tests.unit.domain.constants.fixtures.channel import (
    CHANNEL_AVAILABLE,
    CHANNEL_BASE,
    CHANNEL_BASE_SAMPLE,
    CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
    CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
    CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
    CHANNEL_DEFAULT_COUNT,
    CHANNEL_DEFAULT_CURRENT_ID,
    CHANNEL_DEFAULT_LAST_ID,
    CHANNEL_DEFAULT_STATE,
    CHANNEL_INFO_BY_NAME,
    CHANNEL_INFO_BY_NAMES,
    CHANNEL_MISSING_COUNT,
    CHANNEL_MISSING_CURRENT_ID,
    CHANNEL_MISSING_LAST_ID,
    CHANNEL_MISSING_STATE,
    CHANNEL_NAMES_SAMPLE,
    CHANNEL_NEGATIVE_CURRENT_ID,
    CHANNEL_NEW,
    CHANNEL_REMOVED,
    CHANNEL_UNAVAILABLE,
    CHANNEL_ZERO_CURRENT_ID,
    CHANNELS_FROM_NAMES_SAMPLE,
    CHANNELS_SAMPLE,
)

__all__ = [
    "APPLY_CHANNEL_CHANGES_EXAMPLES",
    "DELETE_CHANNELS_EXAMPLES",
    "DIFF_CHANNEL_ID_EXAMPLES",
    "DISPLAY_CHANNEL_INFO_VARIOUS_EXAMPLES",
    "FORMAT_CHANNEL_STATUS_EXAMPLES",
    "GET_FILTERED_KEYS_EXAMPLES",
    "GET_NORMALIZED_COUNT_EXAMPLES",
    "GET_NORMALIZED_CURRENT_ID_EXAMPLES",
    "GET_NORMALIZED_LAST_ID_EXAMPLES",
    "GET_NORMALIZED_STATE_EXAMPLES",
    "GET_SORTED_KEYS_EXAMPLES",
    "NORMALIZE_CHANNELS_EXAMPLES",
    "NORMALIZE_CHANNEL_EXAMPLES",
    "NORMALIZE_CHANNEL_NAMES_EXAMPLES",
    "PROCESS_CHANNELS_CALLS_EXAMPLES",
    "SORT_CHANNEL_NAMES_EXAMPLES",
    "UPDATE_LAST_ID_AND_STATE_EXAMPLES",
    "UPDATE_WITH_NEW_CHANNELS_EXAMPLES",
]

APPLY_CHANNEL_CHANGES_EXAMPLES: tuple[
    tuple[
        ChannelInfo | None,
        RecordPredicate | None,
        str,
    ],
    ...,
] = (  # type: ignore[assignment]
    (
        {},
        lambda channel: channel["current_id"] == channel["last_id"],
        "empty_overrides_and_predicate",
    ),
    (
        {},
        None,
        "empty_overrides_no_predicate",
    ),
    (
        None,
        None,
        "no_overrides_no_predicate",
    ),
    (
        {
            "current_id": NUM1 + NUM2 + NUM3,
        },
        lambda channel: channel["count"] > 0,  # type: ignore[operator]
        "overrides_and_predicate",
    ),
    (
        {
            "count": NUM1 + NUM2 + NUM3,
            "state": -NUM1,
        },
        None,
        "overrides_only",
    ),
    (
        None,
        lambda channel: channel["state"] == 0,
        "predicate_only",
    ),
)

DELETE_CHANNELS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        ChannelNames,
        ChannelNames,
        str,
    ],
    ...,
] = (
    (
        {
            channel_name: {
                **CHANNEL_AVAILABLE,
            }
            for channel_name in CHANNEL_NAMES_SAMPLE
        },
        CHANNEL_NAMES_SAMPLE,
        [],
        "all_channels_available",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_scanned_no_found_configs",
            "channel_scanned_below_remove_threshold",
            "channel_scanned_remove_threshold",
        ]),
        [],
        [
            "channel_scanned_no_found_configs",
            "channel_scanned_below_remove_threshold",
            "channel_scanned_remove_threshold",
        ],
        "all_channels_delete",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_available",
            "channel_default_count_and_current_gt_last",
            "channel_new",
        ]),
        [
            "channel_available",
            "channel_new",
        ],
        [
            "channel_default_count_and_current_gt_last",
        ],
        "boundary_values",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_gt_last",
            "channel_default_count_and_current_gt_last",
            "channel_scanned_found_configs",
        ]),
        [
            "channel_base_current_gt_last",
            "channel_scanned_found_configs",
        ],
        [
            "channel_default_count_and_current_gt_last",
        ],
        "current_gt_last",
    ),
    (
        {},
        [],
        [],
        "empty",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_removed",
            "channel_removed_below_threshold",
            "channel_scanned_found_configs",
        ]),
        [
            "channel_scanned_found_configs",
        ],
        [
            "channel_removed",
            "channel_removed_below_threshold",
        ],
        "failed_threshold",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_scanned_found_configs",
            "channel_scanned_no_found_configs",
        ]),
        [
            "channel_scanned_found_configs",
        ],
        [
            "channel_scanned_no_found_configs",
        ],
        "one_delete",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_lt_last",
            "channel_default_count_and_current_gt_last",
            "channel_scanned_below_remove_threshold",
        ]),
        [
            "channel_base_current_lt_last",
        ],
        [
            "channel_default_count_and_current_gt_last",
            "channel_scanned_below_remove_threshold",
        ],
        "partial_delete",
    ),
)

DIFF_CHANNEL_ID_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        int,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
        max(
            CHANNEL_MIN_ID_DIFF,
            NUM2 - min(NUM3, NUM2),
        ),
        "current_greater_than_last",
    ),
    (
        {},  # type: ignore[typeddict-item]
        max(
            CHANNEL_MIN_ID_DIFF,
            DEFAULT_LAST_ID - DEFAULT_CURRENT_ID,
        ),
        "empty_channel",
    ),
    (
        CHANNEL_DEFAULT_LAST_ID,
        max(
            CHANNEL_MIN_ID_DIFF,
            DEFAULT_LAST_ID - DEFAULT_CURRENT_ID,
        ),
        "last_id_default",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "current_id": -MESSAGE_OFFSET,
        },
        max(
            CHANNEL_MIN_ID_DIFF,
            NUM3 - (NUM3 + -MESSAGE_OFFSET),
        ),
        "negative_current",
    ),
    (
        CHANNEL_NEW,
        max(
            CHANNEL_MIN_ID_DIFF,
            DEFAULT_LAST_ID - DEFAULT_CURRENT_ID,
        ),
        "new_channel",
    ),
    (
        CHANNEL_BASE_SAMPLE,
        max(
            CHANNEL_MIN_ID_DIFF,
            NUM3 - NUM2,
        ),
        "normal_difference",
    ),
)

DISPLAY_CHANNEL_INFO_VARIOUS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        str,
    ],
    ...,
] = (
    (
        CHANNELS_SAMPLE,
        "mixed_channels",
    ),
    (
        {},
        "no_channels",
    ),
    (
        CHANNEL_INFO_BY_NAME(
            "channel_base_current_equal_last",
        ),
        "single_channel_equal",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_gt_last",
            "channel_base_current_lt_last",
        ]),
        "two_channels",
    ),
)

FORMAT_CHANNEL_STATUS_EXAMPLES: tuple[
    tuple[
        ChannelName,
        ChannelInfo,
        str,
    ],
    ...,
] = (
    (
        "channel_base_current_equal_last",
        CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
        "current_equal_last",
    ),
    (
        "channel_zero_current_id",
        CHANNEL_ZERO_CURRENT_ID,
        "current_zero",
    ),
    (
        "channel_missing_values",
        {},  # type: ignore[typeddict-item]
        "missing_values",
    ),
    (
        "channel_normal",
        CHANNEL_BASE_SAMPLE,
        "normal_case",
    ),
)

GET_FILTERED_KEYS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        ChannelNames,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_INFO_BY_NAME(
            "channel_new",
        ),
        [],
        "channel_new",
    ),
    (
        {},
        [],
        "empty_input",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_equal_last",
            "channel_base_current_lt_last",
            "channel_negative_current_id",
            "channel_new",
            "channel_zero_current_id",
        ]),
        [
            "channel_base_current_lt_last",
            "channel_negative_current_id",
            "channel_zero_current_id",
        ],
        "mixed_channels_some_update",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_scanned_found_configs",
            "channel_scanned_no_found_configs",
            "channel_unavailable",
        ]),
        [],
        "no_channels_need_update",
    ),
    (
        CHANNEL_INFO_BY_NAME(
            "channel_available",
        ),
        [
            "channel_available",
        ],
        "single_channel_update",
    ),
)

GET_NORMALIZED_COUNT_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        int,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_DEFAULT_COUNT,
        DEFAULT_COUNT,
        "default_count",
    ),
    (
        {},  # type: ignore[typeddict-item]
        DEFAULT_COUNT,
        "empty_dict",
    ),
    (
        CHANNEL_MISSING_COUNT,
        DEFAULT_COUNT,
        "missing_count",
    ),
    (
        {
            **CHANNEL_BASE,
            "count": -NUM1,
        },
        DEFAULT_COUNT,
        "negative_count",
    ),
    (
        CHANNEL_BASE_SAMPLE,
        NUM1,
        "positive_count",
    ),
)

GET_NORMALIZED_CURRENT_ID_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        PostID,
        str,
    ],
    ...,
] = (
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "current_id": DEFAULT_CURRENT_ID,
        },
        DEFAULT_CURRENT_ID,
        "absolute_current_at_default",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
        NUM3,
        "absolute_current_equal_last",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
        NUM2,
        "absolute_current_gt_last_clamped",
    ),
    (
        CHANNEL_BASE_SAMPLE,
        min(
            NUM2,
            NUM3,
        ),
        "absolute_current_lt_last",
    ),
    (
        CHANNEL_DEFAULT_CURRENT_ID,
        DEFAULT_CURRENT_ID,
        "default_current_id",
    ),
    (
        {
            **CHANNEL_DEFAULT_LAST_ID,
            "current_id": -NUM2,
        },
        DEFAULT_CURRENT_ID,
        "default_last_id_with_negative_current",
    ),
    (
        CHANNEL_DEFAULT_LAST_ID,
        max(
            NUM2,
            DEFAULT_CURRENT_ID,
        ),
        "default_last_id_with_positive_current",
    ),
    (
        {
            **CHANNEL_DEFAULT_LAST_ID,
            "current_id": NUM2 - NUM2,
        },
        DEFAULT_CURRENT_ID,
        "default_last_id_with_zero_current",
    ),
    (
        {},  # type: ignore[typeddict-item]
        DEFAULT_CURRENT_ID,
        "empty_dict",
    ),
    (
        CHANNEL_MISSING_CURRENT_ID,
        DEFAULT_CURRENT_ID,
        "missing_current_id_with_default_last_id",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "current_id": -(NUM3 * NUM3),
        },
        DEFAULT_CURRENT_ID,
        "relative_negative_below_default_clamped",
    ),
    (
        CHANNEL_NEGATIVE_CURRENT_ID,
        max(
            NUM3 - NUM2,
            DEFAULT_CURRENT_ID,
        ),
        "relative_negative_current",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "current_id": -(NUM3 - NUM2),
        },
        NUM2,
        "relative_negative_resolves_to_different_value",
    ),
    (
        CHANNEL_ZERO_CURRENT_ID,
        max(
            NUM3,
            DEFAULT_CURRENT_ID,
        ),
        "relative_zero_current",
    ),
)

GET_NORMALIZED_LAST_ID_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        PostID,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_DEFAULT_LAST_ID,
        DEFAULT_LAST_ID,
        "default_last_id",
    ),
    (
        {},  # type: ignore[typeddict-item]
        DEFAULT_LAST_ID,
        "empty_dict",
    ),
    (
        CHANNEL_MISSING_LAST_ID,
        DEFAULT_LAST_ID,
        "missing_last_id",
    ),
    (
        {
            **CHANNEL_BASE,
            "last_id": -NUM3,
        },
        DEFAULT_LAST_ID,
        "negative_last_id",
    ),
    (
        CHANNEL_BASE_SAMPLE,
        NUM3,
        "positive_last_id",
    ),
    (
        {
            **CHANNEL_BASE,
            "last_id": NUM3 - NUM3,
        },
        DEFAULT_LAST_ID,
        "zero_last_id",
    ),
)

GET_NORMALIZED_STATE_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        int,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_DEFAULT_STATE,
        DEFAULT_STATE,
        "default_state_with_default_last_id",
    ),
    (
        {},  # type: ignore[typeddict-item]
        DEFAULT_STATE,
        "empty_dict",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "state": NUM1 * NUM1,
        },
        CHANNEL_STATE_AVAILABLE,
        "high_state_ignored_with_positive_last_id",
    ),
    (
        CHANNEL_MISSING_STATE,
        DEFAULT_STATE,
        "missing_state_with_default_last_id",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE,
            "state": -NUM1,
        },
        CHANNEL_STATE_AVAILABLE,
        "negative_state_ignored_with_positive_last_id",
    ),
    (
        {
            **CHANNEL_DEFAULT_LAST_ID,
            "state": -NUM1,
        },
        min(
            -NUM1,
            DEFAULT_STATE,
        ),
        "negative_state_with_default_last_id",
    ),
    (
        CHANNEL_BASE_SAMPLE,
        CHANNEL_STATE_AVAILABLE,
        "positive_last_id_returns_available",
    ),
    (
        {
            **CHANNEL_DEFAULT_LAST_ID,
            "state": NUM1,
        },
        min(
            NUM1,
            DEFAULT_STATE,
        ),
        "positive_state_above_default_with_default_last_id",
    ),
    (
        CHANNEL_REMOVED,
        min(
            CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
            DEFAULT_STATE,
        ),
        "removed_state_with_default_last_id",
    ),
    (
        CHANNEL_UNAVAILABLE,
        min(
            CHANNEL_STATE_UNAVAILABLE,
            DEFAULT_STATE,
        ),
        "unavailable_state_with_default_last_id",
    ),
)

GET_SORTED_KEYS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        bool,
        bool,
        ChannelNames,
        str,
    ],
    ...,
] = (
    (
        CHANNELS_SAMPLE,
        True,
        False,
        [
            "channel_zero_current_id",
            "channel_available",
            "channel_base_current_lt_last",
            "channel_negative_current_id",
        ],
        "apply_filter",
    ),
    (
        {},
        False,
        False,
        [],
        "empty_input",
    ),
    (
        CHANNELS_FROM_NAMES_SAMPLE,
        False,
        False,
        sorted(
            CHANNEL_NAMES_SAMPLE,
            reverse=False,
        ),
        "equal_values_normal_sort",
    ),
    (
        CHANNELS_FROM_NAMES_SAMPLE,
        False,
        True,
        sorted(
            CHANNEL_NAMES_SAMPLE,
            reverse=True,
        ),
        "equal_values_reverse_sort",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_available",
            "channel_base_current_gt_last",
            "channel_negative_current_id",
            "channel_new",
            "channel_unavailable",
        ]),
        False,
        False,
        [
            "channel_base_current_gt_last",
            "channel_new",
            "channel_unavailable",
            "channel_available",
            "channel_negative_current_id",
        ],
        "normal_sort",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_gt_last",
            "channel_negative_current_id",
            "channel_unavailable",
        ]),
        False,
        False,
        [
            "channel_base_current_gt_last",
            "channel_unavailable",
            "channel_negative_current_id",
        ],
        "normalized_channels_sort",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_available",
            "channel_base_current_gt_last",
            "channel_negative_current_id",
            "channel_new",
            "channel_unavailable",
        ]),
        False,
        True,
        [
            "channel_negative_current_id",
            "channel_available",
            "channel_unavailable",
            "channel_new",
            "channel_base_current_gt_last",
        ],
        "reverse_sort",
    ),
    (
        CHANNEL_INFO_BY_NAME(
            "channel_available",
        ),
        False,
        False,
        [
            "channel_available",
        ],
        "single_channel",
    ),
)

NORMALIZE_CHANNEL_EXAMPLES: tuple[
    tuple[
        ChannelInfo,
        ChannelInfo,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_BASE,
        CHANNEL_BASE,
        "default_values",
    ),
    (
        {},  # type: ignore[typeddict-item]
        CHANNEL_BASE,
        "empty_channel_info",
    ),
)

NORMALIZE_CHANNEL_NAMES_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        ChannelsDict,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_lower_one",
            "channel_lower_two",
        ]),
        CHANNEL_INFO_BY_NAMES([
            "channel_lower_one",
            "channel_lower_two",
        ]),
        "all_channel_names_lowercase",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "CHANNEL_UPPER_ONE",
            "CHANNEL_UPPER_TWO",
        ]),
        CHANNEL_INFO_BY_NAMES([
            "channel_upper_one",
            "channel_upper_two",
        ]),
        "all_channel_names_uppercase",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_Available",
            "channel_available",
            "channel_new",
            "channel_NEW",
            "channel_unavailable",
        ]),
        {
            "channel_available": {
                **CHANNEL_BASE,
            },
            **CHANNEL_INFO_BY_NAMES([
                "channel_new",
                "channel_unavailable",
            ]),
        },
        "duplicates_keep_first",
    ),
    (
        {
            name: {  # type: ignore[misc]
                **CHANNEL_BASE,
            }
            for name in (
                NUM1,
                f"channel_{NUM2}",
                float(NUM3),
            )
        },
        {
            str(name): {
                **CHANNEL_BASE,
            }
            for name in (
                NUM1,
                f"channel_{NUM2}",
                float(NUM3),
            )
        },
        "mixed_key_types",
    ),
    (
        {},
        {},
        "no_channels",
    ),
)

NORMALIZE_CHANNELS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        ChannelsDict,
        str,
    ],
    ...,
] = (
    (
        {
            "CHANNEL_BASE_CURRENT_EQUAL_LAST": {
                **CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
            },
            "channel_negative_current_ID": {
                **CHANNEL_NEGATIVE_CURRENT_ID,
            },
            "channel_ZERO_current_id": {
                **CHANNEL_ZERO_CURRENT_ID,
            },
        },
        {
            "channel_base_current_equal_last": {
                **CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
            },
            "channel_negative_current_id": {
                **CHANNEL_NEGATIVE_CURRENT_ID,
                "current_id": NUM3 - NUM2,
            },
            "channel_zero_current_id": {
                **CHANNEL_ZERO_CURRENT_ID,
                "current_id": NUM3 - (NUM2 - NUM2),
            },
        },
        "channel_names_and_values_normalized",
    ),
    (
        CHANNEL_INFO_BY_NAMES([
            "channel_base_current_equal_last",
            "channel_base_current_lt_last",
            "channel_negative_current_id",
            "channel_new",
            "channel_zero_current_id",
        ]),
        {
            "channel_base_current_equal_last": {
                **CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
            },
            "channel_base_current_lt_last": {
                **CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
            },
            "channel_negative_current_id": {
                **CHANNEL_NEGATIVE_CURRENT_ID,
                "current_id": NUM3 - NUM2,
            },
            "channel_new": {
                **CHANNEL_NEW,
            },
            "channel_zero_current_id": {
                **CHANNEL_ZERO_CURRENT_ID,
                "current_id": NUM3 - (NUM2 - NUM2),
            },
        },
        "channel_values_normalized",
    ),
    (
        {},
        {},
        "no_channels",
    ),
)

PROCESS_CHANNELS_CALLS_EXAMPLES: tuple[
    tuple[
        bool,
        bool,
        bool,
        str,
    ],
    ...,
] = (
    (
        True,
        True,
        True,
        "conflict_all_dry_run",
    ),
    (
        False,
        True,
        True,
        "conflict_delete_and_reset",
    ),
    (
        False,
        True,
        False,
        "delete_only",
    ),
    (
        True,
        True,
        False,
        "delete_only_dry_run",
    ),
    (
        False,
        False,
        False,
        "no_action",
    ),
    (
        False,
        False,
        True,
        "reset_all_only",
    ),
    (
        True,
        False,
        True,
        "reset_all_only_dry_run",
    ),
)

SORT_CHANNEL_NAMES_EXAMPLES: tuple[
    tuple[
        ChannelNames,
        str,
    ],
    ...,
] = (
    (
        [
            "channel_a",
            "channel_b",
            "channel_c",
        ],
        "already_sorted",
    ),
    (
        [
            "channel_b",
            "channel_c",
            "CHANNEL_B",
        ],
        "base_case",
    ),
    (
        [
            "channel_c2",
            "CHANNEL_C1",
            "channel_b3",
            "CHANNEL_B2",
        ],
        "digits_letters",
    ),
    (
        [
            "channel_a",
            "CHANNEL_A",
            "channel_b",
            "CHANNEL_B",
        ],
        "duplicates",
    ),
    (
        [],
        "empty_list",
    ),
    (
        [
            "",
            "channel_a",
            "CHANNEL_A",
        ],
        "empty_strings",
    ),
)

UPDATE_LAST_ID_AND_STATE_EXAMPLES: tuple[
    tuple[
        ChannelName,
        ChannelInfo,
        PostID,
        ChannelInfo,
        str,
    ],
    ...,
] = (
    (
        "channel_base",
        {
            **CHANNEL_BASE_SAMPLE,
        },
        LAST_POST_ID,
        {
            **CHANNEL_BASE_SAMPLE,
            "last_id": LAST_POST_ID,
            "state": CHANNEL_STATE_AVAILABLE,
        },
        "basic_update_last_id",
    ),
    (
        "channel_base_default_last_id_decrease_state",
        {
            **CHANNEL_DEFAULT_LAST_ID,
        },
        DEFAULT_LAST_ID,
        {
            **CHANNEL_DEFAULT_LAST_ID,
            "last_id": DEFAULT_LAST_ID,
            "state": min(
                CHANNEL_STATE_UNAVAILABLE - 1,
                CHANNEL_STATE_UNAVAILABLE,
            ),
        },
        "default_last_id_decrease_state",
    ),
    (
        "channel_base_empty_channel_info",
        {},  # type: ignore[typeddict-item]
        LAST_POST_ID,
        {  # type: ignore[typeddict-item]
            "last_id": LAST_POST_ID,
            "state": CHANNEL_STATE_AVAILABLE,
        },
        "empty_channel_info",
    ),
    (
        "channel_base_last_id_equal_last_post_id",
        {
            **CHANNEL_BASE_SAMPLE,
        },
        NUM3,
        {
            **CHANNEL_BASE_SAMPLE,
            "last_id": NUM3,
            "state": CHANNEL_STATE_AVAILABLE,
        },
        "last_id_equal_last_post_id",
    ),
    (
        "channel_base_missing_last_id",
        {
            **CHANNEL_MISSING_LAST_ID,
        },
        LAST_POST_ID,
        {
            **CHANNEL_MISSING_LAST_ID,
            "last_id": LAST_POST_ID,
            "state": CHANNEL_STATE_AVAILABLE,
        },
        "missing_last_id",
    ),
    (
        "channel_base_missing_state",
        {
            **CHANNEL_MISSING_STATE,
        },
        LAST_POST_ID,
        {
            **CHANNEL_MISSING_STATE,
            "last_id": LAST_POST_ID,
            "state": CHANNEL_STATE_AVAILABLE,
        },
        "missing_state",
    ),
    (
        "channel_base_negative_last_post_id",
        {
            **CHANNEL_BASE_SAMPLE,
        },
        DEFAULT_LAST_ID,
        {
            **CHANNEL_BASE_SAMPLE,
            "last_id": DEFAULT_LAST_ID,
            "state": DEFAULT_STATE,
        },
        "negative_last_post_id",
    ),
)

UPDATE_WITH_NEW_CHANNELS_EXAMPLES: tuple[
    tuple[
        ChannelsDict,
        ChannelNames,
        ChannelNames,
        str,
    ],
    ...,
] = (
    (
        CHANNELS_FROM_NAMES_SAMPLE,
        [
            "channel_add_a",
            "channel_add_c",
            "channel_add_b",
            "CHANNEL_ADD_A",
        ],
        [
            *CHANNEL_NAMES_SAMPLE,
            "channel_add_a",
            "CHANNEL_ADD_A",
            "channel_add_b",
            "channel_add_c",
        ],
        "add_new_channels",
    ),
    (
        CHANNELS_SAMPLE,
        [],
        list(CHANNELS_SAMPLE),
        "no_new_channels",
    ),
    (
        {},
        [
            "Channel_new_b",
            "CHANNEL_NEW_A",
            "channel_new_B",
            "channel_new_a",
        ],
        [
            "CHANNEL_NEW_A",
            "channel_new_a",
            "Channel_new_b",
            "channel_new_B",
        ],
        "only_new_channels",
    ),
)
