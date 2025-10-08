from asyncio import create_task, gather

from aiohttp import ClientSession

from adapters.async_.channels import get_first_post_id, get_last_post_id
from core.logger import logger
from core.typing import (
    AsyncSession,
    BatchSize,
    ChannelInfo,
    ChannelName,
    ChannelsDict,
)
from domain.channel import update_count_and_last_id


async def update_info(
    session: AsyncSession,
    channels: ChannelsDict,
    batch_size: BatchSize = 100,
) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")

    async def update_channel(channel_name: ChannelName, channel_info: ChannelInfo) -> None:
        current_id = channel_info.get("current_id", 1)
        last_post_id = await get_last_post_id(session, channel_name)
        update_count_and_last_id(channel_name, channel_info, last_post_id)

        if last_post_id != -1 and current_id == 1:
            channel_info["current_id"] = await get_first_post_id(session, channel_name)
            current_id = channel_info["current_id"]

        if last_post_id == -1:
            return

        channel_info["current_id"] = (
            max(1, last_post_id + current_id) if current_id <= 0 else 
            min(current_id, last_post_id)
        )

    channel_names = list(channels.keys())
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            create_task(update_channel(name, channels[name]))
            for name in channel_names[i:i + batch_size]
        ]
        await gather(*tasks)
