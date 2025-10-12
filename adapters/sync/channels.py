from json import dump, JSONDecodeError, load

from lxml import html

from core.constants import (
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CHANNELS,
    DEFAULT_FILE_URLS,
    DEFAULT_INDENT,
    DEFAULT_LAST_ID,
    DEFAULT_POST_ID,
    PATTERN_TG_CHANNEL_NAME,
    POST_DEFAULT_INDEX,
    POST_FIRST_ID,
    POST_FIRST_INDEX,
    POST_LAST_INDEX,
    TEMPLATE_TG_URL,
    TEMPLATE_TG_URL_AFTER,
    XPATH_POST_IDS,
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
    SyncHTTPClient,
    URL,
)
from core.utils import make_backup
from domain.channel import sort_channel_names
from domain.predicates import should_delete_channel


def _extract_post_id(
    client: SyncHTTPClient,
    url: URL,
    index: PostIndex = POST_DEFAULT_INDEX,
    default: DefaultPostID = DEFAULT_POST_ID,
) -> PostID:
    try:
        response = client.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        post_ids = tree.xpath(XPATH_POST_IDS)

        if not post_ids:
            raise ValueError("No posts found.")

        post_url = post_ids[index]
        post_id = post_url.split("/")[-1]
        return int(post_id)

    except Exception as e:
        logger.debug(
            f"Failed to extract post ID from '{url}': {type(e).__name__}: {e}"
        )
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


def get_first_post_id(client: SyncHTTPClient, channel_name: ChannelName) -> PostID:
    return _extract_post_id(
        client=client,
        url=TEMPLATE_TG_URL_AFTER.format(name=channel_name, id=POST_FIRST_ID),
        index=POST_FIRST_INDEX,
        default=DEFAULT_CURRENT_ID,
    )


def get_last_post_id(client: SyncHTTPClient, channel_name: ChannelName) -> PostID:
    return _extract_post_id(
        client=client,
        url=TEMPLATE_TG_URL.format(name=channel_name),
        index=POST_LAST_INDEX,
        default=DEFAULT_LAST_ID,
    )


def load_channels(path_channels: FilePath = DEFAULT_FILE_CHANNELS) -> ChannelsDict:
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
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
    path_urls: FilePath = DEFAULT_FILE_URLS,
) -> ChannelsAndNames:
    with open(path_channels, "r", encoding="utf-8") as file:
        try:
            channels = load(file)
        except JSONDecodeError:
            channels = {}
    with open(path_urls, "r", encoding="utf-8") as file:
        urls = PATTERN_TG_CHANNEL_NAME.findall(file.read())
    return channels, urls


def save_channels(
    channels: ChannelsDict,
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
) -> None:
    with open(path_channels, "w", encoding="utf-8") as file:
        dump(channels, file, indent=DEFAULT_INDENT, sort_keys=True)
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")


@status(
    start="Saving all channels...",
    end="",
    tracking=False,
)
def save_channels_and_urls(
    channels: ChannelsDict,
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
    path_urls: FilePath = DEFAULT_FILE_URLS,
) -> None:
    make_backup([path_urls, path_channels])

    with open(path_channels, "w", encoding="utf-8") as tg_json, \
        open(path_urls, "w", encoding="utf-8") as urls:
        dump(channels, tg_json, indent=DEFAULT_INDENT, sort_keys=True)
        urls.writelines([
            TEMPLATE_TG_URL.format(name=name) + "\n"
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
