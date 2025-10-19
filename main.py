from argparse import ArgumentParser, HelpFormatter
from subprocess import run
from sys import executable

from core.constants import (
    CHANNEL_MAX_BATCH_EXTRACT,
    CHANNEL_MAX_BATCH_UPDATE,
    CHANNEL_MAX_MESSAGE_OFFSET,
    CHANNEL_MIN_BATCH_EXTRACT,
    CHANNEL_MIN_BATCH_UPDATE,
    CHANNEL_MIN_MESSAGE_OFFSET,
    CLI_SCRIPTS_CONFIG,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    HTTP_MAX_TIMEOUT,
    HTTP_MIN_TIMEOUT,
    MESSAGE_EXIT,
    MESSAGE_UNEXPECTED_ERROR,
    SUPPRESS,
    TEMPLATE_MSG_ERROR_SCRIPT,
    TEMPLATE_MSG_SCRIPT_COMPLETED,
    TEMPLATE_MSG_SCRIPT_STARTED,
)
from core.logger import log_debug_object, logger
from core.typing import ArgsNamespace, CLIParams
from core.utils import (
    collect_args,
    convert_number_in_range,
    normalize_valid_fields,
    repeat_char_line,
    validate_file_path,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=(
            "Run the complete proxy configuration collection "
            "and processing pipeline."
        ),
        epilog=(
            "Show help for all internal scripts used in the pipeline. "
            "Example: python %(prog)s --help-scripts"
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
        ),
    )

    parser.add_argument(
        "--batch-extract",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value,
            min_value=CHANNEL_MIN_BATCH_EXTRACT,
            max_value=CHANNEL_MAX_BATCH_EXTRACT,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--batch-update",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value,
            min_value=CHANNEL_MIN_BATCH_UPDATE,
            max_value=CHANNEL_MAX_BATCH_UPDATE,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--channels",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "--configs-clean",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "--configs-raw",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "--delete-channels",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--duplicate",
        const="",
        help=SUPPRESS,
        nargs="?",
        type=normalize_valid_fields,
    )

    parser.add_argument(
        "--filter",
        help=SUPPRESS,
        type=str,
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-H", "--help-scripts",
        action="store_true",
        help="Display help information for all internal pipeline scripts.",
    )

    parser.add_argument(
        "--include-new",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--message-offset",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value,
            min_value=CHANNEL_MIN_MESSAGE_OFFSET,
            max_value=CHANNEL_MAX_MESSAGE_OFFSET,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "-N", "--no-async",
        action="store_true",
        help=(
            "Use slower but simpler synchronous scraping mode "
            "instead of the default asynchronous mode."
        ),
    )

    parser.add_argument(
        "--no-backup",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--no-dry-run",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--no-normalize",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--reverse",
        action="store_const",
        const="",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--sort",
        const="",
        help=SUPPRESS,
        nargs="?",
        type=normalize_valid_fields,
    )

    parser.add_argument(
        "--time-out",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value,
            min_value=HTTP_MIN_TIMEOUT,
            max_value=HTTP_MAX_TIMEOUT,
            as_int=False,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--urls",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def run_script(
    script_name: str,
    script_args: CLIParams | None = None,
) -> None:
    if script_args is None:
        script_args = []

    logger.info(TEMPLATE_MSG_SCRIPT_STARTED.format(name=script_name))
    logger.info(repeat_char_line(char="-"))

    arguments = [
        executable,
        "-m",
        f"scripts.{script_name}",
        *script_args,
    ]

    log_debug_object("Script launch arguments", arguments)
    if run(check=False, args=arguments).returncode:
        message = TEMPLATE_MSG_ERROR_SCRIPT.format(name=script_name)
        raise RuntimeError(message)

    logger.info(repeat_char_line(char="-"))
    logger.info(TEMPLATE_MSG_SCRIPT_COMPLETED.format(name=script_name))
    logger.info(repeat_char_line(char="="))


def show_scripts_help() -> None:
    for script_name in CLI_SCRIPTS_CONFIG:
        run_script(script_name, script_args=["--help"])


def main() -> None:
    try:
        parsed_args = parse_args()
        if parsed_args.help_scripts:
            return show_scripts_help()

        skipped_mode = "async" if parsed_args.no_async else "sync"
        for script_name, script_config in CLI_SCRIPTS_CONFIG.items():
            if script_config.get("mode") == skipped_mode:
                continue

            run_script(
                script_name=script_name,
                script_args=collect_args(
                    args=parsed_args,
                    flags=script_config.get("flags", []),
                ),
            )
    except KeyboardInterrupt:
        logger.info(MESSAGE_EXIT)
    except Exception:
        logger.exception(MESSAGE_UNEXPECTED_ERROR)


if __name__ == "__main__":
    main()
