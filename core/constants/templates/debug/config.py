from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_COMPLETED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_STARTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_COMPLETED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_EXTRACTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_FILTERED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_RENDERED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_STARTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_EMPTY",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_FETCHED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_REGEX_DONE",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_STARTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_XPATH_DONE",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_COMPLETED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_STARTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_COMPLETED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_STARTED",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_RESULT",
    "TEMPLATE_DEBUG_CONFIG_EXTRACT_STARTED",
    "TEMPLATE_DEBUG_CONFIG_IO_EXPORT_SERIALIZED",
    "TEMPLATE_DEBUG_CONFIG_IO_EXPORT_WRITTEN",
    "TEMPLATE_DEBUG_CONFIG_IO_IMPORT_READ",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_EMPTY",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_NORMALIZED_EMPTY",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_SUCCESS",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_NORMALIZED",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_PARSED",
    "TEMPLATE_DEBUG_CONFIG_IO_LOAD_STARTED",
    "TEMPLATE_DEBUG_CONFIG_IO_SAVE_EXPORT",
    "TEMPLATE_DEBUG_CONFIG_IO_WRITE_COMPLETED",
    "TEMPLATE_DEBUG_CONFIG_IO_WRITE_STARTED",
    "TEMPLATE_DEBUG_CONFIG_UNEXPECTED_FAILURE",
]

TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_COMPLETED: TemplateStr = (
    "[config.extract.batch.completed]: "
    "channels_in_batch={channels_in_batch!r}; "
    "total_collected={total_collected!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_BATCH_STARTED: TemplateStr = (
    "[config.extract.batch.started]: "
    "channels_in_batch={channels_in_batch!r}; "
    "channels={channels!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_COMPLETED: TemplateStr = (
    "[config.extract.completed]: "
    "channels_processed={channels_processed!r}; "
    "total_collected={total_collected!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_EXTRACTED: TemplateStr = (
    "[config.extract.orchestration.extracted]: "
    "channels_processed={channels_processed!r}; "
    "total_collected={total_collected!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_FILTERED: TemplateStr = (
    "[config.extract.orchestration.filtered]: "
    "total_channels={total_channels!r}; "
    "filtered_channels_count={filtered_channels_count!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_RENDERED: TemplateStr = (
    "[config.extract.orchestration.rendered]: "
    "rendered_count={rendered_count!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_ORCHESTRATION_STARTED: TemplateStr = (
    "[config.extract.orchestration.started]: "
    "filtered_channels_count={filtered_channels_count!r}; "
    "filtered_channels={filtered_channels!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_EMPTY: TemplateStr = (
    "[config.extract.parse.empty]: "
    "channel_name={channel_name!r}; "
    "current_id={current_id!r}; "
    "status_code={status_code!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_FETCHED: TemplateStr = (
    "[config.extract.parse.fetched]: "
    "channel_name={channel_name!r}; "
    "current_id={current_id!r}; "
    "status_code={status_code!r}; "
    "html_length={html_length!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_REGEX_DONE: TemplateStr = (
    "[config.extract.parse.regex.done]: "
    "channel_name={channel_name!r}; "
    "configs_count={configs_count!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_STARTED: TemplateStr = (
    "[config.extract.parse.started]: "
    "channel_name={channel_name!r}; "
    "current_id={current_id!r}; "
    "url={url!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PARSE_XPATH_DONE: TemplateStr = (
    "[config.extract.parse.xpath.done]: "
    "channel_name={channel_name!r}; "
    "messages_count={messages_count!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_COMPLETED: TemplateStr = (
    "[config.extract.process.batch.completed]: "
    "channel_name={channel_name!r}; "
    "total_collected={total_collected!r}; "
    "configs_path={configs_path!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCH_STARTED: TemplateStr = (
    "[config.extract.process.batch.started]: "
    "channel_name={channel_name!r}; "
    "ids_count={ids_count!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_COMPLETED: TemplateStr = (
    "[config.extract.process.batches.completed]: "
    "channel_name={channel_name!r}; "
    "batches_processed={batches_processed!r}; "
    "total_collected={total_collected!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_PROCESS_BATCHES_STARTED: TemplateStr = (
    "[config.extract.process.batches.started]: "
    "channel_name={channel_name!r}; "
    "total_ids={total_ids!r}; "
    "ids_per_batch={ids_per_batch!r}; "
    "total_batches={total_batches!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_RESULT: TemplateStr = (
    "[config.extract.result]: "
    "channel_name={result.channel_name!r}; "
    "total_found={result.total_found!r}; "
    "new_found={result.new_found!r}"
)
TEMPLATE_DEBUG_CONFIG_EXTRACT_STARTED: TemplateStr = (
    "[config.extract.started]: "
    "channels_count={channels_count!r}; "
    "max_concurrent_channels={max_concurrent_channels!r}; "
    "ids_per_batch={ids_per_batch!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_EXPORT_SERIALIZED: TemplateStr = (
    "[config.io.export.serialized]: "
    "json_bytes_length={json_bytes_length!r}; "
    "json_indent={json_indent!r}; "
    "configs_count={configs_count!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_EXPORT_WRITTEN: TemplateStr = (
    "[config.io.export.written]: "
    "json_bytes_length={json_bytes_length!r}; "
    "export_path={export_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_IMPORT_READ: TemplateStr = (
    "[config.io.import.read]: "
    "bytes_read={bytes_read!r}; "
    "import_path={import_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_EMPTY: TemplateStr = (
    "[config.io.load.import.empty]: "
    "import_path={import_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_NORMALIZED_EMPTY: TemplateStr = (
    "[config.io.load.import.normalized.empty]: "
    "imported_configs_count={imported_configs_count!r}; "
    "import_path={import_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_IMPORT_SUCCESS: TemplateStr = (
    "[config.io.load.import.success]: "
    "imported_configs_count={imported_configs_count!r}; "
    "normalized_configs_count={normalized_configs_count!r}; "
    "import_path={import_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_NORMALIZED: TemplateStr = (
    "[config.io.load.normalized]: "
    "skip_normalize={skip_normalize!r}; "
    "parsed_configs_count={parsed_configs_count!r}; "
    "normalized_configs_count={normalized_configs_count!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_PARSED: TemplateStr = (
    "[config.io.load.parsed]: "
    "parsed_configs_count={parsed_configs_count!r}; "
    "configs_raw_path={configs_raw_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_LOAD_STARTED: TemplateStr = (
    "[config.io.load.started]: "
    "skip_normalize={skip_normalize!r}; "
    "import_path={import_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_SAVE_EXPORT: TemplateStr = (
    "[config.io.save.export]: "
    "configs_to_export_count={configs_to_export_count!r}; "
    "export_path={export_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_WRITE_COMPLETED: TemplateStr = (
    "[config.io.write.completed]: "
    "written_configs_count={written_configs_count!r}; "
    "configs_path={configs_path!r}"
)
TEMPLATE_DEBUG_CONFIG_IO_WRITE_STARTED: TemplateStr = (
    "[config.io.write.started]: "
    "configs_count={configs_count!r}; "
    "mode={mode!r}; "
    "configs_path={configs_path!r}"
)
TEMPLATE_DEBUG_CONFIG_UNEXPECTED_FAILURE: TemplateStr = (
    "[config.normalize.failed]: "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}; "
    "config={config}"
)
