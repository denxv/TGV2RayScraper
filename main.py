#!/usr/bin/env python

from argparse import ArgumentParser, HelpFormatter
from sys import executable
from subprocess import run

from core.constants import (
    CLI_SCRIPTS_CONFIG,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_LOG_LINE_LENGTH,
    SUPPRESS,
)
from core.logger import logger, log_debug_object
from core.typing import ArgsNamespace, CLIParams, FilePath, Optional
from core.utils import (
    collect_args,
    int_in_range,
    normalize_valid_fields,
    validate_file_path,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description="Run the complete proxy configuration collection and processing pipeline.",
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
        type=lambda value: int_in_range(
            value,
            min_value=1,
            max_value=100,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--batch-update",
        help=SUPPRESS,
        type=lambda value: int_in_range(
            value,
            min_value=1,
            max_value=1000,
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
        "-N", "--no-async",
        action="store_true",
        help=(
            "Use slower but simpler synchronous scraping mode "
            "instead of the default asynchronous mode."
        ),
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
        "--urls",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def run_script(script_name: str, script_args: Optional[CLIParams] = None) -> None:
    if script_args is None:
        script_args = list()

    logger.info(f"Starting script '{script_name}'...")
    logger.info('-' * DEFAULT_LOG_LINE_LENGTH)

    arguments = [
        executable,
        "-m",
        f"scripts.{script_name}",
        *script_args,
    ]

    log_debug_object("Script launch arguments", arguments)
    if run(args=arguments).returncode:
        raise Exception(f"Script '{script_name}' exited with an error!")

    logger.info('-' * DEFAULT_LOG_LINE_LENGTH)
    logger.info(f"Script '{script_name}' completed successfully!")
    logger.info('=' * DEFAULT_LOG_LINE_LENGTH)


def show_scripts_help() -> None:
    for script_name in CLI_SCRIPTS_CONFIG:
        run_script(script_name, args=["--help"])


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
                script_args=collect_args(parsed_args, script_config.get("flags")),
            )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == "__main__":
    main()
