from argparse import (
    ArgumentParser,
    HelpFormatter,
)
from asyncio import (
    CancelledError,
    run,
)

from httpx import (
    AsyncClient,
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
    BATCH_EXTRACT_DEFAULT,
    BATCH_EXTRACT_MAX,
    BATCH_EXTRACT_MIN,
    BATCH_UPDATE_DEFAULT,
    BATCH_UPDATE_MAX,
    BATCH_UPDATE_MIN,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_CONFIGS_RAW,
    HTTP_TIMEOUT_DEFAULT,
    HTTP_TIMEOUT_MAX,
    HTTP_TIMEOUT_MIN,
    SUPPRESS,
)
from core.constants.messages import (
    MESSAGE_ERROR_PROGRAM_EXIT,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
)
from core.logger import (
    log_debug_object,
    logger,
)
from core.typing import (
    ArgsNamespace,
)
from core.utils import (
    abs_path,
    convert_number_in_range,
    validate_file_path,
)
from domain.channel import (
    get_sorted_keys,
    print_channel_info,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=(
            "Asynchronous Telegram channel scraper (stable and fast)."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s -E 20 "
            "-U 100 -T 30.0 --channels channels.json -R configs-raw.txt"
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
        ),
    )

    parser.add_argument(
        "-C", "--channels",
        default=abs_path(
            path=DEFAULT_PATH_CHANNELS,
        ),
        dest="channels",
        help=(
            "Path to the input JSON file containing the list of channels "
            "(default: %(default)s)."
        ),
        metavar="FILE",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-E", "--batch-extract",
        default=BATCH_EXTRACT_DEFAULT,
        dest="batch_extract",
        help=(
            "Number of messages processed in parallel to extract "
            "V2Ray configs (default: %(default)s)."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=BATCH_EXTRACT_MIN,
            max_value=BATCH_EXTRACT_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    parser.add_argument(
        "-R", "--configs-raw",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw",
        help=(
            "Path to the output file for saving scraped V2Ray configs "
            "(default: %(default)s)."
        ),
        metavar="FILE",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    parser.add_argument(
        "-T", "--time-out",
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

    parser.add_argument(
        "-U", "--batch-update",
        default=BATCH_UPDATE_DEFAULT,
        dest="batch_update",
        help=(
            "Maximum number of channels updated in parallel "
            "(default: %(default)s)."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=BATCH_UPDATE_MIN,
            max_value=BATCH_UPDATE_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    args = parser.parse_args()
    log_debug_object(
        title="Parsed command-line arguments",
        obj=args,
    )

    return args


async def main() -> None:
    parsed_args = parse_args()
    try:
        channels = await load_channels(
            path_channels=parsed_args.channels,
        )

        async with AsyncClient(
            timeout=Timeout(
                timeout=parsed_args.time_out,
            ),
        ) as client:
            await update_info(
                client=client,
                channels=channels,
                batch_size=parsed_args.batch_update,
            )
            print_channel_info(
                channels=channels,
            )

            for name in get_sorted_keys(
                channels=channels,
                apply_filter=True,
            ):
                await fetch_and_write_configs(
                    client=client,
                    channel_name=name,
                    channel_info=channels[name],
                    batch_size=parsed_args.batch_extract,
                    path_configs=parsed_args.configs_raw,
                )
    except (
        CancelledError,
        KeyboardInterrupt,
    ):
        logger.info(
            msg=MESSAGE_ERROR_PROGRAM_EXIT,
        )
    except Exception:
        logger.exception(
            msg=MESSAGE_ERROR_UNEXPECTED_FAILURE,
        )
    finally:
        await save_channels(
            channels=channels,
            path_channels=parsed_args.channels,
        )


if __name__ == "__main__":
    run(
        main=main(),
    )
