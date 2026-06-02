from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    HelpFormatter,
)
from subprocess import (
    run as subprocess_run,
)
from sys import (
    executable,
)

from rich.rule import (
    Rule,
)

from core.constants.common import (
    CHANNELS_BATCH_MAX,
    CHANNELS_BATCH_MIN,
    CHANNELS_CONCURRENCY_MAX,
    CHANNELS_CONCURRENCY_MIN,
    CLI_SCRIPTS_CONFIG,
    CONFIGS_BATCH_MAX,
    CONFIGS_BATCH_MIN,
    DEFAULT_CHANNEL_VALUES,
    DEFAULT_HELP_INDENT,
    DEFAULT_HELP_WIDTH,
    DEFAULT_PATH_CONFIGS_EXPORT,
    DEFAULT_PATH_CONFIGS_IMPORT,
    DEFAULT_PROXY_URL,
    HTTP_RETRIES_MAX,
    HTTP_RETRIES_MIN,
    HTTP_RETRY_DELAY_MAX,
    HTTP_RETRY_DELAY_MIN,
    HTTP_TIMEOUT_MAX,
    HTTP_TIMEOUT_MIN,
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
from core.constants.templates.error import (
    TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION,
    TEMPLATE_ERROR_UNKNOWN_SCRIPT_NAMES,
)
from core.constants.templates.info.common import (
    TEMPLATE_INFO_SCRIPT_COMPLETED,
    TEMPLATE_INFO_SCRIPT_STARTED,
)
from core.terminal.console import (
    console,
)
from core.terminal.logger import (
    log_debug_object,
    logger,
    set_console_level,
)
from core.typing import (
    ArgsNamespace,
    CLIParams,
    ParamsStr,
    ScriptName,
    ScriptNames,
)
from core.utils import (
    collect_args,
    convert_number_in_range,
    normalize_condition,
    normalize_valid_fields,
    validate_file_path,
    validate_proxy_url,
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

    group_global = parser.add_argument_group(
        "Global options",
    )
    group_global.add_argument(
        "-D", "--debug",
        action="store_true",
        dest="debug",
        help=(
            "Enable debug logging in console. "
            "By default, console shows INFO level logs."
        ),
    )
    group_global.add_argument(
        "-H", "--help-scripts",
        const=list(CLI_SCRIPTS_CONFIG),
        dest="help_scripts",
        help=(
            "Display help information for internal pipeline scripts. "
            "Specify script names as a comma-separated list. "
            'Example: "scraper, v2ray_cleaner, update_channels". '
            "If used without value (e.g., '-H'), "
            "help is shown for all scripts. "
        ),
        metavar="NAMES",
        nargs="?",
        type=parse_script_names,
    )

    parser.add_argument(
        "--channel-filter",
        help=SUPPRESS,
        type=normalize_condition,
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
        "--channels-batch",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CHANNELS_BATCH_MIN,
            max_value=CHANNELS_BATCH_MAX,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--channels-concurrency",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CHANNELS_CONCURRENCY_MIN,
            max_value=CHANNELS_CONCURRENCY_MAX,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--config-filter",
        help=SUPPRESS,
        type=normalize_condition,
    )

    parser.add_argument(
        "--configs-batch",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=CONFIGS_BATCH_MIN,
            max_value=CONFIGS_BATCH_MAX,
            as_int=True,
            as_str=True,
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
            must_be_file=True,
        ),
    )

    parser.add_argument(
        "--delete-channels",
        action="store_true",
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
        "--export",
        const=DEFAULT_PATH_CONFIGS_EXPORT,
        help=SUPPRESS,
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=False,
        ),
    )

    parser.add_argument(
        "-h", "--help",
        action="help",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--import",
        const=DEFAULT_PATH_CONFIGS_IMPORT,
        help=SUPPRESS,
        nargs="?",
        type=lambda path: validate_file_path(
            path=path,
            must_be_file=True,
        ),
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
        "--no-dry-run",
        action="store_true",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--proxy",
        const=DEFAULT_PROXY_URL,
        help=SUPPRESS,
        nargs="?",
        type=validate_proxy_url,
    )

    parser.add_argument(
        "--reset-all",
        action="store_true",
        help=SUPPRESS,
    )

    for field in DEFAULT_CHANNEL_VALUES:
        parser.add_argument(
            f"--reset-{field.replace('_', '-')}",
            help=SUPPRESS,
            type=lambda value: convert_number_in_range(
                value=value,
                as_int=True,
                as_str=True,
            ),
        )

    parser.add_argument(
        "--retries",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_RETRIES_MIN,
            max_value=HTTP_RETRIES_MAX,
            as_int=True,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--retry-delay",
        help=SUPPRESS,
        type=lambda value: convert_number_in_range(
            value=value,
            min_value=HTTP_RETRY_DELAY_MIN,
            max_value=HTTP_RETRY_DELAY_MAX,
            as_int=False,
            as_str=True,
        ),
    )

    parser.add_argument(
        "--reverse",
        action="store_true",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--skip-normalize",
        action="store_true",
        help=SUPPRESS,
    )

    parser.add_argument(
        "--skip-update",
        action="store_true",
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

    set_console_level(
        logger=logger,
        debug=args.debug,
    )

    log_debug_object(
        obj=args,
        title="Parsed command-line arguments",
    )

    return args


def parse_script_names(
    script_names: ParamsStr,
) -> ScriptNames:
    normalized_script_names = normalize_valid_fields(
        params_str=script_names,
    )

    parsed_script_names = normalized_script_names.split(",")

    invalid_script_names = [
        script_name
        for script_name in parsed_script_names
        if script_name not in CLI_SCRIPTS_CONFIG
    ]

    if invalid_script_names:
        raise ArgumentTypeError(
            TEMPLATE_ERROR_UNKNOWN_SCRIPT_NAMES.format(
                names=", ".join(invalid_script_names),
            ),
        )

    return parsed_script_names


def run_script(
    script_name: ScriptName,
    script_args: CLIParams | None = None,
) -> None:
    script_args = script_args or []

    console.print(Rule(f"[bold cyan]{script_name}"))
    logger.info(
        msg=TEMPLATE_INFO_SCRIPT_STARTED.format(
            name=script_name,
        ),
    )

    arguments = [
        executable,
        "-m",
        f"scripts.{script_name}",
        *script_args,
    ]

    log_debug_object(
        obj=arguments,
        title="Script launch arguments",
    )

    if subprocess_run(
        args=arguments,
        check=False,
    ).returncode:
        raise RuntimeError(
            TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION.format(
                name=script_name,
            ),
        )

    logger.info(
        msg=TEMPLATE_INFO_SCRIPT_COMPLETED.format(
            name=script_name,
        ),
    )
    console.print(Rule(style="dim"))
    console.print()


def show_scripts_help(
    script_names: ScriptNames,
) -> None:
    for script_name in script_names or CLI_SCRIPTS_CONFIG:
        if script_name not in CLI_SCRIPTS_CONFIG:
            continue

        run_script(
            script_name=script_name,
            script_args=[
                "--help",
            ],
        )


def main() -> None:
    try:
        parsed_args = parse_args()

        if parsed_args.help_scripts is not None:
            return show_scripts_help(
                script_names=parsed_args.help_scripts,
            )

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
            msg=MESSAGE_INFO_PROGRAM_EXIT,
        )
    except Exception:
        logger.exception(
            msg=MESSAGE_ERROR_UNEXPECTED_FAILURE,
        )


if __name__ == "__main__":
    main()
