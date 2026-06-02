from asyncio import (
    as_completed,
    create_task,
)

from adapters.channel import (
    get_first_post_id,
    get_last_post_id,
)
from core.constants.common import (
    DEFAULT_CURRENT_ID,
)
from core.constants.messages.info import (
    MESSAGE_INFO_CHANNEL_UPDATE_SKIPPED,
)
from core.constants.messages.warning import (
    MESSAGE_WARNING_NO_CHANNELS_TO_UPDATE,
)
from core.constants.templates.debug.channel import (
    TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_STARTED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_FIRST_ID_FETCHED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_LAST_ID_FETCHED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_STARTED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_STARTED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_STATE_UPDATED,
    TEMPLATE_DEBUG_CHANNEL_UPDATE_UNAVAILABLE,
)
from core.constants.templates.info.channel import (
    TEMPLATE_INFO_CHANNELS_UPDATE_COMPLETED,
    TEMPLATE_INFO_CHANNELS_UPDATE_STARTED,
)
from core.context import (
    HttpContext,
    RuntimeContext,
)
from core.terminal.console import (
    console,
)
from core.terminal.logger import (
    logger,
)
from core.terminal.renderers import (
    render_channel_update,
)
from core.typing import (
    ChannelInfo,
    ChannelName,
    ChannelsDict,
)
from core.utils import (
    batched,
)
from domain.channel import (
    ChannelUpdateResult,
    get_normalized_current_id,
    update_last_id_and_state,
)
from domain.predicates import (
    is_channel_available,
)

__all__ = [
    "update_info",
]


async def _update_channel(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
) -> ChannelUpdateResult:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_STARTED.format(
            channel_name=channel_name,
        ),
    )

    last_post_id = await get_last_post_id(
        ctx=ctx,
        channel_name=channel_name,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_LAST_ID_FETCHED.format(
            channel_name=channel_name,
            last_post_id=last_post_id,
        ),
    )

    result = update_last_id_and_state(
        channel_name=channel_name,
        channel_info=channel_info,
        last_post_id=last_post_id,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_STATE_UPDATED.format(
            result=result,
        ),
    )

    if not is_channel_available(
        channel_info=channel_info,
    ):
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_UNAVAILABLE.format(
                channel_name=channel_name,
            ),
        )
        return result

    normalized_current_id = get_normalized_current_id(
        channel_info=channel_info,
    )

    if normalized_current_id == DEFAULT_CURRENT_ID:
        first_post_id = await get_first_post_id(
            ctx=ctx,
            channel_name=channel_name,
        )
        channel_info["current_id"] = first_post_id

        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_FIRST_ID_FETCHED.format(
                channel_name=channel_name,
                first_post_id=first_post_id,
            ),
        )

    channel_info["current_id"] = get_normalized_current_id(
        channel_info=channel_info,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_COMPLETED.format(
            result=result,
        ),
    )

    return result


async def update_info(
    ctx: RuntimeContext,
    *,
    channels: ChannelsDict,
    skip_update: bool = False,
) -> None:
    if not (channels_count := len(channels)):
        logger.warning(
            msg=MESSAGE_WARNING_NO_CHANNELS_TO_UPDATE,
        )
        return

    if skip_update:
        logger.info(
            msg=MESSAGE_INFO_CHANNEL_UPDATE_SKIPPED,
        )
        return

    logger.info(
        msg=TEMPLATE_INFO_CHANNELS_UPDATE_STARTED.format(
            count=channels_count,
        ),
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_STARTED.format(
            channels_count=channels_count,
            channels_batch_size=ctx.pipeline.channel_update.batch_size,
        ),
    )

    changed_count = 0

    with render_channel_update(
        console=console,
    ) as add_update:
        for channel_name_batch in batched(
            iterable=channels,
            size=ctx.pipeline.channel_update.batch_size,
        ):
            logger.debug(
                msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_STARTED.format(
                    channels_batch_size=len(channel_name_batch),
                    channels=channel_name_batch,
                ),
            )

            tasks = [
                create_task(
                    _update_channel(
                        ctx=ctx.http,
                        channel_name=name,
                        channel_info=channels[name],
                    ),
                )
                for name in channel_name_batch
            ]

            batch_changed = 0

            for task in as_completed(tasks):
                result = await task
                batch_changed += add_update(result)

            changed_count += batch_changed

            logger.debug(
                msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_COMPLETED.format(
                    channels_batch_size=len(channel_name_batch),
                    changed_channels_in_batch=batch_changed,
                ),
            )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_COMPLETED.format(
            channels_count=channels_count,
            changed_channels_count=changed_count,
        ),
    )

    logger.info(
        msg=TEMPLATE_INFO_CHANNELS_UPDATE_COMPLETED.format(
            checked=channels_count,
            changed=changed_count,
        ),
    )
