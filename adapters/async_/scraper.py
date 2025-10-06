from asyncio import create_task, gather

from aiohttp import ClientSession

from adapters.async_.channels import get_last_id
from core.constants import LEN_NAME, LEN_NUMBER
from core.logger import logger


async def update_info(session: ClientSession, channels: dict, batch_size: int = 100) -> None:
    logger.info(f"Updating channel information for {len(channels)} channels...")

    async def update_channel(channel_name: str, channel_info: dict) -> None:
        count = channel_info.get("count", 0)
        last_id = await get_last_id(session, channel_name)

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

    channel_names = list(channels.keys())
    for i in range(0, len(channel_names), batch_size):
        tasks = [
            create_task(update_channel(name, channels[name]))
            for name in channel_names[i:i + batch_size]
        ]
        await gather(*tasks)
