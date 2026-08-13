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
from core.constants.messages.error import (
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
)
from core.constants.messages.info import (
    MESSAGE_INFO_PROGRAM_EXIT,
)
from core.context import (
    IOContext,
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
    normalize_condition,
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
            "Example: PYTHONPATH=. python scripts/update_channels.py "
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
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help=(
            "Enable debug logging in console. "
            "By default, console shows INFO level logs."
        ),
    )
    group_global.add_argument(
        "--no-dry-run",
        action="store_false",
        default=True,
        dest="dry_run",
        help=(
            "Disable dry-run mode and allow modifying channel metadata, "
            "including assigning 'current_id' and resetting fields "
            "(e.g. count, last_id, etc.). "
            "By default, dry-run mode is enabled."
        ),
    )
    group_global.add_argument(
        "--skip-backup",
        action="store_true",
        default=False,
        dest="skip_backup",
        help=(
            "Skip creating backup files for channel and Telegram URL lists. "
            "By default, backup is created."
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
        description=(
            "Common filter for all actions. "
            "If omitted, a built-in default is used per action."
        ),
    )
    group_selection.add_argument(
        "-F", "--channel-filter",
        dest="channel_filter",
        help=(
            "Filter channels using a Python-like condition. Example: "
            '"count < 100 and current_id == last_id or state == -1". '
            "If omitted, all existing channels "
            "except new ones will be selected."
        ),
        metavar="CONDITION",
        type=normalize_condition,
    )

    group_actions = parser.add_argument_group(
        "Channel actions",
        description=(
            "Only one action can be specified per invocation. "
            "Cannot combine --delete-channels, --message-offset, "
            "and reset options."
        ),
    )
    group_actions.add_argument(
        "-D", "--delete-channels",
        action="store_true",
        default=False,
        dest="delete_channels",
        help=(
            "Delete channels matching the filter. "
            "If no filter is specified, deletes unavailable channels "
            "and channels without configuration. "
            "By default, deletion is disabled."
        ),
    )
    group_actions.add_argument(
        "-M", "--message-offset",
        dest="message_offset",
        help=(
            "Assign 'current_id' to channels matching the filter "
            "based on N recent messages. "
            "If no filter is specified, applies to available channels "
            "excluding new ones."
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
        description=(
            "Reset options can be combined with each other, "
            "but not with --delete-channels or --message-offset."
        ),
    )
    group_reset.add_argument(
        "--reset-all",
        action="store_true",
        default=False,
        dest="reset_all",
        help=(
            "Reset all channel values to their defaults "
            "for filtered channels. Can be combined with --reset-<field>. "
            "Without a filter, applies to available non-new channels."
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

    action_count = sum((
        args.delete_channels,
        args.message_offset is not None,
        args.reset_all or any(
            getattr(args, f"reset_{field}", None) is not None
            for field in DEFAULT_CHANNEL_VALUES
        ),
    ))

    if action_count > 1:
        parser.error(
            "Multiple actions cannot be combined. "
            "Specify only one: "
            "--delete-channels, --message-offset, or reset options.",
        )

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
    try:
        parsed_args = parse_args()

        io_ctx = IOContext(
            channels_path=parsed_args.channels_path,
            urls_path=parsed_args.urls_path,
        )

        current_channels, list_channel_names = await load_channels_and_urls(
            ctx=io_ctx,
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
            ctx=io_ctx,
            channels=current_channels,
            skip_backup=parsed_args.skip_backup,
        )
    except (
        CancelledError,
        KeyboardInterrupt,
    ):
        logger.info(
            msg=MESSAGE_INFO_PROGRAM_EXIT,
        )
    except Exception:
        logger.exception(
            msg=MESSAGE_ERROR_UNEXPECTED_FAILURE,
        )


if __name__ == "__main__":
    asyncio_run(
        main=main(),
    )
