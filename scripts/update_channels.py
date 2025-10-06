#!/usr/bin/env python

from argparse import ArgumentParser, HelpFormatter, Namespace, SUPPRESS

from adapters.sync.channels import (
    delete_channels,
    load_channels_and_urls,
    save_channels_and_urls,
    update_with_new_channels,
)
from core.logger import logger, log_debug_object
from core.constants import DEFAULT_PATH_CHANNELS, DEFAULT_PATH_URLS
from core.utils import abs_path, validate_file_path


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Backup, merge new channels from URLs, and update Telegram channel data.",
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s -C channels.json --urls urls.txt"
        ),
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
        "-U", "--urls",
        default=abs_path(DEFAULT_PATH_URLS),
        dest="urls",
        help="Path to a text file containing new channel URLs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def main() -> None:
    try:
        parsed_args = parse_args()
        current_channels, list_channel_names = load_channels_and_urls(
            path_channels=parsed_args.channels,
            path_urls=parsed_args.urls,
        )
        update_with_new_channels(current_channels, list_channel_names)
        delete_channels(current_channels)
        save_channels_and_urls(
            channels=current_channels,
            path_channels=parsed_args.channels,
            path_urls=parsed_args.urls,
        )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == "__main__":
    main()
