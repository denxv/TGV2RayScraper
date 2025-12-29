from core.constants.common import (
    TEXT_LENGTH_MSG_OFFSET,
    TEXT_LENGTH_NAME,
    TEXT_LENGTH_NUMBER,
)

__all__ = [
    "TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED",
    "TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED",
    "TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED",
    "TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED",
    "TEMPLATE_CHANNEL_COUNT_DIFFERENCE",
    "TEMPLATE_CHANNEL_LEFT_TO_CHECK",
    "TEMPLATE_CHANNEL_LOG_STATUS",
    "TEMPLATE_CHANNEL_LOG_UPDATE",
    "TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED",
    "TEMPLATE_CHANNEL_SAVE_COMPLETED",
    "TEMPLATE_CHANNEL_TOTAL_AVAILABLE",
    "TEMPLATE_CHANNEL_TOTAL_MESSAGES",
    "TEMPLATE_CHANNEL_UPDATE_INFO_STARTED",
    "TEMPLATE_CONFIG_DEDUPLICATION_COMPLETED",
    "TEMPLATE_CONFIG_DEDUPLICATION_STARTED",
    "TEMPLATE_CONFIG_EXTRACT_COMPLETED",
    "TEMPLATE_CONFIG_EXTRACT_STARTED",
    "TEMPLATE_CONFIG_FILTER_COMPLETED",
    "TEMPLATE_CONFIG_FILTER_STARTED",
    "TEMPLATE_CONFIG_LOAD_COMPLETED",
    "TEMPLATE_CONFIG_LOAD_STARTED",
    "TEMPLATE_CONFIG_LOG_EXTRACT",
    "TEMPLATE_CONFIG_NORMALIZE_COMPLETED",
    "TEMPLATE_CONFIG_NORMALIZE_STARTED",
    "TEMPLATE_CONFIG_SAVE_COMPLETED",
    "TEMPLATE_CONFIG_SAVE_STARTED",
    "TEMPLATE_CONFIG_SORT_COMPLETED",
    "TEMPLATE_CONFIG_SORT_STARTED",
    "TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS",
    "TEMPLATE_ERROR_CONFIG_UNEXPECTED_FAILURE",
    "TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED",
    "TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD",
    "TEMPLATE_ERROR_EXPECTED_FILE",
    "TEMPLATE_ERROR_EXPECTED_STRING",
    "TEMPLATE_ERROR_FAILED_EXTRACT_POST_ID",
    "TEMPLATE_ERROR_FAILED_FETCH_ID",
    "TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION",
    "TEMPLATE_ERROR_FAILED_SERIALIZATION",
    "TEMPLATE_ERROR_FILE_NOT_EXIST",
    "TEMPLATE_ERROR_INVALID_FIELD",
    "TEMPLATE_ERROR_INVALID_NUMBER",
    "TEMPLATE_ERROR_INVALID_OFFSET",
    "TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE",
    "TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST",
    "TEMPLATE_ERROR_RESPONSE_EMPTY",
    "TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED",
    "TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED",
    "TEMPLATE_FORMAT_CONFIG_NAME",
    "TEMPLATE_FORMAT_CONFIG_SSR_BODY",
    "TEMPLATE_FORMAT_CONFIG_URL",
    "TEMPLATE_FORMAT_CONFIG_URL_BODY",
    "TEMPLATE_FORMAT_CONFIG_URL_LOCATION",
    "TEMPLATE_FORMAT_FILE_BACKUP_NAME",
    "TEMPLATE_FORMAT_FILE_LOG_PATH",
    "TEMPLATE_FORMAT_STRING_BASE64_PADDING",
    "TEMPLATE_FORMAT_STRING_COLORED_LEVEL",
    "TEMPLATE_FORMAT_STRING_QUOTED_NAME",
    "TEMPLATE_FORMAT_TG_URL",
    "TEMPLATE_FORMAT_TG_URL_AFTER",
    "TEMPLATE_MSG_FILE_BACKUP_COMPLETED",
    "TEMPLATE_MSG_SCRIPT_COMPLETED",
    "TEMPLATE_MSG_SCRIPT_STARTED",
    "TEMPLATE_TITLE_DEBUG_OFFSET",
    "TEMPLATE_TITLE_DELETING_CHANNEL",
    "TEMPLATE_TITLE_OBJECT_PRETTY_PRINT",
]

TEMPLATE_CHANNEL_ASSIGNMENT_APPLIED = (
    f"Channel {{name:<{TEXT_LENGTH_NAME + 2}}}"
    " | "
    "applied offset = {offset}"
    " | "
    "current_id normalized."
)
TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_APPLIED = (
    "{message}"
    " - "
    "assignment applied."
)
TEMPLATE_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED = (
    f"Channel {{name:<{TEXT_LENGTH_NAME + 2}}}"
    " | "
    f"ID diff = {{diff:<{TEXT_LENGTH_MSG_OFFSET}}}"
    " | "
    f"offset = {{offset:<{TEXT_LENGTH_MSG_OFFSET}}}"
    " | "
    "skipped messages due to diff > offset."
)
TEMPLATE_CHANNEL_ASSIGNMENT_SKIPPED = (
    "Skipping assignment because check_only={check_only}."
)
TEMPLATE_CHANNEL_COUNT_DIFFERENCE = (
    "Old count: {old_size:,}"
    " | "
    "New count: {new_size:,}"
    " | "
    "({diff:+,})"
)
TEMPLATE_CHANNEL_LEFT_TO_CHECK = (
    "Channels left to check: {count:,}."
)
TEMPLATE_CHANNEL_LOG_STATUS = (
    "| <SS> | "
    f"{{name:<{TEXT_LENGTH_NAME}}}"
    " | "
    f"{{current_id:>{TEXT_LENGTH_NUMBER},}}"
    " / "
    f"{{last_id:<{TEXT_LENGTH_NUMBER},}}"
    " | "
    "({diff:+,})"
)
TEMPLATE_CHANNEL_LOG_UPDATE = (
    "| <UU> | "
    f"{{name:<{TEXT_LENGTH_NAME}}}"
    " | "
    f"{{last_id:>{TEXT_LENGTH_NUMBER},}}"
    " -> "
    f"{{last_post_id:<{TEXT_LENGTH_NUMBER},}}"
    " |"
)
TEMPLATE_CHANNEL_MISSING_ADD_COMPLETED = (
    "Channel '{name}' missing, adding to list."
)
TEMPLATE_CHANNEL_SAVE_COMPLETED = (
    "Saved {count:,} channels in '{path}'."
)
TEMPLATE_CHANNEL_TOTAL_AVAILABLE = (
    "Total channels are available for extracting configs: {count:,}."
)
TEMPLATE_CHANNEL_TOTAL_MESSAGES = (
    "Total messages on channels: {count:,}."
)
TEMPLATE_CHANNEL_UPDATE_INFO_STARTED = (
    "Updating channel information for {count:,} channels..."
)
TEMPLATE_CONFIG_DEDUPLICATION_COMPLETED = (
    "Duplicate removal completed:"
    " "
    "{remain:,} configs remain, {removed:,} removed."
)
TEMPLATE_CONFIG_DEDUPLICATION_STARTED = (
    "Removing duplicates from {count:,} configs using keys: {fields}..."
)
TEMPLATE_CONFIG_EXTRACT_COMPLETED = (
    "Extracted {configs_count:,} configs from {channels_count:,} channels."
)
TEMPLATE_CONFIG_EXTRACT_STARTED = (
    "Extracting configs from {count:,} channels..."
)
TEMPLATE_CONFIG_FILTER_COMPLETED = (
    "Filtered: {count:,} configs kept, {removed:,} removed by condition."
)
TEMPLATE_CONFIG_FILTER_STARTED = (
    "Filtering {count:,} configs by condition: `{condition}`..."
)
TEMPLATE_CONFIG_LOAD_COMPLETED = (
    "Loaded {count:,} configs from '{path}'."
)
TEMPLATE_CONFIG_LOAD_STARTED = (
    "Loading configs from '{path}'..."
)
TEMPLATE_CONFIG_LOG_EXTRACT = (
    "| <EE> | "
    f"{{name:<{TEXT_LENGTH_NAME}}}"
    " | "
    f"{{total:>{TEXT_LENGTH_NUMBER},}}"
    " | "
    "({found:+,})"
)
TEMPLATE_CONFIG_NORMALIZE_COMPLETED = (
    "Configs normalized: {count:,} (removed: {removed:,})."
)
TEMPLATE_CONFIG_NORMALIZE_STARTED = (
    "Normalizing {count:,} configs..."
)
TEMPLATE_CONFIG_SAVE_COMPLETED = (
    "Saved {count:,} configs in '{path}'."
)
TEMPLATE_CONFIG_SAVE_STARTED = (
    "Saving {count:,} configs to '{path}'..."
)
TEMPLATE_CONFIG_SORT_COMPLETED = (
    "Sorting completed: {count:,} configs sorted."
)
TEMPLATE_CONFIG_SORT_STARTED = (
    "Sorting {count:,} configs by fields: {fields} (reverse={reverse})..."
)
TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS = (
    "{protocol} config is missing required fields: {fields}"
)
TEMPLATE_ERROR_CONFIG_UNEXPECTED_FAILURE = (
    "Unexpected failure while normalizing config:"
    "\n"
    "{config}"
    "\n"
    "Exception type: {exc_type}."
    "\n"
    "Exception message: {exc_msg}."
)
TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED = (
    "{protocol} config could not be parsed from URL: '{url}'"
)
TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD = (
    "Duplicate field detected: {field!r}."
)
TEMPLATE_ERROR_EXPECTED_FILE = (
    "'{filepath}' is a directory, expected a file."
)
TEMPLATE_ERROR_EXPECTED_STRING = (
    "Expected string, got {type_name!r}."
)
TEMPLATE_ERROR_FAILED_EXTRACT_POST_ID = (
    "Failed to extract post ID from '{url}' - {exc_type}: {exc_msg}."
)
TEMPLATE_ERROR_FAILED_FETCH_ID = (
    "Failed to fetch ID {current_id} "
    "(channel_name={channel_name}) - {exc_type}: {exc_msg}."
)
TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION = (
    "Script '{name}' execution failed."
)
TEMPLATE_ERROR_FAILED_SERIALIZATION = (
    "Failed to serialize object '{title}' - {exc_type}: {exc_msg}."
)
TEMPLATE_ERROR_FILE_NOT_EXIST = (
    "The file does not exist: '{filepath}'."
)
TEMPLATE_ERROR_INVALID_FIELD = (
    "Invalid field format: {field!r}."
)
TEMPLATE_ERROR_INVALID_NUMBER = (
    "Invalid number: {value}."
)
TEMPLATE_ERROR_INVALID_OFFSET = (
    "Invalid offset {offset}, expected positive integer"
    " - "
    "assignment skipped."
)
TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE = (
    "Expected {min_value} to {max_value}, got {value}."
)
TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST = (
    "Parent directory does not exist: '{parent}'."
)
TEMPLATE_ERROR_RESPONSE_EMPTY = (
    "Received empty response for ID {current_id:,}"
    " "
    "(channel_name={channel_name}, status={status})."
)
TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED = (
    "VMESS JSON could not be decoded: '{json}'"
)
TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED = (
    "VMESS JSON could not be parsed from base64: '{base64}'"
)
TEMPLATE_FORMAT_CONFIG_NAME = (
    "{protocol}"
    "-"
    "{host}"
    "-"
    "{port}"
)
TEMPLATE_FORMAT_CONFIG_SSR_BODY = (
    "{host}"
    ":"
    "{port}"
    ":"
    "{origin}"
    ":"
    "{method}"
    ":"
    "{obfs}"
    ":"
    "{password}"
    "/?"
    "{params}"
)
TEMPLATE_FORMAT_CONFIG_URL = (
    "{url}"
    "#"
    "{name}"
)
TEMPLATE_FORMAT_CONFIG_URL_BODY = (
    "{protocol}"
    "://"
    "{body}"
)
TEMPLATE_FORMAT_CONFIG_URL_LOCATION = (
    "@"
    "{host}"
    ":"
    "{port}"
)
TEMPLATE_FORMAT_FILE_BACKUP_NAME = (
    "{stem}"
    "-"
    "backup"
    "-"
    "{date}"
    "{suffix}"
)
TEMPLATE_FORMAT_FILE_LOG_PATH = (
    "{dir}"
    "/"
    "{name}"
    ".log"
)
TEMPLATE_FORMAT_STRING_BASE64_PADDING = (
    "{string}"
    "{padding}"
)
TEMPLATE_FORMAT_STRING_COLORED_LEVEL = (
    "{color}"
    "{levelname}"
    "{reset}"
)
TEMPLATE_FORMAT_STRING_QUOTED_NAME = (
    "'{name}'"
)
TEMPLATE_FORMAT_TG_URL = (
    "https://t.me/s/{name}"
)
TEMPLATE_FORMAT_TG_URL_AFTER = (
    TEMPLATE_FORMAT_TG_URL + "?after={id}"
)
TEMPLATE_MSG_FILE_BACKUP_COMPLETED = (
    "File '{src_name}' backed up as '{backup_name}'."
)
TEMPLATE_MSG_SCRIPT_COMPLETED = (
    "Script '{name}' completed successfully."
)
TEMPLATE_MSG_SCRIPT_STARTED = (
    "Starting script '{name}'..."
)
TEMPLATE_TITLE_DEBUG_OFFSET = (
    "Debug info for channel '{name}' (check_only={check_only})"
)
TEMPLATE_TITLE_DELETING_CHANNEL = (
    "Deleting channel '{name}' with the following information"
)
TEMPLATE_TITLE_OBJECT_PRETTY_PRINT = (
    "{title}:"
    "\n"
    "{formatted}"
)
