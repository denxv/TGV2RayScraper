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
    ConfigPredicate,
    V2RayConfig,
)
from core.utils import (
    re_fullmatch,
    re_search,
)

__all__ = [
    "is_channel_available",
    "is_channel_fully_scanned",
    "is_new_channel",
    "make_predicate",
    "should_delete_channel",
    "should_set_current_id",
    "should_update_channel",
]


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


def is_new_channel(
    channel_info: ChannelInfo,
) -> bool:
    return all(
        channel_info.get(key, default) == default
        for key, default in DEFAULT_CHANNEL_VALUES.items()
    )


def make_predicate(
    condition: ConditionStr,
) -> ConfigPredicate:
    aeval = Interpreter()

    symtable = {
        "int": int,
        "len": len,
        "re_fullmatch": re_fullmatch,
        "re_search": re_search,
        "str": str,
    }

    def predicate(
        config: V2RayConfig,
    ) -> bool:
        aeval.symtable.clear()
        aeval.symtable.update(symtable)
        aeval.symtable.update(config)

        try:
            result = aeval(
                expr=condition,
            )
        except Exception:  # pragma: no cover
            return False
        else:
            return bool(result)

    return predicate


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


def should_set_current_id(
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


def should_update_channel(
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
