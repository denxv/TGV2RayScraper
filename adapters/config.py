from asyncio import (
    gather,
)
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
from rich.progress import (
    Progress,
    TaskID,
)

from adapters.channel import (
    fetch_with_retry,
)
from core.constants.common import (
    CONFIGS_BATCH_DEFAULT,
    DEFAULT_COUNT,
    DEFAULT_CURRENT_ID,
    DEFAULT_JSON_INDENT,
    DEFAULT_LAST_ID,
    DEFAULT_PATH_CONFIGS_EXPORT,
    DEFAULT_PATH_CONFIGS_IMPORT,
    DEFAULT_PATH_CONFIGS_RAW,
    TELEGRAM_POST_PAGE_SIZE,
    XPATH_TG_MESSAGES_TEXT,
)
from core.constants.formats import (
    FORMAT_TG_CHANNEL_URL_WITH_AFTER,
)
from core.constants.messages.info import (
    MESSAGE_INFO_CONFIG_NORMALIZATION_SKIPPED,
)
from core.constants.messages.warning import (
    MESSAGE_WARNING_NO_CHANNELS_TO_EXTRACT,
)
from core.constants.patterns.v2ray.detector import (
    PATTERN_V2RAY_URL_DETECTOR,
)
from core.constants.templates.common import (
    TEMPLATE_PROGRESS_DESCRIPTION,
)
from core.constants.templates.debug.config import (
    TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_COMPLETED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_STARTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_COMPLETED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_EXTRACTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_FILTERED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_RENDERED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_STARTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_EMPTY,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_FETCHED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_REGEX_DONE,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_STARTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_XPATH_DONE,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_COMPLETED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_STARTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_COMPLETED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_STARTED,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_RESULT,
    TEMPLATE_DEBUG_CONFIG_EXTRACT_STARTED,
    TEMPLATE_DEBUG_CONFIG_IO_EXPORT_SERIALIZED,
    TEMPLATE_DEBUG_CONFIG_IO_EXPORT_WRITTEN,
    TEMPLATE_DEBUG_CONFIG_IO_IMPORT_READ,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_EMPTY,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_NORMALIZED_EMPTY,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_SUCCESS,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_NORMALIZED,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_PARSED,
    TEMPLATE_DEBUG_CONFIG_IO_LOAD_STARTED,
    TEMPLATE_DEBUG_CONFIG_IO_SAVE_EXPORT,
    TEMPLATE_DEBUG_CONFIG_IO_WRITE_COMPLETED,
    TEMPLATE_DEBUG_CONFIG_IO_WRITE_STARTED,
)
from core.constants.templates.error import (
    TEMPLATE_ERROR_CONFIG_IMPORT_FAILED,
    TEMPLATE_ERROR_FAILED_FETCH_ID,
)
from core.constants.templates.info.config import (
    TEMPLATE_INFO_CONFIG_EXPORT_COMPLETED,
    TEMPLATE_INFO_CONFIG_EXPORT_STARTED,
    TEMPLATE_INFO_CONFIG_EXTRACT_COMPLETED,
    TEMPLATE_INFO_CONFIG_EXTRACT_STARTED,
    TEMPLATE_INFO_CONFIG_IMPORT_COMPLETED,
    TEMPLATE_INFO_CONFIG_IMPORT_STARTED,
    TEMPLATE_INFO_CONFIG_LOAD_COMPLETED,
    TEMPLATE_INFO_CONFIG_LOAD_STARTED,
    TEMPLATE_INFO_CONFIG_SAVE_COMPLETED,
    TEMPLATE_INFO_CONFIG_SAVE_STARTED,
)
from core.context import (
    HttpContext,
    IOContext,
    RuntimeContext,
)
from core.terminal.console import (
    console,
)
from core.terminal.logger import (
    logger,
)
from core.terminal.progress import (
    create_extract_progress,
    progress_add_task,
    progress_remove_task,
    progress_update_task,
)
from core.terminal.renderers import (
    render_config_extract,
)
from core.typing import (
    BatchSize,
    ChannelInfo,
    ChannelName,
    ChannelNames,
    ChannelsDict,
    FileMode,
    FilePath,
    PostID,
    PostIDAndRawLines,
    V2RayConfigs,
    V2RayConfigsRaw,
    V2RayRawLines,
)
from core.utils import (
    batched,
    get_batches_count,
)
from domain.channel import (
    get_sorted_keys,
)
from domain.config import (
    ConfigExtractionResult,
    line_to_configs,
    normalize_configs,
)

__all__ = [
    "export_configs",
    "fetch_and_write_configs",
    "import_configs",
    "load_configs",
    "save_configs",
    "write_configs",
]


def _apply_normalization(
    *,
    configs: V2RayConfigs | V2RayConfigsRaw,
    skip_normalize: bool = False,
) -> V2RayConfigs | V2RayConfigsRaw:
    if skip_normalize:
        logger.info(
            msg=MESSAGE_INFO_CONFIG_NORMALIZATION_SKIPPED,
        )
        return configs

    return normalize_configs(
        configs=configs,  # type: ignore[arg-type]
    )


async def _fetch_and_parse_configs(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
    current_id: PostID,
) -> PostIDAndRawLines:
    url = FORMAT_TG_CHANNEL_URL_WITH_AFTER.format(
        name=channel_name,
        id=current_id,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_STARTED.format(
            channel_name=channel_name,
            current_id=current_id,
            url=url,
        ),
    )

    try:
        response = await fetch_with_retry(
            ctx=ctx,
            url=url,
        )

        logger.debug(
            msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_FETCHED.format(
                channel_name=channel_name,
                current_id=current_id,
                status_code=response.status_code,
                html_length=len(response.text),
            ),
        )

        if not response.text.strip():
            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_EMPTY.format(
                    channel_name=channel_name,
                    current_id=current_id,
                    status_code=response.status_code,
                ),
            )
            return current_id, []

        tree = html.fromstring(
            html=response.text,
        )
        messages = tree.xpath(
            XPATH_TG_MESSAGES_TEXT,
        )

        logger.debug(
            msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_XPATH_DONE.format(
                channel_name=channel_name,
                messages_count=len(messages),
            ),
        )
    except Exception as e:
        logger.error(
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
            for match in PATTERN_V2RAY_URL_DETECTOR.finditer(
                string=message,
            )
        ]
        logger.debug(
            msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_REGEX_DONE.format(
                channel_name=channel_name,
                configs_count=len(configs),
            ),
        )
        return current_id, configs


async def _process_channel_configs(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    progress: Progress,
    overall_task: TaskID,
    batch_size: BatchSize = CONFIGS_BATCH_DEFAULT,
    configs_path: FilePath = DEFAULT_PATH_CONFIGS_RAW,
) -> ConfigExtractionResult:
    configs_count = 0

    channel_ids = range(
        channel_info.get(
            "current_id",
            DEFAULT_CURRENT_ID,
        ),
        channel_info.get(
            "last_id",
            DEFAULT_LAST_ID,
        ),
        TELEGRAM_POST_PAGE_SIZE,
    )
    batches_count = get_batches_count(
        items=channel_ids,
        size=batch_size,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_STARTED.format(
            channel_name=channel_name,
            total_ids=len(channel_ids),
            ids_per_batch=batch_size,
            total_batches=batches_count,
        ),
    )

    task_id: TaskID = progress_add_task(
        progress=progress,
        description=TEMPLATE_PROGRESS_DESCRIPTION.format(
            name=channel_name,
            found=configs_count,
        ),
        total=batches_count,
    )

    for channel_id_batch in batched(
        iterable=channel_ids,
        size=batch_size,
    ):
        configs_count += await _process_channel_configs_batch(
            ctx=ctx,
            channel_name=channel_name,
            channel_info=channel_info,
            channel_ids=channel_id_batch,
            configs_path=configs_path,
        )

        progress_update_task(
            progress=progress,
            task_id=task_id,
            advance=1.0,
            description=TEMPLATE_PROGRESS_DESCRIPTION.format(
                name=channel_name,
                found=configs_count,
            ),
        )

    await progress_remove_task(
        progress=progress,
        task_id=task_id,
        advance=1.0,
        overall_task=overall_task,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_COMPLETED.format(
            channel_name=channel_name,
            batches_processed=batches_count,
            total_collected=configs_count,
        ),
    )

    channel_info["current_id"] = max(
        channel_info.get(
            "last_id",
            DEFAULT_LAST_ID,
        ),
        DEFAULT_CURRENT_ID,
    )

    result = ConfigExtractionResult(
        channel_name=channel_name,
        total_found=channel_info.get(
            "count",
            DEFAULT_COUNT,
        ),
        new_found=configs_count,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_RESULT.format(
            result=result,
        ),
    )

    return result


async def _process_channel_configs_batch(
    ctx: HttpContext,
    *,
    channel_name: ChannelName,
    channel_info: ChannelInfo,
    channel_ids: tuple[int, ...],
    configs_path: FilePath = DEFAULT_PATH_CONFIGS_RAW,
) -> int:
    configs_count = 0
    collected_configs: V2RayRawLines = []

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_STARTED.format(
            channel_name=channel_name,
            ids_count=len(channel_ids),
        ),
    )

    results = await gather(*(
        _fetch_and_parse_configs(
            ctx=ctx,
            channel_name=channel_name,
            current_id=current_id,
        )
        for current_id in channel_ids
    ))

    for current_id, configs in results:
        channel_info["current_id"] = current_id

        if not configs:
            continue

        count = len(configs)
        configs_count += count
        channel_info["count"] += count

        collected_configs.extend(configs)

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_COMPLETED.format(
            channel_name=channel_name,
            total_collected=len(collected_configs),
            configs_path=configs_path,
        ),
    )

    if collected_configs:
        await write_configs(
            configs=collected_configs,
            configs_path=configs_path,
            mode="a",
        )

    return configs_count


async def _run_channel_extraction(
    ctx: RuntimeContext,
    *,
    channel_names: ChannelNames,
    channels: ChannelsDict,
) -> list[ConfigExtractionResult]:
    channel_extract_results: list[ConfigExtractionResult] = []

    ids_per_batch = ctx.pipeline.config_extraction.batch_size
    max_concurrent = ctx.pipeline.config_extraction.max_concurrent_channels

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_STARTED.format(
            channels_count=len(channel_names),
            max_concurrent_channels=max_concurrent,
            ids_per_batch=ids_per_batch,
        ),
    )

    with create_extract_progress(
        console=console,
    ) as progress:
        overall_task: TaskID = progress_add_task(
            progress=progress,
            description="[bold]Total",
            total=len(channel_names),
        )

        for channel_name_batch in batched(
            iterable=channel_names,
            size=max_concurrent,
        ):
            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_STARTED.format(
                    channels_in_batch=len(channel_name_batch),
                    channels=channel_name_batch,
                ),
            )

            results: list[ConfigExtractionResult] = await gather(*(
                _process_channel_configs(
                    ctx=ctx.http,
                    channel_name=name,
                    channel_info=channels[name],
                    progress=progress,
                    overall_task=overall_task,
                    batch_size=ids_per_batch,
                    configs_path=ctx.io.configs_raw_path,
                )
                for name in channel_name_batch
            ))

            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_COMPLETED.format(
                    channels_in_batch=len(channel_name_batch),
                    total_collected=sum(
                        result.new_found
                        for result in results
                    ),
                ),
            )

            channel_extract_results.extend(results)

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_COMPLETED.format(
            channels_processed=len(channel_extract_results),
            total_collected=sum(
                result.new_found
                for result in channel_extract_results
            ),
        ),
    )

    return channel_extract_results


async def _try_import_configs(
    *,
    import_path: FilePath,
    skip_normalize: bool = False,
) -> V2RayConfigs | V2RayConfigsRaw | None:
    imported_configs = await import_configs(
        import_path=import_path,
    )

    if not (imported_configs_count := len(imported_configs)):
        logger.debug(
            msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_EMPTY.format(
                import_path=import_path,
            ),
        )
        return None

    normalized_configs = _apply_normalization(
        configs=imported_configs,
        skip_normalize=skip_normalize,
    )

    if not (normalized_configs_count := len(normalized_configs)):
        logger.debug(
            msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_NORMALIZED_EMPTY.format(
                imported_configs_count=imported_configs_count,
                import_path=import_path,
            ),
        )
        return None

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_SUCCESS.format(
            imported_configs_count=imported_configs_count,
            normalized_configs_count=normalized_configs_count,
            import_path=import_path,
        ),
    )

    return normalized_configs


async def export_configs(
    *,
    configs: V2RayConfigs,
    export_path: FilePath = DEFAULT_PATH_CONFIGS_EXPORT,
    indent: int = DEFAULT_JSON_INDENT,
) -> None:
    configs_count = len(configs)

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_EXPORT_STARTED.format(
            count=configs_count,
            path=export_path,
        ),
    )

    serialized = dumps(
        obj=configs,
        ensure_ascii=False,
        indent=indent,
        sort_keys=True,
    )
    json_bytes_length = len(serialized.encode("utf-8"))

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_EXPORT_SERIALIZED.format(
            json_bytes_length=json_bytes_length,
            json_indent=indent,
            configs_count=configs_count,
        ),
    )

    async with aiopen(
        file=export_path,
        mode="w",
        encoding="utf-8",
    ) as file:
        await file.write(serialized)

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_EXPORT_WRITTEN.format(
            json_bytes_length=json_bytes_length,
            export_path=export_path,
        ),
    )

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_EXPORT_COMPLETED.format(
            count=configs_count,
            path=export_path,
        ),
    )


async def fetch_and_write_configs(
    ctx: RuntimeContext,
    *,
    channels: ChannelsDict,
) -> None:
    channels_to_extract = get_sorted_keys(
        channels=channels,
        apply_filter=True,
    )
    filtered_channels_count = len(channels_to_extract)

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_FILTERED.format(
            total_channels=len(channels),
            filtered_channels_count=filtered_channels_count,
        ),
    )

    if not channels_to_extract:
        logger.warning(
            msg=MESSAGE_WARNING_NO_CHANNELS_TO_EXTRACT,
        )
        return

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_EXTRACT_STARTED.format(
            count=filtered_channels_count,
        ),
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_STARTED.format(
            filtered_channels_count=filtered_channels_count,
            filtered_channels=channels_to_extract,
        ),
    )

    results: list[ConfigExtractionResult] = await _run_channel_extraction(
        ctx=ctx,
        channel_names=channels_to_extract,
        channels=channels,
    )

    total_found = sum(
        result.new_found
        for result in results
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_EXTRACTED.format(
            channels_processed=len(results),
            total_collected=total_found,
        ),
    )

    render_config_extract(
        results=results,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_RENDERED.format(
            rendered_count=len(results),
        ),
    )

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_EXTRACT_COMPLETED.format(
            configs_count=total_found,
            channels_count=filtered_channels_count,
        ),
    )


async def import_configs(
    *,
    import_path: FilePath = DEFAULT_PATH_CONFIGS_IMPORT,
) -> V2RayConfigs:
    logger.info(
        msg=TEMPLATE_INFO_CONFIG_IMPORT_STARTED.format(
            path=import_path,
        ),
    )

    async with aiopen(
        file=import_path,
        encoding="utf-8",
    ) as file:
        content = await file.read()

        try:
            logger.debug(
                msg=TEMPLATE_DEBUG_CONFIG_IO_IMPORT_READ.format(
                    bytes_read=len(content.encode("utf-8")),
                    import_path=import_path,
                ),
            )
            configs: V2RayConfigs = loads(
                s=content,
            )
        except JSONDecodeError as e:
            logger.error(
                msg=TEMPLATE_ERROR_CONFIG_IMPORT_FAILED.format(
                    path=import_path,
                    exc_type=type(e).__name__,
                    exc_msg=str(e),
                ),
            )
            return []
        else:
            logger.info(
                msg=TEMPLATE_INFO_CONFIG_IMPORT_COMPLETED.format(
                    count=len(configs),
                    path=import_path,
                ),
            )
            return configs


async def load_configs(
    ctx: IOContext,
    *,
    import_path: FilePath | None = None,
    skip_normalize: bool = False,
) -> V2RayConfigs | V2RayConfigsRaw:
    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_STARTED.format(
            skip_normalize=skip_normalize,
            import_path=import_path,
        ),
    )

    if import_path is not None:
        final_configs = await _try_import_configs(
            import_path=import_path,
            skip_normalize=skip_normalize,
        )

        if final_configs is not None:
            logger.info(
                msg=TEMPLATE_INFO_CONFIG_LOAD_COMPLETED.format(
                    count=len(final_configs),
                    path=import_path,
                ),
            )
            return final_configs

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_LOAD_STARTED.format(
            path=ctx.configs_raw_path,
        ),
    )

    async with aiopen(
        file=ctx.configs_raw_path,
        encoding="utf-8",
    ) as file:
        configs: V2RayConfigsRaw = []
        async for line in file:
            configs.extend(
                line_to_configs(
                    line=line,
                ),
            )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_PARSED.format(
            parsed_configs_count=len(configs),
            configs_raw_path=ctx.configs_raw_path,
        ),
    )

    normalized_configs = _apply_normalization(
        configs=configs,
        skip_normalize=skip_normalize,
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_LOAD_NORMALIZED.format(
            skip_normalize=skip_normalize,
            parsed_configs_count=len(configs),
            normalized_configs_count=len(normalized_configs),
        ),
    )

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_LOAD_COMPLETED.format(
            count=len(normalized_configs),
            path=ctx.configs_raw_path,
        ),
    )

    return normalized_configs


async def save_configs(
    ctx: IOContext,
    *,
    configs: V2RayConfigs,
    export_path: FilePath | None = None,
    mode: FileMode = "w",
) -> None:
    configs_count = len(configs)

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_SAVE_STARTED.format(
            count=configs_count,
            path=ctx.configs_clean_path,
        ),
    )

    await write_configs(
        configs=[
            str(config.get("url", ""))
            for config in configs
        ],
        configs_path=ctx.configs_clean_path,
        mode=mode,
    )

    logger.info(
        msg=TEMPLATE_INFO_CONFIG_SAVE_COMPLETED.format(
            count=configs_count,
            path=ctx.configs_clean_path,
        ),
    )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_SAVE_EXPORT.format(
            configs_to_export_count=configs_count,
            export_path=export_path,
        ),
    )

    if export_path is not None:
        await export_configs(
            configs=configs,
            export_path=export_path,
        )


async def write_configs(
    *,
    configs: V2RayRawLines,
    configs_path: FilePath = DEFAULT_PATH_CONFIGS_RAW,
    mode: FileMode = "w",
) -> None:
    configs_count = len(configs)

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_WRITE_STARTED.format(
            configs_count=configs_count,
            mode=mode,
            configs_path=configs_path,
        ),
    )

    async with aiopen(
        file=configs_path,
        mode=mode,
        encoding="utf-8",
    ) as file:
        await file.writelines(
            f"{config}\n"
            for config in configs
        )

    logger.debug(
        msg=TEMPLATE_DEBUG_CONFIG_IO_WRITE_COMPLETED.format(
            written_configs_count=configs_count,
            configs_path=configs_path,
        ),
    )
