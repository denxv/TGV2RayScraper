from argparse import (
    ArgumentParser,
    HelpFormatter,
)
from subprocess import (
    run,
)
from sys import (
    executable,
)

from core.constants.common import (
    BATCH_EXTRACT_MAX,
    BATCH_EXTRACT_MIN,
    BATCH_UPDATE_MAX,
    BATCH_UPDATE_MIN,
    CLI_SCRIPTS_CONFIG,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    HTTP_TIMEOUT_MAX,
    HTTP_TIMEOUT_MIN,
    MESSAGE_OFFSET_MAX,
    MESSAGE_OFFSET_MIN,
    SUPPRESS,
)
from core.constants.messages import (
    MESSAGE_ERROR_PROGRAM_EXIT,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
)
from core.constants.templates import (
    TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION,
    TEMPLATE_MSG_SCRIPT_COMPLETED,
    TEMPLATE_MSG_SCRIPT_STARTED,
)
from core.logger import (
    log_debug_object,
    logger,
)
from core.typing import (
    ArgsNamespace,
    CLIParams,
)
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
            value=value,
            min_value=BATCH_EXTRACT_MIN,
            max_value=BATCH_EXTRACT_MAX,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--batch-update",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=BATCH_UPDATE_MIN,
            max_value=BATCH_UPDATE_MAX,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--channels",
        help=SUPPRESS,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    parser.add_argument(
        "--configs-clean",
        help=SUPPRESS,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    parser.add_argument(
        "--configs-raw",
        help=SUPPRESS,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
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
        "--message-offset",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=MESSAGE_OFFSET_MIN,
            max_value=MESSAGE_OFFSET_MAX,
            as_int=True,
            as_str=True,
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
            value=value,
            min_value=HTTP_TIMEOUT_MIN,
            max_value=HTTP_TIMEOUT_MAX,
            as_int=False,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--urls",
        help=SUPPRESS,
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    args = parser.parse_args()
    log_debug_object(
        title="Parsed command-line arguments",
        obj=args,
    )

    return args


def run_script(
    script_name: str,
    script_args: CLIParams | None = None,
) -> None:
    if script_args is None:
        script_args = []

    logger.info(
        msg=TEMPLATE_MSG_SCRIPT_STARTED.format(
            name=script_name,
        ),
    )
    logger.info(
        msg=repeat_char_line(
            char="-",
        ),
    )

    arguments = [
        executable,
        "-m",
        f"scripts.{script_name}",
        *script_args,
    ]

    log_debug_object(
        title="Script launch arguments",
        obj=arguments,
    )
    if run(
        check=False,
        args=arguments,
    ).returncode:
        raise RuntimeError(
            TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION.format(
                name=script_name,
            ),
        )

    logger.info(
        msg=repeat_char_line(
            char="-",
        ),
    )
    logger.info(
        msg=TEMPLATE_MSG_SCRIPT_COMPLETED.format(
            name=script_name,
        ),
    )
    logger.info(
        msg=repeat_char_line(
            char="=",
        ),
    )


def show_scripts_help() -> None:
    for script_name in CLI_SCRIPTS_CONFIG:
        run_script(
            script_name=script_name,
            script_args=[
                "--help",
            ],
        )


def main() -> None:
    try:
        parsed_args = parse_args()
        if parsed_args.help_scripts:
            return show_scripts_help()

        for script_name, script_config in CLI_SCRIPTS_CONFIG.items():
            run_script(
                script_name=script_name,
                script_args=collect_args(
                    args=parsed_args,
                    flags=script_config.get("flags", []),
                ),
            )
    except KeyboardInterrupt:
        logger.info(
            msg=MESSAGE_ERROR_PROGRAM_EXIT,
        )
    except Exception:
        logger.exception(
            msg=MESSAGE_ERROR_UNEXPECTED_FAILURE,
        )


if __name__ == "__main__":
    main()
