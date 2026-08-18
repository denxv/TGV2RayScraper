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

from adapters.config import (
    load_configs,
    save_configs,
)
from core.constants.common import (
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CONFIGS_CLEAN,
    DEFAULT_PATH_CONFIGS_EXPORT,
    DEFAULT_PATH_CONFIGS_IMPORT,
    DEFAULT_PATH_CONFIGS_RAW,
    SUPPRESS,
)
from core.constants.locales import (
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE_METAVAR,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER_METAVAR,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_GROUP_TITLE,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_REVERSE,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT,
    CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT_METAVAR,
    CLI_V2RAY_CLEANER_DESCRIPTION,
    CLI_V2RAY_CLEANER_EPILOG,
    CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_DEBUG,
    CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_GROUP_TITLE,
    CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_SKIP_NORMALIZE,
    CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_METAVAR,
    CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_TEMPLATE,
    CLI_V2RAY_CLEANER_INPUT_FILES_GROUP_TITLE,
    CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_METAVAR,
    CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_TEMPLATE,
    CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_METAVAR,
    CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_TEMPLATE,
    CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_METAVAR,
    CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_TEMPLATE,
    CLI_V2RAY_CLEANER_OUTPUT_FILES_GROUP_TITLE,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
    MESSAGE_INFO_PROGRAM_EXIT,
    TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS,
    TEMPLATE_TITLE_COMPILED_URL_PATTERNS_BY_V2RAY_PROTOCOL,
)
from core.constants.patterns.v2ray.registry import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
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
    normalize_condition,
    parse_valid_fields,
    rel_path,
    validate_file_path,
)
from domain.config import (
    process_configs,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=CLI_V2RAY_CLEANER_DESCRIPTION,
        epilog=CLI_V2RAY_CLEANER_EPILOG,
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
        title=CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_GROUP_TITLE,
    )
    group_global.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help=CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_DEBUG,
    )
    group_global.add_argument(
        "--skip-normalize",
        action="store_true",
        default=False,
        dest="skip_normalize",
        help=CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_SKIP_NORMALIZE,
    )

    group_input_files = parser.add_argument_group(
        title=CLI_V2RAY_CLEANER_INPUT_FILES_GROUP_TITLE,
    )
    group_input_files.add_argument(
        "-I", "--configs-raw",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw_path",
        help=CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CONFIGS_RAW,
            ),
        ),
        metavar=CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )
    group_input_files.add_argument(
        "--import",
        const=abs_path(
            path=DEFAULT_PATH_CONFIGS_IMPORT,
        ),
        dest="import_path",
        help=CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CONFIGS_IMPORT,
            ),
        ),
        metavar=CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_METAVAR,
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    group_output_files = parser.add_argument_group(
        title=CLI_V2RAY_CLEANER_OUTPUT_FILES_GROUP_TITLE,
    )
    group_output_files.add_argument(
        "-O", "--configs-clean",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_CLEAN,
        ),
        dest="configs_clean_path",
        help=CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CONFIGS_CLEAN,
            ),
        ),
        metavar=CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_METAVAR,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )
    group_output_files.add_argument(
        "--export",
        const=abs_path(
            path=DEFAULT_PATH_CONFIGS_EXPORT,
        ),
        dest="export_path",
        help=CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_TEMPLATE.format(
            default=rel_path(
                path=DEFAULT_PATH_CONFIGS_EXPORT,
            ),
        ),
        metavar=CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_METAVAR,
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    group_config_processing = parser.add_argument_group(
        title=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_GROUP_TITLE,
    )
    group_config_processing.add_argument(
        "-D", "--duplicate",
        const="protocol, host, port",
        dest="duplicate",
        help=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE,
        metavar=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE_METAVAR,
        nargs="?",
        type=parse_valid_fields,
    )
    group_config_processing.add_argument(
        "-F", "--config-filter",
        dest="config_filter",
        help=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER,
        metavar=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER_METAVAR,
        type=normalize_condition,
    )
    group_config_processing.add_argument(
        "-R", "--reverse",
        action="store_true",
        default=False,
        dest="reverse",
        help=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_REVERSE,
    )
    group_config_processing.add_argument(
        "-S", "--sort",
        const="protocol",
        dest="sort",
        help=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT,
        metavar=CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT_METAVAR,
        nargs="?",
        type=parse_valid_fields,
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
    log_debug_object(
        obj=PATTERNS_V2RAY_URLS_BY_PROTOCOL,
        title=TEMPLATE_TITLE_COMPILED_URL_PATTERNS_BY_V2RAY_PROTOCOL.format(
            count=sum(
                len(patterns)
                for patterns in PATTERNS_V2RAY_URLS_BY_PROTOCOL.values()
            ),
        ),
    )

    return args


async def main() -> None:
    try:
        parsed_args = parse_args()

        io_ctx = IOContext(
            configs_clean_path=parsed_args.configs_clean_path,
            configs_raw_path=parsed_args.configs_raw_path,
        )

        configs = await load_configs(
            ctx=io_ctx,
            import_path=parsed_args.import_path,
            skip_normalize=parsed_args.skip_normalize,
        )

        processed_configs = process_configs(
            configs=configs,  # type: ignore[arg-type]
            args=parsed_args,
        )

        await save_configs(
            ctx=io_ctx,
            configs=processed_configs,
            export_path=parsed_args.export_path,
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
