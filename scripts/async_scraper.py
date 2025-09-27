#!/usr/bin/env python
# coding: utf-8

import asyncio
import json
import re
import aiofiles
import aiohttp
from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter, Namespace
from lxml import html
from pathlib import Path
from tqdm.asyncio import tqdm
from typing import Union

LEN_NAME = 32
LEN_NUMBER = 7
TOTAL_CHANNELS_POST = 0

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


def abs_path(path: str) -> str:
    return str((Path(__file__).parent / path).resolve())


def current_less_last(channel_info: dict) -> bool:
    return channel_info["current_id"] < channel_info["last_id"]


def diff_channel_id(channel_info: dict) -> int:
    return channel_info["last_id"] - channel_info["current_id"]


def existing_file(path: str) -> str:
    filepath = Path(path).resolve()
    if not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: {filepath}")
    return str(filepath)


def format_channel_id(channel_info: dict) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff
    return f"{channel_info['current_id']:>{LEN_NUMBER}} / {channel_info['last_id']:<{LEN_NUMBER}} (+{diff})"


def get_filtered_keys(channels: dict) -> list:
    return list(filter(lambda name: current_less_last(channels[name]), channels.keys()))


async def get_last_id(session: aiohttp.ClientSession, channel_name: str) -> int:
    async with session.get(FURL_TG.format(name=channel_name)) as response:
        content = await response.text()
        list_post = html.fromstring(content).xpath(XPATH_POST_ID)
        return int(list_post[-1].split("/")[-1]) if list_post else -1


def get_sorted_keys(channels: dict, filtering: bool = False, reverse: bool = False) -> list:
    channel_names = get_filtered_keys(channels) if filtering else channels.keys()
    return sorted(channel_names, key=lambda name: diff_channel_id(channels[name]), reverse=reverse)


def int_in_range(value: str, min_value: int = 1, max_value: int = 100) -> int:
    ivalue = int(value)
    if ivalue < min_value or ivalue > max_value:
        raise ArgumentTypeError(f"Expected {min_value} to {max_value}, got {ivalue}")
    return ivalue


async def load_channels(path_channels: str = "tg-channels-current.json") -> dict:
    async with aiofiles.open(path_channels, "r", encoding="utf-8") as file:
        try:
            data = await file.read()
            return json.loads(data)
        except json.JSONDecodeError:
            return {}


def parse_args() -> Namespace:
    channels_rel_path = "../channels/current.json"
    configs_rel_path = "../v2ray/configs-raw.txt"

    parser = ArgumentParser(
        description = "Asynchronous Telegram channel scraper (faster, experimental)",
        epilog="Example: python %(prog)s -E 20 -U 100 --channels channels.json --output configs.txt",
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
        "-E", "--batch-extract",
        default=20,
        dest="batch_extract",
        help="Number of concurrent pages to extract v2ray configs from (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=100),
    )

    parser.add_argument(
        "-O", "--output",
        default=abs_path(configs_rel_path),
        dest="configs",
        help="Path to save scraped V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=existing_file,
    )

    parser.add_argument(
        "-U", "--batch-update",
        default=100,
        dest="batch_update",
        help="Max number of concurrent channels to update info for (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=1000),
    )

    return parser.parse_args()


def print_channel_info(channels: dict) -> None:
    print(f"[INFO] Showing information about the remaining channels...")
    channel_names = get_sorted_keys(channels, filtering=True)
    for name in channel_names:
        print(f" <SS>  {name:<{LEN_NAME}}{format_channel_id(channels[name])}")
    else:
        print(f"\n[INFO] Total channels are available for extracting configs: {len(channels)}")
        print(f"[INFO] Channels left to check: {len(channel_names)}")
        print(f"[INFO] Total messages on channels: {TOTAL_CHANNELS_POST:,}", end="\n\n")


async def save_channels(channels: dict, path_channels: str = "tg-channels-current.json") -> None:
    async with aiofiles.open(path_channels, "w", encoding="utf-8") as file:
        await file.write(json.dumps(channels, indent=4, sort_keys=True, ensure_ascii=False))
        print(f"[INFO] Saved channel data in '{path_channels}'!")


async def save_channel_configs(session: aiohttp.ClientSession, channel_name: str, \
    channel_info: dict, batch_size: int = 20, path_configs: str = "v2ray-configs-raw.txt") -> None:
    v2ray_count = 0
    list_channel_id = list(range(channel_info["current_id"], channel_info["last_id"], 20))
    batch_range = range(0, len(list_channel_id), batch_size)
    bar_channel_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    print(f"[EXTR] Extracting configs from channel '{channel_name}'...")

    async def fetch_and_parse(current_id: int) -> Union[int, list]:
        async with session.get(FURL_TG_AFTER.format(name=channel_name, id=current_id)) as response:
            content = await response.text()
            html_text = html.fromstring(content)
            if v2ray_configs := list(filter(RE_V2RAY.match, html_text.xpath(XPATH_V2RAY))):
                return current_id, v2ray_configs
            return current_id, []

    for channel_id in tqdm(batch_range, ascii=True, bar_format=bar_channel_format, leave=False):
        batch = list_channel_id[channel_id:channel_id + batch_size]
        results = await asyncio.gather(*(fetch_and_parse(_id) for _id in batch))
        for current_id, configs in results:
            channel_info["current_id"] = current_id
            if len(configs) > 0:
                v2ray_count = v2ray_count + len(configs)
                channel_info["count"] = channel_info.get("count", 0) + len(configs)
                await write_configs(configs, path_configs=path_configs, mode="a")

    channel_info["current_id"] = channel_info["last_id"]
    print(f"[EXTR] Found: {v2ray_count} configs!", end="\n\n")


async def update_info(session: aiohttp.ClientSession, channels: dict, batch_size: int = 100) -> None:
    print(f"[INFO] Updating info channels...")

    async def update_channel(channel_name: str, channel_info: dict) -> None:
        count = channel_info.get("count", 0)
        last_id = await get_last_id(session, channel_name)

        if channel_info["last_id"] == last_id == -1:
            channel_info["count"] = 0 if count > 0 else count - 1
        elif channel_info["last_id"] != last_id:
            print(f" <UU>  {channel_name:<{LEN_NAME}}\
                {channel_info['last_id']:>{LEN_NUMBER}} -> {last_id:<{LEN_NUMBER}}")
            channel_info["last_id"] = last_id
            channel_info["count"] = 1 if count <= 0 else count

        if channel_info["current_id"] <= 0:
            diff = channel_info["last_id"] + channel_info["current_id"]
            channel_info["current_id"] = diff if diff > 0 else 1
        elif channel_info["current_id"] > channel_info["last_id"] != -1:
            channel_info["current_id"] = channel_info["last_id"]

    channel_names = list(channels.keys())
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            asyncio.create_task(update_channel(name, channels[name]))
            for name in channel_names[i:i + batch_size]
        ]
        await asyncio.gather(*tasks)
    else:
        print(end="\n")


async def write_configs(configs: list, \
    path_configs: str = "v2ray-configs-raw.txt", mode: str = "w") -> None:
    async with aiofiles.open(path_configs, mode, encoding="utf-8") as file:
        await file.writelines(f"{config}\n" for config in configs)


async def main() -> None:
    args = parse_args()
    try:
        channels = await load_channels(path_channels=args.channels)
        async with aiohttp.ClientSession() as session:
            await update_info(session, channels, batch_size=args.batch_update)
            print_channel_info(channels)
            for name in get_sorted_keys(channels, filtering=True):
                await save_channel_configs(session, name, channels[name], \
                    batch_size=args.batch_extract, path_configs=args.configs)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print(f"[ERROR] Exit from the program!")
    except Exception as exception:
        print(f"[ERROR] {exception}")
    finally:
        await save_channels(channels, path_channels=args.channels)


if __name__ == "__main__":
    asyncio.run(main())
