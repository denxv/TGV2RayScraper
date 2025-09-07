#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
import requests
from lxml import html
from tqdm import tqdm

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


def current_less_last(channel_info: dict) -> bool:
    return channel_info["current_id"] < channel_info["last_id"]


def diff_channel_id(channel_info: dict) -> int:
    return channel_info["last_id"] - channel_info["current_id"]


def format_channel_id(channel_info: dict) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff
    return f"{channel_info['current_id']:>{LEN_NUMBER}} / {channel_info['last_id']:<{LEN_NUMBER}} (+{diff})"


def get_configs_by_channel(channel_name: str, channel_info: dict, \
    path_configs: str = "v2ray-configs-raw.txt") -> int:
    v2ray_count = 0
    bar_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    range_channel_id = range(channel_info["current_id"], channel_info["last_id"], 20)
    print(f"[EXTR] Extracting configs from channel '{channel_name}'...")

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
    return v2ray_count


def get_last_id(channel_name: str) -> int:
    response = SESSION_TG.get(FURL_TG.format(name=channel_name))
    list_post = html.fromstring(response.content).xpath(XPATH_POST_ID)
    return int(list_post[-1].split("/")[-1]) if list_post else -1


def get_sorted_keys(channels: dict) -> list:
    return sorted(channels.keys(), key=lambda name: diff_channel_id(channels[name]))


def load_channels(path_channels: str = "tg-channels-current.json") -> list:
    with open(path_channels, "r", encoding="utf-8") as file:
        return json.load(file)


def print_channel_info(channels: dict) -> None:
    channels_count = 0
    print(f"[INFO] Showing information about the remaining channels...")
    for channel_name, channel_info in channels.items():
        if current_less_last(channel_info):
            channels_count = channels_count + 1
            print(f" <SS>  {channel_name:<{LEN_NAME}}{format_channel_id(channel_info)}")
    else:
        print(f"\n[INFO] Total channels are available for extracting configs: {len(channels)}")
        print(f"[INFO] Channels left to check: {channels_count}")
        print(f"[INFO] Total messages on channels: {TOTAL_CHANNELS_POST:,}", end="\n\n")


def save_channels(channels: list, path_channels: str = "tg-channels-current.json") -> None:
    with open(path_channels, "w", encoding="utf-8") as file:
        json.dump(channels, file, indent=4, sort_keys=True)


def update_info(channels: dict) -> None:
    print(f"[INFO] Updating info channels...")
    for key in channels.keys():
        channel_info = channels[key]
        count = channel_info.get("count", 0)
        last_id = get_last_id(key)

        if channel_info["last_id"] == last_id == -1:
            channel_info["count"] = 0 if count > 0 else count - 1
        elif channel_info["last_id"] != last_id:
            print(f" <UU>  {key:<{LEN_NAME}}\
                {channel_info['last_id']:>{LEN_NUMBER}} -> {last_id:<{LEN_NUMBER}}")
            channel_info["last_id"] = last_id
            channel_info["count"] = 1 if count <= 0 else count

        if channel_info["current_id"] <= 0:
            diff = channel_info["last_id"] + channel_info["current_id"]
            channel_info["current_id"] = diff if diff > 0 else 1
        elif channel_info["current_id"] > channel_info["last_id"] != -1:
            channel_info["current_id"] = channel_info["last_id"]
    else:
        print(end="\n")


def write_configs(configs: list, \
    path_configs: str = "v2ray-configs-raw.txt", mode: str = "w") -> None:
    with open(path_configs, mode, encoding="utf-8") as file:
        file.writelines(f"{config}\n" for config in configs)


def main(path_channels: str = "tg-channels-current.json", 
    path_configs: str = "v2ray-configs-raw.txt") -> None:
    try:
        channels = dict() if not os.path.exists(path_channels) else \
            load_channels(path_channels=path_channels)
        update_info(channels)
        print_channel_info(channels)
        for name in get_sorted_keys(channels):
            channel_info = channels[name]
            if current_less_last(channel_info):
                length = get_configs_by_channel(name, channel_info, path_configs=path_configs)
                print(f"[EXTR] Found: {length} configs!", end="\n\n")
    except KeyboardInterrupt:
        print(f"[ERROR] Exit from the program!")
    except Exception as exception:
        print(f"[ERROR] {exception}")
    finally:
        save_channels(channels, path_channels=path_channels)
        print(f"[INFO] Saved channel data in '{path_channels}'!")


if __name__ == "__main__":
    current_json = os.path.join(os.path.dirname(__file__), "../channels/current.json")
    raw_txt = os.path.join(os.path.dirname(__file__), "../v2ray/configs-raw.txt")
    main(path_channels=current_json, path_configs=raw_txt)
