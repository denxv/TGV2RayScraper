from core.constants import (
    CHANNEL_ACTIVE_THRESHOLD,
    CHANNEL_MIN_ID_DIFF,
    DEFAULT_CHANNEL_MESSAGE_OFFSET,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    LEN_NAME,
    LEN_NUMBER,
    TOTAL_CHANNELS_POST,
)
from core.decorators import status
from core.logger import logger, log_debug_object
from core.typing import (
    ArgsNamespace,
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    PostID,
)
from domain.predicates import (
    should_delete_channel,
    should_set_current_id,
    should_update_channel,
)


def assign_current_id_to_channels(
    channels: ChannelsDict,
    message_offset: int = DEFAULT_CHANNEL_MESSAGE_OFFSET,
    apply_to_new: bool = False,
    check_only: bool = False,
) -> ChannelsDict:
    if not isinstance(message_offset, int) or message_offset <= 0:
        logger.warning(
            f"Invalid offset {message_offset}, expected positive integer — assignment skipped."
        )
        return channels

    channels_to_update = {
        name: info
        for name, info in channels.items()
        if should_set_current_id(info, apply_to_new=apply_to_new)
    }

    for name, info in channels_to_update.items():
        diff = diff_channel_id(info)
        if diff <= message_offset:
            continue

        _msg = (
            f"Channel {f"'{name}'".ljust(LEN_NAME + 2)} | "
            f"ID diff = {diff:<4} | offset = {message_offset:<4} | "
            f"skipped messages due to diff > offset."
        )

        if check_only:
            log_debug_object(
                title=f"Debug info for channel '{name}' ({check_only=})", 
                obj=info,
            )
            logger.warning(_msg)
        else:
            logger.debug(f"{_msg} — assignment applied.")

    if check_only:
        logger.debug(f"Skipping assignment because {check_only=}.")
        return channels

    for name in channels_to_update.keys():
        channels[name]["current_id"] = -message_offset
        logger.debug(f"Channel '{name}': current_id = {-message_offset}")

    return channels


@status(
    start="Deleting inactive channels...",
    end="Inactive channels deleted successfully.",
    tracking=True,
)
def delete_channels(channels: ChannelsDict) -> ChannelsDict:
    updated_channels = {}

    for name, info in channels.items():
        if not should_delete_channel(info):
            updated_channels[name] = info
        else:
            log_debug_object(
                title=f"Deleting channel '{name}' with the following information",
                obj=info,
            )

    return updated_channels


def diff_channel_id(channel_info: ChannelInfo) -> int:
    current_id = get_normalized_current_id(channel_info)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)
    return max(CHANNEL_MIN_ID_DIFF, last_id - current_id)


def format_channel_id(channel_info: ChannelInfo) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff

    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    return f"{current_id:>{LEN_NUMBER}} / {last_id:<{LEN_NUMBER}} (+{diff:,})"


def get_filtered_keys(channels: ChannelsDict) -> ChannelNames:
    return [name for name, info in channels.items() if should_update_channel(info)]


def get_normalized_current_id(channel_info: ChannelInfo) -> PostID:
    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    if last_id == DEFAULT_LAST_ID:
        return DEFAULT_CURRENT_ID

    if current_id <= 0:
        return max(last_id + current_id, DEFAULT_CURRENT_ID)

    if current_id > last_id:
        return last_id

    return current_id


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


def process_channels(channels: ChannelsDict, args: ArgsNamespace) -> ChannelsDict:
    if args.delete_channels:
        channels = delete_channels(channels=channels)
    else:
        logger.info("Channel deletion skipped (default: disabled).")

    if args.message_offset:
        channels = assign_current_id_to_channels(
            channels=channels,
            message_offset=args.message_offset,
            apply_to_new=args.include_new_channels,
            check_only=args.check_only,
        )

    return channels


def sort_channel_names(
    channel_names: ChannelNames, 
    ignore_case: bool = True, 
    reverse: bool = False,
) -> ChannelNames:
    return sorted(
        channel_names,
        key=(str.lower if ignore_case else None),
        reverse=reverse,
    )


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


@status(
    start="Adding missing channels...",
    end="Missing channels added successfully.",
    tracking=True,
)
def update_with_new_channels(
    current_channels: ChannelsDict,
    channel_names: ChannelNames,
) -> ChannelsDict:
    updated_channels = current_channels.copy()
    
    for name in sort_channel_names(channel_names):
        updated_channels.setdefault(name, DEFAULT_CHANNEL_VALUES.copy())
        if name not in current_channels:
            logger.debug(f"Channel '{name}' missing, adding to list.")

    return updated_channels
