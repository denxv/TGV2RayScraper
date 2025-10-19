from argparse import ArgumentParser, HelpFormatter

from adapters.sync.channels import (
    load_channels_and_urls,
    save_channels_and_urls,
)
from core.constants import (
    CHANNEL_MAX_MESSAGE_OFFSET,
    CHANNEL_MIN_MESSAGE_OFFSET,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_URLS,
    MESSAGE_EXIT,
    MESSAGE_UNEXPECTED_ERROR,
    SUPPRESS,
)
from core.logger import log_debug_object, logger
from core.typing import ArgsNamespace
from core.utils import (
    abs_path,
    convert_number_in_range,
    validate_file_path,
)
from domain.channel import (
    process_channels,
    update_with_new_channels,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=(
            "Backup, merge new channels from URLs, "
            "and update Telegram channel data."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s "
            "-C channels.json --urls urls.txt --delete-channels "
            "-M 50 --include-new --no-dry-run --no-backup"
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
        ),
    )

    parser.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="check_only",
        help=(
            "Disable check-only mode and actually assign 'current_id' "
            "(default: enabled)."
        ),
    )

    parser.add_argument(
        "-B", "--no-backup",
        action="store_false",
        dest="make_backups",
        help=(
            "Skip creating backup files for channel and "
            "Telegram URL lists before saving "
            "(default: enabled)."
        ),
    )

    parser.add_argument(
        "-C", "--channels",
        default=abs_path(DEFAULT_PATH_CHANNELS),
        dest="channels_file",
        help=(
            "Path to the input JSON file containing the list of channels "
            "(default: %(default)s)."
        ),
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "-D", "--delete-channels",
        action="store_true",
        dest="delete_channels",
        help=(
            "Delete channels that are unavailable or "
            "meet specific conditions (default: disabled)."
        ),
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-M", "--message-offset",
        dest="message_offset",
        help=(
            "Number of recent messages to include "
            "when assigning 'current_id'."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value,
            min_value=CHANNEL_MIN_MESSAGE_OFFSET,
            max_value=CHANNEL_MAX_MESSAGE_OFFSET,
            as_int=True,
            as_str=False,
        ),
    )

    parser.add_argument(
        "-N", "--include-new",
        action="store_true",
        dest="include_new_channels",
        help="Include new channels in processing.",
    )

    parser.add_argument(
        "-U", "--urls",
        default=abs_path(DEFAULT_PATH_URLS),
        dest="urls_file",
        help=(
            "Path to a text file containing new channel URLs "
            "(default: %(default)s)."
        ),
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
            path_channels=parsed_args.channels_file,
            path_urls=parsed_args.urls_file,
        )

        current_channels = update_with_new_channels(
            current_channels=current_channels,
            channel_names=list_channel_names,
        )
        current_channels = process_channels(
            channels=current_channels,
            args=parsed_args,
        )

        save_channels_and_urls(
            channels=current_channels,
            path_channels=parsed_args.channels_file,
            path_urls=parsed_args.urls_file,
            make_backups=parsed_args.make_backups,
        )
    except KeyboardInterrupt:
        logger.info(MESSAGE_EXIT)
    except Exception:
        logger.exception(MESSAGE_UNEXPECTED_ERROR)


if __name__ == "__main__":
    main()
