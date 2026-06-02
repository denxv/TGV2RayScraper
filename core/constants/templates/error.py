from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_ERROR_CONFIG_IMPORT_FAILED",
    "TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS",
    "TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED",
    "TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD",
    "TEMPLATE_ERROR_EXPECTED_FILE",
    "TEMPLATE_ERROR_EXPECTED_STRING",
    "TEMPLATE_ERROR_FAILED_FETCH_ID",
    "TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION",
    "TEMPLATE_ERROR_FILE_NOT_EXIST",
    "TEMPLATE_ERROR_HTTP_FETCH_FAILED_AFTER_RETRIES",
    "TEMPLATE_ERROR_HTTP_FETCH_RETRY_EXHAUSTED",
    "TEMPLATE_ERROR_HTTP_FETCH_RETRY_LOOP_BROKEN",
    "TEMPLATE_ERROR_INVALID_FIELD",
    "TEMPLATE_ERROR_INVALID_NUMBER",
    "TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS",
    "TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE",
    "TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST",
    "TEMPLATE_ERROR_PROXY_AUTH_OR_PROTOCOL",
    "TEMPLATE_ERROR_PROXY_INVALID_FORMAT",
    "TEMPLATE_ERROR_PROXY_INVALID_PORT",
    "TEMPLATE_ERROR_PROXY_NETWORK",
    "TEMPLATE_ERROR_UNKNOWN_SCRIPT_NAMES",
    "TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED",
    "TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED",
]

TEMPLATE_ERROR_CONFIG_IMPORT_FAILED: TemplateStr = (
    "Failed to import configurations from {path!r} "
    "due to {exc_type!r}: {exc_msg!r}."
)
TEMPLATE_ERROR_CONFIG_MISSING_REQUIRED_FIELDS: TemplateStr = (
    "Failed to process {protocol!r} configuration "
    "due to missing required fields: {fields!r}."
)
TEMPLATE_ERROR_CONFIG_URL_PARSE_FAILED: TemplateStr = (
    "Failed to parse {protocol!r} configuration."
)
TEMPLATE_ERROR_DETECTED_DUPLICATE_FIELD: TemplateStr = (
    "Detected duplicate configuration field: {field!r}."
)
TEMPLATE_ERROR_EXPECTED_FILE: TemplateStr = (
    "Expected a file at {filepath!r}, but found a directory instead."
)
TEMPLATE_ERROR_EXPECTED_STRING: TemplateStr = (
    "Expected a string input, but received type {type_name!r}."
)
TEMPLATE_ERROR_FAILED_FETCH_ID: TemplateStr = (
    "Failed to fetch post {current_id!r} from channel {channel_name!r} "
    "due to {exc_type!r}: {exc_msg!r}."
)
TEMPLATE_ERROR_FAILED_SCRIPT_EXECUTION: TemplateStr = (
    "Script {name!r} failed to complete due to an unexpected error."
)
TEMPLATE_ERROR_FILE_NOT_EXIST: TemplateStr = (
    "File {filepath!r} does not exist."
)
TEMPLATE_ERROR_HTTP_FETCH_FAILED_AFTER_RETRIES: TemplateStr = (
    "Failed to fetch {url!r} after {retries!r} retry attempts."
)
TEMPLATE_ERROR_HTTP_FETCH_RETRY_EXHAUSTED: TemplateStr = (
    "All {retries!r} retry attempts failed for {url!r}."
)
TEMPLATE_ERROR_HTTP_FETCH_RETRY_LOOP_BROKEN: TemplateStr = (
    "Retry loop for {url!r} finished without returning a response."
)
TEMPLATE_ERROR_INVALID_FIELD: TemplateStr = (
    "Invalid field format: {field!r}."
)
TEMPLATE_ERROR_INVALID_NUMBER: TemplateStr = (
    "Invalid number format for value {value!r}."
)
TEMPLATE_ERROR_INVALID_OVERRIDE_FIELDS: TemplateStr = (
    "Detected invalid override fields: {fields!r}."
)
TEMPLATE_ERROR_NUMBER_OUT_OF_RANGE: TemplateStr = (
    "Value {value!r} is out of range. "
    "Expected between {min!r} and {max!r}."
)
TEMPLATE_ERROR_PARENT_DIRECTORY_NOT_EXIST: TemplateStr = (
    "Parent directory {parent!r} does not exist."
)
TEMPLATE_ERROR_PROXY_AUTH_OR_PROTOCOL: TemplateStr = (
    "Proxy communication failed for {url!r} "
    "due to {exc_type!r}: {exc_msg!r}."
)
TEMPLATE_ERROR_PROXY_INVALID_FORMAT: TemplateStr = (
    "Invalid proxy format: {proxy_url!r}.\n"
    "Expected syntax: 'protocol://[username:password@]host:port'.\n"
    "Supported protocols: http, https, socks5, socks5h.\n"
    "Examples:\n"
    "   http://127.0.0.1:8080\n"
    "   https://username:password@localhost:8443\n"
    "   socks5://username:password@[::1]:1080\n"
    "   socks5h://my-proxy.com:10808"
)
TEMPLATE_ERROR_PROXY_INVALID_PORT: TemplateStr = (
    "Port number {port!r} is invalid. "
    "Expected value between {min!r} and {max!r}."
)
TEMPLATE_ERROR_PROXY_NETWORK: TemplateStr = (
    "Connection to {url!r} failed due to {exc_type!r}: {exc_msg!r}."
)
TEMPLATE_ERROR_VMESS_JSON_DECODE_FAILED: TemplateStr = (
    "Failed to decode VMESS JSON payload: {payload!r}."
)
TEMPLATE_ERROR_UNKNOWN_SCRIPT_NAMES: TemplateStr = (
    "Unknown script name(s) provided: {names!r}."
)
TEMPLATE_ERROR_VMESS_JSON_PARSE_FAILED: TemplateStr = (
    "Failed to parse VMESS JSON from base64 payload: {payload!r}."
)
