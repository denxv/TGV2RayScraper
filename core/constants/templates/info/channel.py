from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_INFO_CHANNELS_STATUS_COMPLETED",
    "TEMPLATE_INFO_CHANNELS_STATUS_STARTED",
    "TEMPLATE_INFO_CHANNELS_UPDATE_COMPLETED",
    "TEMPLATE_INFO_CHANNELS_UPDATE_STARTED",
    "TEMPLATE_INFO_CHANNEL_ASSIGNMENT_APPLIED",
    "TEMPLATE_INFO_CHANNEL_ASSIGNMENT_SKIPPED",
    "TEMPLATE_INFO_CHANNEL_COUNT_DIFFERENCE",
    "TEMPLATE_INFO_CHANNEL_RESET_SKIPPED",
    "TEMPLATE_INFO_CHANNEL_RESET_TOTAL",
    "TEMPLATE_INFO_CHANNEL_SAVE_COMPLETED",
]

TEMPLATE_INFO_CHANNEL_ASSIGNMENT_APPLIED: TemplateStr = (
    "Applied offset {offset!r} to channel {name!r}. Current ID normalized."
)
TEMPLATE_INFO_CHANNEL_ASSIGNMENT_SKIPPED: TemplateStr = (
    "Skipping ID assignment for {count:,} channels due to dry-run mode."
)
TEMPLATE_INFO_CHANNEL_COUNT_DIFFERENCE: TemplateStr = (
    "Updated count from {old_size:,} to {new_size:,} ({diff:+,})."
)
TEMPLATE_INFO_CHANNEL_RESET_SKIPPED: TemplateStr = (
    "Skipping reset for {count:,} channels due to dry-run mode."
)
TEMPLATE_INFO_CHANNEL_RESET_TOTAL: TemplateStr = (
    "Selected {count:,} channels for reset."
)
TEMPLATE_INFO_CHANNEL_SAVE_COMPLETED: TemplateStr = (
    "Successfully saved {count:,} channels to {path!r}."
)
TEMPLATE_INFO_CHANNELS_STATUS_COMPLETED: TemplateStr = (
    "Successfully checked {total:,} channels: "
    "{pending:,} pending and {messages:,} messages."
)
TEMPLATE_INFO_CHANNELS_STATUS_STARTED: TemplateStr = (
    "Starting to render status for {count:,} channels..."
)
TEMPLATE_INFO_CHANNELS_UPDATE_COMPLETED: TemplateStr = (
    "Finished updating {checked:,} channels, with {changed:,} changed."
)
TEMPLATE_INFO_CHANNELS_UPDATE_STARTED: TemplateStr = (
    "Starting to update information for {count:,} channels..."
)
