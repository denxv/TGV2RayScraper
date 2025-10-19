from asyncio import create_task, gather

from adapters.async_.channels import (
    get_first_post_id,
    get_last_post_id,
)
from core.constants import (
    DEFAULT_CHANNEL_BATCH_UPDATE,
    DEFAULT_CURRENT_ID,
    DEFAULT_LAST_ID,
    TEMPLATE_MSG_UPDATING_CHANNEL_INFO,
)
from core.logger import logger
from core.typing import (
    AsyncHTTPClient,
    BatchSize,
    ChannelInfo,
    ChannelName,
    ChannelsDict,
)
from domain.channel import update_count_and_last_id


async def update_info(
    client: AsyncHTTPClient,
    channels: ChannelsDict,
    batch_size: BatchSize = DEFAULT_CHANNEL_BATCH_UPDATE,
) -> None:
    logger.info(TEMPLATE_MSG_UPDATING_CHANNEL_INFO.format(
        count=len(channels),
    ))

    async def update_channel(
        channel_name: ChannelName,
        channel_info: ChannelInfo,
    ) -> None:
        current_id = channel_info.get("current_id", DEFAULT_CURRENT_ID)
        last_post_id = await get_last_post_id(
            client=client,
            channel_name=channel_name,
        )

        update_count_and_last_id(
            channel_name=channel_name,
            channel_info=channel_info,
            last_post_id=last_post_id,
        )

        if last_post_id == DEFAULT_LAST_ID:
            return

        if current_id <= 0:
            channel_info["current_id"] = max(
                last_post_id + current_id,
                DEFAULT_CURRENT_ID,
            )
            current_id = channel_info["current_id"]

        if current_id == DEFAULT_CURRENT_ID:
            channel_info["current_id"] = await get_first_post_id(
                client=client,
                channel_name=channel_name,
            )
            current_id = channel_info["current_id"]

        if current_id > last_post_id:
            channel_info["current_id"] = last_post_id

    channel_names = list(channels.keys())
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            create_task(update_channel(name, channels[name]))
            for name in channel_names[i:i + batch_size]
        ]

        await gather(*tasks)
