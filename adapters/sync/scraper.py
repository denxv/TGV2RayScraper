from adapters.sync.channels import get_first_post_id, get_last_post_id
from core.logger import logger
from core.typing import ChannelsDict, SyncSession
from domain.channel import update_count_and_last_id


def update_info(session: SyncSession, channels: ChannelsDict) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")

    for channel_name, channel_info in channels.items():
        current_id = channel_info.get("current_id", 1)
        last_post_id = get_last_post_id(session, channel_name)
        update_count_and_last_id(channel_name, channel_info, last_post_id)

        if last_post_id != -1 and current_id == 1:
            channel_info["current_id"] = get_first_post_id(session, channel_name)
            current_id = channel_info["current_id"]

        if last_post_id == -1:
            continue

        channel_info["current_id"] = (
            max(1, last_post_id + current_id) if current_id <= 0 else 
            min(current_id, last_post_id)
        )
