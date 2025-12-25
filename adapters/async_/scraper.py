from asyncio import (
    as_completed,
    create_task,
)

from adapters.async_.channels import (
    get_first_post_id,
    get_last_post_id,
)
from core.constants.common import (
    BATCH_UPDATE_DEFAULT,
    DEFAULT_CURRENT_ID,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_UPDATE_INFO_STARTED,
)
from core.logger import (
    logger,
)
from core.typing import (
    AsyncHTTPClient,
    BatchSize,
    ChannelInfo,
    ChannelName,
    ChannelsDict,
)
from domain.channel import (
    get_normalized_current_id,
    update_last_id_and_state,
)
from domain.predicates import (
    is_channel_available,
)

__all__ = [
    "update_info",
]


async def update_info(
    client: AsyncHTTPClient,
    channels: ChannelsDict,
    batch_size: BatchSize = BATCH_UPDATE_DEFAULT,
) -> None:
    logger.info(
        msg=TEMPLATE_CHANNEL_UPDATE_INFO_STARTED.format(
            count=len(channels),
        ),
    )

    async def update_channel(
        channel_name: ChannelName,
        channel_info: ChannelInfo,
    ) -> None:
        last_post_id = await get_last_post_id(
            client=client,
            channel_name=channel_name,
        )

        update_last_id_and_state(
            channel_name=channel_name,
            channel_info=channel_info,
            last_post_id=last_post_id,
        )

        if not is_channel_available(
            channel_info=channel_info,
        ):
            return

        normalized_current_id = get_normalized_current_id(
            channel_info=channel_info,
        )

        if normalized_current_id == DEFAULT_CURRENT_ID:
            channel_info["current_id"] = await get_first_post_id(
                client=client,
                channel_name=channel_name,
            )

        channel_info["current_id"] = get_normalized_current_id(
            channel_info=channel_info,
        )

    channel_names = list(channels)
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            create_task(
                update_channel(
                    channel_name=name,
                    channel_info=channels[name],
                ),
            )
            for name in channel_names[i:i + batch_size]
        ]

        for task in as_completed(tasks):
            await task
