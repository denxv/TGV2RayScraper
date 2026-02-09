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
    DEFAULT_PATH_CONFIGS_EXPORT,
    DEFAULT_PATH_CONFIGS_IMPORT,
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
    rel_path,
    validate_file_path,
)
from domain.config import (
    process_configs,
)


def parse_args() -> ArgsNamespace:
    parser = ArgumentParser(
        add_help=False,
        description=(
            "Utility for deduplicating, filtering, normalizing, "
            "and sorting proxy configuration entries."
        ),
        epilog=(
            "Example: PYTHONPATH=. python scripts/%(prog)s "
            "-I configs/v2ray-raw.txt -O configs/v2ray-clean.txt "
            "-F \"re_search(r'speedtest|google', host)\" --reverse "
            '-D "host, port" -S "protocol, host, port" '
            "--import configs/v2ray.json --export"
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

    group_input_files = parser.add_argument_group(
        "Input files",
    )
    group_input_files.add_argument(
        "-I", "--configs-raw",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_RAW,
        ),
        dest="configs_raw_path",
        help=(
            "Path to the input TXT file with raw V2Ray configs for parsing "
            f"(default: {rel_path(DEFAULT_PATH_CONFIGS_RAW)})."
        ),
        metavar="PATH",
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
        help=(
            "Path to the input JSON file with already parsed configs. "
            "If empty or invalid, raw configs will be parsed instead "
            f"(default: {rel_path(DEFAULT_PATH_CONFIGS_IMPORT)})."
        ),
        metavar="PATH",
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
    )

    group_output_files = parser.add_argument_group(
        "Output files",
    )
    group_output_files.add_argument(
        "-O", "--configs-clean",
        default=abs_path(
            path=DEFAULT_PATH_CONFIGS_CLEAN,
        ),
        dest="configs_clean_path",
        help=(
            "Path to the output TXT file for cleaned and processed configs "
            f"(default: {rel_path(DEFAULT_PATH_CONFIGS_CLEAN)})."
        ),
        metavar="PATH",
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
        help=(
            "Path to the output JSON file for exporting parsed configs "
            "for later reuse without re-parsing raw input "
            f"(default: {rel_path(DEFAULT_PATH_CONFIGS_EXPORT)})."
        ),
        metavar="PATH",
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    group_normalization = parser.add_argument_group(
        "Normalization options",
    )
    group_normalization.add_argument(
        "-N", "--no-normalize",
        action="store_false",
        dest="normalize",
        help=(
            "Disable normalization of configs. "
            "By default, normalization is enabled."
        ),
    )

    group_filter_sort = parser.add_argument_group(
        "Filter / Sort",
    )
    group_filter_sort.add_argument(
        "-D", "--duplicate",
        const="protocol, host, port",
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
    group_filter_sort.add_argument(
        "-F", "--config-filter",
        dest="config_filter",
        help=(
            "Filter entries using a Python-like condition. "
            "Example: \"host == '1.1.1.1' and port > 1000\". "
            "Only matching entries are kept. "
            "If omitted, no filtering is applied."
        ),
        metavar="CONDITION",
        type=str,
    )
    group_filter_sort.add_argument(
        "-R", "--reverse",
        action="store_true",
        dest="reverse",
        help="Sort in descending order (only applies with --sort).",
    )
    group_filter_sort.add_argument(
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

        configs = await load_configs(
            configs_path=parsed_args.configs_raw_path,
            import_path=parsed_args.import_path,
            normalize=parsed_args.normalize,
        )

        processed_configs = process_configs(
            configs=configs,  # type: ignore[arg-type]
            args=parsed_args,
        )

        await save_configs(
            configs=processed_configs,
            configs_path=parsed_args.configs_clean_path,
            export_path=parsed_args.export_path,
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
