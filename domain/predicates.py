from asteval import (
    Interpreter,
)

from core.constants.common import (
    CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
    CHANNEL_REMOVE_THRESHOLD,
    CHANNEL_STATE_AVAILABLE,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    DEFAULT_STATE,
)
from core.typing import (
    ChannelInfo,
    ConditionStr,
    Record,
    RecordPredicate,
)
from core.utils import (
    re_fullmatch,
    re_search,
)

__all__ = [
    "has_multiple_channel_actions",
    "is_channel_available",
    "is_channel_fully_scanned",
    "is_channel_pending_update",
    "is_new_channel",
    "make_predicate",
    "should_apply_changes",
    "should_delete_channel",
]


def has_multiple_channel_actions(
    *,
    has_overrides: bool,
    reset_to_defaults: bool,
    should_delete: bool,
) -> bool:
    actions: tuple[bool, ...] = (
        should_delete,
        has_overrides or reset_to_defaults,
    )

    return sum(actions) > 1


def is_channel_available(
    channel_info: ChannelInfo,
) -> bool:
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )
    state = channel_info.get(
        "state",
        DEFAULT_STATE,
    )

    return (
        last_id != DEFAULT_LAST_ID
        and state == CHANNEL_STATE_AVAILABLE
    )


def is_channel_fully_scanned(
    channel_info: ChannelInfo,
) -> bool:
    current_id = channel_info.get(
        "current_id",
        DEFAULT_CURRENT_ID,
    )
    last_id = channel_info.get(
        "last_id",
        DEFAULT_LAST_ID,
    )

    return (
        is_channel_available(
            channel_info=channel_info,
        )
        and current_id >= last_id
    )


def is_channel_pending_update(
    channel_info: ChannelInfo,
) -> bool:
    return (
        is_channel_available(
            channel_info=channel_info,
        )
        and not is_channel_fully_scanned(
            channel_info=channel_info,
        )
    )


def is_new_channel(
    channel_info: ChannelInfo,
) -> bool:
    return all(
        channel_info.get(key, default) == default
        for key, default in DEFAULT_CHANNEL_VALUES.items()
    )


def make_predicate(
    *,
    condition: ConditionStr | None,
) -> RecordPredicate | None:
    if condition is None:
        return None

    aeval = Interpreter()

    symtable = {
        "int": int,
        "len": len,
        "re_fullmatch": re_fullmatch,
        "re_search": re_search,
        "str": str,
    }

    def predicate(
        record: Record,
    ) -> bool:
        aeval.symtable.clear()
        aeval.symtable.update(symtable)
        aeval.symtable.update(record)

        try:
            result = aeval(
                expr=condition,
            )
        except Exception:  # pragma: no cover
            return False
        else:
            return bool(result)

    return predicate


def should_apply_changes(
    channel_info: ChannelInfo,
) -> bool:
    return (
        not is_new_channel(
            channel_info=channel_info,
        )
        and is_channel_available(
            channel_info=channel_info,
        )
    )


def should_delete_channel(
    channel_info: ChannelInfo,
) -> bool:
    count = channel_info.get(
        "count",
        DEFAULT_COUNT,
    )
    state = channel_info.get(
        "state",
        DEFAULT_STATE,
    )

    if state <= CHANNEL_FAILED_ATTEMPTS_THRESHOLD:
        return True

    if is_new_channel(
        channel_info=channel_info,
    ):
        return False

    return (
        count <= CHANNEL_REMOVE_THRESHOLD
        and is_channel_fully_scanned(
            channel_info=channel_info,
        )
    )
