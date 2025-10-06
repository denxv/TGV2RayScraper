from json import dump, JSONDecodeError, load

from lxml import html
from requests import Session

from core.constants import (
    DEFAULT_CHANNEL_VALUES,
    FURL_TG,
    REGEX_CHANNELS_NAME,
    XPATH_POST_ID,
)
from core.decorators import status
from core.logger import logger, log_debug_object
from core.utils import make_backup
from domain.channel import sort_channel_names
from domain.predicates import condition_delete_channels


@status(
    start="Deleting inactive channels...",
    end="Inactive channels deleted successfully.",
    tracking=True,
)
def delete_channels(channels: dict) -> None:
    for channel_name, channel_info in list(channels.items()):
        if condition_delete_channels(channel_info):
            log_debug_object(
                title=(
                    f"Deleting channel '{channel_name}' "
                    "with the following information"
                ),
                obj=channel_info,
            )
            channels.pop(channel_name, None)


def get_last_id(session: Session, channel_name: str) -> int:
    response = session.get(FURL_TG.format(name=channel_name))
    list_post = html.fromstring(response.content).xpath(XPATH_POST_ID)
    return int(list_post[-1].split("/")[-1]) if list_post else -1


def load_channels(path_channels: str = "current.json") -> dict:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            return load(file)
        except JSONDecodeError:
            return {}


@status(
    start="Loading all channels...",
    end="All channels loaded successfully.",
    tracking=False,
)
def load_channels_and_urls(
    path_channels: str = "current.json",
    path_urls: str = "urls.txt",
) -> tuple[dict, list]:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            channels = load(file)
        except json.JSONDecodeError:
            channels = {}
    with open(path_urls, "r", encoding="utf-8") as file:
        urls = REGEX_CHANNELS_NAME.findall(file.read())
    return channels, urls


def save_channels(channels: list, path_channels: str = "current.json") -> None:
    with open(path_channels, "w", encoding="utf-8") as file:
        dump(channels, file, indent=4, sort_keys=True)
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


@status(
    start="Saving all channels...",
    end="",
    tracking=False,
)
def save_channels_and_urls(
    channels: dict,
    path_channels: str = "current.json",
    path_urls: str = "urls.txt",
) -> None:
    make_backup([path_urls, path_channels])

    with open(path_channels, "w", encoding="utf-8") as tg_json, \
        open(path_urls, "w", encoding="utf-8") as urls:
        dump(channels, tg_json, indent=4, sort_keys=True)
        urls.writelines([
            f"https://t.me/s/{name}\n"
            for name in sorted(channels)
        ])

    logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


@status(
    start="Adding missing channels...",
    end="Missing channels added successfully.",
    tracking=True,
)
def update_with_new_channels(current_channels: dict, channel_names: list) -> None:
    for name in sort_channel_names(channel_names):
        if name not in current_channels:
            current_channels.setdefault(name, DEFAULT_CHANNEL_VALUES.copy())
