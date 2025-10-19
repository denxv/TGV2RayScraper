from asyncio import gather

from aiofiles import open as aiopen
from lxml import html
from tqdm.asyncio import tqdm

from core.constants import (
    DEFAULT_CHANNEL_BATCH_EXTRACT,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    FORMAT_CHANNEL_PROGRESS_BAR,
    PATTERN_URL_V2RAY_ALL,
    TEMPLATE_MSG_CONFIGS_FOUND,
    TEMPLATE_MSG_EXTRACTING_CONFIGS,
    TEMPLATE_TG_URL_AFTER,
    XPATH_TG_MESSAGES_TEXT,
)
from core.logger import logger
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


async def fetch_channel_configs(
    client: AsyncHTTPClient,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    batch_size: BatchSize = DEFAULT_CHANNEL_BATCH_EXTRACT,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    batch_id = 20
    list_channel_id = list(range(
        channel_info.get("current_id", DEFAULT_CURRENT_ID),
        channel_info.get("last_id", DEFAULT_LAST_ID),
        batch_id,
    ))

    batch_range = range(0, len(list_channel_id), batch_size)
    logger.info(TEMPLATE_MSG_EXTRACTING_CONFIGS.format(name=channel_name))

    async def fetch_and_parse(current_id: PostID) -> PostIDAndRawLines:
        response = await client.get(TEMPLATE_TG_URL_AFTER.format(
            name=channel_name,
            id=current_id,
        ))

        tree = html.fromstring(response.text)
        messages = tree.xpath(XPATH_TG_MESSAGES_TEXT)

        v2ray_configs = [
            message
            for message in messages
            if PATTERN_URL_V2RAY_ALL.match(message)
        ]

        return current_id, v2ray_configs

    for channel_id in tqdm(
        batch_range,
        ascii=True,
        leave=False,
        bar_format=FORMAT_CHANNEL_PROGRESS_BAR,
    ):
        batch = list_channel_id[channel_id:channel_id + batch_size]
        results = await gather(*(fetch_and_parse(_id) for _id in batch))

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
        channel_info.get("last_id", DEFAULT_LAST_ID),
        DEFAULT_CURRENT_ID,
    )

    logger.info(TEMPLATE_MSG_CONFIGS_FOUND.format(count=v2ray_count))


async def write_configs(
    configs: V2RayRawLines,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    async with aiopen(path_configs, mode, encoding="utf-8") as file:
        await file.writelines(
            f"{config}\n"
            for config in configs
        )
