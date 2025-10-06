from requests import Session

from adapters.sync.channels import get_last_id
from core.constants import LEN_NAME, LEN_NUMBER
from core.logger import logger


def update_info(session: Session, channels: dict) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")
    for channel_name in channels.keys():
        channel_info = channels[channel_name]
        count = channel_info.get("count", 0)
        last_id = get_last_id(session, channel_name)

        if channel_info["last_id"] == last_id == -1:
            channel_info["count"] = 0 if count > 0 else count - 1
        elif channel_info["last_id"] != last_id:
            logger.info(
                f" <UU>  {channel_name:<{LEN_NAME}}"
                f"{channel_info['last_id']:>{LEN_NUMBER}} "
                f"-> {last_id:<{LEN_NUMBER}}"
            )
            channel_info["last_id"] = last_id
            channel_info["count"] = 1 if count <= 0 else count

        if channel_info["current_id"] <= 0:
            diff = channel_info["last_id"] + channel_info["current_id"]
            channel_info["current_id"] = diff if diff > 0 else 1
        elif channel_info["current_id"] > channel_info["last_id"] != -1:
            channel_info["current_id"] = channel_info["last_id"]
