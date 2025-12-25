from adapters.sync.channels import (
    get_first_post_id,
    get_last_post_id,
)
from core.constants.common import (
    DEFAULT_CURRENT_ID,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_UPDATE_INFO_STARTED,
)
from core.logger import (
    logger,
)
from core.typing import (
    ChannelsDict,
    SyncHTTPClient,
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


def update_info(
    client: SyncHTTPClient,
    channels: ChannelsDict,
) -> None:
    logger.info(
        msg=TEMPLATE_CHANNEL_UPDATE_INFO_STARTED.format(
            count=len(channels),
        ),
    )

    for channel_name, channel_info in channels.items():
        last_post_id = get_last_post_id(
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
            continue

        normalized_current_id = get_normalized_current_id(
            channel_info=channel_info,
        )

        if normalized_current_id == DEFAULT_CURRENT_ID:
            channel_info["current_id"] = get_first_post_id(
                client=client,
                channel_name=channel_name,
            )

        channel_info["current_id"] = get_normalized_current_id(
            channel_info=channel_info,
        )
