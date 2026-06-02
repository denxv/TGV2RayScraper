from core.typing import (
    TemplateStr,
)

__all__ = [
    "TEMPLATE_DEBUG_CHANNEL_ASSIGNMENT_OFFSET_APPLIED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FAILED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FETCHED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_EXTRACTED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_EXTRACTED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_SUCCESS",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_COMBINED_COMPLETED",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_NORMALIZED",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSED",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSE_FAILED",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_IO_LOAD_URLS_PARSED",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_BACKUP_CREATED",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_NORMALIZED",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_SERIALIZED",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_URLS_WRITTEN",
    "TEMPLATE_DEBUG_CHANNEL_IO_SAVE_WRITTEN",
    "TEMPLATE_DEBUG_CHANNEL_MISSING_ADD_COMPLETED",
    "TEMPLATE_DEBUG_CHANNEL_RESET_SKIPPED_NO_CHANGES",
    "TEMPLATE_DEBUG_CHANNEL_STATUS_RESULT",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_COMPLETED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_COMPLETED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_FIRST_ID_FETCHED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_LAST_ID_FETCHED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_COMPLETED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_RESULT",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_STARTED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_STATE_UPDATED",
    "TEMPLATE_DEBUG_CHANNEL_UPDATE_UNAVAILABLE",
]

TEMPLATE_DEBUG_CHANNEL_ASSIGNMENT_OFFSET_APPLIED: TemplateStr = (
    "[channel.assignment.applied]: "
    "message={message!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FAILED: TemplateStr = (
    "[channel.extract.post_id.failed]: "
    "url={url!r}; "
    "default={default!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FETCHED: TemplateStr = (
    "[channel.extract.post_id.fetched]: "
    "url={url!r}; "
    "status_code={status_code!r}; "
    "html_length={html_length!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_EXTRACTED: TemplateStr = (
    "[channel.extract.post_id.first.extracted]: "
    "channel_name={channel_name!r}; "
    "post_id={post_id!r}; "
    "default={default!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_FIRST_STARTED: TemplateStr = (
    "[channel.extract.post_id.first.started]: "
    "channel_name={channel_name!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_EXTRACTED: TemplateStr = (
    "[channel.extract.post_id.last.extracted]: "
    "channel_name={channel_name!r}; "
    "post_id={post_id!r}; "
    "default={default!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_LAST_STARTED: TemplateStr = (
    "[channel.extract.post_id.last.started]: "
    "channel_name={channel_name!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_STARTED: TemplateStr = (
    "[channel.extract.post_id.started]: "
    "url={url!r}"
)
TEMPLATE_DEBUG_CHANNEL_EXTRACT_POST_ID_SUCCESS: TemplateStr = (
    "[channel.extract.post_id.success]: "
    "url={url!r}; "
    "index={index!r}; "
    "post_url={post_url!r}; "
    "post_id={post_id!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_COMBINED_COMPLETED: TemplateStr = (
    "[channel.io.load.combined.completed]: "
    "channels_count={channels_count!r}; "
    "names_count={names_count!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_NORMALIZED: TemplateStr = (
    "[channel.io.load.normalized]: "
    "parsed_channels_count={parsed_channels_count!r}; "
    "normalized_channels_count={normalized_channels_count!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSE_FAILED: TemplateStr = (
    "[channel.io.load.parse.failed]: "
    "channels_path={channels_path!r}; "
    "exc_type={exc_type!r}; "
    "exc_msg={exc_msg!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_PARSED: TemplateStr = (
    "[channel.io.load.parsed]: "
    "parsed_channels_count={parsed_channels_count!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_STARTED: TemplateStr = (
    "[channel.io.load.started]: "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_LOAD_URLS_PARSED: TemplateStr = (
    "[channel.io.load.urls.parsed]: "
    "parsed_names_count={parsed_names_count!r}; "
    "urls_path={urls_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_BACKUP_CREATED: TemplateStr = (
    "[channel.io.save.backup.created]: "
    "files_count={files_count!r}; "
    "files_to_backup={files_to_backup!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_NORMALIZED: TemplateStr = (
    "[channel.io.save.normalized]: "
    "channels_count={channels_count!r}; "
    "normalized_channels_count={normalized_channels_count!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_SERIALIZED: TemplateStr = (
    "[channel.io.save.serialized]: "
    "json_bytes_length={json_bytes_length!r}; "
    "json_indent={json_indent!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_STARTED: TemplateStr = (
    "[channel.io.save.started]: "
    "channels_count={channels_count!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_URLS_WRITTEN: TemplateStr = (
    "[channel.io.save.urls.written]: "
    "urls_count={urls_count!r}; "
    "urls_path={urls_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_IO_SAVE_WRITTEN: TemplateStr = (
    "[channel.io.save.written]: "
    "json_bytes_length={json_bytes_length!r}; "
    "channels_path={channels_path!r}"
)
TEMPLATE_DEBUG_CHANNEL_MISSING_ADD_COMPLETED: TemplateStr = (
    "[channel.update.added]: "
    "name={name!r}"
)
TEMPLATE_DEBUG_CHANNEL_RESET_SKIPPED_NO_CHANGES: TemplateStr = (
    "[channel.reset.skipped]: "
    "reset_to_defaults={reset_to_defaults!r}; "
    "valid_overrides={valid_overrides!r}"
)
TEMPLATE_DEBUG_CHANNEL_STATUS_RESULT: TemplateStr = (
    "[channel.status.result]: "
    "channel_name={result.channel_name!r}; "
    "current_id={result.current_id!r}; "
    "last_id={result.last_id!r}; "
    "diff_id={result.diff_id!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_COMPLETED: TemplateStr = (
    "[channel.update.batch.completed]: "
    "channels_batch_size={channels_batch_size!r}; "
    "changed_channels_in_batch={changed_channels_in_batch!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_BATCH_STARTED: TemplateStr = (
    "[channel.update.batch.started]: "
    "channels_batch_size={channels_batch_size!r}; "
    "channels={channels!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_COMPLETED: TemplateStr = (
    "[channel.update.completed]: "
    "channel_name={result.channel_name!r}; "
    "old_last_id={result.old_last_id!r}; "
    "new_last_id={result.new_last_id!r}; "
    "changed={result.changed!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_FIRST_ID_FETCHED: TemplateStr = (
    "[channel.update.first_id.fetched]: "
    "channel_name={channel_name!r}; "
    "first_post_id={first_post_id!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_LAST_ID_FETCHED: TemplateStr = (
    "[channel.update.last_id.fetched]: "
    "channel_name={channel_name!r}; "
    "last_post_id={last_post_id!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_COMPLETED: TemplateStr = (
    "[channel.update.orchestration.completed]: "
    "channels_count={channels_count!r}; "
    "changed_channels_count={changed_channels_count!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_ORCHESTRATION_STARTED: TemplateStr = (
    "[channel.update.orchestration.started]: "
    "channels_count={channels_count!r}; "
    "channels_batch_size={channels_batch_size!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_RESULT: TemplateStr = (
    "[channel.update.result]: "
    "channel_name={result.channel_name!r}; "
    "old_last_id={result.old_last_id!r}; "
    "new_last_id={result.new_last_id!r}; "
    "changed={result.changed!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_STARTED: TemplateStr = (
    "[channel.update.started]: "
    "channel_name={channel_name!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_STATE_UPDATED: TemplateStr = (
    "[channel.update.state.updated]: "
    "channel_name={result.channel_name!r}; "
    "old_last_id={result.old_last_id!r}; "
    "new_last_id={result.new_last_id!r}; "
    "changed={result.changed!r}"
)
TEMPLATE_DEBUG_CHANNEL_UPDATE_UNAVAILABLE: TemplateStr = (
    "[channel.update.unavailable]: "
    "channel_name={channel_name!r}"
)
