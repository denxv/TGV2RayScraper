#!/usr/bin/env python

from argparse import ArgumentParser, HelpFormatter

from httpx import Client

from adapters.sync.channels import load_channels, save_channels
from adapters.sync.configs import fetch_channel_configs
from adapters.sync.scraper import update_info
from core.logger import logger, log_debug_object
from core.constants import (
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_CONFIGS_RAW,
    SUPPRESS,
)
from core.typing import ArgsNamespace
from core.utils import abs_path, validate_file_path
from domain.channel import get_sorted_keys, print_channel_info


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description="Synchronous Telegram channel scraper (simpler, slower).",
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s -C channels.json "
            "--configs-raw configs-raw.txt"
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
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
        "-R", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the output file for saving scraped V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def main() -> None:
    parsed_args = parse_args()
    try:
        channels = load_channels(path_channels=parsed_args.channels)
        with Client() as client:
            update_info(client, channels)
            print_channel_info(channels)
            for name in get_sorted_keys(channels, apply_filter=True):
                fetch_channel_configs(
                    client=client,
                    channel_name=name,
                    channel_info=channels[name],
                    path_configs=parsed_args.configs_raw,
                )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")
    finally:
        save_channels(channels, path_channels=parsed_args.channels)


if __name__ == "__main__":
    main()
