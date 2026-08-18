from argparse import (
    ArgumentParser,
    HelpFormatter,
)
from asyncio import (
    CancelledError,
)
from asyncio import (
    run as asyncio_run,
)

from httpx import (
    AsyncClient,
    ConnectError,
    ProxyError,
    Timeout,
)

from adapters.channel import (
    load_channels,
    save_channels,
)
from adapters.config import (
    fetch_and_write_configs,
)
from adapters.scraper import (
    update_channels_info,
)
from core.constants.common import (
    CHANNELS_BATCH_DEFAULT,
    CHANNELS_BATCH_MAX,
    CHANNELS_BATCH_MIN,
    CHANNELS_CONCURRENCY_DEFAULT,
    CHANNELS_CONCURRENCY_MAX,
    CHANNELS_CONCURRENCY_MIN,
    CONFIGS_BATCH_DEFAULT,
    CONFIGS_BATCH_MAX,
    CONFIGS_BATCH_MIN,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_CONFIGS_RAW,
    DEFAULT_PROXY_URL,
    HTTP_RETRIES_DEFAULT,
    HTTP_RETRIES_MAX,
    HTTP_RETRIES_MIN,
    HTTP_RETRY_DELAY_DEFAULT,
    HTTP_RETRY_DELAY_MAX,
    HTTP_RETRY_DELAY_MIN,
    HTTP_TIMEOUT_DEFAULT,
    HTTP_TIMEOUT_MAX,
    HTTP_TIMEOUT_MIN,
    SUPPRESS,
)
from core.constants.locales import (
    CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH,
    CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH_METAVAR,
    CLI_SCRAPER_CHANNEL_UPDATE_GROUP_TITLE,
    CLI_SCRAPER_CHANNEL_UPDATE_SKIP,
    CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY,
    CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY_METAVAR,
    CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH,
    CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH_METAVAR,
    CLI_SCRAPER_CONFIG_EXTRACT_GROUP_TITLE,
    CLI_SCRAPER_DESCRIPTION,
    CLI_SCRAPER_EPILOG,
    CLI_SCRAPER_GLOBAL_OPTIONS_DEBUG,
    CLI_SCRAPER_GLOBAL_OPTIONS_GROUP_TITLE,
    CLI_SCRAPER_HTTP_CLIENT_GROUP_TITLE,
    CLI_SCRAPER_HTTP_CLIENT_PROXY,
    CLI_SCRAPER_HTTP_CLIENT_PROXY_METAVAR,
    CLI_SCRAPER_HTTP_CLIENT_RETRIES,
    CLI_SCRAPER_HTTP_CLIENT_RETRIES_METAVAR,
    CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY,
    CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY_METAVAR,
    CLI_SCRAPER_HTTP_CLIENT_TIME_OUT,
    CLI_SCRAPER_HTTP_CLIENT_TIME_OUT_METAVAR,
    CLI_SCRAPER_IO_FILES_CHANNELS_METAVAR,
    CLI_SCRAPER_IO_FILES_CHANNELS_TEMPLATE,
    CLI_SCRAPER_IO_FILES_CONFIGS_RAW_METAVAR,
    CLI_SCRAPER_IO_FILES_CONFIGS_RAW_TEMPLATE,
    CLI_SCRAPER_IO_FILES_GROUP_TITLE,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
    MESSAGE_INFO_PROGRAM_EXIT,
    TEMPLATE_ERROR_PROXY_AUTH_OR_PROTOCOL,
    TEMPLATE_ERROR_PROXY_NETWORK,
    TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS,
)
from core.constants.templates.info.common import (
    TEMPLATE_INFO_PROXY_USED,
)
from core.context import (
    ChannelUpdateContext,
    ConfigExtractionContext,
    HttpContext,
    IOContext,
    PipelineRuntimeContext,
    RuntimeContext,
)
from core.terminal.logger import (
    log_debug_object,
    logger,
    set_console_level,
)
from core.typing import (
    ArgsNamespace,
)
from core.utils import (
    abs_path,
    convert_number_in_range,
    rel_path,
    validate_file_path,
    validate_proxy_url,
)
from domain.channel import (
    display_channel_info,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=CLI_SCRAPER_DESCRIPTION,
        epilog=CLI_SCRAPER_EPILOG,
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
        ),
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    group_global = parser.add_argument_group(
        title=CLI_SCRAPER_GLOBAL_OPTIONS_GROUP_TITLE,
    )
    group_global.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help=CLI_SCRAPER_GLOBAL_OPTIONS_DEBUG,
    )

    group_http_client = parser.add_argument_group(
        title=CLI_SCRAPER_HTTP_CLIENT_GROUP_TITLE,
    )
    group_http_client.add_argument(
        "--proxy",
        const=DEFAULT_PROXY_URL,
        dest="proxy_url",
        help=CLI_SCRAPER_HTTP_CLIENT_PROXY,
        metavar=CLI_SCRAPER_HTTP_CLIENT_PROXY_METAVAR,
        nargs="?",
        type=validate_proxy_url,
    )
    group_http_client.add_argument(
        "--retries",
        default=HTTP_RETRIES_DEFAULT,
        dest="retries",
        help=CLI_SCRAPER_HTTP_CLIENT_RETRIES,
        metavar=CLI_SCRAPER_HTTP_CLIENT_RETRIES_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_RETRIES_MIN,
            max_value=HTTP_RETRIES_MAX,
            as_int=True,
            as_str=False,
        ),
    )
    group_http_client.add_argument(
        "--retry-delay",
        default=HTTP_RETRY_DELAY_DEFAULT,
        dest="retry_delay",
        help=CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY,
        metavar=CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_RETRY_DELAY_MIN,
            max_value=HTTP_RETRY_DELAY_MAX,
            as_int=False,
            as_str=False,
        ),
    )
    group_http_client.add_argument(
        "--time-out",
        default=HTTP_TIMEOUT_DEFAULT,
        dest="time_out",
        help=CLI_SCRAPER_HTTP_CLIENT_TIME_OUT,
        metavar=CLI_SCRAPER_HTTP_CLIENT_TIME_OUT_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_TIMEOUT_MIN,
            max_value=HTTP_TIMEOUT_MAX,
            as_int=False,
            as_str=False,
        ),
    )

    group_io_files = parser.add_argument_group(
        title=CLI_SCRAPER_IO_FILES_GROUP_TITLE,
    )
    group_io_files.add_argument(
        "-C", "--channels",
        default=abs_path(
            path=DEFAULT_PATH_CHANNELS,
        ),
        dest="channels_path",
        help=CLI_SCRAPER_IO_FILES_CHANNELS_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CHANNELS,
            ),
        ),
        metavar=CLI_SCRAPER_IO_FILES_CHANNELS_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )
    group_io_files.add_argument(
        "-R", "--configs-raw",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw_path",
        help=CLI_SCRAPER_IO_FILES_CONFIGS_RAW_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CONFIGS_RAW,
            ),
        ),
        metavar=CLI_SCRAPER_IO_FILES_CONFIGS_RAW_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    group_channel_update = parser.add_argument_group(
        title=CLI_SCRAPER_CHANNEL_UPDATE_GROUP_TITLE,
    )
    group_channel_update.add_argument(
        "--skip-update",
        action="store_true",
        default=False,
        dest="skip_update",
        help=CLI_SCRAPER_CHANNEL_UPDATE_SKIP,
    )
    group_channel_update.add_argument(
        "-U", "--channels-batch",
        default=CHANNELS_BATCH_DEFAULT,
        dest="channels_batch",
        help=CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH,
        metavar=CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CHANNELS_BATCH_MIN,
            max_value=CHANNELS_BATCH_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    group_config_extract = parser.add_argument_group(
        title=CLI_SCRAPER_CONFIG_EXTRACT_GROUP_TITLE,
    )
    group_config_extract.add_argument(
        "-E", "--configs-batch",
        default=CONFIGS_BATCH_DEFAULT,
        dest="configs_batch",
        help=CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH,
        metavar=CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CONFIGS_BATCH_MIN,
            max_value=CONFIGS_BATCH_MAX,
            as_int=True,
            as_str=False,
        ),
    )
    group_config_extract.add_argument(
        "-P", "--channels-concurrency",
        default=CHANNELS_CONCURRENCY_DEFAULT,
        dest="channels_concurrency",
        help=CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY,
        metavar=CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY_METAVAR,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CHANNELS_CONCURRENCY_MIN,
            max_value=CHANNELS_CONCURRENCY_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    args = parser.parse_args()

    set_console_level(
        logger=logger,
        debug=args.debug,
    )

    log_debug_object(
        obj=args,
        title=TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS.format(
            name=rel_path(
                path=__file__,
            ),
        ),
    )

    return args


async def main() -> None:
    parsed_args = parse_args()

    try:
        io_ctx = IOContext(
            channels_path=parsed_args.channels_path,
            configs_raw_path=parsed_args.configs_raw_path,
        )

        channels = await load_channels(
            ctx=io_ctx,
        )

        async with AsyncClient(
            proxy=parsed_args.proxy_url,
            timeout=Timeout(
                timeout=parsed_args.time_out,
            ),
        ) as client:
            if parsed_args.proxy_url:
                logger.info(
                    msg=TEMPLATE_INFO_PROXY_USED.format(
                        url=parsed_args.proxy_url,
                    ),
                )

            runtime_ctx = RuntimeContext(
                http=HttpContext(
                    client=client,
                    retries=parsed_args.retries,
                    retry_delay=parsed_args.retry_delay,
                ),
                io=io_ctx,
                pipeline=PipelineRuntimeContext(
                    channel_update=ChannelUpdateContext(
                        batch_size=parsed_args.channels_batch,
                    ),
                    config_extraction=ConfigExtractionContext(
                        batch_size=parsed_args.configs_batch,
                        max_concurrent_channels=parsed_args.channels_concurrency,
                    ),
                ),
            )

            await update_channels_info(
                ctx=runtime_ctx,
                channels=channels,
                skip_update=parsed_args.skip_update,
            )

            display_channel_info(
                channels=channels,
            )

            await fetch_and_write_configs(
                ctx=runtime_ctx,
                channels=channels,
            )
    except (
        CancelledError,
        KeyboardInterrupt,
    ):
        logger.info(
            msg=MESSAGE_INFO_PROGRAM_EXIT,
        )
    except ProxyError as e:
        logger.error(
            msg=TEMPLATE_ERROR_PROXY_AUTH_OR_PROTOCOL.format(
                url=parsed_args.proxy_url,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
    except ConnectError as e:
        logger.error(
            msg=TEMPLATE_ERROR_PROXY_NETWORK.format(
                url=parsed_args.proxy_url,
                exc_type=type(e).__name__,
                exc_msg=str(e),
            ),
        )
    except Exception:
        logger.exception(
            msg=MESSAGE_ERROR_UNEXPECTED_FAILURE,
        )
    finally:
        await save_channels(
            ctx=io_ctx,
            channels=channels,
        )


if __name__ == "__main__":
    asyncio_run(
        main=main(),
    )
