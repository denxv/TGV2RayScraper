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
    update_info,
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
from core.constants.messages.error import (
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
)
from core.constants.messages.info import (
    MESSAGE_INFO_PROGRAM_EXIT,
)
from core.constants.templates.error import (
    TEMPLATE_ERROR_PROXY_AUTH_OR_PROTOCOL,
    TEMPLATE_ERROR_PROXY_NETWORK,
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
        description=(
            "Asynchronous Telegram channel scraper (stable and fast)."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/scraper.py "
            "-C channels/current.json -R configs/v2ray-raw.txt "
            "-E 20 -U 100 --proxy --time-out 30.0 --skip-update"
        ),
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
        "Global options",
    )
    group_global.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help=(
            "Enable debug logging in console. "
            "By default, console shows INFO level logs."
        ),
    )

    group_http_client = parser.add_argument_group(
        "HTTP Client",
    )
    group_http_client.add_argument(
        "--proxy",
        const=DEFAULT_PROXY_URL,
        dest="proxy_url",
        help=(
            "Proxy server URL. Takes precedence over environment variables. "
            "Otherwise checks HTTPS_PROXY, HTTP_PROXY, and ALL_PROXY. "
            "Falls back to local proxy if none are set (default: %(const)s)."
        ),
        metavar="URL",
        nargs="?",
        type=validate_proxy_url,
    )
    group_http_client.add_argument(
        "--retries",
        default=HTTP_RETRIES_DEFAULT,
        dest="retries",
        help=(
            "Maximum number of HTTP request retry attempts after failures "
            "(default: %(default)s)."
        ),
        metavar="N",
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
        help=(
            "Delay between HTTP retry attempts when request fetching fails "
            "(default: %(default)s)."
        ),
        metavar="SECONDS",
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
        help=(
            "HTTP client timeout in seconds for requests used "
            "while updating channel info and "
            "extracting V2Ray configurations (default: %(default)s)."
        ),
        metavar="SECONDS",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_TIMEOUT_MIN,
            max_value=HTTP_TIMEOUT_MAX,
            as_int=False,
            as_str=False,
        ),
    )

    group_files = parser.add_argument_group(
        "Input / Output files",
    )
    group_files.add_argument(
        "-C", "--channels",
        default=abs_path(
            path=DEFAULT_PATH_CHANNELS,
        ),
        dest="channels_path",
        help=(
            "Path to the input JSON file containing the list of channels "
            f"(default: {rel_path(DEFAULT_PATH_CHANNELS)})."
        ),
        metavar="PATH",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )
    group_files.add_argument(
        "-R", "--configs-raw",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw_path",
        help=(
            "Path to the output TXT file for saving scraped V2Ray configs "
            f"(default: {rel_path(DEFAULT_PATH_CONFIGS_RAW)})."
        ),
        metavar="PATH",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    group_update = parser.add_argument_group(
        "Channel update pipeline",
    )
    group_update.add_argument(
        "--skip-update",
        action="store_true",
        default=False,
        dest="skip_update",
        help=(
            "Skip updating channel information. "
            "Avoids redundant requests if channels are already updated. "
            "By default, channels are updated."
        ),
    )
    group_update.add_argument(
        "-U", "--channels-batch",
        default=CHANNELS_BATCH_DEFAULT,
        dest="channels_batch",
        help=(
            "Number of channels processed per batch during update "
            "(default: %(default)s)."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CHANNELS_BATCH_MIN,
            max_value=CHANNELS_BATCH_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    group_extract = parser.add_argument_group(
        "Config extraction pipeline",
    )
    group_extract.add_argument(
        "-E", "--configs-batch",
        default=CONFIGS_BATCH_DEFAULT,
        dest="configs_batch",
        help=(
            "Number of messages processed per batch for config extraction "
            "(default: %(default)s)."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CONFIGS_BATCH_MIN,
            max_value=CONFIGS_BATCH_MAX,
            as_int=True,
            as_str=False,
        ),
    )
    group_extract.add_argument(
        "-P", "--channels-concurrency",
        default=CHANNELS_CONCURRENCY_DEFAULT,
        dest="channels_concurrency",
        help=(
            "Maximum number of channels processed concurrently "
            "during config extraction (default: %(default)s)."
        ),
        metavar="N",
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
        title="Parsed command-line arguments",
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

            await update_info(
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
