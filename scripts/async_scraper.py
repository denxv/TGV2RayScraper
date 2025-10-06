#!/usr/bin/env python

from argparse import ArgumentParser, HelpFormatter, Namespace, SUPPRESS
from asyncio import CancelledError, run

from aiohttp import ClientSession

from adapters.async_.channels import load_channels, save_channels
from adapters.async_.configs import fetch_channel_configs
from adapters.async_.scraper import update_info
from core.logger import logger, log_debug_object
from core.constants import DEFAULT_PATH_CHANNELS, DEFAULT_PATH_CONFIGS_RAW
from core.utils import abs_path, int_in_range, validate_file_path
from domain.channel import get_sorted_keys, print_channel_info


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description = "Asynchronous Telegram channel scraper (faster, experimental).",
        epilog="Example: python %(prog)s -E 20 -U 100 --channels channels.json -R configs-raw.txt",
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=120,
        ),
    )

    parser.add_argument(
        "-C", "--channels",
        default=abs_path(DEFAULT_PATH_CHANNELS),
        dest="channels",
        help="Path to the input JSON file containing the list of channels (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-E", "--batch-extract",
        default=20,
        dest="batch_extract",
        help="Number of messages processed in parallel to extract V2Ray configs (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=100),
    )

    parser.add_argument(
        "-R", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the output file for saving scraped V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "-U", "--batch-update",
        default=100,
        dest="batch_update",
        help="Maximum number of channels updated in parallel (default: %(default)s).",
        metavar="N",
        type=lambda value: int_in_range(value, min_value=1, max_value=1000),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


async def main() -> None:
    parsed_args = parse_args()
    try:
        channels = await load_channels(path_channels=parsed_args.channels)
        async with ClientSession() as session:
            await update_info(session, channels, batch_size=parsed_args.batch_update)
            print_channel_info(channels)
            for name in get_sorted_keys(channels, filtering=True):
                await fetch_channel_configs(
                    session=session, 
                    channel_name=name, 
                    channel_info=channels[name], 
                    batch_size=parsed_args.batch_extract, 
                    path_configs=parsed_args.configs_raw,
                )
    except (CancelledError, KeyboardInterrupt):
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")
    finally:
        await save_channels(channels, path_channels=parsed_args.channels)


if __name__ == "__main__":
    run(main())
