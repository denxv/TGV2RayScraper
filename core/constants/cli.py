from core.typing import (
    CLIStr,
)

__all__ = [
    "CLI_MAIN_DESCRIPTION",
    "CLI_MAIN_EPILOG",
    "CLI_MAIN_GLOBAL_OPTIONS_DEBUG",
    "CLI_MAIN_GLOBAL_OPTIONS_GROUP_TITLE",
    "CLI_MAIN_GLOBAL_OPTIONS_HELP_SCRIPTS",
    "CLI_MAIN_GLOBAL_OPTIONS_HELP_SCRIPTS_METAVAR",
    "CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH",
    "CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH_METAVAR",
    "CLI_SCRAPER_CHANNEL_UPDATE_GROUP_TITLE",
    "CLI_SCRAPER_CHANNEL_UPDATE_SKIP",
    "CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY",
    "CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY_METAVAR",
    "CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH",
    "CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH_METAVAR",
    "CLI_SCRAPER_CONFIG_EXTRACT_GROUP_TITLE",
    "CLI_SCRAPER_DESCRIPTION",
    "CLI_SCRAPER_EPILOG",
    "CLI_SCRAPER_GLOBAL_OPTIONS_DEBUG",
    "CLI_SCRAPER_GLOBAL_OPTIONS_GROUP_TITLE",
    "CLI_SCRAPER_HTTP_CLIENT_GROUP_TITLE",
    "CLI_SCRAPER_HTTP_CLIENT_PROXY",
    "CLI_SCRAPER_HTTP_CLIENT_PROXY_METAVAR",
    "CLI_SCRAPER_HTTP_CLIENT_RETRIES",
    "CLI_SCRAPER_HTTP_CLIENT_RETRIES_METAVAR",
    "CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY",
    "CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY_METAVAR",
    "CLI_SCRAPER_HTTP_CLIENT_TIME_OUT",
    "CLI_SCRAPER_HTTP_CLIENT_TIME_OUT_METAVAR",
    "CLI_SCRAPER_IO_FILES_CHANNELS_METAVAR",
    "CLI_SCRAPER_IO_FILES_CHANNELS_TEMPLATE",
    "CLI_SCRAPER_IO_FILES_CONFIGS_RAW_METAVAR",
    "CLI_SCRAPER_IO_FILES_CONFIGS_RAW_TEMPLATE",
    "CLI_SCRAPER_IO_FILES_GROUP_TITLE",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_DELETE_CHANNELS",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_DESCRIPTION",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_TITLE",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_RESET_ALL",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_METAVAR",
    "CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_TEMPLATE",
    "CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER",
    "CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER_METAVAR",
    "CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_DESCRIPTION",
    "CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_TITLE",
    "CLI_UPDATE_CHANNELS_DESCRIPTION",
    "CLI_UPDATE_CHANNELS_EPILOG",
    "CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_DEBUG",
    "CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_GROUP_TITLE",
    "CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_NO_DRY_RUN",
    "CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_SKIP_BACKUP",
    "CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_METAVAR",
    "CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_TEMPLATE",
    "CLI_UPDATE_CHANNELS_INPUT_FILES_GROUP_TITLE",
    "CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_METAVAR",
    "CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_TEMPLATE",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE_METAVAR",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER_METAVAR",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_GROUP_TITLE",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_REVERSE",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT",
    "CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT_METAVAR",
    "CLI_V2RAY_CLEANER_DESCRIPTION",
    "CLI_V2RAY_CLEANER_EPILOG",
    "CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_DEBUG",
    "CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_GROUP_TITLE",
    "CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_SKIP_NORMALIZE",
    "CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_METAVAR",
    "CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_TEMPLATE",
    "CLI_V2RAY_CLEANER_INPUT_FILES_GROUP_TITLE",
    "CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_METAVAR",
    "CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_TEMPLATE",
    "CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_METAVAR",
    "CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_TEMPLATE",
    "CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_METAVAR",
    "CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_TEMPLATE",
    "CLI_V2RAY_CLEANER_OUTPUT_FILES_GROUP_TITLE",
]

CLI_MAIN_DESCRIPTION: CLIStr = (
    "Run the complete proxy configuration collection "
    "and processing pipeline."
)
CLI_MAIN_EPILOG: CLIStr = (
    "Show help for all internal scripts used in the pipeline. "
    "Example: python %(prog)s --help-scripts"
)
CLI_MAIN_GLOBAL_OPTIONS_DEBUG: CLIStr = (
    "Enable debug logging in console. "
    "By default, console shows INFO level logs."
)
CLI_MAIN_GLOBAL_OPTIONS_GROUP_TITLE: CLIStr = (
    "Global options"
)
CLI_MAIN_GLOBAL_OPTIONS_HELP_SCRIPTS: CLIStr = (
    "Display help information for internal pipeline scripts. "
    "Specify script names as a comma-separated list. "
    'Example: "scraper, v2ray_cleaner, update_channels". '
    "If used without value (e.g., '-H'), "
    "help is shown for all scripts."
)
CLI_MAIN_GLOBAL_OPTIONS_HELP_SCRIPTS_METAVAR: CLIStr = (
    "NAMES"
)
CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH: CLIStr = (
    "Number of channels processed per batch during update "
    "(default: %(default)s)."
)
CLI_SCRAPER_CHANNEL_UPDATE_CHANNELS_BATCH_METAVAR: CLIStr = (
    "N"
)
CLI_SCRAPER_CHANNEL_UPDATE_GROUP_TITLE: CLIStr = (
    "Channel update pipeline"
)
CLI_SCRAPER_CHANNEL_UPDATE_SKIP: CLIStr = (
    "Skip updating channel information. "
    "Avoids redundant requests if channels are already updated. "
    "By default, channels are updated."
)
CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY: CLIStr = (
    "Maximum number of channels processed concurrently "
    "during config extraction (default: %(default)s)."
)
CLI_SCRAPER_CONFIG_EXTRACT_CHANNELS_CONCURRENCY_METAVAR: CLIStr = (
    "N"
)
CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH: CLIStr = (
    "Number of messages processed per batch for config extraction "
    "(default: %(default)s)."
)
CLI_SCRAPER_CONFIG_EXTRACT_CONFIGS_BATCH_METAVAR: CLIStr = (
    "N"
)
CLI_SCRAPER_CONFIG_EXTRACT_GROUP_TITLE: CLIStr = (
    "Config extraction pipeline"
)
CLI_SCRAPER_DESCRIPTION: CLIStr = (
    "Asynchronous Telegram channel scraper (stable and fast)."
)
CLI_SCRAPER_EPILOG: CLIStr = (
    "Example: PYTHONPATH=. python scripts/scraper.py "
    "-C channels/current.json -R configs/v2ray-raw.txt "
    "-E 20 -U 100 --proxy --time-out 30.0 --skip-update"
)
CLI_SCRAPER_GLOBAL_OPTIONS_DEBUG: CLIStr = (
    "Enable debug logging in console. "
    "By default, console shows INFO level logs."
)
CLI_SCRAPER_GLOBAL_OPTIONS_GROUP_TITLE: CLIStr = (
    "Global options"
)
CLI_SCRAPER_HTTP_CLIENT_GROUP_TITLE: CLIStr = (
    "HTTP Client"
)
CLI_SCRAPER_HTTP_CLIENT_PROXY: CLIStr = (
    "Proxy server URL. Takes precedence over environment variables. "
    "Otherwise checks HTTPS_PROXY, HTTP_PROXY, and ALL_PROXY. "
    "Falls back to local proxy if none are set (default: %(const)s)."
)
CLI_SCRAPER_HTTP_CLIENT_PROXY_METAVAR: CLIStr = (
    "URL"
)
CLI_SCRAPER_HTTP_CLIENT_RETRIES: CLIStr = (
    "Maximum number of HTTP request retry attempts after failures "
    "(default: %(default)s)."
)
CLI_SCRAPER_HTTP_CLIENT_RETRIES_METAVAR: CLIStr = (
    "N"
)
CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY: CLIStr = (
    "Delay between HTTP retry attempts when request fetching fails "
    "(default: %(default)s)."
)
CLI_SCRAPER_HTTP_CLIENT_RETRY_DELAY_METAVAR: CLIStr = (
    "SECONDS"
)
CLI_SCRAPER_HTTP_CLIENT_TIME_OUT: CLIStr = (
    "HTTP client timeout in seconds for requests used "
    "while updating channel info and "
    "extracting V2Ray configurations (default: %(default)s)."
)
CLI_SCRAPER_HTTP_CLIENT_TIME_OUT_METAVAR: CLIStr = (
    "SECONDS"
)
CLI_SCRAPER_IO_FILES_CHANNELS_METAVAR: CLIStr = (
    "PATH"
)
CLI_SCRAPER_IO_FILES_CHANNELS_TEMPLATE: CLIStr = (
    "Path to the input JSON file containing the list of channels "
    "(default: {default!r})."
)
CLI_SCRAPER_IO_FILES_CONFIGS_RAW_METAVAR: CLIStr = (
    "PATH"
)
CLI_SCRAPER_IO_FILES_CONFIGS_RAW_TEMPLATE: CLIStr = (
    "Path to the output TXT file for saving scraped V2Ray configs "
    "(default: {default!r})."
)
CLI_SCRAPER_IO_FILES_GROUP_TITLE: CLIStr = (
    "Input / Output files"
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_DELETE_CHANNELS: CLIStr = (
    "Delete channels matching the filter. "
    "If no filter is specified, deletes unavailable channels "
    "and channels without configuration. "
    "By default, deletion is disabled."
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_DESCRIPTION: CLIStr = (
    "Only one action can be specified per invocation. "
    "Deletion cannot be combined with reset/set options. "
    "Reset and set options can be combined with each other."
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_GROUP_TITLE: CLIStr = (
    "Channel actions"
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_RESET_ALL: CLIStr = (
    "Reset all channel values to their defaults "
    "for filtered channels. Can be combined with --set-<field>. "
    "Without a filter, applies to available non-new channels."
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_METAVAR: CLIStr = (
    "N"
)
CLI_UPDATE_CHANNELS_CHANNEL_ACTIONS_SET_FIELD_TEMPLATE: CLIStr = (
    "Set {field!r} to the specified value. "
    "If no value is provided, the default value is used "
    "(default: %(const)s)."
)
CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER: CLIStr = (
    "Filter channels using a Python-like condition. Example: "
    '"count < 100 and current_id == last_id or state == -1". '
    "If omitted, all existing channels "
    "except new ones will be selected."
)
CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_FILTER_METAVAR: CLIStr = (
    "CONDITION"
)
CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_DESCRIPTION: CLIStr = (
    "Common filter for all actions. "
    "If omitted, a built-in default is used per action."
)
CLI_UPDATE_CHANNELS_CHANNEL_SELECTION_GROUP_TITLE: CLIStr = (
    "Channel selection options"
)
CLI_UPDATE_CHANNELS_DESCRIPTION: CLIStr = (
    "Backup channels, merge new URLs, and modify channels "
    "by filter: set or reset fields, or delete unavailable channels."
)
CLI_UPDATE_CHANNELS_EPILOG: CLIStr = (
    "Example: PYTHONPATH=. python scripts/update_channels.py "
    "-C channels/current.json -U channels/urls.txt "
    '-F "count < 100" --set-current-id -100'
)
CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_DEBUG: CLIStr = (
    "Enable debug logging in console. "
    "By default, console shows INFO level logs."
)
CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_GROUP_TITLE: CLIStr = (
    "Global options"
)
CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_NO_DRY_RUN: CLIStr = (
    "Disable dry-run mode and allow modifying channel metadata, "
    "including setting and resetting fields such as "
    "'count', 'last_id', 'current_id', and 'state'. "
    "By default, dry-run mode is enabled."
)
CLI_UPDATE_CHANNELS_GLOBAL_OPTIONS_SKIP_BACKUP: CLIStr = (
    "Skip creating backup files for channel and Telegram URL lists. "
    "By default, backup is created."
)
CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_METAVAR: CLIStr = (
    "PATH"
)
CLI_UPDATE_CHANNELS_INPUT_FILES_CHANNELS_TEMPLATE: CLIStr = (
    "Path to the input JSON file containing the list of channels "
    "(default: {default!r})."
)
CLI_UPDATE_CHANNELS_INPUT_FILES_GROUP_TITLE: CLIStr = (
    "Input files"
)
CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_METAVAR: CLIStr = (
    "PATH"
)
CLI_UPDATE_CHANNELS_INPUT_FILES_URLS_TEMPLATE: CLIStr = (
    "Path to the input TXT file containing new channel URLs "
    "(default: {default!r})."
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE: CLIStr = (
    "Remove duplicate entries by specified comma-separated fields. "
    "If used without value (e.g., '-D'), "
    "the default fields are '%(const)s'. "
    "If omitted, duplicates are not removed."
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_DUPLICATE_METAVAR: CLIStr = (
    "FIELDS"
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER: CLIStr = (
    "Filter entries using a Python-like condition. "
    "Example: \"host == '1.1.1.1' and port > 1000\". "
    "Only matching entries are kept. "
    "If omitted, no filtering is applied."
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_FILTER_METAVAR: CLIStr = (
    "CONDITION"
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_GROUP_TITLE: CLIStr = (
    "Configuration processing"
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_REVERSE: CLIStr = (
    "Sort in descending order (only applies with --sort)."
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT: CLIStr = (
    "Sort entries by comma-separated fields. "
    "If used without value (e.g., '-S'), "
    "the default fields are '%(const)s'. "
    "If omitted, entries are not sorted."
)
CLI_V2RAY_CLEANER_CONFIG_PROCESSING_SORT_METAVAR: CLIStr = (
    "FIELDS"
)
CLI_V2RAY_CLEANER_DESCRIPTION: CLIStr = (
    "Utility for deduplicating, filtering, normalizing, "
    "and sorting proxy configuration entries."
)
CLI_V2RAY_CLEANER_EPILOG: CLIStr = (
    "Example: PYTHONPATH=. python scripts/v2ray_cleaner.py "
    "-I configs/v2ray-raw.txt -O configs/v2ray-clean.txt "
    "-F \"re_search(r'speedtest|google', host)\" --reverse "
    '-D "host, port" -S "protocol, host, port" '
    "--import configs/v2ray.json --export"
)
CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_DEBUG: CLIStr = (
    "Enable debug logging in console. "
    "By default, console shows INFO level logs."
)
CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_GROUP_TITLE: CLIStr = (
    "Global options"
)
CLI_V2RAY_CLEANER_GLOBAL_OPTIONS_SKIP_NORMALIZE: CLIStr = (
    "Skip config normalization to preserve their original structure. "
    "By default, normalization is enabled."
)
CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_METAVAR: CLIStr = (
    "PATH"
)
CLI_V2RAY_CLEANER_INPUT_FILES_CONFIGS_RAW_TEMPLATE: CLIStr = (
    "Path to the input TXT file with raw V2Ray configs for parsing "
    "(default: {default!r})."
)
CLI_V2RAY_CLEANER_INPUT_FILES_GROUP_TITLE: CLIStr = (
    "Input files"
)
CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_METAVAR: CLIStr = (
    "PATH"
)
CLI_V2RAY_CLEANER_INPUT_FILES_IMPORT_TEMPLATE: CLIStr = (
    "Path to the input JSON file with already parsed configs. "
    "If empty or invalid, raw configs will be parsed instead "
    "(default: {default!r})."
)
CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_METAVAR: CLIStr = (
    "PATH"
)
CLI_V2RAY_CLEANER_OUTPUT_FILES_CONFIGS_CLEAN_TEMPLATE: CLIStr = (
    "Path to the output TXT file for cleaned and processed configs "
    "(default: {default!r})."
)
CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_METAVAR: CLIStr = (
    "PATH"
)
CLI_V2RAY_CLEANER_OUTPUT_FILES_EXPORT_TEMPLATE: CLIStr = (
    "Path to the output JSON file for exporting parsed configs "
    "for later reuse without re-parsing raw input "
    "(default: {default!r})."
)
CLI_V2RAY_CLEANER_OUTPUT_FILES_GROUP_TITLE: CLIStr = (
    "Output files"
)
