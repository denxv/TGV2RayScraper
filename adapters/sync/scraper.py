from adapters.sync.channels import get_first_post_id, get_last_post_id
from core.constants import DEFAULT_CURRENT_ID, DEFAULT_LAST_ID
from core.logger import logger
from core.typing import ChannelsDict, SyncSession
from domain.channel import update_count_and_last_id


def update_info(session: SyncSession, channels: ChannelsDict) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")

    for channel_name, channel_info in channels.items():
        current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
        last_post_id = get_last_post_id(session, channel_name)
        update_count_and_last_id(channel_name, channel_info, last_post_id)

        if last_post_id != DEFAULT_LAST_ID and current_id == DEFAULT_CURRENT_ID:
            channel_info["current_id"] = get_first_post_id(session, channel_name)
            current_id = channel_info["current_id"]

        if last_post_id == DEFAULT_LAST_ID:
            continue

        channel_info["current_id"] = (
            max(last_post_id + current_id, DEFAULT_CURRENT_ID)
            if current_id <= 0 else
            min(current_id, last_post_id)
        )
