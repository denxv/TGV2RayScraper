#!/usr/bin/env python
# coding: utf-8

import re
import subprocess
import sys
from pathlib import Path
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    HelpFormatter,
    Namespace,
    SUPPRESS,
)

from scripts.logger import logger, log_debug_object
from scripts.const import (
    SCRIPTS_CONFIG,
)

SCRIPTS_DIR = Path(__file__).parent / "scripts"


def collect_args(args: Namespace, flags: list[str]) -> list[str]:
    params = []
    for flag in flags:
        value = getattr(args, flag_to_name(flag), None)
        if value is not None:
            params.extend([flag] if not value else [flag, value])
    return params


def flag_to_name(flag: str) -> str:
    return flag.lstrip('-').replace('-', '_')


def int_in_range(value: str, min_value: int = 1, max_value: int = 100, \
    as_str: bool = False) -> int | str:
    ivalue = int(value)
    if ivalue < min_value or ivalue > max_value:
        raise ArgumentTypeError(f"Expected {min_value} to {max_value}, got {ivalue}")
    return str(ivalue) if as_str else ivalue


def normalize_valid_params(params: str) -> str:
    return ",".join(parse_valid_params(params)) if params.strip() else ""


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Run the complete proxy configuration collection and processing pipeline.",
        epilog=(
            "Show help for all internal scripts used in the pipeline. "
            "Example: python %(prog)s --help-scripts"
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=100,
        ),
    )

    parser.add_argument(
        "--batch-extract",
        help=SUPPRESS,
        type=lambda value: int_in_range(value, min_value=1, max_value=100, as_str=True),
    )

    parser.add_argument(
        "--batch-update",
        help=SUPPRESS,
        type=lambda value: int_in_range(value, min_value=1, max_value=1000, as_str=True),
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
        type=normalize_valid_params,
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
        type=normalize_valid_params,
    )

    parser.add_argument(
        "--urls",
        help=SUPPRESS,
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def parse_valid_params(params: str) -> list[str]:
    if not isinstance(params, str):
        raise ArgumentTypeError(f"Expected string, got {type(params).__name__!r}")

    seen = set()

    def check_param(param: str) -> str:
        if not re.fullmatch(r"\w+(?:\.\w+)*", param):
            raise ArgumentTypeError(f"Invalid parameter: {param!r}")
        if param in seen:
            raise ArgumentTypeError(f"Duplicate parameter: {param!r}")
        seen.add(param)
        return param

    valid_params = [
        check_param(param) 
        for param in re.split(r"[ ,]+", params.strip())
    ]

    if not valid_params:
        raise ArgumentTypeError("No parameters provided")

    return valid_params


def run_script(script_name: str = "async_scraper.py", args: list = []) -> None:
    repeat_count = 100
    logger.info(f"Starting script '{script_name}'...")
    logger.info('-' * repeat_count)

    arguments = [
        sys.executable, 
        str(SCRIPTS_DIR / script_name), 
        *args,
    ]
    if subprocess.run(args=arguments).returncode:
        raise Exception(f"Script '{script_name}' exited with an error!")

    logger.info('-' * repeat_count)
    logger.info(f"Script '{script_name}' completed successfully!")
    logger.info('=' * repeat_count)


def show_scripts_help() -> None:
    for script_name in SCRIPTS_CONFIG:
        run_script(script_name, args=["--help"])


def validate_file_path(path: str | Path, must_be_file: bool = True) -> str:
    filepath = Path(path).resolve()

    if not filepath.parent.exists():
        raise ArgumentTypeError(f"Parent directory does not exist: '{filepath.parent}'.")

    if filepath.exists() and filepath.is_dir():
        raise ArgumentTypeError(f"'{filepath}' is a directory, expected a file.")

    if must_be_file and not filepath.is_file():
        raise ArgumentTypeError(f"The file does not exist: '{filepath}'.")
    
    return str(filepath)


def main() -> None:
    try:
        parsed_args = parse_args()
        if parsed_args.help_scripts:
            return show_scripts_help()

        skipped_mode = "async" if parsed_args.no_async else "sync"
        for script_name, script_config in SCRIPTS_CONFIG.items():
            if script_config.get("mode") == skipped_mode:
                continue

            run_script(
                script_name=script_name, 
                args=collect_args(parsed_args, script_config.get("flags")),
            )
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == "__main__":
    main()
