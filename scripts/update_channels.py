#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter, Namespace 
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar, Tuple, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
REGEX_CHANNELS_NAME = re.compile(r"http[s]?://t.me/[s/]{0,2}([\w]+)")


def abs_path(path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def condition_delete_channels(channel_info: dict) -> bool:
    return channel_info["count"] <= -3 or channel_info["count"] <= 0 and \
        channel_info["current_id"] >= channel_info["last_id"] != -1


def condition_reset_channels(channel_info: dict) -> bool:
    return channel_info["last_id"] == -1


def existing_file(path: str) -> str:
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        raise ArgumentTypeError(f"The file does not exist: {abs_path}")
    return abs_path


def make_backup(files: list[str]) -> None:
    for path in files:
        if not os.path.exists(path):
            continue
        base = os.path.basename(path)
        name, ext = os.path.splitext(base)
        backup = f"{name}-backup-{datetime.now():%Y%m%d-%H%M%s}{ext}"
        backup_path = os.path.join(os.path.dirname(path), backup)
        os.rename(path, backup_path)
        print(f"[BACK] File '{base}' was renamed to '{backup}' for backup!")


def parse_args() -> Namespace:
    channels_rel_path = "../channels/current.json"
    urls_rel_path = "../channels/urls.txt"

    parser = ArgumentParser(
        description="Update Telegram channels: merge new URLs and create backups",
        epilog="Example: python %(prog)s --channels channels.json --urls urls.txt",
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=100,
        ),
    )

    parser.add_argument(
        "-C", "--channels",
        default=abs_path(channels_rel_path),
        dest="channels",
        help="Path to the current channels JSON file (default: %(default)s).",
        metavar="FILE",
        type=existing_file,
    )

    parser.add_argument(
        "-U", "--urls",
        default=abs_path(urls_rel_path),
        dest="urls",
        help="Path to the text file containing new channel URLs (default: %(default)s).",
        metavar="FILE",
        type=existing_file,
    )

    return parser.parse_args()


def sort_channel_names(channel_names: list) -> list:
    return sorted([name.lower() for name in channel_names])


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
def load_channels(path_channels: str = "tg-channels-current.json", \
    path_urls: str = "tg-channels-urls.txt") -> Tuple[dict, list]:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            channels = json.load(file)
        except json.JSONDecodeError:
            channels = {}
    with open(path_urls, "r", encoding="utf-8") as file:
        urls = REGEX_CHANNELS_NAME.findall(file.read())
    return channels, urls


@status(tag="rest", start="Reseting channels...", end="Reseted channels!")
def reset_channels_to_default(current_channels: dict) -> None:
    for name in current_channels:
        if condition_reset_channels(current_channels[name]):
            current_channels[name] = dict(current_id=1, last_id=-1, count=0)


@status(tag="save", start="Saving channels...")
def save_channels(channels: dict, path_channels: str = "tg-channels-current.json",
    path_urls: str = "tg-channels-urls.txt") -> None:
    make_backup([path_urls, path_channels])
    with open(path_channels, "w", encoding="utf-8") as tg_json, \
        open(path_urls, "w", encoding="utf-8") as urls:
        json.dump(channels, tg_json, indent=4, sort_keys=True)
        urls.writelines([f"https://t.me/s/{name}\n" for name in sorted(channels)])
        print(f"[SAVE] Saved {len(channels)} channels in '{path_channels}'!")


@status(tag="updt", start="Updating channels...", \
    end="Updated channels!", tracking=True)
def update_channels(current_channels: dict, channel_names: list) -> None:
    for name in sort_channel_names(channel_names):
        if name not in current_channels:
            current_channels.setdefault(name, dict(current_id=1, last_id=-1, count=0))


def main() -> None:
    try:
        args = parse_args()
        current_channels, list_channel_names = \
            load_channels(path_channels=args.channels, path_urls=args.urls)
        update_channels(current_channels, list_channel_names)
        delete_channels(current_channels)
        save_channels(current_channels, path_channels=args.channels, path_urls=args.urls)
    except Exception as exception:
        print(f"[ERROR] {exception}")


if __name__ == "__main__":
    main()
