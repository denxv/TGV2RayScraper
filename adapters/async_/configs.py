from asyncio import gather

from aiofiles import open as aiopen
from aiohttp import ClientSession
from lxml import html
from tqdm.asyncio import tqdm

from core.constants import FURL_TG_AFTER, REGEX_V2RAY, XPATH_V2RAY
from core.logger import logger


async def fetch_channel_configs(
    session: ClientSession,
    channel_name: str,
    channel_info: dict,
    batch_size: int = 20,
    path_configs: str = "v2ray-raw.txt",
) -> None:
    v2ray_count = 0
    _const_batch_ID = 20
    list_channel_id = list(range(
        channel_info.get("current_id", 0),
        channel_info.get("last_id", 0),
        _const_batch_ID,
    ))
    batch_range = range(0, len(list_channel_id), batch_size)
    bar_channel_format = " {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} "
    logger.info(f"Extracting configs from channel '{channel_name}'...")

    async def fetch_and_parse(current_id: int) -> int | list:
        async with session.get(FURL_TG_AFTER.format(name=channel_name, id=current_id)) as response:
            content = await response.text()
            html_text = html.fromstring(content)
            if v2ray_configs := list(filter(REGEX_V2RAY.match, html_text.xpath(XPATH_V2RAY))):
                return current_id, v2ray_configs
            return current_id, []

    for channel_id in tqdm(batch_range, ascii=True, bar_format=bar_channel_format, leave=False):
        batch = list_channel_id[channel_id:channel_id + batch_size]
        results = await gather(*(fetch_and_parse(_id) for _id in batch))
        for current_id, configs in results:
            channel_info["current_id"] = current_id
            if len(configs) > 0:
                v2ray_count = v2ray_count + len(configs)
                channel_info["count"] = channel_info.get("count", 0) + len(configs)
                await write_configs(
                    configs,
                    path_configs=path_configs,
                    mode="a",
                )

    channel_info["current_id"] = channel_info.get("last_id", 0)
    logger.info(f"Found: {v2ray_count} configs.")


async def write_configs(configs: list, path_configs: str = "v2ray-raw.txt", mode: str = "w") -> None:
    async with aiopen(path_configs, mode, encoding="utf-8") as file:
        await file.writelines(f"{config}\n" for config in configs)
