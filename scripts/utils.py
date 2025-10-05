from argparse import ArgumentTypeError, Namespace
from base64 import b64decode, b64encode, urlsafe_b64decode
from datetime import datetime
from functools import wraps
from pathlib import Path
from re import fullmatch, search, split
from typing import Callable

from .logger import logger
from .common import abs_path
from .const import (
    LEN_NAME,
    LEN_NUMBER,
    P,
    T,
    TOTAL_CHANNELS_POST,
)


def b64decode_safe(string: str) -> str:
    if not isinstance(string, str) or not (string := string.strip()):
        return ""
    string = f"{string}{'=' * (-len(string) % 4)}"
    for b64_decode in (urlsafe_b64decode, b64decode):
        try:
            return b64_decode(string).decode('utf-8', errors='replace')
        except Exception:
            continue
    return ""


def b64encode_safe(string: str) -> str:
    return b64encode(string.encode('utf-8')).decode('ascii')


def collect_args(args: Namespace, flags: list[str]) -> list[str]:
    params = []
    for flag in flags:
        value = getattr(args, flag_to_name(flag), None)
        if value is not None:
            params.extend([flag] if not value else [flag, value])
    return params


def condition_delete_channels(channel_info: dict) -> bool:
    return channel_info.get("count", 0) <= -3 or channel_info.get("count", 0) <= 0 and \
        channel_info.get("current_id", 1) >= channel_info.get("last_id", -1) != -1


def current_less_last(channel_info: dict) -> bool:
    return channel_info.get("current_id", 1) < channel_info.get("last_id", -1)


def diff_channel_id(channel_info: dict) -> int:
    return channel_info.get("last_id", 0) - channel_info.get("current_id", 0)


def flag_to_name(flag: str) -> str:
    return flag.lstrip('-').replace('-', '_')


def format_channel_id(channel_info: dict) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff
    return (
        f"{channel_info.get('current_id', ''):>{LEN_NUMBER}} "
        f"/ {channel_info.get('last_id', ''):<{LEN_NUMBER}} "
        f"(+{diff})"
    )


def get_filtered_keys(channels: dict) -> list:
    return list(filter(lambda name: current_less_last(channels.get(name, {})), channels.keys()))


def get_sorted_keys(channels: dict, filtering: bool = False, reverse: bool = False) -> list:
    channel_names = get_filtered_keys(channels) if filtering else channels.keys()
    return sorted(channel_names, key=lambda name: diff_channel_id(channels[name]), reverse=reverse)


def int_in_range(value: str, min_value: int = 1, max_value: int = 100, as_str: bool = False) -> int | str:
    ivalue = int(value)
    if ivalue < min_value or ivalue > max_value:
        raise ArgumentTypeError(f"Expected {min_value} to {max_value}, got {ivalue}")
    return str(ivalue) if as_str else ivalue


def make_backup(files: list[str | Path]) -> None:
    for file in files:
        src = Path(file).resolve()
        if not src.exists():
            continue
        backup_name = f"{src.stem}-backup-{datetime.now():%Y%m%d-%H%M%s}{src.suffix}"
        src.rename(src.parent / backup_name)
        logger.info(f"File '{src.name}' backed up as '{backup_name}'.")


def normalize_valid_params(params: str) -> str:
    return ",".join(parse_valid_params(params)) if params.strip() else ""


def parse_valid_params(params: str) -> list[str]:
    if not isinstance(params, str):
        raise ArgumentTypeError(f"Expected string, got {type(params).__name__!r}")

    seen = set()

    def check_param(param: str) -> str:
        if not fullmatch(r"\w+(?:\.\w+)*", param):
            raise ArgumentTypeError(f"Invalid parameter: {param!r}")
        if param in seen:
            raise ArgumentTypeError(f"Duplicate parameter: {param!r}")
        seen.add(param)
        return param

    valid_params = [
        check_param(param) 
        for param in split(r"[ ,]+", params.strip())
    ]

    if not valid_params:
        raise ArgumentTypeError("No parameters provided")

    return valid_params


def print_channel_info(channels: dict) -> None:
    logger.info(f"Showing information about the remaining channels...")
    channel_names = get_sorted_keys(channels, filtering=True)
    for name in channel_names:
        logger.info(f" <SS>  {name:<{LEN_NAME}}{format_channel_id(channels[name])}")
    else:
        logger.info(f"Total channels are available for extracting configs: {len(channels)}")
        logger.info(f"Channels left to check: {len(channel_names)}")
        logger.info(f"Total messages on channels: {TOTAL_CHANNELS_POST:,}")


def re_fullmatch(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(fullmatch(pattern, string))


def re_search(pattern: str, string: str) -> bool:
    if not isinstance(string, str):
        string = str(string)
    return bool(search(pattern, string))


def sort_channel_names(channel_names: list) -> list:
    return sorted([name.lower() for name in channel_names])


def status(start: str, end: str = "", tracking: bool = False) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(target_func: Callable[P, T]) -> Callable[P, T]:
        @wraps(target_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            logger.info(start)
            old_size = len(args[0]) if tracking and args and isinstance(args[0], dict) else None
            result = target_func(*args, **kwargs)
            if tracking and old_size is not None:
                new_size = len(args[0])
                diff = new_size - old_size
                logger.info(f"Old count: {old_size} | New count: {new_size} | ({diff:+})")
            if end:
                logger.info(end)
            return result
        return wrapper
    return decorator


def validate_file_path(path: str | Path, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")
    
    return str(filepath)
