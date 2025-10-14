from asteval import Interpreter

from core.constants import (
    CHANNEL_ACTIVE_THRESHOLD,
    CHANNEL_FAILED_ATTEMPTS_THRESHOLD,
    CHANNEL_REMOVE_THRESHOLD,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
)
from core.typing import (
    ChannelInfo,
    ConditionStr,
    ConfigPredicate,
    V2RayConfig,
)
from core.utils import re_fullmatch, re_search


def is_new_channel(channel_info: ChannelInfo) -> bool:
    return all(
        channel_info.get(key, default) == default
        for key, default in DEFAULT_CHANNEL_VALUES.items()
    )


def make_predicate(condition: ConditionStr) -> ConfigPredicate:
    aeval = Interpreter()
    symtable = {
        "int": int,
        "len": len,
        "re_fullmatch": re_fullmatch,
        "re_search": re_search,
        "str": str,
    }

    def predicate(config: V2RayConfig) -> bool:
        aeval.symtable.clear()
        aeval.symtable.update(symtable)
        aeval.symtable.update(config)
        try:
            return bool(aeval(condition))
        except Exception:
            return False

    return predicate


def should_delete_channel(channel_info: ChannelInfo) -> bool:
    count = channel_info.get("count", DEFAULT_COUNT)
    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    if count <= CHANNEL_FAILED_ATTEMPTS_THRESHOLD:
        return True

    if count == CHANNEL_ACTIVE_THRESHOLD:
        return False

    if count <= CHANNEL_REMOVE_THRESHOLD and \
        last_id != DEFAULT_LAST_ID and current_id >= last_id:
        return True

    return False


def should_set_current_id(channel_info: ChannelInfo, apply_to_new: bool = False) -> bool:
    if not apply_to_new and is_new_channel(channel_info):
        return False

    return True


def should_update_channel(channel_info: ChannelInfo) -> bool:
    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    if last_id != DEFAULT_LAST_ID and current_id < last_id:
        return True
    
    return False
