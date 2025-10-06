from json import dumps, JSONDecodeError, loads

from aiofiles import open as aiopen
from aiohttp import ClientSession
from lxml import html

from core.constants import FURL_TG, XPATH_POST_ID
from core.logger import logger


async def get_last_id(session: ClientSession, channel_name: str) -> int:
    async with session.get(FURL_TG.format(name=channel_name)) as response:
        content = await response.text()
        list_post = html.fromstring(content).xpath(XPATH_POST_ID)
        return int(list_post[-1].split("/")[-1]) if list_post else -1


async def load_channels(path_channels: str = "tg-channels-current.json") -> dict:
    async with aiopen(path_channels, "r", encoding="utf-8") as file:
        try:
            data = await file.read()
            return loads(data)
        except JSONDecodeError:
            return {}


async def save_channels(channels: dict, path_channels: str = "tg-channels-current.json") -> None:
    async with aiopen(path_channels, "w", encoding="utf-8") as file:
        await file.write(dumps(channels, indent=4, sort_keys=True, ensure_ascii=False))
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")
