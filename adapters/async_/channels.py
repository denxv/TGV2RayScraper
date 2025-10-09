from json import dumps, JSONDecodeError, loads

from aiofiles import open as aiopen
from lxml import html

from core.constants import (
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CHANNELS,
    DEFAULT_INDENT,
    DEFAULT_LAST_ID,
    DEFAULT_POST_ID,
    FURL_TG,
    FURL_TG_AFTER,
    POST_DEFAULT_INDEX,
    POST_FIRST_ID,
    POST_FIRST_INDEX,
    POST_LAST_INDEX,
    XPATH_POST_IDS,
)
from core.typing import (
    AsyncSession,
    ChannelName,
    ChannelsDict,
    DefaultPostID,
    FilePath,
    PostID,
    PostIndex,
    URL,
)
from core.logger import logger


async def _extract_post_id(
    session: AsyncSession,
    url: URL,
    index: PostIndex = POST_DEFAULT_INDEX,
    default: DefaultPostID = DEFAULT_POST_ID,
) -> PostID:
    try:
        async with session.get(url) as response:
            response.raise_for_status()

            content = await response.text()
            tree = html.fromstring(content)
            post_ids = tree.xpath(XPATH_POST_IDS)

            if not post_ids:
                raise ValueError("No posts found.")

            post_url = post_ids[index]
            post_id = post_url.split("/")[-1]
            return int(post_id)

    except Exception as e:
        logger.debug(f"Failed to extract post ID from '{url}': {type(e).__name__}: {e}")
        return default


async def get_first_post_id(session: AsyncSession, channel_name: ChannelName) -> PostID:
    return await _extract_post_id(
        session=session,
        url=FURL_TG_AFTER.format(name=channel_name, id=POST_FIRST_ID),
        index=POST_FIRST_INDEX,
        default=DEFAULT_CURRENT_ID,
    )


async def get_last_post_id(session: AsyncSession, channel_name: ChannelName) -> PostID:
    return await _extract_post_id(
        session=session,
        url=FURL_TG.format(name=channel_name),
        index=POST_LAST_INDEX,
        default=DEFAULT_LAST_ID,
    )


async def load_channels(path_channels: FilePath = DEFAULT_FILE_CHANNELS) -> ChannelsDict:
    async with aiopen(path_channels, "r", encoding="utf-8") as file:
        try:
            data = await file.read()
            return loads(data)
        except JSONDecodeError:
            return {}


async def save_channels(
    channels: ChannelsDict,
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
) -> None:
    async with aiopen(path_channels, "w", encoding="utf-8") as file:
        await file.write(dumps(
            channels,
            indent=DEFAULT_INDENT,
            sort_keys=True,
            ensure_ascii=False,
        ))
        logger.info(f"Saved {len(channels)} channels in '{path_channels}'.")
