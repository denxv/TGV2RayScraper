from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_INFO_CHANNELS_STATUS_COMPLETED",
    "TEMPLATE_INFO_CHANNELS_STATUS_STARTED",
    "TEMPLATE_INFO_CHANNELS_UPDATE_COMPLETED",
    "TEMPLATE_INFO_CHANNELS_UPDATE_STARTED",
    "TEMPLATE_INFO_CHANNEL_CHANGES_SKIPPED",
    "TEMPLATE_INFO_CHANNEL_CHANGES_TOTAL",
    "TEMPLATE_INFO_CHANNEL_COUNT_DIFFERENCE",
    "TEMPLATE_INFO_CHANNEL_SAVE_COMPLETED",
]

TEMPLATE_INFO_CHANNEL_CHANGES_SKIPPED: TemplateStr = (
    "Skipping changes for {count:,} channels due to dry-run mode."
)
TEMPLATE_INFO_CHANNEL_CHANGES_TOTAL: TemplateStr = (
    "Selected {count:,} channels for changes."
)
TEMPLATE_INFO_CHANNEL_COUNT_DIFFERENCE: TemplateStr = (
    "Updated count from {old_size:,} to {new_size:,} ({diff:+,})."
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
