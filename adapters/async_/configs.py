from asyncio import gather

from aiofiles import open as aiopen
from lxml import html
from tqdm.asyncio import tqdm

from core.constants import (
    DEFAULT_CHANNEL_BATCH_EXTRACT,
    DEFAULT_CHANNEL_PROGRESS_BAR_FORMAT,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CONFIGS_RAW,
    DEFAULT_LAST_ID,
    FURL_TG_AFTER,
    PATTERN_URL_V2RAY_ALL,
    XPATH_TG_MESSAGES_TEXT,
)
from core.typing import (
    AsyncSession,
    BatchSize,
    ChannelName,
    ChannelInfo,
    FileMode,
    FilePath,
    PostID,
    PostIDAndConfigsRaw,
    V2RayConfigsRaw,
)
from core.logger import logger


async def fetch_channel_configs(
    session: AsyncSession,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    batch_size: BatchSize = DEFAULT_CHANNEL_BATCH_EXTRACT,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
) -> None:
    v2ray_count = 0
    _const_batch_ID = 20
    list_channel_id = list(range(
        channel_info.get("current_id", DEFAULT_CURRENT_ID),
        channel_info.get("last_id", DEFAULT_LAST_ID),
        _const_batch_ID,
    ))
    batch_range = range(0, len(list_channel_id), batch_size)
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    async def fetch_and_parse(current_id: PostID) -> PostIDAndConfigsRaw:
        async with session.get(FURL_TG_AFTER.format(name=channel_name, id=current_id)) as response:
            content = await response.text()
            messages = html.fromstring(content).xpath(XPATH_TG_MESSAGES_TEXT)
            if v2ray_configs := list(filter(PATTERN_URL_V2RAY_ALL.match, messages)):
                return current_id, v2ray_configs
            return current_id, []

    for channel_id in tqdm(
        batch_range,
        ascii=True,
        leave=False,
        bar_format=DEFAULT_CHANNEL_PROGRESS_BAR_FORMAT,
    ):
        batch = list_channel_id[channel_id:channel_id + batch_size]
        results = await gather(*(fetch_and_parse(_id) for _id in batch))
        for current_id, configs in results:
            channel_info["current_id"] = current_id
            if len(configs) > 0:
                v2ray_count = v2ray_count + len(configs)
                channel_info["count"] = channel_info.get("count", DEFAULT_COUNT) + len(configs)
                await write_configs(
                    configs,
                    path_configs=path_configs,
                    mode="a",
                )

    channel_info["current_id"] = max(
        channel_info.get("last_id", DEFAULT_LAST_ID),
        DEFAULT_CURRENT_ID,
    )
    logger.info(f"Found: {v2ray_count} configs.")


async def write_configs(
    configs: V2RayConfigsRaw,
    path_configs: FilePath = DEFAULT_FILE_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    async with aiopen(path_configs, mode, encoding="utf-8") as file:
        await file.writelines(f"{config}\n" for config in configs)
