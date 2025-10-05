#!/usr/bin/env python
# coding: utf-8

import asyncio
import json
from pathlib import Path
from typing import Union
from argparse import (
    ArgumentParser,
    HelpFormatter,
    Namespace,
    SUPPRESS,
)

import aiofiles
from aiohttp import ClientSession
from lxml import html
from tqdm.asyncio import tqdm

from .logger import logger, log_debug_object
from .const import (
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_CONFIGS_RAW,
    FURL_TG,
    FURL_TG_AFTER,
    LEN_NAME,
    LEN_NUMBER,
    REGEX_V2RAY,
    XPATH_POST_ID,
    XPATH_V2RAY,
)
from .utils import (
    abs_path,
    get_sorted_keys,
    int_in_range,
    print_channel_info,
    validate_file_path,
)


async def get_last_id(session: ClientSession, channel_name: str) -> int:
    async with session.get(FURL_TG.format(name=channel_name)) as response:
        content = await response.text()
        list_post = html.fromstring(content).xpath(XPATH_POST_ID)
        return int(list_post[-1].split("/")[-1]) if list_post else -1


async def load_channels(path_channels: str = "tg-channels-current.json") -> dict:
    async with aiofiles.open(path_channels, "r", encoding="utf-8") as file:
        try:
            data = await file.read()
            return json.loads(data)
        except json.JSONDecodeError:
            return {}


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description = "Asynchronous Telegram channel scraper (faster, experimental).",
        epilog="Example: python %(prog)s -E 20 -U 100 --channels channels.json -R configs-raw.txt",
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
        "-E", "--batch-extract",
        default=20,
        dest="batch_extract",
        help="Number of messages processed in parallel to extract V2Ray configs (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=100),
    )

    parser.add_argument(
        "-R", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the output file for saving scraped V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "-U", "--batch-update",
        default=100,
        dest="batch_update",
        help="Maximum number of channels updated in parallel (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=1000),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


async def save_channels(channels: dict, path_channels: str = "tg-channels-current.json") -> None:
    async with aiofiles.open(path_channels, "w", encoding="utf-8") as file:
        await file.write(json.dumps(channels, indent=4, sort_keys=True, ensure_ascii=False))
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


async def save_channel_configs(session: ClientSession, channel_name: str, \
    channel_info: dict, batch_size: int = 20, path_configs: str = "v2ray-configs-raw.txt") -> None:
    v2ray_count = 0
    list_channel_id = list(range(channel_info["current_id"], channel_info["last_id"], 20))
    batch_range = range(0, len(list_channel_id), batch_size)
    bar_channel_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    async def fetch_and_parse(current_id: int) -> Union[int, list]:
        async with session.get(FURL_TG_AFTER.format(name=channel_name, id=current_id)) as response:
            content = await response.text()
            html_text = html.fromstring(content)
            if v2ray_configs := list(filter(REGEX_V2RAY.match, html_text.xpath(XPATH_V2RAY))):
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
    logger.info(f"Found: {v2ray_count} configs.")


async def update_info(session: ClientSession, channels: dict, batch_size: int = 100) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")

    async def update_channel(channel_name: str, channel_info: dict) -> None:
        count = channel_info.get("count", 0)
        last_id = await get_last_id(session, channel_name)

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

    channel_names = list(channels.keys())
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            asyncio.create_task(update_channel(name, channels[name]))
            for name in channel_names[i:i + batch_size]
        ]
        await asyncio.gather(*tasks)


async def write_configs(configs: list, \
    path_configs: str = "v2ray-configs-raw.txt", mode: str = "w") -> None:
    async with aiofiles.open(path_configs, mode, encoding="utf-8") as file:
        await file.writelines(f"{config}\n" for config in configs)


async def main() -> None:
    parsed_args = parse_args()
    try:
        channels = await load_channels(path_channels=parsed_args.channels)
        async with ClientSession() as session:
            await update_info(session, channels, batch_size=parsed_args.batch_update)
            print_channel_info(channels)
            for name in get_sorted_keys(channels, filtering=True):
                await save_channel_configs(
                    session=session, 
                    channel_name=name, 
                    channel_info=channels[name], 
                    batch_size=parsed_args.batch_extract, 
                    path_configs=parsed_args.configs_raw,
                )
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")
    finally:
        await save_channels(channels, path_channels=parsed_args.channels)


if __name__ == "__main__":
    asyncio.run(main())
