from tests.unit.domain.constants.common import (
    CHANNEL_REMOVE_THRESHOLD,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
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
    CHANNEL_MISSING_COUNT,
    CHANNEL_MISSING_CURRENT_ID,
    CHANNEL_MISSING_LAST_ID,
    CHANNEL_MISSING_STATE,
    CHANNEL_NEW,
    CHANNEL_REMOVED,
    CHANNEL_REMOVED_ABOVE_THRESHOLD,
    CHANNEL_REMOVED_BELOW_THRESHOLD,
    CHANNEL_SCANNED_ABOVE_REMOVE_THRESHOLD,
    CHANNEL_SCANNED_BELOW_REMOVE_THRESHOLD,
    CHANNEL_SCANNED_REMOVE_THRESHOLD,
    CHANNEL_UNAVAILABLE,
)

__all__ = [
    "IS_CHANNEL_AVAILABLE_EXAMPLES",
    "IS_CHANNEL_FULLY_SCANNED_EXAMPLES",
    "IS_NEW_CHANNEL_EXAMPLES",
    "MAKE_PREDICATE_EXAMPLES",
    "SHOULD_DELETE_CHANNEL_EXAMPLES",
    "SHOULD_SET_CURRENT_ID_EXAMPLES",
]

IS_CHANNEL_AVAILABLE_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_AVAILABLE,
        True,
        "available_channel",
    ),
    (
        {},
        False,
        "empty_channel",
    ),
    (
        CHANNEL_UNAVAILABLE,
        False,
        "unavailable_channel",
    ),
)

IS_CHANNEL_FULLY_SCANNED_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
        True,
        "current_equals_last",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
        True,
        "current_greater_than_last",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
        False,
        "current_less_than_last",
    ),
    (
        {},
        False,
        "empty_channel",
    ),
    (
        CHANNEL_MISSING_CURRENT_ID,
        False,
        "missing_current_id",
    ),
    (
        CHANNEL_MISSING_LAST_ID,
        False,
        "missing_last_id",
    ),
)

IS_NEW_CHANNEL_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_BASE_SAMPLE,
        False,
        "all_changed",
    ),
    (
        CHANNEL_BASE,
        True,
        "all_defaults",
    ),
    (
        {
            **CHANNEL_BASE,
            "count": DEFAULT_COUNT + NUM1,
        },
        False,
        "count_changed",
    ),
    (
        {
            **CHANNEL_BASE,
            "current_id": DEFAULT_CURRENT_ID + NUM2,
        },
        False,
        "current_id_changed",
    ),
    (
        {
            **CHANNEL_BASE,
            "last_id": DEFAULT_LAST_ID + NUM3,
        },
        False,
        "last_id_changed",
    ),
)

MAKE_PREDICATE_EXAMPLES: tuple[
    tuple[
        str | None,
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        "nonexistent_var > 0",
        {},
        False,
        "except_missing_var",
    ),
    (
        "invalid_syntax ==",
        {},
        False,
        "except_syntax_error",
    ),
    (
        "1 / 0 > 0",
        {},
        False,
        "except_zero_division",
    ),
    (
        "int(port) > 1000",
        {
            "port": "8080",
        },
        True,
        "int_conversion_true",
    ),
    (
        "int(port) > 10000",
        {
            "port": "8080",
        },
        False,
        "int_conversion_false",
    ),
    (
        "port == 8080",
        {
            "port": 8080,
        },
        True,
        "port_match",
    ),
    (
        "port == 80",
        {
            "port": 8080,
        },
        False,
        "port_no_match",
    ),
    (
        "re_fullmatch('test.*', name)",
        {
            "name": "test123",
        },
        True,
        "regex_match",
    ),
    (
        "re_fullmatch('test.*', name)",
        {
            "name": "abc",
        },
        False,
        "regex_no_match",
    ),
    (
        "len(tags) > 2",
        {
            "tags": [
                "a",
                "b",
                "c",
            ],
        },
        True,
        "tags_gt_2",
    ),
    (
        "len(tags) > 3",
        {
            "tags": [
                "a",
                "b",
                "c",
            ],
        },
        False,
        "tags_gt_3",
    ),
    (
        None,
        {},
        True,
        "type_none",
    ),
)

SHOULD_DELETE_CHANNEL_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_AVAILABLE,
        False,
        "channel_available",
    ),
    (
        CHANNEL_NEW,
        False,
        "channel_new",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
            "count": CHANNEL_REMOVE_THRESHOLD,
        },
        False,
        "current_less_than_last",
    ),
    (
        {},
        False,
        "empty_channel",
    ),
    (
        CHANNEL_REMOVED_ABOVE_THRESHOLD,
        False,
        "failed_above_threshold",
    ),
    (
        CHANNEL_REMOVED_BELOW_THRESHOLD,
        True,
        "failed_below_threshold",
    ),
    (
        CHANNEL_REMOVED,
        True,
        "failed_threshold_last_default",
    ),
    (
        {
            **CHANNEL_REMOVED,
            "last_id": NUM3,
        },
        True,
        "failed_threshold_last_no_default",
    ),
    (
        CHANNEL_MISSING_COUNT,
        False,
        "missing_count",
    ),
    (
        CHANNEL_MISSING_CURRENT_ID,
        False,
        "missing_current_id",
    ),
    (
        CHANNEL_MISSING_LAST_ID,
        False,
        "missing_last_id",
    ),
    (
        CHANNEL_MISSING_STATE,
        False,
        "missing_state",
    ),
    (
        CHANNEL_SCANNED_ABOVE_REMOVE_THRESHOLD,
        False,
        "remove_threshold_above",
    ),
    (
        CHANNEL_SCANNED_BELOW_REMOVE_THRESHOLD,
        True,
        "remove_threshold_below",
    ),
    (
        {
            **CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
            "count": CHANNEL_REMOVE_THRESHOLD,
        },
        True,
        "remove_threshold_current_gt_last",
    ),
    (
        {
            **CHANNEL_SCANNED_REMOVE_THRESHOLD,
            "last_id": DEFAULT_LAST_ID,
        },
        False,
        "remove_threshold_last_default",
    ),
    (
        CHANNEL_SCANNED_REMOVE_THRESHOLD,
        True,
        "remove_threshold_equal_ids",
    ),
)

SHOULD_SET_CURRENT_ID_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_AVAILABLE,
        True,
        "available_existing_channel",
    ),
    (
        CHANNEL_NEW,
        False,
        "new_channel",
    ),
    (
        CHANNEL_UNAVAILABLE,
        False,
        "unavailable_channel",
    ),
)

SHOULD_UPDATE_CHANNEL_EXAMPLES: tuple[
    tuple[
        dict[str, object],
        bool,
        str,
    ],
    ...,
] = (
    (
        CHANNEL_BASE,
        False,
        "all_defaults",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
        False,
        "current_equals_last",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
        False,
        "current_greater_than_last",
    ),
    (
        CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
        True,
        "current_less_than_last",
    ),
    (
        {},
        False,
        "empty_dict_defaults_used",
    ),
    (
        CHANNEL_UNAVAILABLE,
        False,
        "last_id_is_default",
    ),
    (
        CHANNEL_AVAILABLE,
        True,
        "last_id_is_not_default",
    ),
    (
        CHANNEL_MISSING_CURRENT_ID,
        True,
        "missing_current_id",
    ),
    (
        CHANNEL_MISSING_LAST_ID,
        False,
        "missing_last_id",
    ),
)
