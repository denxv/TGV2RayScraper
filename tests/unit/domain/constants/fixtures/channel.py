from core.typing import (
    Callable,
    ChannelName,
    ChannelNames,
)
from tests.unit.domain.constants.common import (
    CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
    CHANNEL_REMOVE_THRESHOLD,
    CHANNEL_STATE_AVAILABLE,
    CHANNEL_STATE_UNAVAILABLE,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    DEFAULT_STATE,
    NUM1,
    NUM2,
    NUM3,
)

__all__ = [
    "CHANNELS_FROM_NAMES_SAMPLE",
    "CHANNELS_SAMPLE",
    "CHANNEL_ANY_ID_RELATION",
    "CHANNEL_AVAILABLE",
    "CHANNEL_BASE",
    "CHANNEL_BASE_SAMPLE",
    "CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST",
    "CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST",
    "CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST",
    "CHANNEL_CURRENT_ID",
    "CHANNEL_CURRENT_ID_BY_NAME",
    "CHANNEL_CURRENT_ID_BY_NAMES",
    "CHANNEL_CURRENT_ID_EQUAL_LAST_ID",
    "CHANNEL_CURRENT_ID_GREATER_THAN_LAST_ID",
    "CHANNEL_CURRENT_ID_LESS_THAN_LAST_ID",
    "CHANNEL_DATA_BY_NAME",
    "CHANNEL_DEFAULT_COUNT",
    "CHANNEL_DEFAULT_CURRENT_ID",
    "CHANNEL_DEFAULT_LAST_ID",
    "CHANNEL_DEFAULT_STATE",
    "CHANNEL_INFO_BY_NAME",
    "CHANNEL_INFO_BY_NAMES",
    "CHANNEL_MISSING_COUNT",
    "CHANNEL_MISSING_CURRENT_ID",
    "CHANNEL_MISSING_LAST_ID",
    "CHANNEL_MISSING_STATE",
    "CHANNEL_NAMES_SAMPLE",
    "CHANNEL_NEGATIVE_CURRENT_ID",
    "CHANNEL_NEW",
    "CHANNEL_REMOVED",
    "CHANNEL_REMOVED_ABOVE_THRESHOLD",
    "CHANNEL_REMOVED_BELOW_THRESHOLD",
    "CHANNEL_SCANNED_ABOVE_REMOVE_THRESHOLD",
    "CHANNEL_SCANNED_BELOW_REMOVE_THRESHOLD",
    "CHANNEL_SCANNED_COMPLETE",
    "CHANNEL_SCANNED_FOUND_CONFIGS",
    "CHANNEL_SCANNED_NO_FOUND_CONFIGS",
    "CHANNEL_SCANNED_REMOVE_THRESHOLD",
    "CHANNEL_UNAVAILABLE",
    "CHANNEL_ZERO_CURRENT_ID",
]

CHANNEL_BASE = {
    **DEFAULT_CHANNEL_VALUES,
}
CHANNEL_BASE_SAMPLE = {
    **CHANNEL_BASE,
    "count": NUM1,
    "current_id": NUM2,
    "last_id": NUM3,
    "state": CHANNEL_STATE_AVAILABLE,
}

CHANNEL_CURRENT_ID_EQUAL_LAST_ID = {
    "current_id": NUM3,
    "last_id": NUM3,
}
CHANNEL_CURRENT_ID_GREATER_THAN_LAST_ID = {
    "current_id": NUM3,
    "last_id": NUM2,
}
CHANNEL_CURRENT_ID_LESS_THAN_LAST_ID = {
    "current_id": NUM2,
    "last_id": NUM3,
}

CHANNEL_NEGATIVE_CURRENT_ID = {
    **CHANNEL_BASE_SAMPLE,
    "current_id": -NUM2,
}
CHANNEL_ZERO_CURRENT_ID = {
    **CHANNEL_BASE_SAMPLE,
    "current_id": NUM2 - NUM2,
}

CHANNEL_ANY_ID_RELATION = {
    **CHANNEL_CURRENT_ID_EQUAL_LAST_ID,
    **CHANNEL_CURRENT_ID_GREATER_THAN_LAST_ID,
    **CHANNEL_CURRENT_ID_LESS_THAN_LAST_ID,
}

CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST = {
    **CHANNEL_BASE_SAMPLE,
    **CHANNEL_CURRENT_ID_EQUAL_LAST_ID,
}
CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST = {
    **CHANNEL_BASE_SAMPLE,
    **CHANNEL_CURRENT_ID_GREATER_THAN_LAST_ID,
}
CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST = {
    **CHANNEL_BASE_SAMPLE,
    **CHANNEL_CURRENT_ID_LESS_THAN_LAST_ID,
}

CHANNEL_DEFAULT_COUNT = {
    **CHANNEL_BASE,
    "count": DEFAULT_COUNT,
    "current_id": NUM2,
    "last_id": DEFAULT_LAST_ID,
    "state": CHANNEL_STATE_UNAVAILABLE,
}
CHANNEL_DEFAULT_CURRENT_ID = {
    **CHANNEL_BASE,
    "count": NUM1,
    "current_id": DEFAULT_CURRENT_ID,
    "last_id": NUM3,
    "state": CHANNEL_STATE_AVAILABLE,
}
CHANNEL_DEFAULT_LAST_ID = {
    **CHANNEL_BASE,
    "count": NUM1,
    "current_id": NUM2,
    "last_id": DEFAULT_LAST_ID,
    "state": CHANNEL_STATE_UNAVAILABLE,
}
CHANNEL_DEFAULT_STATE = {
    **CHANNEL_BASE,
    "count": NUM1,
    "current_id": NUM2,
    "last_id": DEFAULT_LAST_ID,
    "state": DEFAULT_STATE,
}

CHANNEL_MISSING_COUNT = {
    key: value
    for key, value in CHANNEL_DEFAULT_COUNT.items()
    if key != "count"
}
CHANNEL_MISSING_CURRENT_ID = {
    key: value
    for key, value in CHANNEL_DEFAULT_CURRENT_ID.items()
    if key != "current_id"
}
CHANNEL_MISSING_LAST_ID = {
    key: value
    for key, value in CHANNEL_DEFAULT_LAST_ID.items()
    if key != "last_id"
}
CHANNEL_MISSING_STATE = {
    key: value
    for key, value in CHANNEL_DEFAULT_STATE.items()
    if key != "state"
}

CHANNEL_AVAILABLE = {
    **CHANNEL_BASE,
    **CHANNEL_ANY_ID_RELATION,
    "state": CHANNEL_STATE_AVAILABLE,
}
CHANNEL_NEW = {
    **CHANNEL_BASE,
}
CHANNEL_UNAVAILABLE = {
    **CHANNEL_DEFAULT_LAST_ID,
    "state": CHANNEL_STATE_UNAVAILABLE,
}

CHANNEL_REMOVED = {
    **CHANNEL_UNAVAILABLE,
    "state": CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
}
CHANNEL_REMOVED_ABOVE_THRESHOLD = {
    **CHANNEL_UNAVAILABLE,
    "state": min(
        CHANNEL_FAILED_ATTEMPTS_THRESHOLD + NUM1,
        CHANNEL_STATE_AVAILABLE,
    ),
}
CHANNEL_REMOVED_BELOW_THRESHOLD = {
    **CHANNEL_UNAVAILABLE,
    "state": CHANNEL_FAILED_ATTEMPTS_THRESHOLD - NUM1,
}
CHANNEL_SCANNED_COMPLETE = {
    **CHANNEL_AVAILABLE,
    **CHANNEL_CURRENT_ID_EQUAL_LAST_ID,
}
CHANNEL_SCANNED_ABOVE_REMOVE_THRESHOLD = {
    **CHANNEL_SCANNED_COMPLETE,
    "count": CHANNEL_REMOVE_THRESHOLD + NUM1,
}
CHANNEL_SCANNED_BELOW_REMOVE_THRESHOLD = {
    **CHANNEL_SCANNED_COMPLETE,
    "count": max(
        CHANNEL_REMOVE_THRESHOLD - NUM1,
        DEFAULT_COUNT,
    ),
}
CHANNEL_SCANNED_FOUND_CONFIGS = {
    **CHANNEL_SCANNED_COMPLETE,
    "count": NUM1,
}
CHANNEL_SCANNED_NO_FOUND_CONFIGS = {
    **CHANNEL_SCANNED_COMPLETE,
    "count": DEFAULT_COUNT,
}
CHANNEL_SCANNED_REMOVE_THRESHOLD = {
    **CHANNEL_SCANNED_COMPLETE,
    "count": CHANNEL_REMOVE_THRESHOLD,
}

CHANNEL_NAMES_SAMPLE = [
    f"channel_{i}"
    for i in range(1, 1000, 3)
]
CHANNELS_FROM_NAMES_SAMPLE = {
    channel_name: {
        **CHANNEL_BASE_SAMPLE,
    }
    for channel_name in CHANNEL_NAMES_SAMPLE
}

CHANNELS_SAMPLE = {
    "channel_available": {
        **CHANNEL_AVAILABLE,
    },
    "channel_base_current_equal_last": {
        **CHANNEL_BASE_SAMPLE_CURRENT_EQUAL_LAST,
    },
    "channel_base_current_gt_last": {
        **CHANNEL_BASE_SAMPLE_CURRENT_GT_LAST,
    },
    "channel_base_current_lt_last": {
        **CHANNEL_BASE_SAMPLE_CURRENT_LT_LAST,
    },
    "channel_default_count_and_current_gt_last": {
        **CHANNEL_DEFAULT_COUNT,
        **CHANNEL_CURRENT_ID_GREATER_THAN_LAST_ID,
        "state": CHANNEL_STATE_AVAILABLE,
    },
    "channel_negative_current_id": {
        **CHANNEL_NEGATIVE_CURRENT_ID,
    },
    "channel_new": {
        **CHANNEL_NEW,
    },
    "channel_removed": {
        **CHANNEL_REMOVED,
    },
    "channel_removed_above_threshold": {
        **CHANNEL_REMOVED_ABOVE_THRESHOLD,
    },
    "channel_removed_below_threshold": {
        **CHANNEL_REMOVED_BELOW_THRESHOLD,
    },
    "channel_scanned_above_remove_threshold": {
        **CHANNEL_SCANNED_ABOVE_REMOVE_THRESHOLD,
    },
    "channel_scanned_below_remove_threshold": {
        **CHANNEL_SCANNED_BELOW_REMOVE_THRESHOLD,
    },
    "channel_scanned_complete": {
        **CHANNEL_SCANNED_COMPLETE,
    },
    "channel_scanned_found_configs": {
        **CHANNEL_SCANNED_FOUND_CONFIGS,
    },
    "channel_scanned_no_found_configs": {
        **CHANNEL_SCANNED_NO_FOUND_CONFIGS,
    },
    "channel_scanned_remove_threshold": {
        **CHANNEL_SCANNED_REMOVE_THRESHOLD,
    },
    "channel_unavailable": {
        **CHANNEL_UNAVAILABLE,
    },
    "channel_zero_current_id": {
        **CHANNEL_ZERO_CURRENT_ID,
    },
}

CHANNEL_DATA_BY_NAME: Callable[
    [ChannelName],
    dict[str, int],
] = lambda name: dict(
    CHANNELS_SAMPLE.get(
        name,
        CHANNEL_BASE.copy(),
    ),
)
CHANNEL_CURRENT_ID: Callable[
    [ChannelName],
    int | None,
] = lambda name: (
    CHANNEL_DATA_BY_NAME(name).get("current_id")
)
CHANNEL_CURRENT_ID_BY_NAME: Callable[
    [ChannelName],
    dict[ChannelName, int | None],
] = lambda name: {
    name: CHANNEL_CURRENT_ID(name),
}
CHANNEL_CURRENT_ID_BY_NAMES: Callable[
    [ChannelNames],
    dict[ChannelName, int | None],
] = lambda names: {
    name: CHANNEL_CURRENT_ID(name)
    for name in names
}
CHANNEL_INFO_BY_NAME: Callable[
    [ChannelName],
    dict[ChannelName, dict[str, int]],
] = lambda name: {
    name: CHANNEL_DATA_BY_NAME(name),
}
CHANNEL_INFO_BY_NAMES: Callable[
    [ChannelNames],
    dict[ChannelName, dict[str, int]],
] = lambda names: {
    name: CHANNEL_DATA_BY_NAME(name)
    for name in names
}
