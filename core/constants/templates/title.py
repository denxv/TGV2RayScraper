from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_TITLE_CHANNEL_DELETE",
    "TEMPLATE_TITLE_CHANNEL_INFO",
    "TEMPLATE_TITLE_CHANNEL_RESET",
]

TEMPLATE_TITLE_CHANNEL_DELETE: TemplateStr = (
    "Channel '{name}' will be deleted with the following information"
)
TEMPLATE_TITLE_CHANNEL_INFO: TemplateStr = (
    "Channel '{name}' with the following information"
)
TEMPLATE_TITLE_CHANNEL_RESET: TemplateStr = (
    "Channel '{name}' was reset with the following changes"
)
