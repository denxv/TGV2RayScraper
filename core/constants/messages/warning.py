from core.typing import (
    MessageStr,
)

__all__ = [
    "MESSAGE_WARNING_CHANNEL_DEDUPLICATION_SKIPPED",
    "MESSAGE_WARNING_NO_CHANNELS_TO_DISPLAY",
    "MESSAGE_WARNING_NO_CHANNELS_TO_EXTRACT",
    "MESSAGE_WARNING_NO_CHANNELS_TO_UPDATE",
]

MESSAGE_WARNING_CHANNEL_DEDUPLICATION_SKIPPED: MessageStr = (
    "Skipping deduplication because no target fields were specified."
)
MESSAGE_WARNING_NO_CHANNELS_TO_DISPLAY: MessageStr = (
    "Skipping display because no channels are available."
)
MESSAGE_WARNING_NO_CHANNELS_TO_EXTRACT: MessageStr = (
    "Skipping extraction because no channels are available."
)
MESSAGE_WARNING_NO_CHANNELS_TO_UPDATE: MessageStr = (
    "Skipping update because no channels are available."
)
