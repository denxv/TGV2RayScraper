#!/usr/bin/env python
# coding: utf-8

import json
import re
from pathlib import Path
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    HelpFormatter,
    Namespace,
    SUPPRESS,
)

import requests
from lxml import html
from tqdm import tqdm

from logger import logger, log_debug_object

DEFAULT_PATH_CHANNELS = "../channels/current.json"
DEFAULT_PATH_CONFIGS_RAW = "../configs/v2ray-raw.txt"
LEN_NAME = 32
LEN_NUMBER = 7
TOTAL_CHANNELS_POST = 0
SESSION_TG = requests.Session()

FURL_TG = "https://t.me/s/{name}"
FURL_TG_AFTER = FURL_TG + "?after={id}"
FURL_TG_BEFORE = FURL_TG + "?before={id}"

XPATH_V2RAY = "//div[@class='tgme_widget_message_text js-message_text']//text()"
XPATH_POST_ID = "//div[@class='tgme_widget_message text_not_supported_wrap js-widget_message']/@data-post"
RE_V2RAY = re.compile(
    r'(?:'
        r'anytls'
    r'|'
        r'hy2'
    r'|'
        r'hysteria2'
    r'|'
        r'\bss\b'
    r'|'
        r'ssr'
    r'|'
        r'trojan'
    r'|'
        r'tuic'
    r'|'
        r'vless'
    r'|'
        r'vmess'
    r'|'
        r'wireguard'
    r')://(?:(?!://)[\S])+'
)


def abs_path(path: str | Path) -> str:
    return str((Path(__file__).parent / path).resolve())


def current_less_last(channel_info: dict) -> bool:
    return channel_info["current_id"] < channel_info["last_id"]


def diff_channel_id(channel_info: dict) -> int:
    return channel_info["last_id"] - channel_info["current_id"]


def format_channel_id(channel_info: dict) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff
    return (
        f"{channel_info['current_id']:>{LEN_NUMBER}} "
        f"/ {channel_info['last_id']:<{LEN_NUMBER}} "
        f"(+{diff})"
    )


def get_filtered_keys(channels: dict) -> list:
    return list(filter(lambda name: current_less_last(channels[name]), channels.keys()))


def get_last_id(channel_name: str) -> int:
    response = SESSION_TG.get(FURL_TG.format(name=channel_name))
    list_post = html.fromstring(response.content).xpath(XPATH_POST_ID)
    return int(list_post[-1].split("/")[-1]) if list_post else -1


def get_sorted_keys(channels: dict, filtering: bool = False, reverse: bool = False) -> list:
    channel_names = get_filtered_keys(channels) if filtering else channels.keys()
    return sorted(channel_names, key=lambda name: diff_channel_id(channels[name]), reverse=reverse)


def load_channels(path_channels: str = "tg-channels-current.json") -> dict:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Synchronous Telegram channel scraper (simpler, slower).",
        epilog="Example: python %(prog)s -C channels.json --configs-raw configs-raw.txt",
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
        "-R", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the output file for saving scraped V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def print_channel_info(channels: dict) -> None:
    logger.info(f"Showing information about the remaining channels...")
    channel_names = get_sorted_keys(channels, filtering=True)
    for name in channel_names:
        logger.info(f" <SS>  {name:<{LEN_NAME}}{format_channel_id(channels[name])}")
    else:
        logger.info(f"Total channels are available for extracting configs: {len(channels)}")
        logger.info(f"Channels left to check: {len(channel_names)}")
        logger.info(f"Total messages on channels: {TOTAL_CHANNELS_POST:,}")


def save_channels(channels: list, path_channels: str = "tg-channels-current.json") -> None:
    with open(path_channels, "w", encoding="utf-8") as file:
        json.dump(channels, file, indent=4, sort_keys=True)
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


def save_channel_configs(channel_name: str, channel_info: dict, \
    path_configs: str = "v2ray-configs-raw.txt") -> None:
    v2ray_count = 0
    bar_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    range_channel_id = range(channel_info["current_id"], channel_info["last_id"], 20)
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    for current_id in tqdm(range_channel_id, ascii=True, bar_format=bar_format, leave=False):
        channel_info["current_id"] = current_id
        response = SESSION_TG.get(FURL_TG_AFTER.format(name=channel_name, id=current_id))
        html_text = html.fromstring(response.content)
        if v2ray_configs := list(filter(RE_V2RAY.match, html_text.xpath(XPATH_V2RAY))):
            v2ray_count = v2ray_count + len(v2ray_configs)
            channel_info["count"] = channel_info.get("count", 0) + len(v2ray_configs)
            write_configs(v2ray_configs, path_configs=path_configs, mode="a")
    else:
        channel_info["current_id"] = channel_info["last_id"]
        logger.info(f"Found: {v2ray_count} configs.")


def update_info(channels: dict) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")
    for channel_name in channels.keys():
        channel_info = channels[channel_name]
        count = channel_info.get("count", 0)
        last_id = get_last_id(channel_name)

        if channel_info["last_id"] == last_id == -1:
            channel_info["count"] = 0 if count > 0 else count - 1
        elif channel_info["last_id"] != last_id:
            logger.info(
                f" <UU>  {channel_name:<{LEN_NAME}}"
                f"{channel_info['last_id']:>{LEN_NUMBER}} "
                f"-> {last_id:<{LEN_NUMBER}}"
            )
            channel_info["last_id"] = last_id
            channel_info["count"] = 1 if count <= 0 else count

        if channel_info["current_id"] <= 0:
            diff = channel_info["last_id"] + channel_info["current_id"]
            channel_info["current_id"] = diff if diff > 0 else 1
        elif channel_info["current_id"] > channel_info["last_id"] != -1:
            channel_info["current_id"] = channel_info["last_id"]


def validate_file_path(path: str | Path, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")
    
    return str(filepath)


def write_configs(configs: list, \
    path_configs: str = "v2ray-configs-raw.txt", mode: str = "w") -> None:
    with open(path_configs, mode, encoding="utf-8") as file:
        file.writelines(f"{config}\n" for config in configs)


def main() -> None:
    parsed_args = parse_args()
    try:
        channels = load_channels(path_channels=parsed_args.channels)
        update_info(channels)
        print_channel_info(channels)
        for name in get_sorted_keys(channels, filtering=True):
            save_channel_configs(
                channel_name=name, 
                channel_info=channels[name], 
                path_configs=parsed_args.configs_raw,
            )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")
    finally:
        save_channels(channels, path_channels=parsed_args.channels)


if __name__ == "__main__":
    main()
