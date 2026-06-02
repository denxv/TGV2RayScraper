from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_WARNING_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED",
    "TEMPLATE_WARNING_INVALID_OFFSET",
]

TEMPLATE_WARNING_CHANNEL_ASSIGNMENT_OFFSET_SKIPPED: TemplateStr = (
    "Skipping ID assignment for channel {name!r} "
    "because difference {diff!r} exceeds offset {offset!r}."
)
TEMPLATE_WARNING_INVALID_OFFSET: TemplateStr = (
    "Skipping assignment because offset {offset!r} is invalid. "
    "Expected a positive integer."
)
