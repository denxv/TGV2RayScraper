from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_TITLE_CHANNEL_CHANGES",
    "TEMPLATE_TITLE_CHANNEL_DELETE",
    "TEMPLATE_TITLE_CHANNEL_INFO",
    "TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS",
    "TEMPLATE_TITLE_CLI_SCRIPT_LAUNCH_ARGUMENTS",
    "TEMPLATE_TITLE_COMPILED_URL_PATTERNS_BY_V2RAY_PROTOCOL",
]

TEMPLATE_TITLE_CHANNEL_CHANGES: TemplateStr = (
    "Channel {name!r} was updated with the following changes"
)
TEMPLATE_TITLE_CHANNEL_DELETE: TemplateStr = (
    "Channel {name!r} will be deleted with the following information"
)
TEMPLATE_TITLE_CHANNEL_INFO: TemplateStr = (
    "Channel {name!r} with the following information"
)
TEMPLATE_TITLE_CLI_PARSED_ARGUMENTS: TemplateStr = (
    "Parsed command-line arguments for script {name!r}"
)
TEMPLATE_TITLE_CLI_SCRIPT_LAUNCH_ARGUMENTS: TemplateStr = (
    "Script {name!r} launch arguments"
)
TEMPLATE_TITLE_COMPILED_URL_PATTERNS_BY_V2RAY_PROTOCOL: TemplateStr = (
    "Compiled {count!r} URL regex patterns by V2Ray protocol"
)
