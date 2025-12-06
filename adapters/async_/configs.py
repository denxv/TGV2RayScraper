from asyncio import (
    gather,
)

from aiofiles import (
    open as aiopen,
)
from lxml import (
    html,
)
from tqdm.asyncio import (
    tqdm,
)

from core.constants.common import (
    BATCH_EXTRACT_DEFAULT,
    BATCH_ID,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    XPATH_TG_MESSAGES_TEXT,
)
from core.constants.formats import (
    FORMAT_PROGRESS_BAR,
)
from core.constants.patterns import (
    PATTERN_V2RAY_PROTOCOLS_URL,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_CONFIGS_FOUND,
    TEMPLATE_CONFIG_EXTRACT_STARTED,
    TEMPLATE_ERROR_FAILED_FETCH_ID,
    TEMPLATE_ERROR_RESPONSE_EMPTY,
    TEMPLATE_FORMAT_TG_URL_AFTER,
)
from core.logger import (
    logger,
)
from core.typing import (
    AsyncHTTPClient,
    BatchSize,
    ChannelInfo,
    ChannelName,
    FileMode,
    FilePath,
    PostID,
    PostIDAndRawLines,
    V2RayRawLines,
)

__all__ = [
    "fetch_channel_configs",
    "write_configs",
]


async def fetch_channel_configs(
    client: AsyncHTTPClient,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    batch_size: BatchSize = BATCH_EXTRACT_DEFAULT,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    list_channel_id = list(
        range(
            channel_info.get(
                "current_id",
                DEFAULT_CURRENT_ID,
            ),
            channel_info.get(
                "last_id",
                DEFAULT_LAST_ID,
            ),
            BATCH_ID,
        ),
    )
    batch_range = range(0, len(list_channel_id), batch_size)

    logger.info(
        msg=TEMPLATE_CONFIG_EXTRACT_STARTED.format(
            name=channel_name,
        ),
    )

    async def fetch_and_parse(
        current_id: PostID,
    ) -> PostIDAndRawLines:
        try:
            response = await client.get(
                url=TEMPLATE_FORMAT_TG_URL_AFTER.format(
                    name=channel_name,
                    id=current_id,
                ),
            )
            response.raise_for_status()

            if not response.text.strip():
                logger.debug(
                    msg=TEMPLATE_ERROR_RESPONSE_EMPTY.format(
                        current_id=current_id,
                        channel_name=channel_name,
                        status=response.status_code,
                    ),
                )
                return current_id, []

            tree = html.fromstring(
                html=response.text,
            )
            messages = tree.xpath(
                XPATH_TG_MESSAGES_TEXT,
            )
        except Exception as e:
            logger.exception(
                msg=TEMPLATE_ERROR_FAILED_FETCH_ID.format(
                    current_id=current_id,
                    channel_name=channel_name,
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                ),
            )
            return current_id, []
        else:
            configs = [
                match.group("url")
                for message in messages
                for match in PATTERN_V2RAY_PROTOCOLS_URL.finditer(
                    string=message,
                )
            ]
            return current_id, configs

    for channel_id in tqdm(
        iterable=batch_range,
        ascii=True,
        leave=False,
        bar_format=FORMAT_PROGRESS_BAR,
    ):
        results = await gather(*(
            fetch_and_parse(
                current_id=_id,
            )
            for _id in list_channel_id[
                channel_id:channel_id + batch_size
            ]
        ))

        for current_id, configs in results:
            channel_info["current_id"] = current_id

            if len(configs) > 0:
                v2ray_count += len(configs)
                channel_info["count"] += len(configs)

                await write_configs(
                    configs=configs,
                    path_configs=path_configs,
                    mode="a",
                )

    channel_info["current_id"] = max(
        channel_info.get(
            "last_id",
            DEFAULT_LAST_ID,
        ),
        DEFAULT_CURRENT_ID,
    )

    logger.info(
        msg=TEMPLATE_CHANNEL_CONFIGS_FOUND.format(
            count=v2ray_count,
        ),
    )


async def write_configs(
    configs: V2RayRawLines,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    async with aiopen(
        file=path_configs,
        mode=mode,
        encoding="utf-8",
    ) as file:
        await file.writelines(
            f"{config}\n"
            for config in configs
        )
