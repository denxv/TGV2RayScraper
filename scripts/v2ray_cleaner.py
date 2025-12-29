from argparse import (
    ArgumentParser,
    HelpFormatter,
)
from asyncio import (
    CancelledError,
    run,
)

from adapters.config import (
    load_configs,
    save_configs,
)
from core.constants.common import (
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CONFIGS_CLEAN,
    DEFAULT_PATH_CONFIGS_RAW,
    SUPPRESS,
)
from core.constants.messages import (
    MESSAGE_ERROR_PROGRAM_EXIT,
    MESSAGE_ERROR_UNEXPECTED_FAILURE,
)
from core.constants.patterns import (
    PATTERNS_V2RAY_URLS_BY_PROTOCOL,
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
    parse_valid_fields,
    validate_file_path,
)
from domain.config import (
    process_configs,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=(
            "Utility to normalize, filter, deduplicate, "
            "and sort proxy configuration entries."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s "
            "-I configs-raw.txt -O configs-clean.txt "
            "--filter \"re_search(r'speedtest|google', host)\" "
            '-D "host, port" -S "protocol, host, port"'
        ),
        formatter_class=lambda prog: HelpFormatter(
            prog=prog,
            max_help_position=DEFAULT_HELP_INDENT,
            width=DEFAULT_HELP_WIDTH,
        ),
    )

    parser.add_argument(
        "-D", "--duplicate",
        const="protocol,host,port",
        dest="duplicate",
        help=(
            "Remove duplicate entries by specified comma-separated fields. "
            "If used without value (e.g., '-D'), "
            "the default fields are '%(const)s'. "
            "If omitted, duplicates are not removed."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_fields,
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
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw",
        help=(
            "Path to the input file with raw V2Ray configs "
            "(default: %(default)s)."
        ),
        metavar="FILE",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    parser.add_argument(
        "-N", "--no-normalize",
        action="store_false",
        dest="normalize",
        help="Disable normalization (enabled by default).",
    )

    parser.add_argument(
        "-O", "--configs-clean",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_CLEAN,
        ),
        dest="configs_clean",
        help=(
            "Path to the output file for cleaned and processed configs "
            "(default: %(default)s)."
        ),
        metavar="FILE",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
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
            "If used without value (e.g., '-S'), "
            "the default fields are '%(const)s'. "
            "If omitted, entries are not sorted."
        ),
        metavar="FIELDS",
        nargs="?",
        type=parse_valid_fields,
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

        log_debug_object(
            title="Compiled URL regex patterns by V2Ray protocol",
            obj=PATTERNS_V2RAY_URLS_BY_PROTOCOL,
        )

        configs_raw = await load_configs(
            path_configs_raw=parsed_args.configs_raw,
        )

        configs_clean = process_configs(
            configs=configs_raw,
            args=parsed_args,
        )

        await save_configs(
            configs=configs_clean,
            path_configs_clean=parsed_args.configs_clean,
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
