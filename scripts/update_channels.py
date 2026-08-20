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
    SUPPRESS,
)
from core.constants.formats import (
    FORMAT_CHANNEL_SET_DEST,
    FORMAT_CHANNEL_SET_OPTION,
)
from core.constants.locales import (
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_DELETE_CHANNELS,
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_DESCRIPTION,
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_TITLE,
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_RESET_ALL,
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_METAVAR,
    CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_TEMPLATE,
    CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER,
    CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER_METAVAR,
    CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_DESCRIPTION,
    CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_TITLE,
    CLI_UPDATE_CHANNELS_DESCRIPTION,
    CLI_UPDATE_CHANNELS_EPILOG,
    CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_DEBUG,
    CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_GROUP_TITLE,
    CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_NO_DRY_RUN,
    CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_SKIP_BACKUP,
    CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_METAVAR,
    CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_TEMPLATE,
    CLI_UPDATE_CHANNELS_INPUT_FILES_GROUP_TITLE,
    CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_METAVAR,
    CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_TEMPLATE,
    MESSAGE_ERROR_MULTIPLE_ACTIONS_SPECIFIED,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
    MESSAGE_INFO_PROGRAM_EXIT,
    TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS,
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
    get_channel_overrides,
    normalize_condition,
    rel_path,
    validate_file_path,
)
from domain.channel import (
    process_channels,
    update_with_new_channels,
)
from domain.predicates import (
    has_multiple_channel_actions,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=CLI_UPDATE_CHANNELS_DESCRIPTION,
        epilog=CLI_UPDATE_CHANNELS_EPILOG,
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
        title=CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_GROUP_TITLE,
    )
    group_global.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help=CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_DEBUG,
    )
    group_global.add_argument(
        "--no-dry-run",
        action="store_false",
        default=True,
        dest="dry_run",
        help=CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_NO_DRY_RUN,
    )
    group_global.add_argument(
        "--skip-backup",
        action="store_true",
        default=False,
        dest="skip_backup",
        help=CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_SKIP_BACKUP,
    )

    group_input_files = parser.add_argument_group(
        title=CLI_UPDATE_CHANNELS_INPUT_FILES_GROUP_TITLE,
    )
    group_input_files.add_argument(
        "-C", "--channels",
        default=abs_path(
            path=DEFAULT_PATH_CHANNELS,
        ),
        dest="channels_path",
        help=CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CHANNELS,
            ),
        ),
        metavar=CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )
    group_input_files.add_argument(
        "-U", "--urls",
        default=abs_path(
            path=DEFAULT_PATH_URLS,
        ),
        dest="urls_path",
        help=CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_URLS,
            ),
        ),
        metavar=CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    group_channel_selection = parser.add_argument_group(
        title=CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_TITLE,
        description=CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_DESCRIPTION,
    )
    group_channel_selection.add_argument(
        "-F", "--channel-filter",
        dest="channel_filter",
        help=CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER,
        metavar=CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER_METAVAR,
        type=normalize_condition,
    )

    group_channel_actions = parser.add_argument_group(
        title=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_TITLE,
        description=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_DESCRIPTION,
    )
    group_channel_actions.add_argument(
        "-D", "--delete-channels",
        action="store_true",
        default=False,
        dest="delete_channels",
        help=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_DELETE_CHANNELS,
    )
    group_channel_actions.add_argument(
        "--reset-all",
        action="store_true",
        default=False,
        dest="reset_all",
        help=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_RESET_ALL,
    )
    for field, default in DEFAULT_CHANNEL_VALUES.items():
        group_channel_actions.add_argument(
            FORMAT_CHANNEL_SET_OPTION.format(
                field=field.replace("_", "-"),
            ),
            const=default,
            dest=FORMAT_CHANNEL_SET_DEST.format(
                field=field,
            ),
            help=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_TEMPLATE.format(
                field=field,
            ),
            metavar=CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_METAVAR,
            nargs="?",
            type=type(default),
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

    if has_multiple_channel_actions(
        has_overrides=bool(
            get_channel_overrides(
                args=args,
            ),
        ),
        reset_to_defaults=args.reset_all,
        should_delete=args.delete_channels,
    ):
        parser.error(
            message=MESSAGE_ERROR_MULTIPLE_ACTIONS_SPECIFIED,
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
            channel_filter=parsed_args.channel_filter,
            channel_overrides=get_channel_overrides(
                args=parsed_args,
            ),
            dry_run=parsed_args.dry_run,
            reset_to_defaults=parsed_args.reset_all,
            should_delete=parsed_args.delete_channels,
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
