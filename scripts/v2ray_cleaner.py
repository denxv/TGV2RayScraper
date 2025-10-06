#!/usr/bin/env python

from argparse import ArgumentParser, HelpFormatter, Namespace, SUPPRESS

from adapters.sync.configs import load_configs, save_configs
from core.logger import logger, log_debug_object
from core.constants import DEFAULT_PATH_CONFIGS_CLEAN, DEFAULT_PATH_CONFIGS_RAW, URL_PATTERNS
from core.utils import abs_path, parse_valid_params, validate_file_path
from domain.config import process_configs


def parse_args() -> Namespace:
    parser = ArgumentParser(
        add_help=False,
        description="Utility to normalize, filter, deduplicate, and sort proxy configuration entries.",
        epilog=(
            "Example: python %(prog)s -I configs-raw.txt -O configs-clean.txt --filter "
            "\"re_search(r'speedtest|google', host)\" -D \"host, port\" -S \"protocol, host, port\""
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=30,
            width=120,
        ),
    )

    parser.add_argument(
        "-D", "--duplicate",
        const="protocol,host,port",
        dest="duplicate",
        help=(
            "Remove duplicate entries by specified comma-separated fields. "
            "If used without value (e.g., '-D'), the default fields are '%(const)s'. "
            "If omitted, duplicates are not removed."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_params,
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "-F", "--filter",
        dest="filter",
        help=(
            "Filter entries using a Python-like condition. "
            "Example: \"host == '1.1.1.1' and port > 1000\". "
            "Only matching entries are kept. "
            "If omitted, no filtering is applied."
        ),
        metavar="CONDITION",
        type=str,
    )

    parser.add_argument(
        "-I", "--configs-raw",
        default=abs_path(DEFAULT_PATH_CONFIGS_RAW),
        dest="configs_raw",
        help="Path to the input file with raw V2Ray configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=True),
    )

    parser.add_argument(
        "-N", "--no-normalize",
        action="store_false",
        dest="normalize",
        help="Disable normalization (enabled by default).",
    )

    parser.add_argument(
        "-O", "--configs-clean",
        default=abs_path(DEFAULT_PATH_CONFIGS_CLEAN),
        dest="configs_clean",
        help="Path to the output file for cleaned and processed configs (default: %(default)s).",
        metavar="FILE",
        type=lambda path: validate_file_path(path, must_be_file=False),
    )

    parser.add_argument(
        "-R", "--reverse",
        action="store_true",
        dest="reverse",
        help="Sort in descending order (only applies with --sort).",
    )

    parser.add_argument(
        "-S", "--sort",
        const="protocol",
        dest="sort",
        help=(
            "Sort entries by comma-separated fields. "
            "If used without value (e.g., '-S'), the default fields are '%(const)s'. "
            "If omitted, entries are not sorted."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_params,
    )

    args = parser.parse_args()
    log_debug_object("Parsed command-line arguments", args)

    return args


def main() -> None:
    try:
        log_debug_object("List of compiled URL regex patterns", URL_PATTERNS)
        parsed_args = parse_args()
        configs = load_configs(path_configs_raw=parsed_args.configs_raw)
        configs = process_configs(configs=configs, args=parsed_args)
        save_configs(configs=configs, path_configs_clean=parsed_args.configs_clean)
    except KeyboardInterrupt:
        logger.info("Exit from the program.")
    except Exception:
        logger.exception("Unexpected error occurred.")


if __name__ == '__main__':
    main()
