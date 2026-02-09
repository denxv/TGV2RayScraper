from argparse import (
    ArgumentParser,
    HelpFormatter,
)
from asyncio import (
    CancelledError,
    run,
)

from adapters.channel import (
    load_channels_and_urls,
    save_channels_and_urls,
)
from core.constants.common import (
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_URLS,
    MESSAGE_OFFSET_MAX,
    MESSAGE_OFFSET_MIN,
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
    rel_path,
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
            "Backup channels, merge new URLs, "
            "filter channels, reset fields, "
            "delete unavailable channels, "
            "and update 'current_id'."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s "
            "-C channels/current.json -U channels/urls.txt "
            '-F "count < 100" --no-dry-run --reset-all'
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
        "--no-backup",
        action="store_false",
        dest="backup",
        help=(
            "Skip creating backup files for channel and Telegram URL lists. "
            "By default, backup is created."
        ),
    )
    group_global.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help=(
            "Disable check-only mode and actually assign 'current_id'. "
            "By default, dry-run mode is enabled."
        ),
    )

    group_files = parser.add_argument_group(
        "Input files",
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
        "-U", "--urls",
        default=abs_path(
            path=DEFAULT_PATH_URLS,
        ),
        dest="urls_path",
        help=(
            "Path to the input TXT file containing new channel URLs "
            f"(default: {rel_path(DEFAULT_PATH_URLS)})."
        ),
        metavar="PATH",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    group_selection = parser.add_argument_group(
        "Channel selection options",
    )
    group_selection.add_argument(
        "-F", "--channel-filter",
        dest="channel_filter",
        help=(
            "Filter channels using a Python-like condition. Example: "
            '"count < 100 and current_id == last_id or state == -1". '
            "Only channels matching the condition will be selected. "
            "If omitted, all existing channels "
            "except new ones will be selected."
        ),
        metavar="CONDITION",
        type=str,
    )

    group_actions = parser.add_argument_group(
        "Channel actions",
    )
    group_actions.add_argument(
        "-D", "--delete-channels",
        action="store_true",
        dest="delete_channels",
        help=(
            "Delete channels that are unavailable or "
            "meet specific conditions. By default, deletion is disabled."
        ),
    )
    group_actions.add_argument(
        "-M", "--message-offset",
        dest="message_offset",
        help=(
            "Number of recent messages to include "
            "when assigning 'current_id'."
        ),
        metavar="N",
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=MESSAGE_OFFSET_MIN,
            max_value=MESSAGE_OFFSET_MAX,
            as_int=True,
            as_str=False,
        ),
    )

    group_reset = parser.add_argument_group(
        "Channel reset options",
    )
    group_reset.add_argument(
        "--reset-all",
        action="store_true",
        dest="reset_all",
        help=(
            "Reset all channel values to their defaults. "
            "Can be used together with --reset-<field> "
            "to set specific values, and/or with --channel-filter "
            "to select which channels are affected (default: disabled)."
        ),
    )
    for field, default in DEFAULT_CHANNEL_VALUES.items():
        group_reset.add_argument(
            f"--reset-{field.replace('_', '-')}",
            const=default,
            dest=f"reset_{field}",
            help=(
                f"Reset '{field}' to the specified value. "
                "If no value is provided, the default value is used "
                "(default: %(const)s)."
            ),
            metavar="N",
            nargs="?",
            type=type(default),
        )

    args = parser.parse_args()

    log_debug_object(
        title="Parsed command-line arguments",
        obj=args,
    )

    return args


async def main() -> None:
    try:
        parsed_args = parse_args()

        current_channels, list_channel_names = await load_channels_and_urls(
            channels_path=parsed_args.channels_path,
            urls_path=parsed_args.urls_path,
        )

        current_channels = update_with_new_channels(
            current_channels=current_channels,
            channel_names=list_channel_names,
        )
        current_channels = process_channels(
            channels=current_channels,
            args=parsed_args,
        )

        await save_channels_and_urls(
            channels=current_channels,
            channels_path=parsed_args.channels_path,
            urls_path=parsed_args.urls_path,
            make_backups=parsed_args.backup,
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


if __name__ == "__main__":
    run(
        main=main(),
    )
