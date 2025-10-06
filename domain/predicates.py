from typing import Any, Callable

from asteval import Interpreter

from core.utils import re_fullmatch, re_search


def condition_delete_channels(channel_info: dict) -> bool:
    return channel_info.get("count", 0) <= -3 or channel_info.get("count", 0) <= 0 and \
        channel_info.get("current_id", 1) >= channel_info.get("last_id", -1) != -1


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
