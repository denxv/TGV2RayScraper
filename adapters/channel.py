from asyncio import (
    sleep,
)
from json import (
    JSONDecodeError,
    dumps,
    loads,
)

from aiofiles import (
    open as aiopen,
)
from httpx import (
    HTTPStatusError,
    RequestError,
    Response,
)
from lxml import (
    html,
)

from core.constants.common import (
    DEFAULT_CURRENT_ID,
    DEFAULT_JSON_INDENT,
    DEFAULT_LAST_ID,
    HTTP_RETRIES_MIN,
    HTTP_RETRY_DELAY_MAX,
    POST_DEFAULT_ID,
    POST_DEFAULT_INDEX,
    POST_FIRST_ID,
    POST_FIRST_INDEX,
    POST_LAST_INDEX,
    XPATH_POST_IDS,
)
from core.constants.formats import (
    FORMAT_TG_CHANNEL_URL,
    FORMAT_TG_CHANNEL_URL_WITH_AFTER,
)
from core.constants.messages.error import (
    MESSAGE_ERROR_NO_POSTS_FOUND,
)
from core.constants.messages.info import (
    MESSAGE_INFO_BACKUP_SKIPPED,
    MESSAGE_INFO_CHANNEL_LOAD_COMPLETED,
    MESSAGE_INFO_CHANNEL_LOAD_STARTED,
    MESSAGE_INFO_CHANNEL_SAVE_COMPLETED,
    MESSAGE_INFO_CHANNEL_SAVE_STARTED,
)
from core.constants.patterns.telegram import (
    PATTERN_TG_CHANNEL_NAME,
)
from core.constants.templates.debug.channel import (
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FAILED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FETCHED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_EXTRACTED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_STARTED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_EXTRACTED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_STARTED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_STARTED,
    TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_SUCCESS,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_COMBINED_COMPLETED,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_NORMALIZED,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSE_FAILED,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSED,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_STARTED,
    TEMPLATE_DEBUG_CHANNEL_IO_LOAD_URLS_PARSED,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_BACKUP_CREATED,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_NORMALIZED,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_SERIALIZED,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_STARTED,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_URLS_WRITTEN,
    TEMPLATE_DEBUG_CHANNEL_IO_SAVE_WRITTEN,
)
from core.constants.templates.debug.common import (
    TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_FAILED,
    TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_STARTED,
    TEMPLATE_DEBUG_HTTP_FETCH_SUCCESS,
    TEMPLATE_DEBUG_HTTP_FETCH_WITH_RETRY_STARTED,
)
from core.constants.templates.error import (
    TEMPLATE_ERROR_HTTP_FETCH_FAILED_AFTER_RETRIES,
    TEMPLATE_ERROR_HTTP_FETCH_RETRY_EXHAUSTED,
    TEMPLATE_ERROR_HTTP_FETCH_RETRY_LOOP_BROKEN,
)
from core.constants.templates.info.channel import (
    TEMPLATE_INFO_CHANNEL_SAVE_COMPLETED,
)
from core.context import (
    HttpContext,
    IOContext,
)
from core.decorators import (
    status,
)
from core.terminal.logger import (
    logger,
)
from core.typing import (
    URL,
    ChannelName,
    ChannelsAndNames,
    ChannelsDict,
    DefaultPostID,
    PostID,
    PostIndex,
)
from core.utils import (
    make_backup,
)
from domain.channel import (
    normalize_channel_names,
)

__all__ = [
    "fetch_with_retry",
    "get_first_post_id",
    "get_last_post_id",
    "load_channels",
    "load_channels_and_urls",
    "save_channels",
    "save_channels_and_urls",
]


async def _extract_post_id(
    ctx: HttpContext,
    *,
    url: URL,
    default: DefaultPostID = POST_DEFAULT_ID,
    index: PostIndex = POST_DEFAULT_INDEX,
) -> PostID:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_STARTED.format(
            url=url,
        ),
    )

    try:
        response = await fetch_with_retry(
            ctx=ctx,
            url=url,
        )

        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FETCHED.format(
                url=url,
                status_code=response.status_code,
                html_length=len(response.text),
            ),
        )

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
            msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FAILED.format(
                url=url,
                default=default,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
        return default
    else:
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_SUCCESS.format(
                url=url,
                index=index,
                post_url=post_url,
                post_id=int(post_id),
            ),
        )
        return int(post_id)


async def fetch_with_retry(
    ctx: HttpContext,
    *,
    url: URL,
) -> Response:
    retries = max(ctx.retries, HTTP_RETRIES_MIN)

    logger.debug(
        msg=TEMPLATE_DEBUG_HTTP_FETCH_WITH_RETRY_STARTED.format(
            retries=retries,
            url=url,
        ),
    )

    for retry_attempt in range(1, retries + 1):
        response: Response | None = None

        try:
            logger.debug(
                msg=TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_STARTED.format(
                    attempt=retry_attempt,
                    retries=retries,
                    url=url,
                ),
            )

            response = await ctx.client.get(
                url=url,
            )
            response.raise_for_status()
        except (
            HTTPStatusError,
            RequestError,
        ) as e:
            retry_delay = min(
                ctx.retry_delay * retry_attempt,
                HTTP_RETRY_DELAY_MAX,
            )

            if retry_attempt < retries:
                logger.debug(
                    msg=TEMPLATE_DEBUG_HTTP_FETCH_ATTEMPT_FAILED.format(
                        attempt=retry_attempt,
                        retries=retries,
                        retry_delay=retry_delay,
                        status_code=response and response.status_code,
                        url=url,
                        exc_type=type(e).__name__,
                        exc_msg=str(e),
                    ),
                )
            else:
                logger.error(
                    msg=TEMPLATE_ERROR_HTTP_FETCH_FAILED_AFTER_RETRIES.format(
                        url=url,
                        retries=retries,
                    ),
                )
                raise RuntimeError(
                    TEMPLATE_ERROR_HTTP_FETCH_RETRY_EXHAUSTED.format(
                        retries=retries,
                        url=url,
                    ),
                ) from e

            await sleep(
                delay=retry_delay,
            )
        else:
            logger.debug(
                msg=TEMPLATE_DEBUG_HTTP_FETCH_SUCCESS.format(
                    status_code=response.status_code,
                    url=url,
                ),
            )
            return response

    raise RuntimeError(
        TEMPLATE_ERROR_HTTP_FETCH_RETRY_LOOP_BROKEN.format(
            url=url,
        ),
    )


async def get_first_post_id(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
) -> PostID:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_STARTED.format(
            channel_name=channel_name,
        ),
    )

    post_id = await _extract_post_id(
        ctx=ctx,
        url=FORMAT_TG_CHANNEL_URL_WITH_AFTER.format(
            name=channel_name,
            id=POST_FIRST_ID,
        ),
        default=DEFAULT_CURRENT_ID,
        index=POST_FIRST_INDEX,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_EXTRACTED.format(
            channel_name=channel_name,
            post_id=post_id,
            default=DEFAULT_CURRENT_ID,
        ),
    )

    return post_id


async def get_last_post_id(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
) -> PostID:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_STARTED.format(
            channel_name=channel_name,
        ),
    )

    post_id = await _extract_post_id(
        ctx=ctx,
        url=FORMAT_TG_CHANNEL_URL.format(
            name=channel_name,
        ),
        default=DEFAULT_LAST_ID,
        index=POST_LAST_INDEX,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_EXTRACTED.format(
            channel_name=channel_name,
            post_id=post_id,
            default=DEFAULT_LAST_ID,
        ),
    )

    return post_id


async def load_channels(
    ctx: IOContext,
) -> ChannelsDict:
    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_STARTED.format(
            channels_path=ctx.channels_path,
        ),
    )

    try:
        async with aiopen(
            file=ctx.channels_path,
            encoding="utf-8",
        ) as file:
            channels_json_str = await file.read()

        loaded_channels = loads(
            s=channels_json_str,
        )
        loaded_channels_count = len(loaded_channels)

        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSED.format(
                parsed_channels_count=loaded_channels_count,
                channels_path=ctx.channels_path,
            ),
        )

        normalized_channels = normalize_channel_names(
            channels=loaded_channels,
        )
    except JSONDecodeError as e:
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSE_FAILED.format(
                channels_path=ctx.channels_path,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
        return {}
    else:
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_NORMALIZED.format(
                parsed_channels_count=loaded_channels_count,
                normalized_channels_count=len(normalized_channels),
                channels_path=ctx.channels_path,
            ),
        )
        return normalized_channels


@status(
    start=MESSAGE_INFO_CHANNEL_LOAD_STARTED,
    end=MESSAGE_INFO_CHANNEL_LOAD_COMPLETED,
    tracking=False,
)
async def load_channels_and_urls(  # type: ignore[misc]
    ctx: IOContext,
) -> ChannelsAndNames:
    loaded_channels = await load_channels(
        ctx=ctx,
    )

    async with aiopen(
        file=ctx.urls_path,
        encoding="utf-8",
    ) as file:
        urls_str = await file.read()

    channel_names = [
        name.lower()
        for name in PATTERN_TG_CHANNEL_NAME.findall(
            string=urls_str,
        )
    ]
    channel_names_count = len(channel_names)

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_URLS_PARSED.format(
            parsed_names_count=channel_names_count,
            urls_path=ctx.urls_path,
        ),
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_LOAD_COMBINED_COMPLETED.format(
            channels_count=len(loaded_channels),
            names_count=channel_names_count,
        ),
    )

    return (
        loaded_channels,
        channel_names,
    )


async def save_channels(
    ctx: IOContext,
    *,
    channels: ChannelsDict,
    indent: int = DEFAULT_JSON_INDENT,
) -> None:
    channels_count = len(channels)

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_STARTED.format(
            channels_count=channels_count,
            channels_path=ctx.channels_path,
        ),
    )

    normalized_channels = normalize_channel_names(
        channels=channels,
    )
    normalized_channels_count = len(normalized_channels)

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_NORMALIZED.format(
            channels_count=channels_count,
            normalized_channels_count=normalized_channels_count,
            channels_path=ctx.channels_path,
        ),
    )

    serialized = dumps(
        obj=normalized_channels,
        ensure_ascii=False,
        indent=indent,
        sort_keys=True,
    )
    json_bytes_length = len(serialized.encode("utf-8"))

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_SERIALIZED.format(
            json_bytes_length=json_bytes_length,
            json_indent=indent,
            channels_path=ctx.channels_path,
        ),
    )

    async with aiopen(
        file=ctx.channels_path,
        mode="w",
        encoding="utf-8",
    ) as file:
        await file.write(serialized)

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_WRITTEN.format(
            json_bytes_length=json_bytes_length,
            channels_path=ctx.channels_path,
        ),
    )

    logger.info(
        msg=TEMPLATE_INFO_CHANNEL_SAVE_COMPLETED.format(
            count=normalized_channels_count,
            path=ctx.channels_path,
        ),
    )


@status(
    start=MESSAGE_INFO_CHANNEL_SAVE_STARTED,
    end=MESSAGE_INFO_CHANNEL_SAVE_COMPLETED,
    tracking=False,
)
async def save_channels_and_urls(  # type: ignore[misc]
    ctx: IOContext,
    *,
    channels: ChannelsDict,
    indent: int = DEFAULT_JSON_INDENT,
    skip_backup: bool = False,
) -> None:
    if skip_backup:
        logger.info(
            msg=MESSAGE_INFO_BACKUP_SKIPPED,
        )
    else:
        files_to_backup = [
            ctx.channels_path,
            ctx.urls_path,
        ]
        make_backup(
            files=files_to_backup,
        )
        logger.debug(
            msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_BACKUP_CREATED.format(
                files_count=len(files_to_backup),
                files_to_backup=files_to_backup,
            ),
        )

    normalized_channels = normalize_channel_names(
        channels=channels,
    )

    urls_list = [
        FORMAT_TG_CHANNEL_URL.format(
            name=name,
        )
        for name in sorted(normalized_channels)
    ]

    async with aiopen(
        file=ctx.urls_path,
        mode="w",
        encoding="utf-8",
    ) as file:
        await file.writelines(
            f"{url}\n"
            for url in urls_list
        )

    logger.debug(
        msg=TEMPLATE_DEBUG_CHANNEL_IO_SAVE_URLS_WRITTEN.format(
            urls_count=len(urls_list),
            urls_path=ctx.urls_path,
        ),
    )

    await save_channels(
        ctx=ctx,
        channels=normalized_channels,
        indent=indent,
    )
