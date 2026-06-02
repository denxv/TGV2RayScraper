from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_INFO_FILE_BACKUP_COMPLETED",
    "TEMPLATE_INFO_PROXY_USED",
    "TEMPLATE_INFO_SCRIPT_COMPLETED",
    "TEMPLATE_INFO_SCRIPT_STARTED",
]

TEMPLATE_INFO_FILE_BACKUP_COMPLETED: TemplateStr = (
    "Successfully backed up {src_name!r} as {backup_name!r}."
)
TEMPLATE_INFO_PROXY_USED: TemplateStr = (
    "Routing all traffic through proxy {url!r}."
)
TEMPLATE_INFO_SCRIPT_COMPLETED: TemplateStr = (
    "Successfully completed execution of script {name!r}."
)
TEMPLATE_INFO_SCRIPT_STARTED: TemplateStr = (
    "Starting execution of script {name!r}..."
)
