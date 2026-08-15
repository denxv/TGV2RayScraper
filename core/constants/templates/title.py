from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_TITLE_CHANNEL_CHANGES",
    "TEMPLATE_TITLE_CHANNEL_DELETE",
    "TEMPLATE_TITLE_CHANNEL_INFO",
]

TEMPLATE_TITLE_CHANNEL_CHANGES: TemplateStr = (
    "Channel '{name}' was updated with the following changes"
)
TEMPLATE_TITLE_CHANNEL_DELETE: TemplateStr = (
    "Channel '{name}' will be deleted with the following information"
)
TEMPLATE_TITLE_CHANNEL_INFO: TemplateStr = (
    "Channel '{name}' with the following information"
)
