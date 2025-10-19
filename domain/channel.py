from core.constants import (
    CHANNEL_ACTIVE_THRESHOLD,
    CHANNEL_MIN_ID_DIFF,
    DEFAULT_CHANNEL_MESSAGE_OFFSET,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    MESSAGE_CHANNEL_SKIP_DELETE,
    MESSAGE_DELETE_COMPLETED,
    MESSAGE_DELETE_STARTED,
    MESSAGE_SHOW_CHANNELS_INFO,
    MESSAGE_UPDATE_COMPLETED,
    MESSAGE_UPDATE_STARTED,
    TEMPLATE_MSG_ASSIGNMENT_OFFSET,
    TEMPLATE_MSG_CHANNEL_MISSING,
    TEMPLATE_MSG_CHANNELS_LEFT,
    TEMPLATE_MSG_DEBUG_OFFSET,
    TEMPLATE_MSG_DELETING_CHANNEL,
    TEMPLATE_MSG_DIFF_OFFSET,
    TEMPLATE_MSG_DIFF_OFFSET_APPLIED,
    TEMPLATE_MSG_INVALID_OFFSET,
    TEMPLATE_MSG_LOG_STATUS,
    TEMPLATE_MSG_LOG_UPDATE,
    TEMPLATE_MSG_SKIP_ASSIGNMENT,
    TEMPLATE_MSG_TOTAL_CHANNELS,
    TEMPLATE_MSG_TOTAL_MESSAGES,
)
from core.decorators import status
from core.logger import log_debug_object, logger
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
    *,
    apply_to_new: bool = False,
    check_only: bool = False,
) -> ChannelsDict:
    if not isinstance(message_offset, int) or message_offset <= 0:
        logger.warning(TEMPLATE_MSG_INVALID_OFFSET.format(
            offset=message_offset,
        ))
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

        _message = TEMPLATE_MSG_DIFF_OFFSET.format(
            name=f"'{name}'",
            diff=diff,
            offset=message_offset,
        )

        if check_only:
            log_debug_object(
                title=TEMPLATE_MSG_DEBUG_OFFSET.format(
                    name=name,
                    check_only=check_only,
                ),
                obj=info,
            )
            logger.warning(_message)
        else:
            logger.debug(TEMPLATE_MSG_DIFF_OFFSET_APPLIED.format(
                message=_message,
            ))

    if check_only:
        logger.debug(TEMPLATE_MSG_SKIP_ASSIGNMENT.format(
            check_only=check_only,
        ))
        return channels

    for name in channels_to_update:
        channels[name]["current_id"] = -message_offset
        logger.debug(TEMPLATE_MSG_ASSIGNMENT_OFFSET.format(
            name=name,
            offset=-message_offset,
        ))

    return channels


@status(
    start=MESSAGE_DELETE_STARTED,
    end=MESSAGE_DELETE_COMPLETED,
    tracking=True,
)
def delete_channels(channels: ChannelsDict) -> ChannelsDict:
    updated_channels = {}

    for name, info in channels.items():
        if not should_delete_channel(info):
            updated_channels[name] = info
        else:
            log_debug_object(
                title=TEMPLATE_MSG_DELETING_CHANNEL.format(name=name),
                obj=info,
            )

    return updated_channels


def diff_channel_id(channel_info: ChannelInfo) -> int:
    current_id = get_normalized_current_id(channel_info)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    return max(CHANNEL_MIN_ID_DIFF, last_id - current_id)


def format_channel_status(
    channel_name: ChannelName,
    channel_info: ChannelInfo,
) -> tuple[int, str]:
    diff = diff_channel_id(channel_info)
    current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
    last_id = channel_info.get("last_id", DEFAULT_LAST_ID)

    return (
        diff,
        TEMPLATE_MSG_LOG_STATUS.format(
            name=channel_name,
            current_id=current_id,
            last_id=last_id,
            diff=diff,
        ),
    )


def get_filtered_keys(channels: ChannelsDict) -> ChannelNames:
    return [
        name
        for name, info in channels.items()
        if should_update_channel(info)
    ]


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
    *,
    apply_filter: bool = False,
    reverse: bool = False,
) -> ChannelNames:
    channel_names = list(channels.keys())

    if apply_filter:
        channel_names = get_filtered_keys(channels)

    return sorted(
        channel_names,
        key=lambda name: diff_channel_id(channels[name]),
        reverse=reverse,
    )


def print_channel_info(channels: ChannelsDict) -> None:
    logger.info(MESSAGE_SHOW_CHANNELS_INFO)

    total_channels_post = 0
    channel_names = get_sorted_keys(channels, apply_filter=True)

    for name in channel_names:
        diff, status_line = format_channel_status(
            channel_name=name,
            channel_info=channels[name],
        )
        total_channels_post += diff
        logger.info(status_line)

    logger.info(TEMPLATE_MSG_TOTAL_CHANNELS.format(count=len(channels)))
    logger.info(TEMPLATE_MSG_CHANNELS_LEFT.format(count=len(channel_names)))
    logger.info(TEMPLATE_MSG_TOTAL_MESSAGES.format(count=total_channels_post))


def process_channels(
    channels: ChannelsDict,
    args: ArgsNamespace,
) -> ChannelsDict:
    if args.delete_channels:
        channels = delete_channels(channels=channels)
    else:
        logger.info(MESSAGE_CHANNEL_SKIP_DELETE)

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
    *,
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
        logger.info(TEMPLATE_MSG_LOG_UPDATE.format(
            name=channel_name,
            last_id=last_id,
            last_post_id=last_post_id,
        ))
        channel_info["last_id"] = last_post_id
        channel_info["count"] = max(count, CHANNEL_ACTIVE_THRESHOLD)
    elif last_id == last_post_id and last_post_id == DEFAULT_LAST_ID:
        channel_info["count"] = min(count - 1, DEFAULT_COUNT)


@status(
    start=MESSAGE_UPDATE_STARTED,
    end=MESSAGE_UPDATE_COMPLETED,
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
            logger.debug(TEMPLATE_MSG_CHANNEL_MISSING.format(name=name))

    return updated_channels
