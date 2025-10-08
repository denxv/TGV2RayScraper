from json import dump, JSONDecodeError, load

from lxml import html

from core.constants import (
    DEFAULT_CHANNEL_VALUES,
    FURL_TG,
    FURL_TG_AFTER,
    REGEX_CHANNELS_NAME,
    XPATH_POST_ID,
)
from core.decorators import status
from core.logger import logger, log_debug_object
from core.typing import (
    ChannelName,
    ChannelNames,
    ChannelsAndNames,
    ChannelsDict,
    DefaultPostID,
    FilePath,
    PostID,
    PostIndex,
    SyncSession,
    URL,
)
from core.utils import make_backup
from domain.channel import sort_channel_names
from domain.predicates import should_delete_channel


def _extract_post_id(
    session: SyncSession,
    url: URL,
    index: PostIndex = 0,
    default: DefaultPostID = 0,
) -> PostID:
    try:
        response = session.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        post_ids = tree.xpath(XPATH_POST_ID)

        if not post_ids:
            raise ValueError("No posts found.")

        post_url = post_ids[index]
        post_id = post_url.split("/")[-1]
        return int(post_id)

    except Exception as e:
        logger.debug(f"Failed to extract post ID from '{url}': {type(e).__name__}: {e}")
        return default


@status(
    start="Deleting inactive channels...",
    end="Inactive channels deleted successfully.",
    tracking=True,
)
def delete_channels(channels: ChannelsDict) -> None:
    for channel_name, channel_info in list(channels.items()):
        if should_delete_channel(channel_info):
            log_debug_object(
                title=(
                    f"Deleting channel '{channel_name}' "
                    "with the following information"
                ),
                obj=channel_info,
            )
            channels.pop(channel_name, None)


def get_first_post_id(session: SyncSession, channel_name: ChannelName) -> PostID:
    url = FURL_TG_AFTER.format(name=channel_name, id=1)
    return _extract_post_id(session, url, index=0, default=1)


def get_last_post_id(session: SyncSession, channel_name: ChannelName) -> PostID:
    url = FURL_TG.format(name=channel_name)
    return _extract_post_id(session, url, index=-1, default=-1)


def load_channels(path_channels: FilePath = "current.json") -> ChannelsDict:
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
    path_channels: FilePath = "current.json",
    path_urls: FilePath = "urls.txt",
) -> ChannelsAndNames:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            channels = load(file)
        except JSONDecodeError:
            channels = {}
    with open(path_urls, "r", encoding="utf-8") as file:
        urls = REGEX_CHANNELS_NAME.findall(file.read())
    return channels, urls


def save_channels(
    channels: ChannelsDict,
    path_channels: FilePath = "current.json",
) -> None:
    with open(path_channels, "w", encoding="utf-8") as file:
        dump(channels, file, indent=4, sort_keys=True)
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


@status(
    start="Saving all channels...",
    end="",
    tracking=False,
)
def save_channels_and_urls(
    channels: ChannelsDict,
    path_channels: FilePath = "current.json",
    path_urls: FilePath = "urls.txt",
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
def update_with_new_channels(
    current_channels: ChannelsDict,
    channel_names: ChannelNames,
) -> None:
    for name in sort_channel_names(channel_names):
        if name not in current_channels:
            logger.debug(f"Channel '{name}' missing, adding to list.")
            current_channels.setdefault(name, DEFAULT_CHANNEL_VALUES.copy())
