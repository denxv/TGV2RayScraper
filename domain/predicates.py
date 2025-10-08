from typing import Any, Callable

from asteval import Interpreter

from core.utils import re_fullmatch, re_search


def make_predicate(condition: str) -> Callable[[dict[str, Any]], bool]:
    aeval = Interpreter()
    symtable = {
        "int": int,
        "len": len,
        "re_fullmatch": re_fullmatch,
        "re_search": re_search,
        "str": str,
    }

    def predicate(config: dict[str, Any]) -> bool:
        aeval.symtable.clear()
        aeval.symtable.update(symtable)
        aeval.symtable.update(config)
        try:
            return bool(aeval(condition))
        except Exception:
            return False

    return predicate


def should_delete_channel(channel_info: dict) -> bool:
    count = channel_info.get("count", 0)
    current_id = channel_info.get("current_id", 1)
    last_id = channel_info.get("last_id", -1)

    if count <= -3:
        return True

    if count != 1 and count <= 0 and \
        last_id != -1 and current_id >= last_id:
        return True

    return False


def should_update_channel(channel_info: dict) -> bool:
    current_id = channel_info.get("current_id", 1)
    last_id = channel_info.get("last_id", -1)

    if last_id != -1 and current_id < last_id:
        return True
    
    return False
