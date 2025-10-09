from core.constants import (
    CHANNEL_ACTIVE_THRESHOLD,
    CHANNEL_MIN_ID_DIFF,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    LEN_NAME,
    LEN_NUMBER,
    TOTAL_CHANNELS_POST,
)
from core.logger import logger
from core.typing import (
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    PostID,
)
from domain.predicates import should_update_channel


def diff_channel_id(channel_info: ChannelInfo) -> int:
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)
    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    return max(CHANNEL_MIN_ID_DIFF, last_id - current_id)


def format_channel_id(channel_info: ChannelInfo) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff

    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    return f"{current_id:>{LEN_NUMBER}} / {last_id:<{LEN_NUMBER}} (+{diff})"


def get_filtered_keys(channels: ChannelsDict) -> ChannelNames:
    return [name for name, info in channels.items() if should_update_channel(info)]


def get_sorted_keys(
    channels: ChannelsDict,
    apply_filter: bool = False,
    reverse: bool = False,
) -> ChannelNames:
    channel_names = get_filtered_keys(channels) if apply_filter else list(channels.keys())
    return sorted(channel_names, key=lambda name: diff_channel_id(channels[name]), reverse=reverse)


def print_channel_info(channels: ChannelsDict) -> None:
    logger.info(f"Showing information about the remaining channels...")
    channel_names = get_sorted_keys(channels, apply_filter=True)
    for name in channel_names:
        logger.info(f" <SS>  {name:<{LEN_NAME}}{format_channel_id(channels[name])}")
    else:
        logger.info(f"Total channels are available for extracting configs: {len(channels)}")
        logger.info(f"Channels left to check: {len(channel_names)}")
        logger.info(f"Total messages on channels: {TOTAL_CHANNELS_POST:,}")


def sort_channel_names(channel_names: ChannelNames) -> ChannelNames:
    return sorted([name.lower() for name in channel_names])


def update_count_and_last_id(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    last_post_id: PostID,
) -> None:
    count = channel_info.get("count", DEFAULT_COUNT)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    if last_id != last_post_id:
        logger.info(
            f" <UU>  {channel_name:<{LEN_NAME}}"
            f"{last_id:>{LEN_NUMBER}} -> {last_post_id:<{LEN_NUMBER}}"
        )
        channel_info["last_id"] = last_post_id
        channel_info["count"] = max(count, CHANNEL_ACTIVE_THRESHOLD)
    elif last_id == last_post_id and last_post_id == DEFAULT_LAST_ID:
        channel_info["count"] = min(count - 1, DEFAULT_COUNT)
