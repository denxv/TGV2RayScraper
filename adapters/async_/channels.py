from json import JSONDecodeError, dumps, loads

from aiofiles import open as aiopen
from lxml import html

from core.constants import (
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CHANNELS,
    DEFAULT_INDENT,
    DEFAULT_LAST_ID,
    DEFAULT_POST_ID,
    MESSAGE_NO_POSTS_FOUND,
    POST_DEFAULT_INDEX,
    POST_FIRST_ID,
    POST_FIRST_INDEX,
    POST_LAST_INDEX,
    TEMPLATE_MSG_ERROR_POST_ID,
    TEMPLATE_MSG_SAVE_CHANNELS,
    TEMPLATE_TG_URL,
    TEMPLATE_TG_URL_AFTER,
    XPATH_POST_IDS,
)
from core.logger import logger
from core.typing import (
    URL,
    AsyncHTTPClient,
    ChannelName,
    ChannelsDict,
    DefaultPostID,
    FilePath,
    PostID,
    PostIndex,
)


async def _extract_post_id(
    client: AsyncHTTPClient,
    url: URL,
    index: PostIndex = POST_DEFAULT_INDEX,
    default: DefaultPostID = DEFAULT_POST_ID,
) -> PostID:
    try:
        response = await client.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.text)
        post_ids = tree.xpath(XPATH_POST_IDS)

        if not post_ids:
            raise ValueError(MESSAGE_NO_POSTS_FOUND)  # noqa: TRY301

        post_url = post_ids[index]
        post_id = post_url.split("/")[-1]

    except Exception as e:
        logger.debug(
            TEMPLATE_MSG_ERROR_POST_ID.format(
                url=url,
                exc_type=type(e).__name__,
                exc_msg=e,
            ),
        )
        return default
    else:
        return int(post_id)


async def get_first_post_id(
    client: AsyncHTTPClient,
    channel_name: ChannelName,
) -> PostID:
    return await _extract_post_id(
        client=client,
        url=TEMPLATE_TG_URL_AFTER.format(
            name=channel_name,
            id=POST_FIRST_ID,
        ),
        index=POST_FIRST_INDEX,
        default=DEFAULT_CURRENT_ID,
    )


async def get_last_post_id(
    client: AsyncHTTPClient,
    channel_name: ChannelName,
) -> PostID:
    return await _extract_post_id(
        client=client,
        url=TEMPLATE_TG_URL.format(
            name=channel_name,
        ),
        index=POST_LAST_INDEX,
        default=DEFAULT_LAST_ID,
    )


async def load_channels(
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
) -> ChannelsDict:
    async with aiopen(path_channels, encoding="utf-8") as file:
        try:
            data = await file.read()
            channels: ChannelsDict = loads(data)
        except JSONDecodeError:
            return {}
        else:
            return channels


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

    logger.info(TEMPLATE_MSG_SAVE_CHANNELS.format(
        count=len(channels),
        path=path_channels,
    ))
