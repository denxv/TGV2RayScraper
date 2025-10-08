from core.constants import LEN_NAME, LEN_NUMBER, TOTAL_CHANNELS_POST
from core.logger import logger
from domain.predicates import should_update_channel


def diff_channel_id(channel_info: dict) -> int:
    return channel_info.get("last_id", 0) - channel_info.get("current_id", 0)


def format_channel_id(channel_info: dict) -> str:
    global TOTAL_CHANNELS_POST
    diff = diff_channel_id(channel_info)
    TOTAL_CHANNELS_POST = TOTAL_CHANNELS_POST + diff
    return (
        f"{channel_info.get('current_id', 0):>{LEN_NUMBER}} "
        f"/ {channel_info.get('last_id', 0):<{LEN_NUMBER}} "
        f"(+{diff})"
    )


def get_filtered_keys(channels: dict) -> list:
    return [name for name, info in channels.items() if should_update_channel(info)]


def get_sorted_keys(channels: dict, apply_filter: bool = False, reverse: bool = False) -> list:
    channel_names = get_filtered_keys(channels) if apply_filter else list(channels.keys())
    return sorted(channel_names, key=lambda name: diff_channel_id(channels[name]), reverse=reverse)


def print_channel_info(channels: dict) -> None:
    logger.info(f"Showing information about the remaining channels...")
    channel_names = get_sorted_keys(channels, apply_filter=True)
    for name in channel_names:
        logger.info(f" <SS>  {name:<{LEN_NAME}}{format_channel_id(channels[name])}")
    else:
        logger.info(f"Total channels are available for extracting configs: {len(channels)}")
        logger.info(f"Channels left to check: {len(channel_names)}")
        logger.info(f"Total messages on channels: {TOTAL_CHANNELS_POST:,}")


def sort_channel_names(channel_names: list) -> list:
    return sorted([name.lower() for name in channel_names])
