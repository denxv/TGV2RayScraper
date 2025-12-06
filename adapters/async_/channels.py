from json import (
    JSONDecodeError,
    dumps,
    loads,
)

from aiofiles import (
    open as aiopen,
)
from lxml import (
    html,
)

from core.constants.common import (
    DEFAULT_CURRENT_ID,
    DEFAULT_FILE_CHANNELS,
    DEFAULT_JSON_INDENT,
    DEFAULT_LAST_ID,
    POST_DEFAULT_ID,
    POST_DEFAULT_INDEX,
    POST_FIRST_ID,
    POST_FIRST_INDEX,
    POST_LAST_INDEX,
    XPATH_POST_IDS,
)
from core.constants.messages import (
    MESSAGE_ERROR_NO_POSTS_FOUND,
)
from core.constants.templates import (
    TEMPLATE_CHANNEL_SAVE_COMPLETED,
    TEMPLATE_ERROR_FAILED_EXTRACT_POST_ID,
    TEMPLATE_FORMAT_TG_URL,
    TEMPLATE_FORMAT_TG_URL_AFTER,
)
from core.logger import (
    logger,
)
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
from domain.channel import (
    normalize_channel_names,
)

__all__ = [
    "get_first_post_id",
    "get_last_post_id",
    "load_channels",
    "save_channels",
]


async def _extract_post_id(
    client: AsyncHTTPClient,
    url: URL,
    index: PostIndex = POST_DEFAULT_INDEX,
    default: DefaultPostID = POST_DEFAULT_ID,
) -> PostID:
    try:
        response = await client.get(
            url=url,
        )
        response.raise_for_status()

        tree = html.fromstring(
            html=response.text,
        )
        post_ids = tree.xpath(
            XPATH_POST_IDS,
        )

        if not post_ids:
            raise ValueError(  # noqa: TRY301
                MESSAGE_ERROR_NO_POSTS_FOUND,
            )

        post_url = post_ids[index]
        post_id = post_url.split("/")[-1]

    except Exception as e:
        logger.debug(
            msg=TEMPLATE_ERROR_FAILED_EXTRACT_POST_ID.format(
                url=url,
                exc_type=type(e).__name__,
                exc_msg=str(e),
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
        url=TEMPLATE_FORMAT_TG_URL_AFTER.format(
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
        url=TEMPLATE_FORMAT_TG_URL.format(
            name=channel_name,
        ),
        index=POST_LAST_INDEX,
        default=DEFAULT_LAST_ID,
    )


async def load_channels(
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
) -> ChannelsDict:
    async with aiopen(
        file=path_channels,
        encoding="utf-8",
    ) as file:
        try:
            channels_json_str = await file.read()
            return normalize_channel_names(
                channels=loads(
                    s=channels_json_str,
                ),
            )
        except JSONDecodeError:
            return {}


async def save_channels(
    channels: ChannelsDict,
    path_channels: FilePath = DEFAULT_FILE_CHANNELS,
) -> None:
    normalized_channels = normalize_channel_names(
        channels=channels,
    )

    async with aiopen(
        file=path_channels,
        mode="w",
        encoding="utf-8",
    ) as file:
        await file.write(
            dumps(
                obj=normalized_channels,
                ensure_ascii=False,
                indent=DEFAULT_JSON_INDENT,
                sort_keys=True,
            ),
        )

    logger.info(
        msg=TEMPLATE_CHANNEL_SAVE_COMPLETED.format(
            count=len(normalized_channels),
            path=path_channels,
        ),
    )
