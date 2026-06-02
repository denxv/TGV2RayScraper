from core.typing import (
    MessageStr,
)

__all__ = [
    "MESSAGE_INFO_BACKUP_SKIPPED",
    "MESSAGE_INFO_CHANNEL_DELETE_COMPLETED",
    "MESSAGE_INFO_CHANNEL_DELETE_SKIPPED",
    "MESSAGE_INFO_CHANNEL_DELETE_STARTED",
    "MESSAGE_INFO_CHANNEL_LOAD_COMPLETED",
    "MESSAGE_INFO_CHANNEL_LOAD_STARTED",
    "MESSAGE_INFO_CHANNEL_SAVE_COMPLETED",
    "MESSAGE_INFO_CHANNEL_SAVE_STARTED",
    "MESSAGE_INFO_CHANNEL_UPDATE_COMPLETED",
    "MESSAGE_INFO_CHANNEL_UPDATE_SKIPPED",
    "MESSAGE_INFO_CHANNEL_UPDATE_STARTED",
    "MESSAGE_INFO_CONFIG_NORMALIZATION_SKIPPED",
    "MESSAGE_INFO_PROGRAM_EXIT",
]

MESSAGE_INFO_BACKUP_SKIPPED: MessageStr = (
    "Skipping backup for current channels and URLs."
)
MESSAGE_INFO_CHANNEL_DELETE_COMPLETED: MessageStr = (
    "Successfully deleted inactive channels."
)
MESSAGE_INFO_CHANNEL_DELETE_SKIPPED: MessageStr = (
    "Skipping channel deletion because it is disabled by default."
)
MESSAGE_INFO_CHANNEL_DELETE_STARTED: MessageStr = (
    "Starting to delete inactive channels..."
)
MESSAGE_INFO_CHANNEL_LOAD_COMPLETED: MessageStr = (
    "Successfully loaded all channels."
)
MESSAGE_INFO_CHANNEL_LOAD_STARTED: MessageStr = (
    "Starting to load all channels..."
)
MESSAGE_INFO_CHANNEL_SAVE_COMPLETED: MessageStr = (
    ""
)
MESSAGE_INFO_CHANNEL_SAVE_STARTED: MessageStr = (
    "Starting to save all channels..."
)
MESSAGE_INFO_CHANNEL_UPDATE_COMPLETED: MessageStr = (
    "Successfully added missing channels."
)
MESSAGE_INFO_CHANNEL_UPDATE_SKIPPED: MessageStr = (
    "Skipping channel update because existing data is being used."
)
MESSAGE_INFO_CHANNEL_UPDATE_STARTED: MessageStr = (
    "Starting to add missing channels..."
)
MESSAGE_INFO_CONFIG_NORMALIZATION_SKIPPED: MessageStr = (
    "Skipping config normalization to preserve raw structure."
)
MESSAGE_INFO_PROGRAM_EXIT: MessageStr = (
    "Program exited successfully."
)
