#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, Tuple, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
REGEX_CHANNELS_NAME = re.compile(r"http[s]?://t.me/[s/]{0,2}([\w]+)")


def condition_channel_to_default(channel_info: dict) -> bool:
    return channel_info["count"] == 0 and \
        channel_info["current_id"] == 1 and \
        channel_info["last_id"] == -1


def condition_delete_channels(channel_info: dict) -> bool:
    return False if condition_channel_to_default(channel_info) else \
        channel_info["count"] <= -3 or channel_info["count"] == 0 and \
        channel_info["last_id"] <= channel_info["current_id"]


def condition_reset_channels(channel_info: dict) -> bool:
    return channel_info["last_id"] == -1


def create_file(file_path: str, data: str = "") -> str:
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
    return file_path


def status(tag: str, start: str, end: str = "", tracking: bool = False) -> \
    Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(target_func: Callable[P, T]) -> Callable[P, T]:
        @wraps(target_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            print(f"[{tag.upper()}] {start}")
            old_size = len(args[0]) if tracking and args and isinstance(args[0], dict) else None
            result = target_func(*args, **kwargs)
            if tracking and old_size is not None:
                new_size = len(args[0])
                diff = new_size - old_size
                print(f"[{tag.upper()}] Old: {old_size} | New: {new_size} | ({diff:+})")
            print(f"[{tag.upper()}] {end}\n\n" if end else "", end="")
            return result
        return wrapper
    return decorator


@status(tag="delt", start="Deleting channels...", \
    end="Deleted channels!", tracking=True)
def delete_channels(channels: dict) -> None:
    for channel_name, channel_info in list(channels.items()):
        if condition_delete_channels(channel_info):
            channels.pop(channel_name)


@status(tag="load", start="Loading channels...", end="Loaded channels!")
def load_channels(path_channels: str = "tg-channels-current.json", 
    path_urls: str = "tg-channels-urls.txt") -> Tuple[dict, list]:
    with open(create_file(path_channels, "{}"), "r", encoding="utf-8") as channels, \
        open(create_file(path_urls), "r", encoding="utf-8") as tg_urls:
        return json.load(channels), REGEX_CHANNELS_NAME.findall(tg_urls.read())


@status(tag="rest", start="Reseting channels...", end="Reseted channels!")
def reset_channels_to_default(current_channels: dict) -> None:
    for name in current_channels:
        if condition_reset_channels(current_channels[name]):
            current_channels[name] = dict(current_id=1, last_id=-1, count=0)


@status(tag="save", start="Saving channels...")
def save_channels(channels: dict, path_channels: str = "tg-channels-current.json") -> None:
    if os.path.exists(path_channels):
        dir_name, base_name = os.path.split(path_channels)
        file_name, file_ext = os.path.splitext(base_name)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{file_name}-backup-{timestamp}{file_ext}"
        backup_path = os.path.join(dir_name, backup_name)
        os.rename(path_channels, backup_path)
        print(f"[SAVE] File '{base_name}' was renamed to '{backup_name}' for backup!")

    with open(path_channels, "w", encoding="utf-8") as tg_json:
        json.dump(channels, tg_json, indent=4, sort_keys=True)
        print(f"[SAVE] Saved {len(channels)} channels in '{path_channels}'!")


def sorted_channels_name(channel_names: list) -> list:
    return sorted([name.lower() for name in channel_names])


@status(tag="updt", start="Updating channels...", \
    end="Updated channels!", tracking=True)
def update_channels(current_channels: dict, channel_names: list) -> None:
    for name in sorted_channels_name(channel_names):
        if name not in current_channels:
            current_channels.setdefault(name, dict(current_id=1, last_id=-1, count=0))


def main(path_channels: str = "tg-channels-current.json", \
    path_urls: str = "tg-channels-urls.txt") -> None:
    try:
        current_channels, list_channel_names = \
            load_channels(path_channels=path_channels, path_urls=path_urls)
        update_channels(current_channels, list_channel_names)
        delete_channels(current_channels)
        save_channels(current_channels, path_channels=path_channels)
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == "__main__":
    current_json = os.path.join(os.path.dirname(__file__), "../channels/current.json")
    urls_txt = os.path.join(os.path.dirname(__file__), "../channels/urls.txt")
    main(path_channels=current_json, path_urls=urls_txt)
