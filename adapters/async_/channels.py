from json import dumps, JSONDecodeError, loads

from aiofiles import open as aiopen
from aiohttp import ClientSession
from lxml import html

from core.constants import FURL_TG, FURL_TG_AFTER, XPATH_POST_ID
from core.logger import logger


async def _extract_post_id(session: ClientSession, url: str, index: int = 0, default: int = 0) -> int:
    try:
        async with session.get(url) as response:
            response.raise_for_status()

            content = await response.text()
            tree = html.fromstring(content)
            post_ids = tree.xpath(XPATH_POST_ID)

            if not post_ids:
                raise ValueError("No posts found.")

            post_url = post_ids[index]
            post_id = post_url.split("/")[-1]
            return int(post_id)

    except Exception as e:
        logger.debug(f"Failed to extract post ID from '{url}': {type(e).__name__}: {e}")
        return default


async def get_first_post_id(session: ClientSession, channel_name: str) -> int:
    url = FURL_TG_AFTER.format(name=channel_name, id=1)
    return await _extract_post_id(session, url, index=0, default=1)


async def get_last_post_id(session: ClientSession, channel_name: str) -> int:
    url = FURL_TG.format(name=channel_name)
    return await _extract_post_id(session, url, index=-1, default=-1)


async def load_channels(path_channels: str = "current.json") -> dict:
    async with aiopen(path_channels, "r", encoding="utf-8") as file:
        try:
            data = await file.read()
            return loads(data)
        except JSONDecodeError:
            return {}


async def save_channels(channels: dict, path_channels: str = "current.json") -> None:
    async with aiopen(path_channels, "w", encoding="utf-8") as file:
        await file.write(dumps(channels, indent=4, sort_keys=True, ensure_ascii=False))
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")
