#!/usr/bin/env python
# coding: utf-8

import json
from pathlib import Path
from argparse import (
    ArgumentParser,
    HelpFormatter,
    Namespace,
    SUPPRESS,
)

from .logger import logger, log_debug_object
from .const import (
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_URLS,
    REGEX_CHANNELS_NAME,
)
from .utils import (
    abs_path,
    condition_delete_channels,
    make_backup,
    sort_channel_names,
    status,
    validate_file_path,
)


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Backup, merge new channels from URLs, and update Telegram channel data.",
        epilog="Example: python %(prog)s -C channels.json --urls urls.txt",
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=120,
        ),
    )

    parser.add_argument(
        "-C", "--channels",
        default=abs_path(DEFAULT_PATH_CHANNELS),
        dest="channels",
        help="Path to the input JSON file containing the list of channels (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-U", "--urls",
        default=abs_path(DEFAULT_PATH_URLS),
        dest="urls",
        help="Path to a text file containing new channel URLs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


@status(
    start="Deleting inactive channels...",
    end="Inactive channels deleted successfully.",
    tracking=True,
)
def delete_channels(channels: dict) -> None:
    for channel_name, channel_info in list(channels.items()):
        if condition_delete_channels(channel_info):
            channels.pop(channel_name, None)


@status(
    start="Loading all channels...",
    end="All channels loaded successfully.",
    tracking=False,
)
def load_channels(
    path_channels: str = "tg-channels-current.json",
    path_urls: str = "tg-channels-urls.txt",
) -> tuple[dict, list]:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            channels = json.load(file)
        except json.JSONDecodeError:
            channels = {}
    with open(path_urls, "r", encoding="utf-8") as file:
        urls = REGEX_CHANNELS_NAME.findall(file.read())
    return channels, urls


@status(
    start="Saving all channels...",
    end="",
    tracking=False,
)
def save_channels(
    channels: dict,
    path_channels: str = "tg-channels-current.json",
    path_urls: str = "tg-channels-urls.txt",
) -> None:
    make_backup([path_urls, path_channels])
    with open(path_channels, "w", encoding="utf-8") as tg_json, \
        open(path_urls, "w", encoding="utf-8") as urls:
        json.dump(channels, tg_json, indent=4, sort_keys=True)
        urls.writelines([f"https://t.me/s/{name}\n" for name in sorted(channels)])
    logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


@status(
    start="Adding missing channels...",
    end="Missing channels added successfully.",
    tracking=True,
)
def update_with_new_channels(current_channels: dict, channel_names: list) -> None:
    for name in sort_channel_names(channel_names):
        if name not in current_channels:
            current_channels.setdefault(name, dict(current_id=1, last_id=-1, count=0))


def main() -> None:
    try:
        parsed_args = parse_args()
        current_channels, list_channel_names = load_channels(
            path_channels=parsed_args.channels, 
            path_urls=parsed_args.urls,
        )
        update_with_new_channels(current_channels, list_channel_names)
        delete_channels(current_channels)
        save_channels(
            channels=current_channels, 
            path_channels=parsed_args.channels, 
            path_urls=parsed_args.urls,
        )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == "__main__":
    main()
