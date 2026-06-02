from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_INFO_CONFIG_DEDUPLICATION_COMPLETED",
    "TEMPLATE_INFO_CONFIG_DEDUPLICATION_STARTED",
    "TEMPLATE_INFO_CONFIG_EXPORT_COMPLETED",
    "TEMPLATE_INFO_CONFIG_EXPORT_STARTED",
    "TEMPLATE_INFO_CONFIG_EXTRACT_COMPLETED",
    "TEMPLATE_INFO_CONFIG_EXTRACT_STARTED",
    "TEMPLATE_INFO_CONFIG_FILTER_COMPLETED",
    "TEMPLATE_INFO_CONFIG_FILTER_STARTED",
    "TEMPLATE_INFO_CONFIG_IMPORT_COMPLETED",
    "TEMPLATE_INFO_CONFIG_IMPORT_STARTED",
    "TEMPLATE_INFO_CONFIG_LOAD_COMPLETED",
    "TEMPLATE_INFO_CONFIG_LOAD_STARTED",
    "TEMPLATE_INFO_CONFIG_NORMALIZE_COMPLETED",
    "TEMPLATE_INFO_CONFIG_NORMALIZE_STARTED",
    "TEMPLATE_INFO_CONFIG_SAVE_COMPLETED",
    "TEMPLATE_INFO_CONFIG_SAVE_STARTED",
    "TEMPLATE_INFO_CONFIG_SORT_COMPLETED",
    "TEMPLATE_INFO_CONFIG_SORT_STARTED",
]

TEMPLATE_INFO_CONFIG_DEDUPLICATION_COMPLETED: TemplateStr = (
    "Successfully removed {removed:,} duplicate configurations, "
    "leaving {remain:,} configs."
)
TEMPLATE_INFO_CONFIG_DEDUPLICATION_STARTED: TemplateStr = (
    "Starting to remove duplicates from {count:,} configurations "
    "using fields: {fields!r}..."
)
TEMPLATE_INFO_CONFIG_EXPORT_COMPLETED: TemplateStr = (
    "Successfully exported {count:,} configurations to {path!r}."
)
TEMPLATE_INFO_CONFIG_EXPORT_STARTED: TemplateStr = (
    "Starting to export {count:,} configurations to {path!r}..."
)
TEMPLATE_INFO_CONFIG_EXTRACT_COMPLETED: TemplateStr = (
    "Successfully extracted {configs_count:,} configurations "
    "from {channels_count:,} channels."
)
TEMPLATE_INFO_CONFIG_EXTRACT_STARTED: TemplateStr = (
    "Starting to extract configurations from {count:,} channels..."
)
TEMPLATE_INFO_CONFIG_FILTER_COMPLETED: TemplateStr = (
    "Successfully filtered configurations, "
    "keeping {count:,} and removing {removed:,}."
)
TEMPLATE_INFO_CONFIG_FILTER_STARTED: TemplateStr = (
    "Starting to filter {count:,} configurations "
    "by condition: {condition!r}..."
)
TEMPLATE_INFO_CONFIG_IMPORT_COMPLETED: TemplateStr = (
    "Successfully imported {count:,} configurations from {path!r}."
)
TEMPLATE_INFO_CONFIG_IMPORT_STARTED: TemplateStr = (
    "Starting to import configurations from {path!r}..."
)
TEMPLATE_INFO_CONFIG_LOAD_COMPLETED: TemplateStr = (
    "Successfully loaded {count:,} configurations from {path!r}."
)
TEMPLATE_INFO_CONFIG_LOAD_STARTED: TemplateStr = (
    "Starting to load configurations from {path!r}..."
)
TEMPLATE_INFO_CONFIG_NORMALIZE_COMPLETED: TemplateStr = (
    "Successfully normalized {count:,} configurations, "
    "removing {removed:,}."
)
TEMPLATE_INFO_CONFIG_NORMALIZE_STARTED: TemplateStr = (
    "Starting to normalize {count:,} configurations..."
)
TEMPLATE_INFO_CONFIG_SAVE_COMPLETED: TemplateStr = (
    "Successfully saved {count:,} configurations to {path!r}."
)
TEMPLATE_INFO_CONFIG_SAVE_STARTED: TemplateStr = (
    "Starting to save {count:,} configurations to {path!r}..."
)
TEMPLATE_INFO_CONFIG_SORT_COMPLETED: TemplateStr = (
    "Successfully sorted {count:,} configurations."
)
TEMPLATE_INFO_CONFIG_SORT_STARTED: TemplateStr = (
    "Starting to sort {count:,} configurations by {fields!r} "
    "(reverse={reverse!r})..."
)
